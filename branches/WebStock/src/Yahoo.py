import BeautifulSoup
import datetime
import urllib2
from utilities import isString, dateFromString, publicInterface, Cache, checkCache, delegateInterface
import Website
import re
from Website import SymbolNotFound, DateNotFound
import SymbolLookup
from Cached import cached

import sys
sys.path.append(r"C:\Users\John\Workspace\Webstock\src\Experimental")
from Registry import Register
from Service import Service
from Signature import Signature

class Yahoo(Website.Website):
	""" Class represents a scraping framework for the yahoo website.  Currently provides price information. 
	
	>>> scraper = Yahoo()
	>>> scraper.getHigh("IRBT",datetime.date(2007,4,2)) == 13.37
	True
	
	>>> scraper.getLow("IRBT",datetime.date(2007,4,2)) == 13.12
	True
	
	>>> scraper.getVolume("IRBT",datetime.date(2007,4,2)) == 174900.0
	True
	
	>>> scraper.getOpen("IRBT",datetime.date(2007,4,2)) == 13.20
	True
	
	>>> scraper.getClose("IRBT",datetime.date(2007,4,2)) == 13.19
	True
	
	Adjusted close is used to account for splits and dividends
	>>> scraper.getAdjustedClose("IRBT",datetime.date(2007,4,2)) ==	13.19
	True
	
	We can get a group of prices just by adding another date.
	
	>>> scraper.getClose("IRBT", datetime.date(2007,1,5), datetime.date(2007,1,10)) == [17.77, 17.56, 18.20]
	True
	
	Date information can be gathered seperately(inclusive on begining and exclusive on ending)
	>>> scraper.getDates("IRBT", datetime.date(2007,1,5), datetime.date(2007,1,10))
	[datetime.date(2007, 1, 5), datetime.date(2007, 1, 8), datetime.date(2007, 1, 9)]
	
	Or it can be combined
	>>> results = scraper.getClose("IRBT", datetime.date(2007,1,5), datetime.date(2007,1,10), zipDate=True)
	>>> items = results.items()
	>>> items.sort()
	>>> items == [(datetime.date(2007,1,5), 17.77), (datetime.date(2007,1,8), 17.56), (datetime.date(2007,1,9), 18.20)]
	True
	
	Searching for a bad symbol will get an error.  Leaving out the date altogether gets today's value.
	
	>>> scraper.getClose("CHEESE")
	Traceback (most recent call last):
		...
	SymbolNotFound: Could not find symbol : \"CHEESE\"
	
	Searching for a date that data is not available for will also throw an error.
	
	>>> scraper.getClose("BAC", datetime.date(2007,12,30))
	Traceback (most recent call last):
		...
	DateNotFound: Symbol \"BAC\" does not support date : 2007-12-30
	
	You can check for this yourself by calling
	
	>>> scraper.hasDate("BAC", datetime.date(2007,12,30))
	False
	
	inv:
		isinstance(self._soupFactory, Yahoo.SoupFactory)
		isinstance(self._tradingDateCollectionCache,Cache)
		all(hasattr(self,x) for x in publicInterface(Yahoo.TradingDay))
	
	"""
	
	def __init__(self):
		self._soupFactory = Yahoo.SoupFactory()
		self._tradingDateCollectionCache = Cache(lambda key: Yahoo.TradingDayCollection(self._soupFactory,key))
		self.resolver = SymbolLookup.SymbolLookup()
		
	class SoupFactory(object):
		""" Does the work of getting to the price website and building a soup object
		
		
		inv:
			isinstance(self._basicSoupCache, Cache)
			isinstance(self._priceSoupCache, Cache)
			isinstance(self._yahooRoot, basestring)
			self._yahooRoot == "http://finance.yahoo.com"
			self._yahooRoot == Yahoo.SoupFactory._yahooRoot
		"""
		_yahooRoot = "http://finance.yahoo.com"
		
		def __init__(self):
			""" Sets up stuff so I can begin looking up webpages """
			self._basicSoupCache = Cache(lambda key: self._buildBasicSoup(key))
			self._priceSoupCache = Cache(lambda key: self._buildPriceSoup(key))
			print "building a new yahoo"
			
		
		def buildPriceSoup(self, symbol):
			""" Does a lookup of symbol and returns the historical prices page of that soup object.  If
			symbol does not exist, throws.  Caches result on symbol. 
			
			This is exercised via other units.
			#a trophy use case just to exercise the contracts
			
			>>> factory = Yahoo.SoupFactory()
			>>> priceSoup = factory.buildPriceSoup("IRBT")
			
			>>> priceSoup = factory.buildPriceSoup("FART")
			Traceback (most recent call last):
				...
			SymbolNotFound: Could not find symbol : \"FART\"
			
			
			pre:
				isString(symbol)
			post[self._priceSoupCache]:
				isinstance(__return__,BeautifulSoup.BeautifulSoup)
				symbol in self._priceSoupCache.keys()
				isinstance(self._priceSoupCache[symbol], BeautifulSoup.BeautifulSoup)
				self._priceSoupCache[symbol] == __return__
				(len(self._priceSoupCache.keys()) - len(__old__.self._priceSoupCache.keys()) == 1) if (symbol not in __old__.self._priceSoupCache.keys()) else True
			
			"""
			if not self.hasBasicSoup(symbol):
				raise SymbolNotFound(symbol)
		
#			return self._priceSoupCache[symbol]
			return self._buildPriceSoup(symbol)
		
		@classmethod
		@cached(100)
		def _buildPriceSoup(cls, symbol):
			""" Builds a soup from a given symbol.  Assumes symbol exists. 
			
			pre:
				self.hasBasicSoup(symbol)
				isString(symbol)
			post[]:
				isinstance(__return__,BeautifulSoup.BeautifulSoup)
			
			"""
			url = cls._buildPriceURL(symbol)
			webpage = urllib2.urlopen(url)
			return BeautifulSoup.BeautifulSoup(webpage)
		
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
				isinstance(__return__,bool)
			"""
			if not self.hasBasicSoup(symbol) or not self.buildPriceSoup(symbol):
				return False
			return True
		
		@classmethod
		def _buildPriceURL(cls, symbol):
			""" Returns the URL for the historical price information for this symbol.  Assumes
			symbol is valid 
			
			pre:
				self.hasBasicSoup(symbol)
				isString(symbol)
			post[]:
				isString(__return__)
			"""
			soup = cls.buildBasicSoup(symbol)
			historicalPricesRE = re.compile("Historical Prices")
			
			#for future reference:
			# for link in soup.findAll('a',text=historicalPricesRE):
			# that ^^^ will return the one link I'm looking for
			# but it only returns the navigable string!
			
			for link in soup.findAll('a'):
				if historicalPricesRE.search(str(link.string)):
					return cls._buildYahooURL(link['href'])
		
		@classmethod
		def _buildYahooURL(cls, relativeURL):
			""" Builds the URL to get from http://yahoo... 
			
			pre:
				isinstance(relativeURL, basestring)
			post[]:
				isinstance(__return__, basestring)
			
			"""
			return "".join([cls._yahooRoot,relativeURL])
		
		@classmethod
		def _buildBasicURL(cls, symbol):
			""" Returns what should be the URL for the root page for this symbol. 
			
			pre:
				isString(symbol)
			post[]:
				isString(__return__)
			"""
			return cls._buildYahooURL("/q?s=%s" % symbol) 
			
		@classmethod
		def buildBasicSoup(cls, symbol):
			""" Finds the root yahoo page for this symbol.  Can be used to see if symbol exists.
			The webpage looked up will be found no matter what, but analysis of whats in the soup 
			is done by other functions like hasBasicSoup.  Cache's basic soup pages.
			
			Trophy to exercise contracts:
			
			>>> scraper = Yahoo.SoupFactory()
			>>> basicSoup = scraper.buildBasicSoup("IRBT")
			
			pre:
				isString(symbol)
			post[self._basicSoupCache]:
				isinstance(__return__,BeautifulSoup.BeautifulSoup)
				symbol in self._basicSoupCache.keys()
				isinstance(self._basicSoupCache[symbol], BeautifulSoup.BeautifulSoup)
				self._basicSoupCache[symbol] == __return__
				(len(self._basicSoupCache.keys()) - len(__old__.self._basicSoupCache.keys()) == 1) if (symbol not in __old__.self._basicSoupCache.keys()) else True
			 """

			return cls._buildBasicSoup(symbol)
			#return self._basicSoupCache[symbol]
		
		@classmethod
		@cached(100)
		def _buildBasicSoup(cls, symbol):
			""" Finds the root yahoo page for this symbol.  Does not cache. 
			
			pre:
				isString(symbol)
			post[]:
				isinstance(__return__,BeautifulSoup.BeautifulSoup)
			"""
			url = cls._buildBasicURL(symbol)
			webpage = urllib2.urlopen(url)
			return BeautifulSoup.BeautifulSoup(webpage)
		
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
			potentialBasicSoup = self.buildBasicSoup(symbol)
			rightTitleRe = re.compile("".join([symbol,": Summary for .* - Yahoo! Finance"]))
			wrongTitleRe = re.compile("Symbol Lookup from Yahoo! Finance")
			
			title = potentialBasicSoup.find('title')
			
			if rightTitleRe.search(str(title)):
				return True
			elif wrongTitleRe.search(str(title)):
				return False
			else:
				raise Exception("I dont know whether this is a basic soup or not")
			
	
	class TradingDayCollection(object):
		""" Downloads and parses price information from a soup object.
		Price information closed on symbol/soup.
		
		inv:
			isinstance(self.tradingDayDict, dict) if self.invSet else True
			all(isinstance(x,datetime.date) for x in self.tradingDayDict.keys()) if self.invSet else True
			all(isinstance(x,Yahoo.TradingDay) for x in self.tradingDayDict.values()) if self.invSet else True
			isinstance(self.dateList,list) if self.invSet else True 
			all(isinstance(x,datetime.date) for x in self.dateList) if self.invSet else True
			all(x in self.tradingDayDict for x in self.dateList) if self.invSet else True
			all(x in self.dateList for x in self.tradingDayDict.keys()) if self.invSet else True
			self.dateList == sorted(self.dateList) if self.invSet else True
			self.dateList[-1] <= datetime.date.today()
		
		"""
		
		def __init__(self, factory, symbol):
			""" Parses soup to find downloadable historical data and then 
			becomes a container for that data, providing collection like
			access with dates being index
			
			pre:
				isinstance(factory,Yahoo.SoupFactory) 
				isinstance(symbol,basestring)
			"""
			self.invSet = False
			self._factory = factory
			self._symbol = symbol
			self._soup = self._factory.buildPriceSoup(self._symbol)
			self.tradingDayDict = self._parseCSV(self._getHistoricalPriceCSV(self._soup))
			self.dateList = sorted(self.tradingDayDict.keys())
			self.invSet = True
		
		def _getHistoricalPriceCSV(self, soup):
			""" Parses the soup to find the price link and returns it's contents(after a URL lookup) 
			
			Returns a file like object containing all the price information.
			
			pre:
				isinstance(soup,BeautifulSoup.BeautifulSoup)
			post[]:
				#returns a file-like object
				hasattr(__return__,"readlines")
			"""
			linkRe = re.compile("Download To Spreadsheet")
			
			for link in soup.findAll('a'):
				if linkRe.search(str(link)):
					return urllib2.urlopen(link['href'])
		
		def _parseCSV(self, commaDelimitedInfo):
			""" Parses commaDelimitedInfo into a base database holding dates to TradingDays 
			
			Takes in a file-like object containing price information and stores it in a 
			common dict, returns dict.
			
			pre:
				#takes in a file like object
				hasattr(commaDelimitedInfo,"readlines")
			
			post[]:
				isinstance(__return__,dict)
				all(isinstance(x,datetime.date) for x in __return__.keys())
				all(isinstance(x,Yahoo.TradingDay) for x in __return__.values())
			"""
			toReturn = {}
			for entry in commaDelimitedInfo.readlines()[1:]:
				splitEntry = entry.split(",")
				date = dateFromString(splitEntry[0])
				(open,high,low,close,volume,adjclose) = [float(x) for x in splitEntry[1:]]
				if date in toReturn:
					continue
				#the above is put in right now so that duplicate dates, which might occur
				#due to bugs before 1969, are for now, ignored.
				toReturn[date] = Yahoo.TradingDay(date, open, high, low, close, volume, adjclose)
			
			return toReturn
		
		def _getitem_slice_(self,index):
			""" Private method that handles indexing on slices.  Right now stepsize isn't
			really supported, although this is probably a TODO.  Throws if begining date
			is before supported dates, or after date is after supported dates, OR begining
			date is after ending date.
			
			
			
			pre:
				isinstance(index,slice)
				index.step == 1 or index.step == None
			post[]:
				isinstance(__return__, list)
				all(isinstance(x,Yahoo.TradingDay) for x in __return__)
			"""
			
			if (index.start < self.dateList[0] or index.stop > self.dateList[-1] or
				index.start > index.stop):
				raise Exception("Invalid slicing in TradingDayCollection")
			 
			return [self.tradingDayDict[x] for x in self.getDates(index.start,index.stop)]
			
		
		def _getitem_date_(self,index):
			""" Private method for getting an item based on a single date index.
			
			pre:
				isinstance(index,datetime.date)
			post[]:
				isinstance(__return__,Yahoo.TradingDay)
				
			"""
			if index not in self.dateList:
				raise DateNotFound(self._symbol,index)
			return self.tradingDayDict[index]
			
		def __getitem__(self, index):
			""" Provides index access to the collection of trading days.
			index can be a single date or a slice of dates. If index(date) does
			not exist, throws.
			
			pre:
				isinstance(index, datetime.date) or isinstance(index,slice)
				(isinstance(index.start,datetime.date) and isinstance(index.stop,datetime.date)) if isinstance(index,slice) else True
			post[]:
				isinstance(__return__,Yahoo.TradingDay) if isinstance(index,datetime.date) else True
				isinstance(__return__,list) if isinstance(index,slice) else True
				all(isinstance(x,Yahoo.TradingDay) for x in __return__) if isinstance(index,slice) else True
			
			"""
			if(isinstance(index,slice)):
				return self._getitem_slice_(index)
			elif(isinstance(index, datetime.datetime)): #maitenence.  passing datetimes around everywhere else, and dates here. added support for dates.
				return self._getitem_date_(datetime.date(index.year,index.month,index.day))
			elif(isinstance(index,datetime.date)):
				return self._getitem_date_(index)
			#should i handle integer arguments as well?
			#just date arguments for now
			#dict access automatically throws if index is not in here.
			
		def __iter__(self):
			""" Provides iterator access, iterating on date and returning
			each TradingDay in sequence 
			
			#can't do post condition checking on the generator...
			"""
			for tradingDay in self.dateList:
				yield self.tradingDayDict[tradingDay]
		
		def hasDate(self, aDate):
			""" Predicate that returns whether or not this date is in the collection of
			trading dates for this stock 
			
			pre:
				isinstance(aDate,datetime.date)
			post[]:
				isinstance(__return__,bool)
			"""
			return (aDate in self.dateList)
			
		def getDates(self, dateFrom=None, dateTo=None):
			""" Returns the trading dates available between dateFrom and dateTo.  If either is left out, assumed to be the very
			begining or very end
			
			pre:
				isinstance(dateFrom,datetime.date) if dateFrom else True
				isinstance(dateTo,datetime.date) if dateTo else True
			post[]:
				isinstance(__return__,list)
				all(isinstance(x,datetime.date) for x in __return__)
				__return__ == sorted(__return__)
				#inclusive of the begining and exclusive of the end
				dateTo not in __return__ 
			"""
			if not dateFrom:
				dateFrom = self.getBeginingDate()
			if not dateTo:
				dateTo = self.getEndingDate()
			
			toReturn =  [date for date in self.dateList if (date >= dateFrom) and (date <= dateTo)]
			return toReturn[:-1] if dateTo in toReturn else toReturn #strip off the last date exclusively if it's in the list			
			
		def getBeginingDate(self):
			""" Returns the first date this collection supports 
			
			post[]:
				isinstance(__return__,datetime.date)
			"""
			return self.dateList[0]
			
		
		def getEndingDate(self):
			""" Returns the last date this collection supports 
			
			post[]:
				isinstance(__return__,datetime.date)
			"""
			return self.dateList[-1]
	
	class TradingDay(object):
		""" Price information closed on date 
		
		inv:
			isinstance(self.date,datetime.date)
			isinstance(self.high,float)
			isinstance(self.low,float)
			isinstance(self.close,float)
			isinstance(self.open,float)
			isinstance(self.volume,float)
			isinstance(self.adjclose,float)
			self.high >= self.low
			self.close >= self.low and self.close <= self.high
			self.open >= self.low and self.open <= self.high
			self.high >= 0.0
			self.low >= 0.0
			self.close >= 0.0
			self.open >= 0.0
			self.volume >= 0.0
			self.adjclose >= 0.0
		"""
		def __init__(self, date, open, high, low, close, volume, adjclose):
			""" Builds the simple information holder trading day 
			
			pre:
				isinstance(date,datetime.date)
				isinstance(high,float)
				isinstance(low,float)
				isinstance(close,float)
				isinstance(open,float)
				isinstance(volume,float)
				isinstance(adjclose,float)
			"""		
			
			self.date = date
			self.high = high
			self.low = low
			self.close = close
			self.open = open
			self.volume = volume
			self.adjclose = adjclose
		
		def getDate(self):
			""" Returns the date that this trading day represents 
			
			post[self.date]:
				self.date == __old__.self.date
				isinstance(__return__,datetime.date)
			"""
			return self.date
		
		def getHigh(self):
			""" Returns the high price for this trading day 
			
			post[self.high]:
				self.high == __old__.self.high
				isinstance(__return__,float)
			"""
			return self.high
		
		def getLow(self):
			""" Returns the low price for this trading day 
			
			post[self.low]:
				self.low == __old__.self.low
				isinstance(__return__,float)
			"""
			return self.low
		
		def getClose(self):
			""" Returns the closing price for this trading day 
			
			post[self.close]:
				self.close == __old__.self.close
				isinstance(__return__,float)
			"""
			return self.close
		
		def getOpen(self):
			""" Returns the opening price for this trading day 
			
			post[self.open]:
				self.open == __old__.self.open
				isinstance(__return__,float)
			
			"""
			return self.open
		
		def getVolume(self):
			""" Returns the volume information for this trading day 
			
			post[self.volume]:
				self.volume == __old__.self.volume
				isinstance(__return__,float)
			"""
			return self.volume
		
		def getAdjustedClose(self):
			""" Returns the adjusted close information for this trading day 
			
			post[self.adjclose]:
				self.adjclose == __old__.self.adjclose
				isinstance(__return__,float)
			"""
			return self.adjclose
		
		def isValid(self):
			""" Helper that just does the invariance checks."""
			return all([self.open <= self.high, 
						self.close <= self.high, 
						self.open >= self.low,
						self.close >= self.close,
						self.low <= self.high,
						self.open >= 0.0,
						self.close >= 0.0,
						self.high >= 0.0,
						self.low >= 0.0,
						self.volume >= 0.0,
						self.adjclose >= 0.0])
	
	def _priceWrapper(self, method, symbol, dateTo=None, dateFrom=None, zipDate=False, **kwargs):
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
			callable(getattr(Yahoo.TradingDay,method))
			isString(symbol)
			(not zipDate) if (not dateFrom) else dateFrom
		post[self._tradingDateCollectionCache]:
			isinstance(__return__,list) if (dateFrom and not zipDate) else True
			isinstance(__return__,float) if not dateFrom else True
			isinstance(__return__,dict) if zipDate else True
			all(isinstance(x,datetime.date) for x in __return__.keys()) if zipDate else True
			all(isinstance(x,float) for x in __return__.values()) if zipDate else True
			all(isinstance(x,float) for x in __return__) if (dateFrom and not zipDate) else True
			checkCache(self._tradingDateCollectionCache,__old__.self._tradingDateCollectionCache,symbol)
			
		"""
#		if symbol not in self._tradingDateCollectionCache:
#			self._tradingDateCollectionCache[symbol] = Yahoo.TradingDayCollection(self._soupFactory,symbol)

	   #maintenence. the Registry paradigm passes in a date keyword, while this actual wrapper takes in a 'dateTo' 
	   #and 'dateFrom'.  I unfortunately did way more to yahoo than just provide a web interface to find certain things
	   #which is bad.  
		if "date" in kwargs and not dateTo:
			dateTo = kwargs["date"]
			
		#resolve to yahoo style symbols
		symbol = self.resolver.getYahoo(symbol)
		
		#three cases:
		#if no date is passed in, use today.
		if not dateTo:
			tradingDay = self._tradingDateCollectionCache[symbol][datetime.date.today()]
			return getattr(tradingDay,method)()
			
		#if one date is passed in
		if dateTo and not dateFrom:
			tradingDay = self._tradingDateCollectionCache[symbol][dateTo]
			return getattr(tradingDay,method)()
			
			
		
		#if both dates passed in
		tradingDays = self._tradingDateCollectionCache[symbol][dateTo:dateFrom]
		values = [getattr(x,method)() for x in tradingDays]
		if(zipDate):
			dates = [x.getDate() for x in tradingDays]
			return dict(zip(dates,values))
		else:
			return values
		
	
	def hasPrice(self, symbol):
		""" Predicate whether or not price information exists for the given symbol
		
		>>> scraper = Yahoo()
		>>> scraper.hasPrice("IRBT")
		True
		
		>>> scraper.hasPrice("CHEESE")
		False
	
		pre:
			isString(symbol)
		post[]:
			isinstance(__return__,bool)
		 
		"""
		
		#resolve to yahoo style symbols
		symbol = self.resolver.getYahoo(symbol)
		
		return self._soupFactory.hasPriceSoup(symbol) 
	
	def getDates(self, symbol, dateFrom=None, dateTo=None):
		""" Gets all trading days available for this symbol from dateFrom to dateTo.  Throws 
		if symbol is bad.  
		
		>>> scraper = Yahoo()
		>>> scraper.getDates("IRBT", datetime.date(2007,1,5), datetime.date(2007,1,10))
		[datetime.date(2007, 1, 5), datetime.date(2007, 1, 8), datetime.date(2007, 1, 9)]
		
		>>> scraper.getDates("IRBT", datetime.date(2007,1,6), datetime.date(2007,1,7))
		[]
		
		In the future, this might give dates backwards, but for now, at least it shouldn't fail.
		
		>>> scraper.getDates("IRBT", datetime.date(2007,1,10), datetime.date(2007,1,5))
		[]
		
		If either date is not provided, assumed to be the very begining or very end.
		
		>> len(scraper.getDates("IRBT")) >= 100
		True
	
		pre:
			isinstance(dateFrom, datetime.date) if dateFrom else True
			isinstance(dateTo, datetime.date) if dateFrom else True
			isString(symbol)
		post[self._tradingDateCollectionCache]:
			isinstance(__return__,list)
			all(isinstance(x,datetime.date) for x in __return__)
			__return__ == sorted(__return__)
			checkCache(self._tradingDateCollectionCache,__old__.self._tradingDateCollectionCache,symbol)
		"""
		
		#resolve to yahoo style symbols
		symbol = self.resolver.getYahoo(symbol)
		
		return self._tradingDateCollectionCache[symbol].getDates(dateFrom,dateTo) #-1 at the end because normal slices just give you the begining incluse and ending exclusive
	
	def hasDate(self, symbol, date=None):
		""" Predicate whether or not price information for the given symbol is available for
		the given date.  If symbol is bad, throws. 
		
		>>> scraper = Yahoo()
		>>> scraper.hasDate(("IRBT"), datetime.date(2007, 6, 1))
		True
		
		>>> scraper.hasDate(("IRBT"), datetime.date(2007, 6, 2))
		False
		
		>>> scraper.hasDate(("CHEESE"), datetime.date(2007, 5, 1))
		Traceback (most recent call last):
			...
		SymbolNotFound: Could not find symbol : \"CHEESE\"
		
		pre:
			isinstance(date,datetime.date)
			isString(symbol)
		post[self._tradingDateCollectionCache]:
			isinstance(__return__,bool)
			checkCache(self._tradingDateCollectionCache,__old__.self._tradingDateCollectionCache,symbol)
		
		"""
		
#		if symbol not in self._tradingDateCollectionCache:
#			self._tradingDateCollectionCache[symbol] = Yahoo.TradingDayCollection(self._soupFactory,symbol)
		
		#resolve to yahoo style symbols
		symbol = self.resolver.getYahoo(symbol)
		
		if not date:
			date = datetime.date.today()
			
		return self._tradingDateCollectionCache[symbol].hasDate(date)
delegateInterface(Yahoo,Yahoo.TradingDay,Yahoo._priceWrapper)

Register(Service.Daily("High"))(Yahoo.getHigh)
Register(Service.Meta("DailyTradingDayDates"))(Yahoo.getDates)
Register(Service.Meta("DailyFundamentalsDates"))(Yahoo.getDates)