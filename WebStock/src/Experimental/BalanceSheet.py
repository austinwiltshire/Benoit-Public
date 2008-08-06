# each class represents what?
# it coudl be on symbol dates, so a quarterly balance sheet total assets might be one row in a database
# or each class could be on the whoel thing, so one class would be 'balance sheet'


# going with:
""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """

class Bloomberg(object):
	pass

class BalanceSheet(Bloomberg):
	pass
	

class QuarterlyBalanceSheet(BalanceSheet):
	Bloomberg.Interface(BalanceSheet, "CashAndEquivalents", Bloomberg.Signature(symbol, FinancialDate.Quarter))
	#this above method should tell bloomberg that BalanceSheet requires someone to provide CashAndEquivalents
	#it makes a contract saying it will provide the symbol and Quarter, and queries whether someone can provide
	# that given the inputs
	

class AnnualBalanceSheet(object):
	pass

class PluginRegistry(type):
	""" PluginRegistry metaclass takes in a class, inspects it's members and does a name lookup on them.  For members that it has
	a plugin registered for, it adds properties for those names which link back to the registered plugin. """
	def __new__(cls, name, bases, dct):
		return super(PluginRegistry,cls).__new__(cls, name, bases, dct)
	def __init__(cls, name, bases, dct):
		return super(PluginRegistry,cls).__init__(cls, name, bases, dct)
	
