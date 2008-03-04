from BeautifulSoup import BeautifulSoup
import urllib2
import re
import datetime

class Bloomberg(object):
    """ A Bloomberg is a stock information service provider.  It can host any number of "
    " services depending on what is available, such as price, volume, etc. information for "
    " any stock and any date """
    pass 

class Website(Bloomberg):
    """ Website is a Bloomberg that gets its information from a particular website. """
    pass

class GoogleSoup(object):
    """ Helper for Google website """
    
    keywords = {"Revenue":({"Div":"IncomeStatement","Regex":r"(?<!(Other |Total ))Revenue"}),\
                "OtherRevenue":({"Div":"IncomeStatement","Regex":r"Other Revenue, Total"})}
    
    #TODO: you are here.  i want to basically just create a table that will map different
    #attributes to their regex's, as well as define attributes automatically from this table
    #based on the name of the attribute, appended with 'quarterly' or 'annual'.
    #Google needs to inherit an interface similar to this one.  going to have to use 
    #getAttr[] heavily
    
    numberRe = re.compile(r"[\d{3,3},]*\d{0,3}\.\d+|-")
    dateRe = re.compile(r"\d+ months Ending (?P<year>\d{4,4})-(?P<month>\d{2,2})-(?P<day>\d{2,2})")    
    

    
    def __init__(self, soup):
        self.quarterlyDates = []
        self.annualDates = []
        #assumes that across balance sheet, cash flows, etc... same dates are used.
        
        self.labels = {"BalanceSheet":{"Annual":soup.find('div', id='balannualdiv'),\
                                      "Quarterly":soup.find('div', id='balinterimdiv')},\
                       "IncomeStatement":{"Annual":soup.find('div', id='incannualdiv'),\
                                          "Quarterly":soup.find('div', id='incinterimdiv')},\
                       "CashFlowStatement":{"Annual":soup.find('div', id='casannualdiv'),\
                                            "Quarterly":soup.find('div', id='casinterimdiv')},\
                       "Dates":{"Annual":soup.find('div', id='incannualdiv'),\
                                "Quarterly":soup.find('div', id='incinterimdiv')}}
        
        #TODO: put this in XML?
        
        for name,arguments in self.keywords.items():
            self.addAttribute(name,arguments)
        
    def addAttribute(self, name, arguments):
        
        annualMethodName = "getAnnual%s" % name
        quarterlyMethodName = "getQuarterly%s" % name
        
        annualVariableName = "annual%s" % name
        quarterlyVariableName = "quarterly%s" % name
        
        annualDiv = self.labels[arguments['Div']]['Annual']
        quarterlyDiv = self.labels[arguments['Div']]['Quarterly']
        
        searchRe = re.compile(arguments['Regex'])
        
        annualMethod = lambda : self.webparse(annualVariableName, searchRe\
                                              , annualDiv, self.getAnnualDates())
        quarterlyMethod = lambda : self.webparse(quarterlyVariableName, searchRe\
                                              , quarterlyDiv, self.getQuarterlyDates())
        
        self.__setattr__(annualMethodName, annualMethod)
        self.__setattr__(quarterlyMethodName, quarterlyMethod)
        self.__setattr__(annualVariableName, None)
        self.__setattr__(quarterlyVariableName, None)
        
    def getRows(self, div, searchRe):
        """ Get the rows associated with the regular expression searchRe """
        
        trs = div.findAll('tr')[1:]
        #get all trs, except the first because its just the dates.
        
        tds = None
        for tr in trs:    
            tds = tr.findAll('td')
            if tds[0].string and searchRe.search(tds[0].string) != None:
                break
            if tds[0].b.string and searchRe.search(tds[0].b.string) != None: #important names are bolded
                break
            #TODO: 'find' syntax again
        
        values = []
        for result in tds[1:]:
            #if there is no result, google tends to put a '-' after a 'span' tag
            if result.find("span"):
                val = result.find("span")
            else:
                val = result
            
            #check using a regex whether there is a number or a '-' in this td
            match = self.numberRe.search(val.string)
            if match:
                val = match.group()
            else:
                continue
            
            #clean up the string for storage
            val = val.replace(",","")
            
            val = float(val) if val != "-" else "-"
            
            #add it to results.
            values.append(val)
            
        return values
    
    def webparse(self, variableName, searchRe, division, dates):
        if not self.__getattribute__(variableName):
                self.__setattr__(variableName, self.getRows(division, searchRe))
        
        return dict(zip(dates, self.__getattribute__(variableName)))
     
    def getQuarterlyDates(self):
        if not self.quarterlyDates :
            quarterlyDiv = self.labels['Dates']['Quarterly']
        
            tds = quarterlyDiv.findAll('td')[1:]
            #TODO: replace this with a callable or something?
            #get all td's, except the first because it is just 'in millions of USD ...
            
            tds = [self.dateRe.search(td.b.string) for td in tds if td.b and td.b.string and self.dateRe.search(td.b.string)]    
            #TODO: should this be simplified in a loop or can I improve my div.findAll above to get this sort of stuff?
        
            self.quarterlyDates = [datetime.date(int(td.group('year')), int(td.group('month')), int(td.group('day'))) for td in tds]
            
        return self.quarterlyDates
    
    def getAnnualDates(self):
        if not self.annualDates :
            annualDiv = self.labels['Dates']['Annual']
        
            tds = annualDiv.findAll('td')[1:]
            #TODO: replace this with a callable or something?
            #get all td's, except the first because it is just 'in millions of USD ...
            
            tds = [self.dateRe.search(td.b.string) for td in tds if td.b and td.b.string and self.dateRe.search(td.b.string)]    
            #TODO: should this be simplified in a loop or can I improve my div.findAll above to get this sort of stuff?
        
            self.annualDates = [datetime.date(int(td.group('year')), int(td.group('month')), int(td.group('day'))) for td in tds]
            
        return self.annualDates

class Google(Website):

    def __init__(self):
        self.cachedPages = {}
        
    def buildURL(self, symbol):
        baseURL = "http://finance.google.com/finance?q=%s" % symbol
        page = urllib2.urlopen(baseURL)
        page = BeautifulSoup(page)
        
        inc = re.compile("Income.*Statement")
        links = page.findAll('a')
        
        suffix = filter(lambda x: x.string != None\
                         and inc.search(x.string) != None,links)[0]['href']
        return "".join(["http://finance.google.com/finance",suffix])
    
        #TODO: figure out 'find' syntax for lists.  there ought to be a find for lists.
        #TODO: instead of filter, us decorate, find, undecorate.
        #TODO: might be able to put this all in the page.findAll method call
        
    def buildSoup(self, symbol):
        url = self.buildURL(symbol)
        return BeautifulSoup(urllib2.urlopen(url))
    
    keywordRe = re.compile(r"get(Quarterly|Annual)(?P<keyword>[A-z]*)")
    
    def __getattr__(self, name):
        #get the keyword - strip off 'get' and 'quarterly' or 'annual'
        keyword = self.keywordRe.search(name).group('keyword') 
        
        if GoogleSoup.keywords.has_key(keyword):
            return lambda *args: self.__myGetAttr__(name, *args)
        else: 
            raise AttributeError()
        
    def __myGetAttr__(self, name, *args):
        #do some type checking here
        
        symbol=None
        date=None
        
        #should have one/two arguments, one is a symbol string, one is a date 
        if(len(args) == 0 or len(args) > 2):
            raise AttributeError()
        
        #first should be a string
        if not isinstance(args[0], str):
            raise AttributeError()
        symbol = args[0]
        
        #second should be a date
        if(len(args) == 2):
            if not isinstance(args[1], datetime.date):
                raise AttributeError()
            date = args[1]
            
        if not self.cachedPages.has_key(symbol):
            self.cachedPages[symbol] = GoogleSoup(self.buildSoup(symbol))
            
        if date:
            return getattr(self.cachedPages[symbol], name)()[date]
        else:
            return getattr(self.cachedPages[symbol], name)()