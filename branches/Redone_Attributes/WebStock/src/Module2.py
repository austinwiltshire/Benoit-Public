""" Currently the core module of my Stock DSL syntax.  This is to give easy, english like, access to stock information to aid in further experimentation.  It also
handles persistance, lookup and cacheing.  Example:

Symbol("IRBT").Date(4,20,2008).Prices.High

"""

from elixir import session
import datetime
from functools import partial
from utilities import Lazy, findFirst #isClassMethod, Lazy
from itertools import chain
from Adapt import Adapt
from Flyweight import Flyweight
from sqlalchemy import desc, asc
from Periodic import WebDates, NewDates, AvailableDates
from Cached import cached
import WebsiteExceptions

from SEC import Metadata, Daily, FinancialPeriod
import Financials
from Daily import Prices
from Daily import Fundamentals

class Technicals(object):
	""" Placeholder class. """
	def __init__(self, name, date):
		self.name = name
		self.date = date

class Symbol(Flyweight):
	""" Symbol is the basis of the Stock DSL, and provides symbol name information.  It's functionality is used declaratively to further define particular stock
	information. """
	
	def _flyweight_init_(self, name):
		""" Requires stock symbol information. """
		self.name = Adapt(name,unicode)
		self.Date = cached(100)(partial(StockDate, name))
		
	@Lazy
	def Meta(self):
		""" Provides access to stock metadata. """
		return Metadata.fetch(self.name)
	
	@cached(15)
	def AvailableDates(self, cls):
		return sorted([Adapt(x.Date,datetime.date) for x in cls.query().filter_by(_Symbol=self.name).all()])
	
	def prefetch(self, deep_prefetch=False):
		""" Work in progress.  Preloads all information, given a stock date. """
		
		#how might prefetch work?
#  given any SECFiling, a prefetch should first gather
# that filing's dates that are important, so i need a date service
# for each type of date - a meta would just have a 'once'
# daily would have all valid trading days - this i have a calender for, 
# but i also need ranges available from yahoo
# quarter would get quarterly dates from the web
# a\nnual would get annual dates for the web
# then a prefetch would go ahead and create an array of the SECfilings
# one for each date.
# well, there's really two kinds of prefetch, i'd need one that would 
# prefetch all the stuff for an SECFiling, this would probably be easy
# and another to find all available dates and build an array of them
# this prefetch doesn't need to be saved, just the act of getting things
# will commit it to the database.  

# a potential benefit might be having whether SECFiling/registry commits
# or not as a class variable inside, as either true or false.  usually
# it'd be true, but for prefetch it'd make sense to turn it off so things
# can pile up for commits.  i could commit manually.
#	#prefecth problems...
#	#prefetch method must be accessed via the 'fetch' method from market.symbol...., otherwise, multiple entries get put into 
#	#the database since that is the only way to get access to 'fetched' data.  i need to look further into enforcing uniqueness of
#	#data by symbol and date.  the constraints don't seem to be able to be enforced...
		
#TODO: could add annual/quarterly logic here too.
#		session.configure(autocommit=False,autoflush=False)


	   	#i'm pre-searching for these dates and doing this all up front to avoid accidental commits in the middle of everything.
	   	annualIncDates = NewDates(Financials.Annual.IncomeStatement, self.name)
	   	annualCasDates = NewDates(Financials.Annual.CashFlowStatement, self.name)
	   	annualBalDates = NewDates(Financials.Annual.BalanceSheet, self.name)
	   	quarterIncDates = NewDates(Financials.Quarter.IncomeStatement, self.name)
	   	quarterCasDates = NewDates(Financials.Quarter.CashFlowStatement, self.name)
	   	quarterBalDates = NewDates(Financials.Quarter.BalanceSheet, self.name)
	   	
	   	pricesDates = NewDates(Daily.Prices, self.name)
	   	quarterDerivedDates = NewDates(Financials.Quarter.Derived, self.name)
		annualDerivedDates = NewDates(Financials.Annual.Derived, self.name)

		try:
			
			self.Meta.prefetch()
			session.commit()	

#			for _date in NewDates(Financials.Annual.IncomeStatement, self.name):
	   	   	for _date in annualIncDates:
				Financials.Annual.IncomeStatement.new(self.name, _date)
		   	   	#self.Date(_date.month,_date.day,_date.year).Financials.Annual.IncomeStatement.prefetch()
	#		
			session.commit()	
#			for _date in NewDates(Financials.Quarter.IncomeStatement, self.name):
	   	   	for _date in quarterIncDates:
				Financials.Quarter.IncomeStatement.new(self.name, _date)
	#	   	   	self.Date(_date.month,_date.day,_date.year).Financials.Quarter.IncomeStatement.prefetch()
	#
			session.commit()			
	   	   	for _date in annualCasDates:
#			for _date in NewDates(Financials.Annual.CashFlowStatement, self.name):
				Financials.Annual.CashFlowStatement.new(self.name, _date)
	#			self.Date(_date.month,_date.day,_date.year).Financials.Annual.CashFlowStatement.prefetch()
	#			prefetched.update({_date:self.Date(_date.month,_date.day,_date.year).Financials.Annual.CashFlowStatement.prefetch()})
	#
			session.commit()	
	
	   	   	for _date in quarterCasDates:		
#			for _date in NewDates(Financials.Quarter.CashFlowStatement, self.name):
				Financials.Quarter.CashFlowStatement.new(self.name, _date)
	#			self.Date(_date.month,_date.day,_date.year).Financials.Quarter.CashFlowStatement.prefetch()
	#		
			session.commit()		
			#for _date in NewDates(Financials.Annual.BalanceSheet, self.name):
			for _date in annualBalDates:
				Financials.Annual.BalanceSheet.new(self.name, _date)
	#			self.Date(_date.month,_date.day,_date.year).Financials.Annual.BalanceSheet.prefetch()
	#		
			session.commit()	
	
#			for _date in NewDates(Financials.Quarter.BalanceSheet, self.name):
	   	   	for _date in quarterBalDates:
				Financials.Quarter.BalanceSheet.new(self.name, _date)
				
			session.commit()	
	#			self.Date(_date.month,_date.day,_date.year).Financials.Quarter.BalanceSheet.prefetch()	
			
			#for _date in NewDates(Daily.Prices, self.name):
			for _date in pricesDates:
				Daily.Prices.new(self.name, _date)		
			
			session.commit()		 	
				
			#for _date in NewDates(Financials.Quarter.Derived, self.name):
			for _date in quarterDerivedDates:
			 	Financials.Quarter.Derived.new(self.name, _date)
			 	
			session.commit()		
				 	
			#for _date in NewDates(Financials.Annual.Derived, self.name):
			for _date in annualDerivedDates:
			 	Financials.Annual.Derived.new(self.name, _date)
			 	
			session.commit()	
			
			#expensive prefetches.  And they're all off line.  Actually, this would be best done with some raw SQL stuff.  We only need to do a handfull of selects
			# per stock.  but it's being selected over and over and over again.  Each select forces a commit.  Hense it's slow.
			if(deep_prefetch):	 	
				for _date in NewDates(Daily.Fundamentals, self.name):
					Daily.Fundamentals.new(self.name, _date)
		
		
			session.commit()
		
		except:
			session.rollback()
			session.close()
			raise
		#session.configure(autocommit=True,autoflush=True)
#			i+=1
#			if i%100==0:
#				i=0
#				session.commit()
#		
#		return prefetched
		
#TODO: figure out how to do this property correctly
#	@Property
	def Symbol(self):
		return self.name

class StockDate(Flyweight):
	""" Stock date further defines stock information by declaring a particular date to look up.  Daily information is easily queried this way, and quarterly and 
	other information can be queried by using functions like MostRecent. """
	
	def _flyweight_init_(self, name, month, day, year):
		self.date = date = datetime.date(year, month, day)
		self.name = name
		
	def ClosestAvailable(self, cls):
		""" Returns the closest available date to the one this StockDate represents, whether it's in the past or future. """
		dt = min(Symbol(self.name).AvailableDates(cls), key=lambda x: abs((self.date - x).days))
		return cls.fetch(self.name, dt)
		
	def MostRecent(self, cls):
		""" Returns the most recent dates available given a date and a persistant host class.  
		
		Implementation Notes:
		Query and annual logic would make sense here, allowing most recent hints and configuration information on whether or not it should check
		the web.  If the returned date is beyond a certain range, as defined by annual and quarterly logic, AND the stock is still registered as active,
		which can be added to Metadata, then we'll check the web.  Arguments to the function itself could also modify this behavior.  It's a fuzzy topic,
		maybe i can ask grant if there are required times filing dates must be in by, or required waiting periods to give me a better range.  For instance,
		if I knew the last date was on X, can i predict from that alone the next date? 
		"""
		#print Sym
		dt = findFirst(reversed(Symbol(self.name).AvailableDates(cls)), lambda x: x<= self.date)		
		if not dt:
			raise WebsiteExceptions.DateNotFound(self.name, self.date)
		return cls.fetch(self.name, dt)
		#return cls.query.filter_by(_Symbol=self.name).filter(cls._Date <= self.date).order_by(desc(cls._Date)).first()
				
	def NextAvailable(self, cls):
		""" Opposite of Most Recent. """
		dt = findFirst(Symbol(self.name).AvailableDates(cls), lambda x: x >= self.date)
		if not dt:
			raise WebsiteExceptions.DateNotFound(self.name, self.date)
		return cls.fetch(self.name, dt)
		#return cls.query.filter_by(_Symbol=self.name).filter(cls._Date >= self.date).order_by(asc(cls._Date)).first()
		
	@Lazy
	def Financials(self):
		""" Provides access to financial information like Income and Balance Sheets. """
		return Financials.FinancialPeriod(self.name, self.date)

	@Lazy
	def Prices(self):
		""" Provides access to price information like highs and lows. """
		return Daily.Prices.fetch(self.name, self.date)
	
	@Lazy
	def Technicals(self):
		""" Provides access to technicals information like MACD and Put to Call ratio.  Not currently implemented. """
		return Technicals(self.name, self.date)
	
	@Lazy
	def Fundamentals(self):
		""" Provides access to fundamentals information like PE and EPS. """
		return Daily.Fundamentals.fetch(self.name, self.date)
	
#TODO: fix the below to make the properties work as read only properties.
#	@Property
#	def Date(self):
#		return self.date
	
#	@Property
#	def Symbol(self):
#		return self.name