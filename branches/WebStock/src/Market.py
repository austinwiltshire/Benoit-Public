"""
This introduces the symbol object, which provides convienient object oriented access to 
stock info.  This stock info is both closed, or capable of being closed, on the symbol name
and the date it's collected.  Special dates are provided for quarters and annuals, as well
as for things that happen every day, like prices.

IRBT = Symbol("IRBT")
IRBT.BalanceSheet.Quarter(datetime.datetime(2008,6,28)).CashAndEquivalents
___
IRBT.CashFlowStatement.Annual(datetime.datetime(2008, 1, 1)).CapitalExpenditures
___
IRBT.IncomeStatement.Quarter(datetime.datetime(2008,6,28)).Revenue
___
IRBT.Prices(datetime.datetime(2008,6,28)).High
___
IRBT.Technicals.MACD(datetime.datetime(....))
___
IRBT.Fundamentals.FreeCashFlow.Quarter....
___

"""
from SEC import TradingDay, Metadata, Fundamentals, Quarter, Annual
from utilities import Lazy, isClassMethod

class TimeAccess(object):
	def __init__(self, symbol, module):
		self.symbol = symbol
		self.module = module
	
	class ShortCircuit(object):
		def __init__(self, cls, symbol):
			self.cls = cls
			self.symbol = symbol
			
		def __getattr__(self, name):
			if isClassMethod(self.cls, name):
				return lambda *args, **kwargs : getattr(self.cls, name)(self.symbol, *args, **kwargs)
			else:
				raise AttributeError, name
	
	@Lazy
	def BalanceSheet(self):
		return TimeAccess.ShortCircuit(self.module.BalanceSheet, self.symbol)
	
	@Lazy
	def CashFlowStatement(self):
		return TimeAccess.ShortCircuit(self.module.CashFlowStatement, self.symbol)
#		return self.module.CashFlowStatement.fetch(self.symbol, self.date)
	
	@Lazy
	def IncomeStatement(self):
		return self.module.IncomeStatement.fetch(self.symbol, self.date)
	
	def __call__(self, date):
		return TimeClosure(self.symbol, date, self.module)	

class TimeClosure(object):
	def __init__(self, symbol, date, module):
		self.symbol = symbol
		self.date = date
		self.module = module
		
		#ok, what if TIME CLOSURE had a state pattern?  if date was provided, we get fully closed annual or quarterly stuff.  if date is not provided,
		#we get protected access to the class methods of the annual and quarterly versions?
		
	@Lazy
	def BalanceSheet(self):
		return self.module.BalanceSheet.fetch(self.symbol, self.date)
	
	@Lazy
	def CashFlowStatement(self):
		return self.module.CashFlowStatement.fetch(self.symbol, self.date)
	
	@Lazy
	def IncomeStatement(self):
		return self.module.IncomeStatement.fetch(self.symbol, self.date)		

class Symbol(object):
	""" Symbol closes it's accessors on the stock symbol name """
	
	def __init__(self, name):
		self.name = name
		self._metacache = None
		
	@Lazy
	def Meta(self):
		return Metadata.Metadata.fetch(self.name)
	
	class DailyClosure(object):
		def __init__(self, symbol, day):
			self.symbol = symbol
			self.day = day
		
		@Lazy	
		def TradingDay(self):
			return TradingDay.TradingDay.fetch(self.symbol, self.day)
		
		@Lazy
		def Fundamentals(self):
			return Fundamentals.Fundamentals.fetch(self.symbol, self.day)
		
		#TODO: look into using partial application from the functools module for this.
			
			#could also turn this into some sort of describtor that discriminates between timeaccess and time closer between attribute and function access.

	@Lazy
	def Annual(self):
		return TimeAccess(self.name, Annual)
#	def Annual(self, date=None):
#		if not date:
#			return TimeAccess(self.name, Annual)
#		else:
#			return TimeClosure(self.name, date, Annual)
	
	@Lazy
	def Quarter(self):
		return TimeAccess(self.name, Quarter)
#	   return TimeClosure(self.name, date, Quarter)
	
	def Daily(self, date):
		return Symbol.DailyClosure(self.name, date)
		 