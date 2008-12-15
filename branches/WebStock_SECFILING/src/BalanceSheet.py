<<<<<<< .working
from SECFiling import PersistantHost, Required, Provided, Quarterly, Annual, Daily
from elixir import Field, DateTime, Float, Entity, Unicode
=======
from SECFiling import Field, Float
>>>>>>> .merge-right.r125


""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """

<<<<<<< .working
class BalanceSheet(PersistantHost):
=======
class BalanceSheet(object):
>>>>>>> .merge-right.r125
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
<<<<<<< .working
	Symbol = Required(Unicode(60))
	Date = Required(DateTime)
	CashAndEquivalents = Provided(Float(precision=4))=======
	CashAndEquivalents = Field(Float(precision=4))>>>>>>> .merge-right.r125
