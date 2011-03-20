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
import WebsiteExceptions

import LRUCache

#resolver = SymbolLookup()

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
            parsedDate = self._parseDate(date)

            #the below is put in right now so that duplicate dates, which might occur
            #due to bugs before 1969, are for now, ignored.            
            if parsedDate in self.dates:
                continue
            
            self.dates[parsedDate] = PriceForDate(parsedDate, priceInfo)

    def __getitem__(self, index):
        return self.dates[index]
    
    def getDates(self):
        return sorted(self.dates.keys())
    
    def _parseDate(self, date):
        return datetime.datetime.strptime(date,"%Y-%m-%d").date()

    
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
    def __init__(self, cache_size=100):
        self._cache = LRUCache.LRUCache(cache_size)
    
    def historicalPrices(self, symbol):
        
        key = symbol
        if key in self._cache:
            val = self._cache[key]
        else:
            self._cache[key] = val = self.download_historical_prices(symbol)
        return val
       
    def download_historical_prices(self, symbol):
        
        #TODO: will check date sanity up front using financial date
        #and rear-end check after the website hit
        
        fromDate = datetime.date(1950,1,1)
        toDate = datetime.date.today()
        
        #NOTE: introduce yahoo symbol class that stands for a yahoo symbol rather than using this resolver.    
        #resolve to yahoo style symbols
        #symbol = resolver.getYahoo(symbol)
        
        #we'll introduce a financial date class, rather than adaptation
        assert isinstance(fromDate, datetime.date)
        #fromDate = Adapt(fromDate, datetime.date)
        
        assert isinstance(toDate, datetime.date)
        #toDate = Adapt(toDate, datetime.date)
        
        baseArgs = {'ignore':'.csv'}
        args = baseArgs.copy()
        
        args.update(self._buildSymbol(symbol))
        args.update(self._buildToDate(toDate))
        args.update(self._buildFromDate(fromDate))
        
        url = self._historicalPricesURL(args)
        raw_url = urlparse.urlunparse(url)
        
        try:
            return ParsedCSV(urllib2.urlopen(raw_url))
        except urllib2.HTTPError, e:
            raise WebsiteExceptions.SymbolNotFound(symbol)
    
    def getPriceForDate(self, symbol, date):
        
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        
        all_prices = self.historicalPrices(symbol)
        try:
            return all_prices[date]
        except KeyError, e:
            raise WebsiteExceptions.DateNotFound(symbol, date)
    
    def getHigh(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].high
        
        return self.getPriceForDate(symbol, date).high
    
    def getAdjustedClose(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].adjclose
        
        return self.getPriceForDate(symbol, date).adjclose
    
    def getVolume(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].volume
        
        return self.getPriceForDate(symbol, date).volume
       
    def getLow(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].low
        
        return self.getPriceForDate(symbol, date).low
    

    def getOpen(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].open
        
        return self.getPriceForDate(symbol, date).open

    def getDates(self, symbol):
        #yahoo has a bug that it gives us 1962,1,1 so we throw those out.
        return [_date for _date in self.historicalPrices(symbol).getDates() if _date > datetime.date(1962,01,02)]
    
    def getClose(self, symbol, date):
        #typecheck rather than adapt and use financial date in the future
        assert isinstance(date, datetime.date)
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].close
        
        return self.getPriceForDate(symbol, date).close
        
    def _buildToDate(self, date):
        
        #constants derived from how the website currently works
        KEY_TO_DATE_MONTH = 'd'
        KEY_TO_DATE_DAY = 'e'
        KEY_TO_DATE_YEAR = 'f'
        
        return {KEY_TO_DATE_MONTH:date.month-1, KEY_TO_DATE_DAY:date.day, KEY_TO_DATE_YEAR:date.year}

    def _buildFromDate(self, date):
        
        #constants derived from how the website currently works
        KEY_FROM_DATE_MONTH = 'a'
        KEY_FROM_DATE_DAY = 'b'
        KEY_FROM_DATE_YEAR = 'c'
        
        return {KEY_FROM_DATE_MONTH:date.month-1, KEY_FROM_DATE_DAY:date.day, KEY_FROM_DATE_YEAR:date.year}

    def _buildSymbol(self, symbol):
        
        #constants derived from how the website currently works
        KEY_SYMBOL = 's'
        
        return {KEY_SYMBOL:symbol}
    
    def _historicalPricesURL(self, dct):
        #urlencode second argument decodes lists
        
        schema = 'http'
        basePage = 'ichart.finance.yahoo.com'
        path = 'table.csv'
        
        return (schema, basePage, path, '', urllib.urlencode(dct, doseq=True), '')        