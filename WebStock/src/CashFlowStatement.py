from SECFiling import Field, Float


""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """



class CashFlowStatement(object):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	NetIncomeStartingLine = Field(Float(precision=4))
	
#	@classmethod
#	def AvailableDates(cls, symbol):
#		return [x.Date for x in cls.query().filter(symbol=symbol).all()]
	
#	@classmethod
#	def NewDates(cls, symbol):
#		return Registry[Meta("quarterlyCashFlowDates")](symbol)
	
#	@classmethod
#	def UnavailableDates(cls, symbol):
#		return  set(cls.NewDates()) - set(cls.AvailableDates())
	
	#for symbol in symbol
	#	for date in cls.unavailabledates(symbol):
	#		cls(symbol,date).prefetch()
