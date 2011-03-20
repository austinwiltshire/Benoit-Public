from SECFiling import Require, Provide
from Bloomberg import PersistantHost
from elixir import DateTime, Float, Unicode #Field, DateTime, Float, Entity, Unicode
from elixir import Date as DateT

""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """


class BalanceSheet(object):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	
	Symbol = Require(Unicode(60))
	Date = Require(DateT)
	CashAndEquivalents = Provide(Float(precision=4))
	TotalCommonSharesOutstanding = Provide(Float(precision=4))