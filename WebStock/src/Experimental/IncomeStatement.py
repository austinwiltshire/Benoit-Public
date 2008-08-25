# each class represents what?
# it coudl be on symbol dates, so a quarterly balance sheet total assets might be one row in a database
# or each class could be on the whoel thing, so one class would be 'balance sheet'
from Signature import Signature, SignatureMap
import datetime
from Registry import Registry
from Service import Service
from elixir import *
from sqlalchemy import UniqueConstraint
from SECFiling import SECFiling, AnnualFiling, QuarterlyFiling, BuilderMeta

metadata.bind = "sqlite:///SEC.sqlite"
metadata.bind.echo = True

#TODO:
# run test that uniqueness is enforced

# going with:
""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """

class IncomeStatement(SECFiling):
	services = {"Revenue":lambda : Field(Float(precision=4))}

AnnualIncomeStatement = BuilderMeta.Builder("AnnualIncomeStatement",IncomeStatement,AnnualFiling)
QuarterlyIncomeStatement = BuilderMeta.Builder("QuarterlyIncomeStatement",IncomeStatement,QuarterlyFiling)

#class AnnualIncomeStatement(Entity, AnnualFiling):
#	""" Represents a Quarterly Balance sheet and provides interface access to members of the quarterly balance sheet, closed over
#	Symbol and Date via the object's constructor """
#	
#	Symbol = Field(Unicode(10))
#	Date = Field(DateTime)
#	
#	using_table_options(UniqueConstraint('Symbol', 'Date'))
#	
#	def __init__(self, symbol, date):
#		super(AnnualIncomeStatement,self).__init__()
#		self.Symbol = symbol
#		self.Date = date
#	
#	_Revenue = Field(Float(precision=4))
#	Revenue = Registry.getService(*AnnualFiling.buildService("Revenue"))
#	
#	def __repr__(self):
#		return str(self)
#	
#	def __str__(self):
#		return "<Annual Income Statement for %s on %s>" % (self.Symbol, self.Date)
#
#class QuarterlyIncomeStatement(QuarterlyFiling,Entity):
#	Symbol = Field(Unicode(10))
#	Date = Field(DateTime)
#	
#	using_table_options(UniqueConstraint('Symbol', 'Date'))
#	
#	def __init__(self, symbol, date):
#		super(QuarterlyIncomeStatement,self).__init__()
#		self.Symbol = symbol
#		self.Date = date
#	
#	_Revenue = Field(Float(precision=4))
#	Revenue = Registry.getService(*QuarterlyFiling.buildService("Revenue"))