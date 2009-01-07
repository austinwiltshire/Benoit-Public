""" This module defines the IncomeStatement financial document, which holds stuff like NetIncome and PreferredDividends """

from SECFiling import PersistantHost, Required, Provided
from elixir import Float, Unicode, DateTime

class IncomeStatement(PersistantHost):
	""" Holds NetIncome and other Income Statement information in a declarative syntax. """
	
	Symbol = Required(Unicode(60))
	Date = Required(DateTime)
	
	PreferredDividends = Provided(Float(precision=4))
	NetIncome = Provided(Float(precision=4))
	Revenue = Provided(Float(precision=4))
	UnusualExpense = Provided(Float(precision=4))

