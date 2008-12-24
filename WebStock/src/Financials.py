import Annual
import Quarter
from utilities import Lazy

class FinancialPeriod(object):
	def __init__(self, symbol, date):
		self.symbol = symbol
		self.date = date
	
	@Lazy
	def Quarter(self):
		return Financials(Quarter, self.symbol, self.date)

	@Lazy
	def Annual(self):
		return Financials(Annual, self.symbol, self.date)
		
class Financials(object):
	def __init__(self, module, symbol, date):
		self.module = module
		self.symbol = symbol
		self.date = date
	
	@Lazy
	def BalanceSheet(self):
		return self.module.BalanceSheet.fetch(self.symbol, self.date)
	
	@Lazy
	def IncomeStatement(self):
		return self.module.IncomeStatement.fetch(self.symbol, self.date)

	@Lazy
	def CashFlowStatement(self):
		return self.module.CashFlowStatement.fetch(self.symbol, self.date)