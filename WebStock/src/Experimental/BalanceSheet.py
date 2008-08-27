# each class represents what?
# it coudl be on symbol dates, so a quarterly balance sheet total assets might be one row in a database
# or each class could be on the whoel thing, so one class would be 'balance sheet'
from Signature import Signature, SignatureMap
import datetime
from Registry import Registry
from Service import Service
from elixir import *
from sqlalchemy import UniqueConstraint
#metadata.bind = "sqlite:///balancesheet.sqlite"
#metadata.bind.echo = True
from SECFiling import SECFiling, AnnualFiling, QuarterlyFiling, BuilderMeta


# going with:
""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """



class BalanceSheet(SECFiling):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	CashAndEquivalents = Field(Float(precision=4))
#	services = {"CashAndEquivalents":lambda : Field(Float(precision=4))}
		
	
#qbcDict = {"Symbol":Field(Unicode(10)), "Date":Field(DateTime), "__init__":init, "_CashAndEquivalents":Field(Float(precision=4)), 
#		"CashAndEquivalents":Registry.getService(*QuarterlyFiling.buildService("CashAndEquivalents"))}

#QuarterlyBalanceSheet = BalanceSheetBuilder("QuarterlyBalanceSheet", (QuarterlyFiling,Entity), qbcDict)
QuarterlyBalanceSheet = QuarterlyFiling("QuarterlyBalanceSheet",BalanceSheet)
AnnualBalanceSheet = AnnualFiling("AnnualBalanceSheet",BalanceSheet)

#class QuarterlyBalanceSheet(QuarterlyFiling, Entity):
#	""" Represents a Quarterly Balance sheet and provides interface access to members of the quarterly balance sheet, closed over
#	Symbol and Date via the object's constructor """
#	
#	Symbol = Field(Unicode(10))
#	Date = Field(DateTime)
#	
#	using_table_options(UniqueConstraint('Symbol', 'Date'))
#	
#	def __init__(self, symbol, date):
#		super(QuarterlyBalanceSheet,self).__init__()
#		self.Symbol = symbol
#		self.Date = date
#	
#	_CashAndEquivalents = Field(Float(precision=4))
#	CashAndEquivalents = Registry.getService(*QuarterlyFiling.buildService("CashAndEquivalents"))
#	
#	def __repr__(self):
#		return str(self)
#	
#	def __str__(self):
#		return "<Quarterly Balance Sheet for %s on %s>" % (self.Symbol, self.Date)

#class AnnualBalanceSheet(AnnualFiling, Entity):
#	Symbol = Field(Unicode(10))
#	Date = Field(DateTime)
#	
#	using_table_options(UniqueConstraint('Symbol', 'Date'))
#	
#	def __init__(self, symbol, date):
#		super(AnnualBalanceSheet,self).__init__()
#		self.Symbol = symbol
#		self.Date = date
#		
#	_CashAndEquivalents = Field(Float(precision=4))
#	CashAndEquivalents = Registry.getService(*AnnualFiling.buildService("CashAndEquivalents"))
#	
#	def __repr__(self):
#		return str(self)
#	
#	def __str__(self):
#		return "<Annual Balance Sheet for %s on %s>" % (self.Symbol, self.Date)