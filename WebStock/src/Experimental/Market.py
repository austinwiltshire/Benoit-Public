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
		 