""" The fundamentals module contians the persistance information for fundamentals, which are generally derivatives of the price and financial information. """

from SECFiling import PersistantHost, Required, Provided
from elixir import Float, Unicode, DateTime

class Fundamentals(PersistantHost):
	""" Contains fundamentals information such as PriceToEarnings and EarningsPerShare.
	
	Implementation Note:
	Perhaps providing a new Attribute, called Alias, who's constructor takes an already previously defined attribute, would allow for nice EPS and PE syntax here.
	"""
	
	Symbol = Required(Unicode(60))
	Date = Required(DateTime)
	
	PriceToEarnings = Provided(Float(precision=4))
	NetRevenues = Provided(Float(precision=4))
	EarningsPerShare = Provided(Float(precision=4))