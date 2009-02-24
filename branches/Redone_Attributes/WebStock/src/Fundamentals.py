""" The fundamentals module contians the persistance information for fundamentals, which are generally derivatives of the price and financial information. """

from SECFiling import PersistantHost, Require, Provide
from elixir import Float, Unicode, DateTime
from elixir import Date as DateT

class Fundamentals(PersistantHost):
	""" Contains fundamentals information such as PriceToEarnings and EarningsPerShare.
	
	Implementation Note:
	Perhaps providing a new Attribute, called Alias, who's constructor takes an already previously defined attribute, would allow for nice EPS and PE syntax here.
	"""
	
	Symbol = Require(Unicode(60))
	Date = Require(DateT)
	
	PriceToEarnings = Provide(Float(precision=4))
	NetRevenues = Provide(Float(precision=4))
	EarningsPerShare = Provide(Float(precision=4))