from SECFiling import Periodic, AttributeService, RegisteredService, Quarterly, Annual, Daily
from elixir import Field, DateTime, Float, Entity, Unicode

""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """

class BalanceSheet(Periodic):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	Symbol = AttributeService(Field(Unicode(60)))
	Date = AttributeService(Field(DateTime))
	CashAndEquivalents = RegisteredService(Field(Float(precision=4)))

QBS = Quarterly(BalanceSheet)
ABS = Annual(BalanceSheet)
DBS = Daily(BalanceSheet)