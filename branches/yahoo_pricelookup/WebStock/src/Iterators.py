"""
Some motivating use cases:

>>> IRBT = Symbol("IRBT")
>>> for day in Daily(IRBT):
...  cash = day.MostRecent(Quarterly.BalanceSheet).CashAndEquivalents
...  high = day.Prices.High
...  return cash / high

That should return IRBT's first available price information I have.  If either are none, it should return none.

>>> IRBT = Symbol("IRBT")
>>> for day in Monthly(IRBT,1): #first trading day of each month
...  high = day.Prices.High

That returns the high for the first day of each month.

>>> IRBT = Symbol("IRBT")
>>> for day in Yearly(IRBT,date=(4,20),start=date(2007,1,1)):
...  pass

That returns april 20th for every year I have available, starting at 2007.


Annually and quarterly are done in the following manner:

>>> for day in IRBT.getAvailableDates(Quarterly.BalanceSheet)

Slicing on iterators is also supported:

>>> iter = Daily(IRBT)
>>> for day in iter[date(2006,12,1):date(2007,12,1)]:
...  #equivalent to Daily(IRBT,start=date(2006,12,1),end=date(2007,12,1)

or on indices

>>> iter = Daily(IRBT)
>>> for day in iter[5:]:
...  #equivalent to the start being the fifth trading day after the first available date.

"""

from dateutil.rrule import *
import itertools
import FinancialDate
import Daily as DailyModule

def Span(lst):
	""" Simple function that returns the begining and end of a list, as a tuple. """
	return (lst[0],lst[-1])

class DateIterator(object):
	def __init__(self,symbol,ruleGen,start,end):
		self.symbol = symbol
		self.ruleGen = ruleGen
		self.rule = ruleGen(start,end)
	
	def __iter__(self):
		return (self.symbol.Date(day.month,day.day,day.year) for day in self.rule)
	
	def __getslice__(self, slice):
		return DateIterator(self.symbol, self.ruleGen, start=slice.first, end=slice.second)
	   	return DateIterator(self.symbol, self.ruleGen, start=self.rule[slice.first], end=self.rule[slice.end])
	   #check behavior of normal slices to get the inclusion right
	
	def __getitem__(self, index):
		return self.symbol.Date(day.month,day.day,day.year)

def Daily(symbol, start=None, end=None):
	availableDates = symbol.AvailableDates(DailyModule.Prices)
	return DateIterator(symbol, ruleGenBuilder(DAILY), Span(availableDates)[0], Span(availableDates)[1])
	
def ruleGenBuilder(*args, **kwargs):
	def _(start,end):
		kwargs['dtstart'] = start
		kwargs['until'] = end
		rule = rrule(*args, **kwargs)
		return FinancialDate.BuildTradingDateRule2(rule)
	return _
	
	
		
		
		
	

