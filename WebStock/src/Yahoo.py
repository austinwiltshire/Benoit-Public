import BeautifulSoup
import datetime
from utilities import isString

class Yahoo(website):
	""" Class represents a scraping framework for the yahoo website.  Currently provides price information. 
	
	>>> scraper = Yahoo()
	>>> scraper.getHigh("IRBT",datetime.date(2007,4,1))
	18.25
	
	>>> scraper.getLow("IRBT",datetime.date(2007,4,1))
	17.50
	
	>>> scraper.getVolume("IRBT",datetime.date(2007,4,1))
	226900.00
	
	>>> scraper.getOpen("IRBT",datetime.date(2007,4,1))
	18.06
	
	>>> scraper.getClose("IRBT",datetime.date(2007,4,1))
	17.87
	
	Adjusted close is used to account for splits and dividends
	>>> scraper.getAdjustedClose("IRBT",datetime.date(2007,4,1))
	17.87
	
	We can get a group of prices just by adding another date.
	
	>>> scraper.getClose("IRBT", datetime.date(2007,5,1), datetime.date(2007,10,1))
	[17.77, 17.56, 18.20, 17.89]
	
	Date information can be gathered seperately
	>>> scraper.getDates("IRBT", datetime.date(2007,5,1), datetime.date(2007,10,1))
	[datetime.date(2007,5,1), datetime.date(2007,8,1), datetime.date(2007,9,1), datetime.date(2007,10,1)]
	
	Or it can be combined
	>>> results = scraper.getClose("IRBT", datetime.date(2007,5,1), datetime.date(2007,10,1), zipDate=True)
	>>> items = result.items()
	>>> items.sort()
	>>> for item in items:
	>>> ... print item
	(datetime.date(2007,5,1), 17.77)
	(datetime.date(2007,8,1), 17.56)
	(datetime.date(2007,9,1), 18.20)
	(datetime.date(2007,10,1), 17.89)
	
	Searching for a bad symbol will get an error.  Leaving out the date altogether gets today's value.
	
	>>> scraper.getClose("CHEESE")
	Traceback (most recent call last):
		...
	SymbolNotFound: Could not find symbol : \"CHEESE\"
	
	Searching for a date that data is not available for will also throw an error.
	
	>>> scraper.getAnnualDeferredTaxes("CFC", datetime.date(2007,12,30))
	Traceback (most recent call last):
		...
	DateNotFound: Symbol \"CFC\" does not support date : 2007-12-30
	
	You can check for this yourself by calling
	
	>>> scraper.hasPrice("CFC", datetime.date(2007,12,30))
	False
	
	inv:
		self.soupFactory != None
	
	"""
	
	class SoupFactory:
		""" Does the work of getting to the price website and building a soup object"""
		def __init__(self):
			""" Sets up stuff so I can begin looking up webpages """
			pass
		
		def buildPriceSoup(self, symbol):
			""" Does a lookup of symbol and returns the historical prices page of that soup object.  If
			symbol does not exist, throws. 
			
			#TODO: add a unit test for this since an example would have to parse a soup object...
			
			pre:
				isString(symbol)
			post[]:
				isinstance(__return__,BeautifulSoup.BeautifulSoup)
			
			"""
			pass
		
		def _buildPriceSoup(self, symbol):
			""" Builds a soup from a given symbol.  Assumes symbol exists. 
			
			pre:
				self.hasPriceSoup(symbol)
				isString(symbol)
			post[]:
				isinstance(__return__,BeautifulSoup.BeautifulSoup)
			
			"""
		
		def hasPriceSoup(self, symbol):
			""" Predicate to return whether this symbol supports historical price information 
			
			>>> scraper = Yahoo.SoupFactory()
			>>> scraper.hasPriceSoup("IRBT")
			True
			
			>>> scraper.hasPriceSoup("FART")
			False
			#TODO: is there a case where a basic soup exists but historical price data does not?
			
			pre:
				isString(symbol)
			post[]:
				isinstance(__return__,boolean)
			"""
			pass
		
		def _buildPriceURL(self, symbol):
			""" Returns the URL for the historical price information for this symbol.  Assumes
			symbol is valid 
			
			pre:
				self.hasBasicSoup(symbol)
				isString(symbol)
			post[]:
				isString(__return__)
			"""
			pass
		
		def _buildBasicURL(self, symbol):
			""" Returns what should be the URL for the root page for this symbol. 
			
			pre:
				isString(symbol)
			post[]:
				isString(__return__)
			"""
			pass
			
		def buildBasicSoup(self, symbol):
			""" Finds the root yahoo page for this symbol.  Can be used to see if symbol exists.
			The webpage looked up will be found no matter what, but analysis of whats in the soup 
			is done by other functions like hasBasicSoup.
			
			pre:
				isString(symbol)
			post[]:
				isinstance(__return__,BeautifulSoup.BeautifulSoup)
			 """
			pass
		
		def hasBasicSoup(self, symbol):
			""" Predicate returning whether the root yahoo page for this symbol is that of one that
			supports information.  In other words, if this returns false, yahoo does not support
			this symbol
			
			>>> scraper = Yahoo.SoupFactory()
			>>> scraper.hasBasicSoup("FART")
			False
			
			>>> scraper.hasBasicSoup("IRBT")
			True
			
			pre:
				isString(symbol)
			post[]:
				isinstance(__return__,bool)
			 
			"""
			pass
	
	class TradingDayCollection:
		""" Downloads and parses price information from a soup object.
		Price information closed on symbol/soup.
		"""
		
		def __init__(self, soup):
			""" Parses soup to find downloadable historical data and then 
			becomes a container for that data, providing collection like
			access with dates being index """
			pass
		
		def _getHistoricalPrice(self, soup):
			""" Parses the soup to find the price link and returns it's contents(after a URL lookup) """
			pass
		
		def _parseCSV(self, commaDelimitedInfo):
			""" Parses commaDelimitedInfo into a base database holding dates to TradingDays """
			pass
		
		def __getitem__(self, index):
			""" Provides index access to the collection of trading days.
			index can be a single date or a slice of dates. If index(date) does
			not exist, throws."""
			#should i handle integer arguments as well?
			pass
			
		def iter(self):
			""" Provides iterator access, iterating on date and returning
			each TradingDay in sequence """
			pass
		
		def hasDate(self, aDate):
			""" Predicate that returns whether or not this date is in the collection of
			trading dates for this stock """
			pass
			#can i build my own generator class that will handle slice notation on dates?
			
		def getDates(self, dateFrom, dateTo):
			""" Returns the trading days available between dateFrom and dateTo """
			
		def getBeginingDate(self):
			""" Returns the first date this collection supports """
			pass
		
		def getEndingDate(self):
			""" Returns the last date this collection supports """
			pass
	
	class TradingDay:
		""" Price information closed on date """
		def __init__(self, date, high, low, close, open, volume, adjclose):
			""" Builds the simple information holder trading day """
			pass
		
		def getDate(self):
			""" Returns the date that this trading day represents """
			pass
		
		def getHigh(self):
			""" Returns the high price for this trading day """
			pass
		
		def getLow(self):
			""" Returns the low price for this trading day """
			pass
		def getClose(self):
			""" Returns the closing price for this trading day """
			pass
		def getOpen(self):
			""" Returns the opening price for this trading day """
			pass
		def getVolume(self):
			""" Returns the volume information for this trading day """
			pass
		def getAdjustedClose(self):
			""" Returns the adjusted close information for this trading day """
			pass
	
	def _PriceWrapper(self, method, symbol, dateTo=None, dateFrom=None, zipDate=False):
		""" Wraps the delegated interface TradingDay.  Symbol is used as a dict
		lookup to find a corresponding PriceCollection, to which date range
		information is passed to get a collection of TradingDay objects, where
		the method is called.  If dateTo is none, we assume today.  If dateFrom
		is none, we assume we only return the date asked for.  If the date does not 
		exist, or today was not a trading day in the case that dateTo did not exist, we 
		throw.  If symbol does not exist, we throw. 
		
		pre:
			isinstance(dateTo, datetime.date) if dateTo else True
			isinstance(dateFrom, datetime.date) if dateFrom else True
			isString(method)
			callable(getattr(TradingDay,method))
			isString(symbol)
			(not zipDate) if (not dateFrom) else dateFrom
		post[]:
			isinstance(__return__,list) if (dateFrom and not zipDate) else isinstance(__return__,float)
			isinstance(__return__,dict) if zipDate else True
			all(isinstance(x,datetime.date) for x in __return__.keys()) if zipDate else True
			all(isinstance(x,float) for x in __return__.values()) if zipDate else True
			all(isinstance(x,float) for x in __return__) if (dateFrom and not zipDate) else True
			
		"""
		pass
	
	def hasPrice(self, symbol):
		""" Predicate whether or not price information exists for the given symbol
		
		>>> scraper = Yahoo()
		>>> scraper.hasPrice("IRBT")
		True
	
		pre:
			isString(symbol)
		post[]:
			isinstance(__return__,bool)
		 
		"""
		pass
	
	def getDates(self, symbol, dateFrom, dateTo):
		""" Gets all trading days available for this symbol from dateFrom to dateTo.  Throws 
		if symbol is bad.
		
		>>> scraper = Yahoo()
		>>> scraper.getDates("IRBT", datetime.date(2007,5,1), datetime.date(2007,10,1))
		[datetime.date(2007,5,1), datetime.date(2007,8,1), datetime.date(2007,9,1), datetime.date(2007,10,1)]
	
		pre:
			isinstance(dateFrom, datetime.date)
			isinstance(dateTo, datetime.date)
			isString(symbol)
		post[]:
			isinstance(__return__,list)
			all(isinstance(x,datetime.date) for x in __return__)
		"""
		pass
	
	def _getDates(self, symbol, dateFrom, dateTo):
		""" Gets all trading days available for this symbol from dateFrom to dateTo.  Assumes
		symbol is good. 
		
		pre:
			isinstance(dateFrom, datetime.date)
			isinstance(dateTo,datetime.date)
			isString(symbol)
			self.hasPrice(symbol)
		post[]:
			isinstance(__return__,list)
			all(isinstance(x,datetime.date) for x in __return__)
		
		"""
		pass
	
	def hasDate(self, symbol, date):
		""" Predicate whether or not price information for the given symbol is available for
		the given date.  If symbol is bad, throws. 
		
		>>> scraper = Yahoo()
		>>> scraper.hasDate(("IRBT"), datetime.date(2007, 4, 1))
		True
		
		>>> scraper.hasDate(("IRBT"), datetime.date(2007, 6, 1))
		False
		
		>>> scraper.hasDate(("CHEESE"), datetime.date(2007, 5, 1))
		Traceback (most recent call last):
			...
		SymbolNotFound: Could not find symbol : \"CHEESE\"
		
		pre:
			isinstance(date,datetime.date)
			isString(symbol)
		post[]:
			isinstance(__return__,bool)
		
		"""
		pass
	
	def _hasDate(self, symbol, date):
		""" Predicate whether or not price information for the given symbol is available for 
		the given date.  Assumes symbol is valid 
		
		pre:
			isinstance(date,datetime.date)
			isString(symbol)
			self.hasPrice(symbol)
		post[]:
			isinstance(__return__,bool)
		"""
		
		pass
	
	def _DelegateInterface(self):
		pass
	#push this up to an inheritable object.  