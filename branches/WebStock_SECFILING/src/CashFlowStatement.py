from SECFiling import PersistantHost, Provided, Required
from elixir import Float, Unicode, DateTime

""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """



class CashFlowStatement(PersistantHost):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	Symbol = Required(Unicode(60))
	Date = Required(DateTime)
	NetIncomeStartingLine = Provided(Float(precision=4))