""" Module used in the declarative syntax to access stock information.

Implementation Note:
This is a tall order, but this could be generated dynamically by the user looking up what modules he can see, and what modules are being asked for by his own user.
Then generic functions can take care of what information is required for what constructor. """

import Annual
import Quarter
from utilities import Lazy

class FinancialPeriod(object):
	""" This class signifies access to a particular type of periodic financials, like quarterly and annual financials. """
	
	def __init__(self, symbol, date):
		self.symbol = symbol
		self.date = date
	
	@Lazy
	def Quarter(self):
		""" Returns quarterly access to financials. """
		return Financials(Quarter, self.symbol, self.date)

	@Lazy
	def Annual(self):
		""" Returns annual access to financials. """
		return Financials(Annual, self.symbol, self.date)

#TODO: switch the names of these two classes.
class Financials(object):
	""" This class allows access to particular documents such as the Balance Sheet and Income Statement. """
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