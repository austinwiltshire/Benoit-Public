# each class represents what?
# it coudl be on symbol dates, so a quarterly balance sheet total assets might be one row in a database
# or each class could be on the whoel thing, so one class would be 'balance sheet'
from Signature import Signature, SignatureMap
import datetime
from Registry import Registry
from Service import Service
from elixir import *
metadata.bind = "sqlite:///balancesheet.sqlite"
metadata.bind.echo = True


# going with:
""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """

class Bloomberg(object):
	""" Provides functions for mapping "Hosts" to "Interfaces".  Hosts are things that say they can provide a certain service
	given a certain contract, while Interfaces are items that need that service and also provide a certain contract/signature.
	Bloomberg does the job of matching up interfaces to hosts """

class BalanceSheet(Bloomberg):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	pass
	
class QuarterlyBalanceSheet(BalanceSheet,Entity):
	""" Represents a Quarterly Balance sheet and provides interface access to members of the quarterly balance sheet, closed over
	Symbol and Date via the object's constructor """
	
	Symbol = Field(Unicode(10))
	Date = Field(DateTime)
	
	def __init__(self, symbol, date):
		super(QuarterlyBalanceSheet,self).__init__()
		self.Symbol = symbol
		self.Date = date
	
	_CashAndEquivalents = Field(Float(precision=4))
	CashAndEquivalents = Registry.getService(Service("CashAndEquivalents",Signature((unicode,"symbol"),(datetime.date, "date"))),
											 SignatureMap({"symbol":"Symbol", "date":"Date"}), "_CashAndEquivalents")
	
	def __repr__(self):
		return str(self)
	
	def __str__(self):
		return "<Quarterly Balance Sheet for %s on %s>" % (self.Symbol, self.Date)
	
	#Registry.Interface(BalanceSheet, "CashAndEquivalents", Signature(("symbol",unicode),("date",datetime.date)))
	#this above method should tell bloomberg that BalanceSheet requires someone to provide CashAndEquivalents
	#it makes a contract saying it will provide the symbol and Quarter, and queries whether someone can provide
	# that given the inputs
	
	
	

class AnnualBalanceSheet(object):
	pass