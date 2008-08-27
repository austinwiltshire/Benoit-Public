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
from elixir import *
import Registry
import Google
import BalanceSheet
import IncomeStatement

setup_all(True)

class Symbol(object):
	""" Symbol closes it's accessors on the stock symbol name """
	
	def __init__(self, name):
		self.name = name
		
	class QuarterClosure(object):
		def __init__(self, symbol, quarter):
			self.symbol = symbol
			self.quarter = quarter
			
	   	   	self.BalanceSheet = BalanceSheet.QuarterlyBalanceSheet.fetch(self.symbol, self.quarter)
			#self.CashFlowStatement = CashFlowStatement.CashFlowStatement.fetchQuarterlyCashFlowStatement(self.symbol, self.quarter)
			self.IncomeStatement = IncomeStatement.QuarterlyIncomeStatement.fetch(self.symbol, self.quarter)
	
	class AnnualClosure(object):
		def __init__(self, symbol, quarter):
			self.symbol = symbol
			self.quarter = quarter
			
			#self.BalanceSheet = BalanceSheet.BalanceSheet.fetchQuarterlyBalanceSheet(self.symbol, self.quarter)
			#self.CashFlowStatement = CashFlowStatement.CashFlowStatement.fetchQuarterlyCashFlowStatement(self.symbol, self.quarter)
			self.IncomeStatement = IncomeStatement.AnnualIncomeStatement.fetch(self.symbol, self.quarter)
			
	def Annual(self, date):
		return Symbol.AnnualClosure(self.name, date)
	
	def Quarter(self, date):
		return Symbol.QuarterClosure(self.name, date)
		 