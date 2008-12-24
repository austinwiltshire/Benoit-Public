from datetime import datetime, date
from functools import partial
from utilities import isClassMethod, Lazy
from itertools import chain
from Adapt import Adapt
from Flyweight import Flyweight
from sqlalchemy import desc
from Periodic import WebDates, NewDates

from SEC import Metadata, Daily, FinancialPeriod
import Financials
from Daily import Prices
from Daily import Fundamentals

class Technicals(object):
	def __init__(self, name, date):
		self.name = name
		self.date = date

class Symbol(Flyweight):
	def __init__(self, name):
		self.name = Adapt(name,unicode)
		self.Date = partial(StockDate, name)
		
	@Lazy
	def Meta(self):
		return Metadata.fetch(self.name)
	
	def AvailableDates(self, cls):
		return [Adapt(x.Date,date) for x in cls.query().filter_by(_Symbol=self.name).all()]
	
	def prefetch(self):
		
		
		prefetched = {}
		annual = {}
		for _date in WebDates(Financials.Annual.IncomeStatement, self.name):
			annual.update({_date:self.Date(_date.month,_date.day,_date.year).Financials.Annual.IncomeStatement.prefetch()})
		
		for _date in WebDates(Financials.Quarter.IncomeStatement, self.name):
			quarter.update({_date:self.Date(_date.month,_date.day,_date.year).Financials.Quarter.IncomeStatement.prefetch()})
			
		prefetch["IncomeStatement"] = {"Annual":annual,}
		
		
		
		for _date in WebDates(Financials.Annual.CashFlowStatement, self.name):
			prefetched.update({_date:self.Date(_date.month,_date.day,_date.year).Financials.Annual.CashFlowStatement.prefetch()})
		
		for _date in WebDates(Financials.Quarter.CashFlowStatement, self.name):
			prefetched.update({_date:self.Date(_date.month,_date.day,_date.year).Financials.Quarter.CashFlowStatement.prefetch()})
			
		for _date in WebDates(Financials.Annual.BalanceSheet, self.name):
			prefetched.update({_date:self.Date(_date.month,_date.day,_date.year).Financials.Annual.BalanceSheet.prefetch()})
		
		for _date in WebDates(Financials.Quarter.BalanceSheet, self.name):
			prefetched.update({_date:self.Date(_date.month,_date.day,_date.year).Financials.Quarter.BalanceSheet.prefetch()})
		
		return prefetched
		
	
#	@Property
	def Symbol(self):
		return self.name

class StockDate(Flyweight):
	def __init__(self, name, month, day, year):
		self.date = date = datetime(year, month, day)
		self.name = name
		
	def MostRecent(self, cls):
		return cls.query.filter_by(_Symbol=self.name).filter(cls._Date <= self.date).order_by(desc(cls._Date)).first()
			
	@Lazy
	def Financials(self):
		return Financials.FinancialPeriod(self.name, self.date)

	@Lazy
	def Prices(self):
		return Daily.Prices.fetch(self.name, self.date)
	
	@Lazy
	def Technicals(self):
		return Technicals(self.name, self.date)
	
	@Lazy
	def Fundamentals(self):
		return Daily.Fundamentals.fetch(self.name, self.date)

#	@Property
#	def Date(self):
#		return self.date
	
#	@Property
#	def Symbol(self):
#		return self.name