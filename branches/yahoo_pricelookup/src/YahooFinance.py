"""
Examples:
>>> from datetime import date
>>> prices = HistoricalPrices()
>>> round(prices.getHigh("MRK", date(2007,12,31)))
59.0

>>> round(prices.getLow("IBM", date(2008,9,30)))
112.0

>> round(prices.getVolume("SBUX", date(2008,09,29)))
20719700

>>> round(prices.getOpen("CSCO", date(2008,01,25)))
26.0

>>> round(prices.getClose("CSCO", date(2008,01,24)))
25.0

>>> round(prices.getAdjustedClose("CSCO", date(2008,01,30)))
24.0

Exceptions are thrown for dates not supported, or symbols not supported.

>>> prices.getHigh("CHEESE", date(2007,9,30))
Traceback (most recent call last):
    ...
SymbolNotFound: Could not find symbol : \"CHEESE\"

Or if the date is invalid:

>>> prices.getLow("BAC", date(2007,12,30))
Traceback (most recent call last):
    ...
DateNotFound: Symbol \"BAC\" does not support date : 2007-12-30
"""

#from Registry import Register
import urllib
import urlparse
import urllib2
#from Adapt import Adapt
import datetime
#from SymbolLookup import SymbolLookup
import Cached
import WebsiteExceptions

#resolver = SymbolLookup()

#constants derived from how the website currently works
DATE_FORMAT = "%Y-%m-%d"
KEY_SYMBOL = 's'
KEY_TO_DATE_MONTH = 'd'
KEY_TO_DATE_DAY = 'e'
KEY_TO_DATE_YEAR = 'f'
KEY_FREQUENCY = 'g'
VALUE_DAILY = 'd'
KEY_FROM_DATE_MONTH = 'a'
KEY_FROM_DATE_DAY = 'b'
KEY_FROM_DATE_YEAR = 'c'

schema = 'http'
basePage = 'ichart.finance.yahoo.com'
path = 'table.csv'
baseArgs = {'ignore':'.csv'}

#curry urlencode to always decode lists
urlencode = lambda dct: urllib.urlencode(dct, True)

def historicalPricesURL(dct):
    return (schema, basePage, path, '', urlencode(dct), '')

def buildToDate(date):
    return {KEY_TO_DATE_MONTH:date.month-1, KEY_TO_DATE_DAY:date.day, KEY_TO_DATE_YEAR:date.year}

def buildFromDate(date):
    return {KEY_FROM_DATE_MONTH:date.month-1, KEY_FROM_DATE_DAY:date.day, KEY_FROM_DATE_YEAR:date.year}

def buildSymbol(symbol):
    return {KEY_SYMBOL:symbol}

def parseDate(date):
    return datetime.datetime.strptime(date,"%Y-%m-%d").date()

class ParsedCSV(object):
    def __init__(self, csvFile):
        self.dates = {}
        
        #we need to pull out the first line since it's descriptive.  for shits and giggles we use it as a check as well.
        schema = csvFile.readline()
        assert schema == "Date,Open,High,Low,Close,Volume,Adj Close\n"
        
        for entry in csvFile:
            splitEntry = entry.split(",")

            date = splitEntry[0]
            priceInfo = [float(price) for price in splitEntry[1:]]
            parsedDate = parseDate(date)

            #the below is put in right now so that duplicate dates, which might occur
            #due to bugs before 1969, are for now, ignored.            
            if parsedDate in self.dates:
                continue
            
            self.dates[parsedDate] = PriceForDate(parsedDate, priceInfo)

    def __getitem__(self, index):
        return self.dates[index]
    
    def getDates(self):
        return sorted(self.dates.keys())
    
#Plain ole' data
class PriceForDate(object):
    def __init__(self, date, priceArray):
        self.date = date
        self.open = priceArray[0]
        self.high = priceArray[1]
        self.low = priceArray[2]
        self.close = priceArray[3]
        self.volume = priceArray[4]
        self.adjclose = priceArray[5]
                  
   
class HistoricalPrices(object):
    def __init__(self):
        pass
    
    @Cached.cached(100)
    def historicalPrices(self, symbol, fromDate=None, toDate=None):
        
        #TODO: will check date sanity up front using financial date
        #and rear-end check after the website hit
        
        if not fromDate:
            fromDate = datetime.date(1950,1,1)
        if not toDate:
            toDate = datetime.date.today()
        
        #NOTE: introduce yahoo symbol class that stands for a yahoo symbol rather than using this resolver.    
        #resolve to yahoo style symbols
        #symbol = resolver.getYahoo(symbol)
        
        #we'll introduce a financial date class, rather than adaptation
        assert isinstance(fromDate, datetime.date)
        #fromDate = Adapt(fromDate, datetime.date)
        
        assert isinstance(toDate, datetime.date)
        #toDate = Adapt(toDate, datetime.date)
        args = baseArgs.copy()
        
        args.update(buildSymbol(symbol))
        args.update(buildToDate(toDate))
        args.update(buildFromDate(fromDate))
        
        url = historicalPricesURL(args)
        raw_url = urlparse.urlunparse(url)
        
        try:
            return ParsedCSV(urllib2.urlopen(raw_url))
        except urllib2.HTTPError, e:
            raise WebsiteExceptions.SymbolNotFound(symbol)
    
    @WebsiteExceptions.ThrowsDateError
    def getHigh(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].high
        return self.historicalPrices(symbol)[date].high
    
    @WebsiteExceptions.ThrowsDateError
    def getAdjustedClose(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].adjclose
        return self.historicalPrices(symbol)[date].adjclose
    
    #TODO: remove throwsdate error once date checking is done on front ends
    @WebsiteExceptions.ThrowsDateError
    def getVolume(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].volume
        return self.historicalPrices(symbol)[date].volume
       
    @WebsiteExceptions.ThrowsDateError
    def getLow(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].low
        return self.historicalPrices(symbol)[date].low
    

    @WebsiteExceptions.ThrowsDateError
    def getOpen(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].open
        return self.historicalPrices(symbol)[date].open

    def getDates(self, symbol):
        #yahoo has a bug that it gives us 1962,1,1 so we throw those out.
        return [_date for _date in self.historicalPrices(symbol).getDates() if _date > datetime.date(1962,01,02)]
    
    @WebsiteExceptions.ThrowsDateError
    def getClose(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].close
        return self.historicalPrices(symbol)[date].close
        
        