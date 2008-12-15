from SECFiling import PersistantHost, Required, Provided
from elixir import Float, Unicode, DateTime

""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """



class TradingDay(PersistantHost):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	Symbol = Required(Unicode(60))
	Date = Required(DateTime)
	High = Provided(Float(precision=4))
