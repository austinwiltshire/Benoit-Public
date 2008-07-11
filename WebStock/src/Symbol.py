"""

Symbol provides a single point of interface to a UnifiedBloomberg, where all calls to bloomberg data are closed on symbol.
This is assumed to be the first argument to all methods, and it is assumed to be a string.

For instance:

>>> ub = UnifiedBloomberg.UnifiedBloomberg(Yahoo.Yahoo,Website.Google)
>>> IRBT = Symbol("IRBT",ub)
>>> IRBT.getHigh(datetime.date(2006,4,20)) == 13.25
True

>>> IRBT.getAnnualRevenue(datetime.date(2006,12,31)) == 13000
True

Multiple iterator functions are provided: 

>>> for day in Daily(IRBT)[datetime.date(2006,1,1):datetime.date(2006,1,10)]:
... 	print day.getHigh()
13.25
13.25
13.25
13.25
...

#note that 'quarterly' is dropped from getOperatingCashFlow() ...

>>> for quarter in Quarterly(IRBT)[datetime.date(2007,1,1):]: # all quarters after 2007
... 	print quarter.getOperatingCashFlow(), quarter.getDate(), quarter.getQuarter()
1000, 2007-3-31, First Quarter
1000, 2007-6-31, Second Quarter
1000, 2007-9-31, Third Quarter
1000, 2007-12-31, Fourth Quarter
...

>>> for year in Annually(IRBT)[:datetime.date(2006,1,1)]: #all years before 2006
...		print year.getTotalAssets(), year.getDate(), year.getYear()
1000, 2005-3-31, 2005


# add test for google meta data since it doesnt ever take date
# add test for yahoo collection data

"""

import UnifiedBloomberg
import Website
import Yahoo
import datetime
from utilities import publicInterface

from dateutil.rrule import *

class Market(object):
	""" A market is a factory for Symbols, which provide access to stock information by symbol name. """
	
	def __init__(self, bloomberg):
		""" A market decides what information it can provide by receiving a bloomberg.  Generally this is a UnifiedBloomberg
		object will all the bloomberg information you want hosted per object. """
		
		class InnerMarketSymbol:
			""" This inner helper class is built on the spot inside Market's initializer.  It associates all the bloomberg's
			information with this class.  This class serves to provide a closure on the stock name itself, and is what market
			returns when you ask it for a particular stock symbol.  All bloomberg information is available from this class, however
			the stock symbol itself does not need to be passed in. 
			
			#inv:
				symbolText is constant
			
			"""
			
			def __init__(self, symbolText, market):
				""" InnerMarketSymbol is really little than just a closure on the symbolText, which is a unicode string.  It
				allows you to ask for any information on any stock without having to pass in the actual symbol name once its
				been associated with the symbol name. It also requires a market reference since ultimately all calls are
				deferred back to market and it's bloomberg object which actually hosts the data. """
				
				self.symbolText = symbolText
				self.market = market
			
			def _getSymbolText(self):
				""" A private accessor method for the internally maintained symbolText.  This, once set, should never change. """
				return self.symbolText
		
		for method in publicInterface(bloomberg):
			setattr(InnerMarketSymbol,method,self._delegateCallBald(bloomberg,method))
			
		self.Symbol = InnerMarketSymbol
			
		class InnerMarketSymbolDate:
			""" This is a variant on a InnerMarketSymbol, in that this object ALSO closes on a particular date, such that for
			most bloomberg information, the user does not need to pass in anything.  This means that any bloomberg info that 
			takes a date range cannot be used with this class, however all objects that take a particular date can be used. """
			
			def __init__(self, symbolText, date, market):
				""" Similar to the InnerMarketSymbol, this object requires symbolText to close on and a market to 
				delegate actual calls back to.  In addition, this object also tracks and maintains a single date which it 
				also passes to all of its bloomberg calls. 
				
				#inv:
					symbol and date are constant
				"""
				
				self.symbolText = symbolText
				self.market = market
				
				if isinstance(date, datetime.datetime):
					date = date.date()
				
				self.date = date
			
			def _getSymbolText(self):
				""" Private accessor to get the symbol text that this object is closed on.  This internally held text should
				never change, once set. """
				return self.symbolText
			
			def getAssociatedDate(self):
				""" This is a public function to allow access to the date that this object has been set to, which is convienient
				especially when this object is being used by iterators. """
				return self.date
			
		for method in publicInterface(bloomberg):
			setattr(InnerMarketSymbolDate,method,self._delegateCallDate(bloomberg,method))
			
		self.SymbolDate = InnerMarketSymbolDate
	
	def _delegateCallBald(self, bloomberg ,method):
		""" This helper method is used to return a pre-built function that InnerSymbols use to delegate any bloomberg calls
		back up to the market, closing on symbol of course.  It expects a bloomberg to call the method on, and a method
		string as well.  Using these, it passes back a pre-built function that takes in a symbol and calls the passed in method
		on the passed in bloomberg using the passed in symbol. """
		def _(symbol,*args,**kwargs):
			""" Internal helper function that closes on a bloomberg and a method string but exposes symbol, which is a string,
			to the caller. This in turn is held by InnerSymbol objects that they may close on the symbol text."""
			return getattr(bloomberg,method)(symbol._getSymbolText(),*args,**kwargs)
		return _
	
	def _delegateCallDate(self, bloomberg ,method):
		""" This helper method is used to return a pre-built function that InnerSymbolDates use to delegate any bloomberg calls
		back up to the market, closing on symbol and date of course.  It expects a bloomberg to call the method on, and a method
		string as well.  Using these, it passes back a pre-built function that takes in a symbol and date and calls the passed in method
		on the passed in bloomberg using the passed in symbol and date. """
		def _(symbolDate,*args,**kwargs):
			""" Internal helper function that closes on a bloomberg and a method string but exposes symbol and date, which is a string,
			to the caller. This in turn is held by InnerSymbolDate objects that they may close on the symbol text."""
			return getattr(bloomberg,method)(symbolDate._getSymbolText(),symbolDate.getAssociatedDate(),*args,**kwargs)
		return _
	
	def _getIterator(self, rule, symbol):
		""" This is an internal private helper function that is used to build iterators.  It expects to be passed in a rule, generally
		descended from dateutils.rrule, that defines a recurence of dates.  It then intersects the set of dates this rule generates
		with the set of dates available from the symbol to create a list of dates that this iterator will iterate over.  It returns
		an object with this information held internally that has iterator semantics. """
		
		dates = symbol.getDates()
		begin,end = dates[0],dates[-1]
		
		recurenceRule = rule(begin,end)
		
		recurences = set((x.date() for x in recurenceRule))
		dates = recurences.intersection(set(dates))
		dates = sorted(list(dates))
		
		return self.SymbolDateIterator(symbol._getSymbolText(), dates, self)
	
	@staticmethod
	def recurenceRuleClosure(freq_, **kwargs):
		""" Is used to build recurrence rules with the date start and date end bound later """
		return lambda begin,end: rrule(freq=freq_, dtstart=begin, until=end, **kwargs)
	
	def Daily(self, symbol):
		""" This convienience method returns an iterator who's iteration is set to days a stock is traded.  This 
		range of dates is in order of earlier dates to later dates, and the iterator returns an InnerSymbolDate object
		that allows access to a stock's bloomberg data closed on date. 
		"""
		return self.SymbolDateIterator(symbol, self.recurenceRuleClosure(freq_=DAILY), self)
	
	def Monthly(self, symbol):
		""" This convienience function builds an iterator who's period is based on months, returning one day per month
		of a given stock, in order of earlier dates to later dates, with access to its bloomberg data."""
		return self.SymbolDateIterator(symbol, self.recurenceRuleClosure(freq_=MONTHLY), self)
	
	def Yearly(self, symbol):
		""" This convienience function builds an iterator who's period is based on years, returning one day per year 
		of a given stock, in order of earlier dates to later dates, with access to its bloomberg data. """
		return self.SymbolDateIterator(symbol, self.recurenceRuleClosure(freq_=YEARLY), self)

	def Quarterly(self, symbol):
		""" The quarterly and annual iterators depend on special information from a bloomberg that provides SEC document
		information.  Hence, they iterate over the quarterly dates of which quaterly SEC information exists, and can thus be 
		queried from the InnerSymbolDate object they return.  Other information that requires a date can also be queried. """
		return self.SymbolQuarterlyIterator(symbol, self)
	
	def Annually(self, symbol):
		""" The quarterly and annual iterators depend on special information from a bloomberg that provides SEC document date
		information.  Hence, this object iterates over the annual data, on the days the documents were filed, earliest dates
		to later dates.  The iterator returns a closed InnerSymbolDate on which sec information can be queried, as well as any
		other bloomberg information that requires a date."""
		return self.SymbolAnnualIterator(symbol, self)

	class SymbolQuarterlyIterator(object):
		""" Quarterly and Annual iterators can not depend on simple date rules since quarterly information and annual information
		is released only at specific times.  This iterator queries the underlying bloomberg on when these dates exist for the
		stock it is assigned to track, and then returns InnerSymbolDate objects closed on symbol and date such that sec information
		access is incredibly easy. Other information that is available for the given dates is, of course, still available via these
		iterators.""" 
		
		def __init__(self, symbol, market):
			""" This class requires a symbol, already created from a market, to be passed in, allowing easy access to its date
			and other information.  They also require a market object, which their outer class provides via the Quarterly convienience
			function, to build SymbolDate objects. """
			self.market = market
			self.symbol = symbol
			
			self.symbolText = symbol._getSymbolText()
			
			cashdates = set(symbol.getQuarterlyCashFlowDates())
			incomedates = set(symbol.getQuarterlyIncomeStatementDates())
			balancedates = set(symbol.getQuarterlyBalanceSheetDates())
		
			self.dates = sorted(cashdates.intersection(incomedates).intersection(balancedates))
			self.index = 0
			self.max = len(self.dates)
			
		def __iter__(self):
			""" The SymbolQuarterlyIterator is itself an iterable object.  Building a new iterator, though, resets the internal
			index.
			
			TODO: is it possible that an iterator may be iterating and then be passed somewhere else, where its index will be restarted?
			"""
			self.index = 0
			return self
			
		def next(self):
			""" This iterator begins at the first available quarter and goes to the last, providing a closed SymbolDate object
			for each quarter's sec filing date. """
			if self.index == self.max:
				raise StopIteration()
			self.index += 1
			return self.market.getSymbolDate(self.symbolText, self.dates[self.index-1])
		
	class SymbolAnnualIterator(object):
		""" Quarterly and Annual iterators can not depend on simple date rules since quarterly information and annual information
		is released only at specific times.  This iterator queries the underlying bloomberg on when these dates exist for the
		stock it is assigned to track, and then returns InnerSymbolDate objects closed on symbol and date such that sec information
		access is incredibly easy. Other information that is available for the given dates is, of course, still available via these
		iterators.
		"""
		def __init__(self, symbol, market):
			self.market = market
			self.symbol = symbol
			
			self.symbolText = symbol._getSymbolText()
			
			cashdates = set(symbol.getAnnualCashFlowDates())
			incomedates = set(symbol.getAnnualIncomeStatementDates())
			balancedates = set(symbol.getAnnualBalanceSheetDates())
		
			self.dates = sorted(cashdates.intersection(incomedates).intersection(balancedates))
			self.index = 0
			self.max = len(self.dates)
			
		def __iter__(self):
			""" The SymbolAnnuallyIterator is itself an iterable object.  Building a new iterator, though, resets the internal
			index.
			
			TODO: is it possible that an iterator may be iterating and then be passed somewhere else, where its index will be restarted?
			"""
			self.index = 0
			return self
			
		def next(self):
			""" This iterator begins at the first available year and goes to the last, providing a closed SymbolDate object
			for each year's sec filing date. """
			if self.index == self.max:
				raise StopIteration()
			self.index += 1
			return self.market.getSymbolDate(self.symbolText, self.dates[self.index-1])
			
	class SymbolDateIterator(object):
		""" This is a multipurpose iterator that returns SymbolDate objects from earliest to latest according to some passed
		in date rule and the dates available for the underlying asset. It is used by the convienience functions Daily, Monthly and
		Yearly """
		
		def __init__(self, symbol, ruleBuilder, market, begin=None, end=None, interval=None):
			""" The constructor for this iterator requires an underlying symbol object to retrieve date and other information,
			a ruleBuilder which expects a date range, a market object passed in by the convienience function, and optional
			range and interval information. """
			self.market = market
			self.ruleBuilder = ruleBuilder
			self.symbol = symbol
						
			self.symbolText = symbol._getSymbolText()
			self.availableDates = symbol.getDates()
			
			if not begin:
				begin = self.availableDates[0]
			
			if not end:
				end = self.availableDates[-1]
				
			if not interval:
				interval = 1
			
			self.interval = interval
				
			rule = ruleBuilder(begin,end)
			recurenceDatesSet = set((x.date() for x in rule[::interval])) #putting interval as a slice on rule here allows us to  go backwards if we want.
			 	   	   	   	   	   	   	   	   	   	   	   	   	   	   	  #which is required to allow SymbolDateIterator to have proper slice notation
			availableDatesSet = set(self.availableDates)
			
			
			#interval is really funny.  right now, it takes every other day out of the recurenceRule set, which means that if the
			#recurence rule set says
			# 1, 3, 5, 7... at interval = 2
			# but the trading days available to me are
			# 2,3,4,5,6,9
			# then the set intersection between the two will be
			# 3,5...
			# while if the interval was done at the final intersection level, the first recurence rule would say
			# 1,2,3,4,5,6,7,8,9...
			# and my dates would still be
			# 2,3,4,5,6,9
			# but now my skip would be
			# 2,4,6,10
					
			self.realdates = sorted(list(recurenceDatesSet.intersection(availableDatesSet)))
			self.max = len(self.realdates)
			
			self.index = 0
			
		def next(self):
			""" This iterator simply pops off the next date from some internally built range of dates and provides a closed
			SymbolDate object for that date. """
			if self.index == self.max:
				raise StopIteration()
			self.index += 1
			return self.market.getSymbolDate(self.symbolText, self.realdates[self.index-1])
		
		def __iter__(self):
			""" The iterator resets itself every time this function is called, otherwise, the SymbolDateIterator object is itself
			iterable. """
			self.index = 0
			return self
		
		def __getitem__(self, sliceOrIndex):
			""" Slicing notation is a little complicated.  If you just want a single date, you can actually get that from 
			any iterator, so long as I actually have info on the date.  For slices, the following rules apply - first, the 
			period BEGINS with the start date, so if you are slicing a yearly iterator, the start of your slice is the new
			start of the period, and years will repeat on that date.  For example, passing in 2005-1-1 as the begining date
			to a yearly iterator will get an iterator that starts at 2005-1-1 and repeats at 2006-1-1, 2007-1-1 ...  The 
			ending date is just the date to stop at.  Intervals are given in integers, and represent the number of dates
			to 'skip' between... A rarely used thing - but slice notation needs to be complete I think. """
			
			
			if isinstance(sliceOrIndex, datetime.date):
				#in the case of a single datetime, i don't really want this thing to act like an iterator.
				index = self.availableDates.index(sliceOrIndex) #done so that list throws an error if i look for a date i dont have
				return self.market.getSymbolDate(self.symbolText, self.availableDates[index])				
			elif isinstance(sliceOrIndex, slice):
				begin = sliceOrIndex.start
				end = sliceOrIndex.stop
				interval = sliceOrIndex.step
				return self.market.SymbolDateIterator(self.symbol, self.ruleBuilder, self.market, begin, end, interval)
			else:
				raise TypeError("A datetime.date or slice of datetime.dates is required")
				
			
		

			
#	def _delegateMethod(self, method):
#		""" Sets the name 'method' on self to be a delegated call to bloomberg.method, except with the first argument
#		bound to symbol """
		
#		setattr(self,method,lambda *args,**kwargs: self._delegateBloombergCall(method, *args, **kwargs))
			
	
	def getSymbol(self, symbolText):
		""" This is a factory function that takes in raw symbol text and provides a closed object on that text, in other words,
		an object that provides bloomberg-like access, yet the user is not required to pass in the symbol string.  This object
		"remembers" what symbol string it's assigned to and can be passed around more convieniently to other functions. """
		return self.Symbol(symbolText, self)
	
	def getSymbolDate(self, symbolText, date):
		""" Similar to getSymbol, this is a factory function that returns an object closed on symbol string AND date, allowing
		the object to be passed around easily and queried without the caller having to know what it's underlying symbol string 
		or date is.  It is also used heavily in the suported symbol date iterators. """
		return self.SymbolDate(symbolText, date, self)
	
#	class Symbol(object):
#		def __init__(self, symbolText, bloomberg):
#			""" Ctor for Symbol.  Binds this symbol to the actual market symbol symbolText, and gives access to any bloomberg information
#			inside bloomberg 
#			
#			>>> SBUX = Symbol("SBUX", UnifiedBloomberg.UnifiedBloomberg(Website.Google,Yahoo.Yahoo))
#			>>> SBUX.getHigh(datetime.date(2006,4,20)) == 30.0
#			True
#			
#			>>> SBUX.getQuarterlyRevenue(datetime.date(2006,3,31)) == 3000
#			True
#			
#			>>> SBUX.getAnnualTotalAssets(datetime.date(2006,3,31)) == 3000
#			False
#			
#			#Requires that the symbol be valid, otherwise raises an InvalidSymbol error.  
#			
#			>>> CHEESE = Symbol("CHEESE", UnifiedBloomberg.UnifiedBloomberg(Website.Google,Yahoo.Yahoo))
#			Traceback (most recent call last):
#			  ...
#			SymbolNotFound: Could not find symbol : \"CHEESE\"
#			
#			>>> DDPrices = Symbol("DD", Yahoo.Yahoo)
#			>>> DDPrices.getHigh(datetime.date(2006,4,20)) == 20.0
#			True
#			
#			pre:
#			  isinstance(symbolText,basestring)
#			  isinstance(bloomberg,Website.Bloomberg)
#			#post[]:
#			  
#			"""
#			self.symbolText = symbolText
#			self._delegatedBloomberg = bloomberg
#			for method in publicInterface(bloomberg):
#				self._delegateMethod(method)
#	
#			  #TODO: move the inspection out in the open when you make Bloomberg stuff explicit.  refactoring the bloomberg
#			  # stuff will also unify the outside delegation versus inside delegation
#			  
#		def _delegateMethod(self, method):
#			""" Sets the name 'method' on self to be a delegated call to bloomberg.method, except with the first argument
#			bound to symbol """
#			
#			setattr(self,method,lambda *args,**kwargs: self._delegateBloombergCall(method, *args, **kwargs))
#			
#		
#			
#		def _delegateBloombergCall(self, method, *args, **kwargs):
#			""" 
#			  Wraps a delegated call to an underlying bloomberg.  Unfortunately, due to the need for a hack, we go ahead
#			  and use the inspect module to tell whether or not a function needs a date or not.  This function expects the
#			  method on the underlying bloomberg, and then the rest are args.
#			  
#			  Eh, we might not use inspect after all
#	
#			pre:
#				isinstance(method, basestring)
#				hasattr(self._delegatedBloomberg,method)
#				callable(getattr(self._delegatedBloomberg,method))
#				'symbol' in inspect.getargspec[0]
#				
#			#post[]:	
#			"""
#			return getattr(self._delegatedBloomberg,method)(self.symbolText, *args, **kwargs)
#		
#		def _getText(self):
#			""" Used inside to be able to build symbols and symbol dates off eachother """
#			return self.text
#	
#	class SymbolDate(object):
#		def __init__(self, symbolText, date, bloomberg):
#			"""Inner class used with the iterators Daily, Monthly, etc.  Binds not only to a symbol but to a date as well.
#				Ctor for Symbol.  Binds this symbol to the actual market symbol symbolText, and gives access to any bloomberg information
#				inside bloomberg 
#		
#				>>> SBUX = Symbol("SBUX", UnifiedBloomberg.UnifiedBloomberg(Website.Google,Yahoo.Yahoo))
#				>>> SBUX.getHigh(datetime.date(2006,4,20)) == 30.0
#				True
#		
#				>>> SBUX.getQuarterlyRevenue(datetime.date(2006,3,31)) == 3000
#				True
#		
#				>>> SBUX.getAnnualTotalAssets(datetime.date(2006,3,31)) == 3000
#				False
#		
#				#Requires that the symbol be valid, otherwise raises an InvalidSymbol error.  
#		
#				>>> CHEESE = Symbol("CHEESE", UnifiedBloomberg.UnifiedBloomberg(Website.Google,Yahoo.Yahoo))
#				Traceback (most recent call last):
#					...
#				SymbolNotFound: Could not find symbol : \"CHEESE\"
#		
#				>>> DDPrices = Symbol("DD", Yahoo.Yahoo)
#				>>> DDPrices.getHigh(datetime.date(2006,4,20)) == 20.0
#				True
#		
#				pre:
#					isinstance(symbolText,basestring)
#					isinstance(bloomberg,Website.Bloomberg)
#			"""
#			self.symbolText = symbolText
#			self.date = date
#			self._delegatedBloomberg = bloomberg
#			for method in publicInterface(bloomberg):
#				self._delegateMethod(method)
#
#		def _delegateMethod(self, method):
#			""" Sets the name 'method' on self to be a delegated call to bloomberg.method, except with the first argument
#				bound to symbol """
#		
#			setattr(self,method,lambda *args,**kwargs: self._delegateBloombergCall(method, *args, **kwargs))
#		
#		def _delegateBloombergCall(self, method, *args, **kwargs):
#			"""Wraps a delegated call to an underlying bloomberg.  Unfortunately, due to the need for a hack, we go ahead
#				and use the inspect module to tell whether or not a function needs a date or not.  This function expects the
#				method on the underlying bloomberg, and then the rest are args.
#		  
#				Eh, we might not use inspect after all
#
#				pre:
#					isinstance(method, basestring)
#					hasattr(self._delegatedBloomberg,method)
#					callable(getattr(self._delegatedBloomberg,method))
#					'symbol' in inspect.getargspec[0]
#			"""
#			return getattr(self._delegatedBloomberg,method)(self.symbolText, self.date, *args, **kwargs)
#		
#		 
#		
#	class SymbolIterator(object):
#		def __init__(self, symbolText, recuranceDates, bloomberg):
#			""" Used to build the Daily, Monthly, etc., iterators object.  Timedelta is derived from dateutil types, YEARLY,
#			MONTHLY, etc.  Recurance Rule holds the timedelta information and is provided by convienience functions.
#			Bloomberg is passed in so i can	build symboldates on the chosen date (I'm going to change t his to date) """
#			 
#			self.timedelta = timedelta
#			self.symbolText = symbolText
#			self.index = 0
#			self.bloomberg
#			self.max = len(dates)
#			
#		def __get__(self, indexSlice):
#			if isinstance(indexSlice,slice):
#				return self._getSlice(indexSlice)
#			
#			else:
#				return self._getIndex(indexSlice)
#			
#		def _getSlice(self, slice):
#			if not slice.step:
#				step = 1
#			else:
#				step = slice.step
#					
#			datebegin = self.dates.index(slice.start)
#			dateend = self.dates.index(slice.stop)
#					
#			return SymbolIterator(self.symbol, timedelta*step, self.dates[datebegin:dateend])
#		
#		def _getIndex(self, index):
#			return SymbolDate(self.symbolText, self.dates[self.dates.index(index)], self.bloomberg)
#		
#		def __iter__(self):
#			return self
#		
#		def next(self):
#			self.index += 1
#			if self.index - 1 > self.max:
#				raise StopIteration()
#			return SymbolDate(self.symbolText, self.dates[self.index-1], self.bloomberg)
#			
##""" use cases:
##	Daily(IRBT)[datetime.date(2006,5,20):datetime.date(2006,5,25):1]
##	returns an array of symbols closed on name and date between 2006,5,20-25 going one day at a time.
##	Monthly(IRBT)[datetime.date(2006,5,20):datetime.date(2007,5,20):2]
##	returns an array of symbols closed on name and date between the two dates going two months at a time
#				#i roughly know what i need to do here, but im so spacey im afraid of making a mistake.  so im just gonna stop for now.
#				#but some notes i need to write down: associated with each bloomberg ought to be a time delta that you can get
#				#for it, like daily, quartelry, etc.  new bloombergs need to be added for dates.  a bloomberg can be defined by 
#				#reporting a single web attribute, so yahoo and google are actually amalgamtions of bloombergs.
#
#
##could these be better described as function objects?
#
#
#
#
#def Daily(symbol):
#	dates = symbol.getDates()
#	begin,end = symbol[0],symbol[-1]
#	return Symbol.SymbolIterator(symbol, rrule(freq=DAILY,dtstart=begin,until=end))
#
#def Monthly(symbol):
#	pass
#
#def Quarterly(symbol):
#	pass
#
#def Weekly(symbol):
#	pass
#
#def Annually(symbol):
#	pass
#
#class FuzzyDate(object):
#	""" Basically deals with all my fuzzy date problems, I need to define the comparison operators,etc, on other datetimes, basically
#	to fulfill whatever rule is passed in """
#	def __init__(self, date, rule):
#		self.date = date
#		self.rule = rule
#		
#		
##provides quarter data structure, which is static and basically just defines quarter.name ("First Quarter, Second Quarter, etc") and
##quarter.number (1,2,3)...
#
##provides date iterators, daily, weekly, monthly, quarterly, annual as functions
#
##these iterators also need to suppport slice notation that uses datetime.dates as indices
##question: should these functions have changeable policy on what a date does?  
## example: dateslice = closest, means take the index thats given and find the closest date I have to it
## dateslice = next, means take the index and find the next date after that one(if i dont have that one)
## dateslice = previous, means take the index and find the date thats before it (if i dont have the index)
## dateslice = specific, means only take the dateslice i've given you and throw an error otherwise.
#
##symbols need ot provide accessors to date, both daily for prices, quarterly and yearly for financials.

