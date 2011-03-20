from SECFiling import Require, Provide
from Bloomberg import PersistantHost
from elixir import DateTime, Float, Unicode #Field, DateTime, Float, Entity, Unicode
from elixir import Date as DateT

Float4 = lambda : Float(precision=4)

""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """


class Derived(object):
	""" Contains information that is derived from various financial statements.  Generally any 'fundamental' that only changes quartelry or
	annually, is put here. """
	
	Symbol = Require(Unicode(60))
	Date = Require(DateT)
	
	FreeCashFlow = Provide(Float4())
	NetRevenues = Provide(Float(precision=4))
	EarningsPerShare = Provide(Float(precision=4))
	FreeCashFlowPerShare = Provide(Float(precision=4))
		
