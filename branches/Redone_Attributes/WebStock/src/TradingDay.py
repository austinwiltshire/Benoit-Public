""" Prices holds price information such as high, lows, close and volume. """

from SECFiling import PersistantHost, Required, Provided
from elixir import Float, Unicode, DateTime

#TODO: change name of this module from TradingDay to prices.

class Prices(PersistantHost):
	""" Class provides access to price information such as high, lows, close and volume. """
	Symbol = Required(Unicode(60))
	Date = Required(DateTime)
	High = Provided(Float(precision=4))
	Close = Provided(Float(precision=4))