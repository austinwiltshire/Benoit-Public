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
	def __init__(self, bloomberg):
		class InnerMarketSymbol:
			def __init__(self, symbolText, market):
				self.symbolText = symbolText
				self.market = market
			
			def _getSymbolText(self):
				return self.symbolText
		
		for method in publicInterface(bloomberg):
			setattr(InnerMarketSymbol,method,self._delegateCallBald(bloomberg,method))
			
		self.Symbol = InnerMarketSymbol
			
		class InnerMarketSymbolDate:
			def __init__(self, symbolText, date, market):
				self.symbolText = symbolText
				self.market = market
				
				if isinstance(date, datetime.datetime):
					date = date.date()
				
				self.date = date
			
			def _getSymbolText(self):
				return self.symbolText
			
			def getAssociatedDate(self):
				return self.date
			
		for method in publicInterface(bloomberg):
			setattr(InnerMarketSymbolDate,method,self._delegateCallDate(bloomberg,method))
			
		self.SymbolDate = InnerMarketSymbolDate
	
	def _delegateCallBald(self, bloomberg ,method):
		def _(symbol,*args,**kwargs):
			return getattr(bloomberg,method)(symbol._getSymbolText(),*args,**kwargs)
		return _
	
	def _delegateCallDate(self, bloomberg ,method):
		def _(symbolDate,*args,**kwargs):
			return getattr(bloomberg,method)(symbolDate._getSymbolText(),symbolDate.getAssociatedDate(),*args,**kwargs)
		return _
	
	def Daily(self, symbol):
		dates = symbol.getDates()
		begin,end = dates[0],dates[-1]
		recurenceRule = rrule(freq=DAILY,dtstart=begin,until=end)
		
		#currently i combine the two sets, but this rule might change
		recurences = set((x.date() for x in recurenceRule))
				
		dates = recurences.intersection(set(dates))
		dates = sorted(list(dates))
		
		return self.SymbolDateIterator(symbol._getSymbolText(), dates, self)
	
	def Monthly(self, symbol):
		dates = symbol.getDates()
		begin,end = dates[0],dates[-1]
		recurenceRule = rrule(freq=MONTHLY,dtstart=begin,until=end)
		
		#currently i combine the two sets, but this rule might change
		recurences = set((x.date() for x in recurenceRule))
				
		dates = recurences.intersection(set(dates))
		dates = sorted(list(dates))
		
		return self.SymbolDateIterator(symbol._getSymbolText(), dates, self)
	
	class SymbolDateIterator(object):
		def __init__(self, symbolText, dates, market):
			self.market = market
			self.symbolText = symbolText
			self.index = 0
			self.max = len(dates)
			self.dates = dates
			
		def next(self):
			if self.index == self.max-1:
				raise StopIteration()
			self.index += 1
			return self.market.getSymbolDate(self.symbolText, self.dates[self.index])
		
		def __iter__(self):
			return self
			
			
		

			
#	def _delegateMethod(self, method):
#		""" Sets the name 'method' on self to be a delegated call to bloomberg.method, except with the first argument
#		bound to symbol """
		
#		setattr(self,method,lambda *args,**kwargs: self._delegateBloombergCall(method, *args, **kwargs))
			
	
	def getSymbol(self, symbolText):
		return self.Symbol(symbolText, self)
	
	def getSymbolDate(self, symbolText, date):
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

