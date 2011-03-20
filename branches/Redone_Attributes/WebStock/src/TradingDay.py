""" Prices holds price information such as high, lows, close and volume. """

from SECFiling import PersistantHost, Require, Provide
from elixir import Float, Unicode, DateTime
from elixir import Date as DateT

#TODO: change name of this module from TradingDay to prices.

class Prices(object):
	""" Class provides access to price information such as high, lows, close and volume. """
	Symbol = Require(Unicode(60))
	Date = Require(DateT)
	
	High = Provide(Float(precision=4))
	Low = Provide(Float(precision=4))
	Open = Provide(Float(precision=4))
	Close = Provide(Float(precision=4))
	Volume = Provide(Float(precision=4))
	AdjustedClose = Provide(Float(precision=4))