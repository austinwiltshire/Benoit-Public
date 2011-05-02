"""
Examples:
>>> from datetime import datetime
>>> prices = HistoricalPrices()
>>> round(prices.getHigh("MRK", datetime(2007,12,31)))
59.0

>>> round(prices.getLow("IBM", datetime(2008,9,30)))
112.0

>> round(prices.getVolume("SBUX", datetime(2008,09,29)))
20719700

>>> round(prices.getOpen("CSCO", datetime(2008,01,25)))
26.0

>>> round(prices.getClose("CSCO", datetime(2008,01,24)))
25.0

>>> round(prices.getAdjustedClose("CSCO", datetime(2008,01,30)))
24.0

Exceptions are thrown for dates not supported, or symbols not supported.

>>> prices.getHigh("CHEESE", datetime(2008,01,30))
Traceback (most recent call last):
    ...
SymbolNotFound: Could not find symbol : \"CHEESE\"

Or if the date is invalid:

>>> prices.getLow("BAC", datetime(2007,12,30))
Traceback (most recent call last):
    ...
DateNotFound: Symbol \"BAC\" does not support date : 2007-12-30 00:00:00
"""

#from Registry import Register
import urllib
import urlparse
import urllib2
#from Adapt import Adapt
import datetime
#from SymbolLookup import SymbolLookup
import YahooFinanceExceptions
import FinancialDate

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
            
            self.dates[parsedDate] = PriceForDate(parsedDate, *priceInfo)

    def __getitem__(self, index):
        return self.dates[index]
    
    def getDates(self):
        return sorted(self.dates.keys())
    
    def _parseDate(self, date):
        return datetime.datetime.strptime(date,"%Y-%m-%d")

class PriceForDate(object):
    def __init__(self, date, open, high, low, close, volume, adjclose):
        self.date = date
        self.open = open
        self.high = high
        self.low = low
        self.close = close
        self.volume = volume
        self.adjclose = adjclose
                  
   
class HistoricalPrices(object):
    
    #yahoo has a bug that it gives us 1962,1,1 for any day on or before that one, so we start the day after
    YAHOO_BASE_DATE = datetime.datetime(1962, 1, 2)
    
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
        
     
        fromDate = self.YAHOO_BASE_DATE
        toDate = datetime.datetime.today()
        
        #NOTE: introduce yahoo symbol class that stands for a yahoo symbol rather than using this resolver.    
        #resolve to yahoo style symbols
        #symbol = resolver.getYahoo(symbol)
        
        #we'll introduce a financial date class, rather than adaptation
        assert isinstance(fromDate, datetime.datetime)
        #fromDate = Adapt(fromDate, datetime.date)
        
        assert isinstance(toDate, datetime.datetime)
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
            raise YahooFinanceExceptions.SymbolNotFound(symbol)
    
    def getPriceForDate(self, symbol, date):
        """ Gets a price object for a day, given a symbol and a date. """
        
        self._check_date(symbol, date)
        
        all_prices = self.historicalPrices(symbol)
        try:
            return all_prices[date]
        except KeyError, e:
            raise YahooFinanceExceptions.DateNotFound(symbol, date)
    
    def getHigh(self, symbol, date):
        """ Gets the highest price for a day given a symbol and a date. """
        
        self._check_date(symbol, date)
       
        return self.getPriceForDate(symbol, date).high
    
    def getAdjustedClose(self, symbol, date):
        """ Gets the close adjusted for splits and dividends by Yahoo for a day, given a symbol and a date. """
        
        self._check_date(symbol, date)

        #return historicalPrices(symbol)[Adapt(date,datetime.date)].adjclose
        
        return self.getPriceForDate(symbol, date).adjclose
    
    def getVolume(self, symbol, date):
        """ Gets trading volume for a day, given a symbol and a date. """
        
        self._check_date(symbol, date)
        
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].volume
        
        return self.getPriceForDate(symbol, date).volume
       
    def getLow(self, symbol, date):
        """ Gets the lowest price for a day given a symbol and a date. """
        
        self._check_date(symbol, date)

        #return historicalPrices(symbol)[Adapt(date,datetime.date)].low
        
        return self.getPriceForDate(symbol, date).low
    

    def getOpen(self, symbol, date):
        """ Gets the opening price given a symbol and a date. """
        
        self._check_date(symbol, date)
        
        #return historicalPrices(symbol)[Adapt(date,datetime.date)].open
        
        return self.getPriceForDate(symbol, date).open

    def getDates(self, symbol):
        """ Gets all supported trading dates for a symbol, up to January 2nd, 1961 due to yahoo constraints. """
        
        return [_date for _date in self.historicalPrices(symbol).getDates() if _date >= self.YAHOO_BASE_DATE]
    
    def getClose(self, symbol, date):
        """ Gets the closing price given a symbol and a date """
        
        self._check_date(symbol, date)
        
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
    
    def _check_date(self, symbol, date):
        assert isinstance(date, datetime.datetime)
        if not FinancialDate.IsTradingDay(date) or date < self.YAHOO_BASE_DATE:
            raise YahooFinanceExceptions.DateNotFound(symbol, date)