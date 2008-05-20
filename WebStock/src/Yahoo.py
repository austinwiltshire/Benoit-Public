class Yahoo(Website):
	""" Provides webservices to collect data from Yahoo"""
	
	def _delegateInterface(self, interface, wrapper):
		""" adds member functions in interface and calls wrapper on them """
		#TODO: upgrade this to a higher level objet
		

	
	def _priceWrapper(self, method, symbol, *args):
		"""modeled on google wrapper."""
		
						
	def validSymbol(self, symbol):
		""" Predicate that returns whether symbol is a valid symbol """
		pass
	
	#Yahoo does a delegate interface that closes on symbol against pricedata.
	#price data hosts trading dates and prices, move the other stuff out into
	#a helper class, prolly the one that builds soups.
	#remove "symbol" aspect of the functions and move them out to Yahoo.
	class Pricedata:
		""" Provides webservices to collect price data from Yahoo """
		def __init__(self, soup):
			""" Takes in a beautiful soup of the historical price website so 
			it can download the comma delimited file and get price information. """
		
		def getClose(self, date=None):
			""" Gets the price for symbol.  Throws SymbolNotFound if there is no symbol
			by that name.  If date is provided, gets the price for that date.  If date is
			not found, throws a DateNotFound error.  If date is not provided, gets today's
			price.  If date is not provided and date is not a trading date, throws 
			DateNotFound. """
			pass
		
		def getOpen(self, date=None):
			pass
		
		def getHigh(self, date=None):
			pass
		
		def getLow(self, date=None):
			pass
		
		def getVolume(self, date=None):
			pass
		
		def getAdjustedClose(self, date=None):
			pass
			
		def hasPrice(self, date=None):
			""" Boolean function that returns true if price data is available for symbol
			on date.  If date is not provided, its assumed to be today(even if its not a
			trading day).  Throws SymbolNotFound if symbol doesnt exist. """
			pass
		
		def _hasPrice(self, date=None):
			""" Same as hasPrice but assumes symbol exists."""

		
		def getCloses(self, dateFrom=None, dateTo=None):
			""" Returns an array of prices, returned as a list of floats, for symbol from
			dateFrom to dateTo(at least all prices that are available). If dateFrom is
			not provided, it is assumed to be from the begining of available data.  If 
			dateTo is not provided, it is assumed to be the end of available data(most 
			likely today).  If symbol does not exist, SymbolNotFound error is thrown.
			If there are no available dates between the bounds, DateNotFound is thrown."""
			pass
		
		def hasPrices(self, dateFrom=None, dateTo=None):
			""" Throws if invalid symbol.  Returns true if price data exists between dateFrom
			and dateTo.  If both are left blank, this is a generic supports-price-data 
			predicate that will return true if I have ANY price data for the symbol """
			pass
		
		def _hasPrices(self, dateFrom=None, dateTo=None):
			""" Assumes valid symbol, otherwise same as hasPrices """
		
		def getTradingDates(self, dateFrom=None, dateTo=None):
			""" Returns an array of datetime.date objects that have price data associated
			with them for this symbol.  If symbol is not found, throws a SymbolNotFound,
			if there are no dates available in the range, returns a DateNotFound error."""
			pass
		
		def hasTradingDates(self, dateFrom=None, dateTo=None):
			""" Predicate returns true if there are ANY trading dates in the range. """
			pass
		
		def _hasTradingDates(self, datesFrom=None, dateTo=None):
			""" Same as hasTradingDates, but assumes symbol is valid """
		
		def isTradingDate(self, date=None):
			""" Predicate that returns true whether date is a trading date for symbol.
			  If date is none, returns true whether or not today
			is a trading date(new information) for this symbol. """
			pass
		
		def _isTradingDate(self, date=None):
			""" Same as above but assumes a valid symbol """
			pass
		
		def getPricesAndDates(self, dateFrom=None, dateTo=None):
			""" simply zips up getPrices for dateFrom and dateTo with getTradingDates
			for dateFrom and dateTo """