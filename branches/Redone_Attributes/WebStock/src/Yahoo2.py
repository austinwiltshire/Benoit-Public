"""
Examples:
>>> from datetime import date
>>> round(getHigh("MRK", date(2007,12,31)))
59.0

>>> round(getLow("IBM", date(2008,9,30)))
112.0

>> round(getVolume("SBUX", date(2008,09,29)))
20719700

>>> round(getOpen("CSCO", date(2008,01,25)))
26.0

>>> round(getClose("CSCO", date(2008,01,24)))
25.0

>>> round(getAdjustedClose("CSCO", date(2008,01,30)))
24.0

Exceptions are thrown for dates not supported, or symbols not supported.

>>> getHigh("CHEESE", date(2007,9,30))
Traceback (most recent call last):
	...
SymbolNotFound: Could not find symbol : \"CHEESE\"

Or if the date is invalid:

>>> getLow("BAC", date(2007,12,30))
Traceback (most recent call last):
	...
DateNotFound: Symbol \"BAC\" does not support date : 2007-12-30
"""

from Registry import Register
import urllib
from urlparse import urlunparse
from urllib2 import urlopen, HTTPError
from Adapt import Adapt
import datetime
from SymbolLookup import SymbolLookup
from utilities import head, tail
from Cached import cached
from Google import ThrowsDateError

from WebsiteExceptions import DateNotFound, SymbolNotFound

resolver = SymbolLookup()

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

@cached(100)
def historicalPrices(symbol, fromDate=None, toDate=None):
	if not fromDate:
		fromDate = datetime.date(1950,1,1)
	if not toDate:
		toDate = datetime.date.today()
		
	#resolve to yahoo style symbols
	symbol = resolver.getYahoo(symbol)
	
	fromDate = Adapt(fromDate, datetime.date)
	toDate = Adapt(toDate, datetime.date)
	args = baseArgs.copy()
	
	args.update(buildSymbol(symbol))
	args.update(buildToDate(toDate))
	args.update(buildFromDate(fromDate))
	
	url = historicalPricesURL(args)
	raw_url = urlunparse(url)
	
	try:
		return ParsedCSV(urlopen(raw_url))
	except HTTPError, e:
		raise SymbolNotFound(symbol)

class ParsedCSV(object):
	def __init__(self, csvFile):
		self.dates = {}
		
		#we need to pull out the first line since it's descriptive.  for shits and giggles we use it as a check as well.
		schema = csvFile.readline()
		assert schema == "Date,Open,High,Low,Close,Volume,Adj Close\n"
		
		for entry in csvFile:
			splitEntry = entry.split(",")

			date = head(splitEntry)
			priceInfo = [float(price) for price in tail(splitEntry)]
			parsedDate = parseDate(head(splitEntry))

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
			
		#invariant checks.. TODO: check these in the database instead.  
#		if not all([self.open <= self.high, 
#					self.close <= self.high, 
#					self.open >= self.low,
#					self.close >= self.close,
#					self.low <= self.high,
#					self.open >= 0.0,
#					self.close >= 0.0,
#					self.high >= 0.0,
#					self.low >= 0.0,
#					self.volume >= 0.0,
#					self.adjclose >= 0.0]):
			#print self.date, self.open, self.high, self.low, self.close, self.volume, self.adjclose, "failed invariant checks."	
		
@ThrowsDateError
def getHigh(symbol, date):
	return historicalPrices(symbol)[Adapt(date,datetime.date)].high
	
@ThrowsDateError
def getClose(symbol, date):
	return historicalPrices(symbol)[Adapt(date,datetime.date)].close
	
def getDates(symbol):
	#yahoo has a bug that it gives us 1962,1,1 so we throw those out.
	return [_date for _date in historicalPrices(symbol).getDates() if _date > datetime.date(1962,01,02)]


@ThrowsDateError
def getOpen(symbol, date):
	return historicalPrices(symbol)[Adapt(date,datetime.date)].open

@ThrowsDateError
def getLow(symbol, date):
	return historicalPrices(symbol)[Adapt(date,datetime.date)].low

@ThrowsDateError
def getVolume(symbol, date):
	return historicalPrices(symbol)[Adapt(date,datetime.date)].volume

@ThrowsDateError
def getAdjustedClose(symbol, date):
	return historicalPrices(symbol)[Adapt(date,datetime.date)].adjclose

		
#Register("DailyHigh",getHigh)
#Register("DailyClose",getClose)
#Register("DailyPricesDates",getDates)
#Register("DailyFundamentalsDates",getDates)