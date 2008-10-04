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
from SEC import BalanceSheet, IncomeStatement, CashFlowStatement, TradingDay, Metadata

class Symbol(object):
	""" Symbol closes it's accessors on the stock symbol name """
	
	def __init__(self, name):
		self.name = name
		self._metacache = None
		
	@property
	def Meta(self):
		if not self._metacache:
			self._metacache = Metadata.Metadata.fetch(self.name)
		return self._metacache
	
	class DailyClosure(object):
		def __init__(self, symbol, day):
			self.symbol = symbol
			self.day = day
			
	   	   	self.TradingDay = TradingDay.TradingDay.fetch(self.symbol, self.day)
		
	class QuarterClosure(object):
		#TODO: look into using partial application from the functools module for this.
		def __init__(self, symbol, quarter):
			self.symbol = symbol
			self.quarter = quarter
			
	   	   	self.BalanceSheet = BalanceSheet.QuarterlyBalanceSheet.fetch(self.symbol, self.quarter)
			self.CashFlowStatement = CashFlowStatement.QuarterlyCashFlowStatement.fetch(self.symbol, self.quarter)
			self.IncomeStatement = IncomeStatement.QuarterlyIncomeStatement.fetch(self.symbol, self.quarter)
	
	class AnnualClosure(object):
		def __init__(self, symbol, quarter):
			self.symbol = symbol
			self.quarter = quarter
			
			self.BalanceSheet = BalanceSheet.AnnualBalanceSheet.fetch(self.symbol, self.quarter)
			self.CashFlowStatement = CashFlowStatement.AnnualCashFlowStatement.fetch(self.symbol, self.quarter)
			self.IncomeStatement = IncomeStatement.AnnualIncomeStatement.fetch(self.symbol, self.quarter)
			
	def Annual(self, date):
		return Symbol.AnnualClosure(self.name, date)
	
	def Quarter(self, date):
		return Symbol.QuarterClosure(self.name, date)
	
	def Daily(self, date):
		return Symbol.DailyClosure(self.name, date)
		 