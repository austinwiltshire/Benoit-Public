""" This module defines the IncomeStatement financial document, which holds stuff like NetIncome and PreferredDividends """

from SECFiling import PersistantHost, Require, Provide
from elixir import Float, Unicode
from elixir import Date as DateT

class IncomeStatement(object):
	""" Holds NetIncome and other Income Statement information in a declarative syntax. """
	
	Symbol = Require(Unicode(60))
	Date = Require(DateT)
	
	PreferredDividends = Provide(Float(precision=4))
	NetIncome = Provide(Float(precision=4))
	Revenue = Provide(Float(precision=4))
	UnusualExpense = Provide(Float(precision=4))

