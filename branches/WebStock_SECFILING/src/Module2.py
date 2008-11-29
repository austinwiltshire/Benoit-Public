from datetime import datetime
from functools import partial
from utilities import isClassMethod, Lazy
from itertools import chain

from SEC import Metadata#, Daily, FinancialPeriod

class Technicals(object):
	def __init__(self, name, date):
		self.name = name
		self.date = date

class Symbol(object):
	def __init__(self, name):
		self.name = name
		self.Date = partial(StockDate, name)
		
	@Lazy
	def Financials(self):
		return FinancialPeriod.Meta(self.name)
	
	@Lazy
	def Meta(self):
		return Metadata.fetch(self.name)

class StockDate(object):
	def __init__(self, name, month, day, year):
		self.date = date = datetime(year, month, day)
		self.name = name
		
	@Lazy
	def Financials(self):
		return FinancialPeriod.Normal(self.name, self.date)

	@Lazy
	def Prices(self):
		return Daily.TradingDay.fetch(self.name, self.date)
	
	@Lazy
	def Technicals(self):
		return Technicals(self.name, self.date)
	
	@Lazy
	def Fundamentals(self):
		return Daily.Fundamentals.fetch(self.name, self.date)
