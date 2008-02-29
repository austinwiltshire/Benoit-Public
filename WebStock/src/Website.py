from BeautifulSoup import BeautifulSoup
import urllib2
import re

class Bloomberg(object):
    """ A Bloomberg is a stock information service provider.  It can host any number of "
    " services depending on what is available, such as price, volume, etc. information for "
    " any stock and any date """
    pass 

class Website(Bloomberg):
    """ Website is a Bloomberg that gets its information from a particular website. """
    pass

class Google(Website):
    def __init__(self):
        cachedPages = {}
    
    def getRevenue(self, symbol, type='annual', date=None):
        """ Returns the income statement as a dict for the symbol at the date.  If date is "
        " blank then returns all income statements available for the symbol in order """
        
        type = type.lower()
        if type!='annual' or type!='quarterly':
            raise Exception("type needs to be annual or quarterly")
        
        if symbol in cachedPages:
            mypage = cachedPages[symbol]
        else:
            buildURL = self.buildURL(symbol)
            page = urllib2.urlopen(buildURL)
            mypage = BeautifulSoup(html)
            cachedPages[symbol] = mypage
        
        divisions = mypage.findAll(lambda tag: tag.name == 'div' and tag.has_key('id'))
        
        if type=='annual':
            divname = 'incannualdiv'
        if type=='quarterly':
            divname = 'incinterimdiv'
        
        
        div = None
        for division in divisions:
            if division['id'] == divname:
                div = division
        
        tds = div.findAll('td')[1:]
        #get all td's, except the first because it is just 'in millions of USD ...'
        
        datere = re.compile(r"\d+ months Ending (?P<year>\d{4,4})-(?P<month>\d{2,2})-(?P<day>\d{2,2})")    
        
        tds = map(lambda td: datere.search(td), tds)
        dates = map(lambda td: datetime.date(td.group('year'), td.group('month'), td.group('day')))
        #dates should be in order of most recent first and least recent last
        
        trs = divisions.findAll('tr')[1:]
        #get all trs, except the first because its just the dates.
        revenuere = re.compile("Revenue")
        number = re.compile(r"[\d{3,3},]*\d{3,3}\.\d+")
        
        for tr in trs:
            tds = tr.findAll('td')
            if revenuere.search(tds.string) != None:
                revenues = map(lambda td: number.search(td), tds[1:])
                revenues = map(lambda r: r.replace(",",""), revenues)
                revenues = map(lambda r: float(r), revenues)
                return zip(tds[1:],dates)