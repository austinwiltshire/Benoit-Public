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
    
    balanceSheetAnnualDiv = "balannualdiv"
    balanceSheetQuarterlyDiv = "balinterimdiv"
    cashFlowsAnnualDiv = "casannualdiv"
    cashFlowsQuarterlyDiv = "casinterimdiv"
    incomeStatementAnnualDiv = "incintirimdiv"
    incomeStatementQuarterlyDiv = "incannualdiv"
    
    revenueRE = re.compile("Revenue")
    
    def __init__(self, soup):
        self.quarterlyDates = []
        self.annualDates = []
        #assumes that across balance sheet, cash flows, etc... same dates are used.
        
        self.balanceSheetAnnualDiv = soup.find('div', id=balanceSheetAnnualDiv)
        self.balanceSheetQuarterlyDiv = soup.find('div', id=balanceSheetQuarterlyDiv)
        self.cashFlowsAnnualDiv = soup.find('div', id=cashFlowsAnnualDiv)
        self.cashFlowsQuarterlyDiv = soup.find('div', id=cashFlowsQuarterlyDiv)
        self.incomeStatementAnnualDiv = soup.find('div', id=incomeStatementAnnualDiv)
        self.incomeStatementQuarterlyDiv = soup.find('div', id=incomeStatementQuarterlyDiv)
        
        self.revenueQuarterly = None
        self.revenueAnnual = None
        
    def getRevenueQuarterly(self):
        if self.revenueQuarterly:
            return self.revenueQuarterly
        
        revenueQuarterly = self.incomeStatementQuarterlyDiv.find("...") #YOU ARE HERE
            

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
    
    def getRevenue(self, symbol, type='annual', date=None):
        """ Returns the income statement as a dict for the symbol at the date.  If date is "
        " blank then returns all income statements available for the symbol in order """
        
        type = type.lower()
        if type!='annual' and type!='quarterly':
            print type
            raise Exception("type needs to be annual or quarterly")
        
        if symbol in self.cachedPages:
            mypage = self.cachedPages[symbol]
        else:
            buildURL = self.buildURL(symbol)
            html = urllib2.urlopen(buildURL)
            mypage = BeautifulSoup(html)
            self.cachedPages[symbol] = mypage
        
        if type=='annual':
            divname = 'incannualdiv'
        if type=='quarterly':
            divname = 'incinterimdiv'
            
        div = mypage.find('div', id=divname)
        
#        div = None
 #       for division in divisions:
  #          if division['id'] == divname:
   #             div = division
        
        tds = div.findAll('td')[1:]
        #TODO: replace this with a callable or something?
        
        #get all td's, except the first because it is just 'in millions of USD ...'
        
        datere = re.compile(r"\d+ months Ending (?P<year>\d{4,4})-(?P<month>\d{2,2})-(?P<day>\d{2,2})")    

        tds = [datere.search(td.b.string) for td in tds if td.b and td.b.string and datere.search(td.b.string)]
        #TODO: should this be simplified in a loop or can I improve my div.findAll above to get this sort of stuff?
        
#        tds = map(lambda td: datere.search(td.string) if td.string != None else , tds)
        dates = [datetime.date(int(td.group('year')), int(td.group('month')), int(td.group('day'))) for td in tds]
#        dates = map(lambda td: datetime.date(td.group('year'), td.group('month'), td.group('day')), tds)
        #dates should be in order of most recent first and least recent last
        
        trs = div.findAll('tr')[1:]
        #get all trs, except the first because its just the dates.
        revenuere = re.compile("Revenue")
        number = re.compile(r"[\d{3,3},]*\d{0,3}\.\d+|-")
        
        for tr in trs:
            tds = tr.findAll('td')
            if tds[0].string and revenuere.search(tds[0].string) != None:
                    revenues = [number.search(r.string).group() for r in tds[1:] if number.search(r.string)]
                    revenues = [r.replace(",","") for r in revenues]
                    revenues = [float(r) if r != "-" else r for r in revenues]
#                    revenues = map(lambda r: number.search(r.string), tds[1:])
                    #revenues = map(lambda r: r.replace(",",""), revenues)
                    #revenues = map(lambda r: float(r), revenues)
                    return dict(zip(dates,revenues))