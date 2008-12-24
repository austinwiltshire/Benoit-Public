"""
This module contains the beginings of a Financial Calendering API.  Currently it contains date policies, which
are standard, module helper classes for distinguishing date resolution.

Also contains stubs for Year and Quarter types, which should provide convienient, unified access to dates.
"""

import datetime
from dateutil.rrule import *
import dateutil.relativedelta

def toDatetime(aDate):
	return datetime.datetime(aDate.year,aDate.month,aDate.day)

def toDate(aDate):
	return datetime.date(aDate.year,aDate.month,aDate.day)

def lastDayOfMonth(aDate):
	return datetime.datetime(aDate.year,(aDate.month+1)%12,1) - dateutil.relativedelta.relativedelta(days=1)

def YearDay(aDate):
	#could also add week and weekday
	baseyear = datetime.datetime(aDate.year, 1, 1)
	return (aDate - baseyear).days + 1

def NthTradingDayAfter(aDate, n):
	
	if aDate in AllTradingDays: #start so i'm always on a trading day.
		trialDate = aDate
	else:
		trialDate = AllTradingDays.after(aDate) 
	
	if n==0: #in case we actually just want the trading day we passed in
		return trialDate
	
	for x in range(n):
		trialDate = AllTradingDays.after(trialDate)
	return trialDate

def NthTradingDayBefore(aDate, n):
	trialDate = aDate
	
	if n==0: #in case we actually just want the trading day we passed in
		if aDate in AllTradingDays:
			return aDate
		else:
			return AllTradingDays.after(aDate)
	
	for x in range(n):
		trialDate = AllTradingDays.before(trialDate)
	return trialDate

		 

#def LocalDailyRule(baserule):
#	if baserule._freq == DAILY:
#		return baserule
#	if baserule._freq == WEEKLY:
#		return rrule(DAILY,byweekday=baserule._byweekday,bymonth=baserule._dtstart.month,byyear=baserule._dtstart.year)
#	if baserule._freq == MONTHLY:
#		return rrule(DAILY,byweekday=baserule._byweekday,bymonth=baserule._dtstart.month,byyear=baserule._dtstart.year)
#	if baserule._freq == YEARLY:
#		return rrule(DAILY,byweekday=baserule._byweekday,bymonth=baserule._bymonth,byyear=baserule._dtstart.year)

#TODO: were these always market holidays?  I can change up the dates by manipulating dtstart and until, for example, I might
#change MLK day to be a market holiday only after 1989 or something.  more research needed
def BuildTradingDateRule(beginDate=datetime.date(1900,1,1), otherIncRules=None, otherExRules=None, otherIncDates=None, otherExDates=None):
	
	days_of_mourning = {"Eisenhower":datetime.datetime(1969,3,31), 
					    "MartinLutherKing":datetime.datetime(1968,4,9),
						"Truman":datetime.datetime(1972,12,28),
						"JFK":datetime.datetime(1963,11,25),
						"LBJ":datetime.datetime(1973,1,25),
 					  	"Nixon":datetime.datetime(1994,4,27),
 		 		  	   	"Reagan":datetime.datetime(2004,6,11),
			 		  	"Ford":datetime.datetime(2007,1,2) }
	
	acts_of_god = {"SnowDay":datetime.datetime(1969,2,10), #apparently horrible weather and snow.
				   "NewYorkCityBlackout":datetime.datetime(1977,7,14), 
				   "HurricaneGloria":datetime.datetime(1985,9,27)}
	
	acts_of_war = {"WorldTradeCenter1":datetime.datetime(2001,9,11),
				   "WorldTradeCenter2":datetime.datetime(2001,9,12),
				   "WorldTradeCenter3":datetime.datetime(2001,9,13),
				   "WorldTradeCenter4":datetime.datetime(2001,9,14) }
				
	paper_crisis_additions = {"LincolnsBirthday":datetime.datetime(1968,2,12),
							  "DayAfterIndependenceDay":datetime.datetime(1968,7,5), 	
							  "VeteransDay":datetime.datetime(1968,11,11) }
								 
	one_small_step_for_man = {"MoonLanding":datetime.datetime(1969,7,21) } # first lunar landing
	
	exception_dates = {}
	exception_dates.update(days_of_mourning)
	exception_dates.update(acts_of_god)
	exception_dates.update(acts_of_war)
	exception_dates.update(paper_crisis_additions)
	exception_dates.update(one_small_step_for_man)

	#check out : www.chronos-st.org/NYSE_Observed_Holidays-1885-Present.html
	
	Holidays = {"PaperCrisis":rrule(WEEKLY,bymonth=(6,7,8,9,10,11,12),byweekday=(WE),dtstart=datetime.datetime(1968,6,6),until=datetime.datetime(1969,1,1)),
			 	"ElectionDayEveryYear":rrule(YEARLY,bymonth=11,bymonthday=(2,3,4,5,6,7,8),byweekday=(TU),dtstart=beginDate,until=datetime.datetime(1969,1,1)),
			 	"ElectionDayPresidential":rrule(YEARLY,bymonth=11,bymonthday=(2,3,4,5,6,7,8),byweekday=(TU),interval=4,dtstart=datetime.datetime(1972,1,1),until=datetime.datetime(1984,1,1)),			 	
			 	"WashingtonsBirthdayWeek":rrule(YEARLY,bymonthday=22,bymonth=2,byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate,until=datetime.datetime(1971,1,1)),
			 	"WashingtonsBirthdaySun":rrule(YEARLY,bymonthday=23,bymonth=2,byweekday=(MO),dtstart=beginDate,until=datetime.datetime(1971,1,1)),
			 	"WashingtonsBirthdaySat":rrule(YEARLY,bymonthday=21,bymonth=2,byweekday=(FR),dtstart=beginDate,until=datetime.datetime(1971,1,1)),
			 	"OldMemorialDayWeek":rrule(YEARLY,bymonthday=30,bymonth=5,byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate,until=datetime.datetime(1970,1,1)),
			 	"OldMemorialDaySun":rrule(YEARLY,bymonthday=31,bymonth=5,byweekday=(MO),dtstart=beginDate,until=datetime.datetime(1970,1,1)),
			 	"OldMemorialDaySat":rrule(YEARLY,bymonthday=29,bymonth=5,byweekday=(FR),dtstart=beginDate,until=datetime.datetime(1970,1,1)), #there was no celebration of memorial day in 1970
			 	"NewYearsDayWeek":rrule(YEARLY,bymonthday=1,bymonth=1,byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate),
			 	"NewYearsDaySun":rrule(YEARLY,bymonthday=2,bymonth=1,byweekday=(MO),dtstart=beginDate),
		  	    "IndependenceDayWeek":rrule(YEARLY,bymonth=7,bymonthday=(4),byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate),
		  	    "IndependenceDaySun":rrule(YEARLY,bymonth=7,bymonthday=5,byweekday=(MO),dtstart=beginDate),
		  	    "IndependenceDaySat":rrule(YEARLY,bymonth=7,bymonthday=3,byweekday=(FR),dtstart=beginDate),
		  	    "ChristmasWeek":rrule(YEARLY,bymonth=12,bymonthday=25,byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate),
		  	    "ChristmasSun":rrule(YEARLY,bymonth=12,bymonthday=26,byweekday=(MO),dtstart=beginDate),
		  	    "ChristmasSat":rrule(YEARLY,bymonth=12,bymonthday=24,byweekday=(FR),dtstart=beginDate),
		  	    "GoodFriday":rrule(YEARLY,byeaster=-2,dtstart=beginDate),
		  	    "MartinLutherKingDay":rrule(YEARLY,bymonth=1,byweekday=MO(+3),dtstart=datetime.datetime(1998,1,1)),
		  	    "PresidentsDay":rrule(YEARLY,bymonth=2,byweekday=MO(+3),dtstart=datetime.datetime(1971,1,1)),
		  	    "LaborDay":rrule(YEARLY,bymonth=9,byweekday=MO(+1), dtstart=beginDate),
		  	    "NewMemorialDay":rrule(YEARLY,bymonth=5,byweekday=MO(-1),dtstart=datetime.datetime(1971,1,1)),
		  	    "ThanksgivingDay":rrule(YEARLY,bymonth=11,byweekday=TH(4),dtstart=beginDate)}
	
	PaperCrisisRule = rrule(WEEKLY,bymonth=(6,7,8,9,10,11,12),byweekday=(WE),dtstart=datetime.datetime(1968,6,6),until=datetime.datetime(1969,1,1))
	PaperCrisisSet = rruleset()
	PaperCrisisSet.rrule(PaperCrisisRule)
	PaperCrisisSet.exdate(datetime.datetime(1968,6,5))
	PaperCrisisSet.exdate(datetime.datetime(1968,7,3))
	PaperCrisisSet.exdate(datetime.datetime(1968,9,4))
	PaperCrisisSet.exdate(datetime.datetime(1968,11,6))
	PaperCrisisSet.exdate(datetime.datetime(1968,11,13))
	PaperCrisisSet.exdate(datetime.datetime(1968,11,27))
	Holidays["PaperCrisis"] = PaperCrisisSet
	
	
	tradingDates = rruleset(cache=True)
	tradingDates.rrule(rrule(DAILY,byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate))
	for holiday in Holidays.values():
		tradingDates.exrule(holiday)
	
	if otherIncRules:
		for rule in otherIncRules:
			tradingDates.rrule(rule)
			
	if otherExRules:
		for rule in otherExRules:
			tradingDates.rrule(rule)
			
	if otherIncDates:
		for date in otherIncDates:
			tradingDates.rdate(date)
	
	if otherExDates:
		for date in otherExDates:
			tradingDates.exdate(date)	
			
	for exception_day in exception_dates.values():
		tradingDates.exdate(exception_day)
	
	return tradingDates

def BuildTradingDateRule2(baseRule):
	beginDate = baseRule._dtstart
	
	if isinstance(baseRule,rrule):
		baseRuleSet = rruleset()
		baseRuleSet.rrule(baseRule)
	else:
		baseRuleSet = baseRule
	
	days_of_mourning = {"Eisenhower":datetime.datetime(1969,3,31), 
					    "MartinLutherKing":datetime.datetime(1968,4,9),
						"Truman":datetime.datetime(1972,12,28),
						"JFK":datetime.datetime(1963,11,25),
						"LBJ":datetime.datetime(1973,1,25),
 					  	"Nixon":datetime.datetime(1994,4,27),
 		 		  	   	"Reagan":datetime.datetime(2004,6,11),
			 		  	"Ford":datetime.datetime(2007,1,2) }
	
	acts_of_god = {"SnowDay":datetime.datetime(1969,2,10), #apparently horrible weather and snow.
				   "NewYorkCityBlackout":datetime.datetime(1977,7,14), 
				   "HurricaneGloria":datetime.datetime(1985,9,27)}
	
	acts_of_war = {"WorldTradeCenter1":datetime.datetime(2001,9,11),
				   "WorldTradeCenter2":datetime.datetime(2001,9,12),
				   "WorldTradeCenter3":datetime.datetime(2001,9,13),
				   "WorldTradeCenter4":datetime.datetime(2001,9,14) }
				
	paper_crisis_additions = {"LincolnsBirthday":datetime.datetime(1968,2,12),
							  "DayAfterIndependenceDay":datetime.datetime(1968,7,5), 	
							  "VeteransDay":datetime.datetime(1968,11,11) }
								 
	one_small_step_for_man = {"MoonLanding":datetime.datetime(1969,7,21) } # first lunar landing
	
	exception_dates = {}
	exception_dates.update(days_of_mourning)
	exception_dates.update(acts_of_god)
	exception_dates.update(acts_of_war)
	exception_dates.update(paper_crisis_additions)
	exception_dates.update(one_small_step_for_man)

	#check out : www.chronos-st.org/NYSE_Observed_Holidays-1885-Present.html
	
	Holidays = {"PaperCrisis":rrule(WEEKLY,bymonth=(6,7,8,9,10,11,12),byweekday=(WE),dtstart=datetime.datetime(1968,6,6),until=datetime.datetime(1969,1,1)),
			 	"ElectionDayEveryYear":rrule(YEARLY,bymonth=11,bymonthday=(2,3,4,5,6,7,8),byweekday=(TU),dtstart=beginDate,until=datetime.datetime(1969,1,1)),
			 	"ElectionDayPresidential":rrule(YEARLY,bymonth=11,bymonthday=(2,3,4,5,6,7,8),byweekday=(TU),interval=4,dtstart=datetime.datetime(1972,1,1),until=datetime.datetime(1984,1,1)),			 	
			 	"WashingtonsBirthdayWeek":rrule(YEARLY,bymonthday=22,bymonth=2,byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate,until=datetime.datetime(1971,1,1)),
			 	"WashingtonsBirthdaySun":rrule(YEARLY,bymonthday=23,bymonth=2,byweekday=(MO),dtstart=beginDate,until=datetime.datetime(1971,1,1)),
			 	"WashingtonsBirthdaySat":rrule(YEARLY,bymonthday=21,bymonth=2,byweekday=(FR),dtstart=beginDate,until=datetime.datetime(1971,1,1)),
			 	"OldMemorialDayWeek":rrule(YEARLY,bymonthday=30,bymonth=5,byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate,until=datetime.datetime(1970,1,1)),
			 	"OldMemorialDaySun":rrule(YEARLY,bymonthday=31,bymonth=5,byweekday=(MO),dtstart=beginDate,until=datetime.datetime(1970,1,1)),
			 	"OldMemorialDaySat":rrule(YEARLY,bymonthday=29,bymonth=5,byweekday=(FR),dtstart=beginDate,until=datetime.datetime(1970,1,1)), #there was no celebration of memorial day in 1970
			 	"NewYearsDayWeek":rrule(YEARLY,bymonthday=1,bymonth=1,byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate),
			 	"NewYearsDaySun":rrule(YEARLY,bymonthday=2,bymonth=1,byweekday=(MO),dtstart=beginDate),
		  	    "IndependenceDayWeek":rrule(YEARLY,bymonth=7,bymonthday=(4),byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate),
		  	    "IndependenceDaySun":rrule(YEARLY,bymonth=7,bymonthday=5,byweekday=(MO),dtstart=beginDate),
		  	    "IndependenceDaySat":rrule(YEARLY,bymonth=7,bymonthday=3,byweekday=(FR),dtstart=beginDate),
		  	    "ChristmasWeek":rrule(YEARLY,bymonth=12,bymonthday=25,byweekday=(MO,TU,WE,TH,FR),dtstart=beginDate),
		  	    "ChristmasSun":rrule(YEARLY,bymonth=12,bymonthday=26,byweekday=(MO),dtstart=beginDate),
		  	    "ChristmasSat":rrule(YEARLY,bymonth=12,bymonthday=24,byweekday=(FR),dtstart=beginDate),
		  	    "GoodFriday":rrule(YEARLY,byeaster=-2,dtstart=beginDate),
		  	    "MartinLutherKingDay":rrule(YEARLY,bymonth=1,byweekday=MO(+3),dtstart=datetime.datetime(1998,1,1)),
		  	    "PresidentsDay":rrule(YEARLY,bymonth=2,byweekday=MO(+3),dtstart=datetime.datetime(1971,1,1)),
		  	    "LaborDay":rrule(YEARLY,bymonth=9,byweekday=MO(+1), dtstart=beginDate),
		  	    "NewMemorialDay":rrule(YEARLY,bymonth=5,byweekday=MO(-1),dtstart=datetime.datetime(1971,1,1)),
		  	    "ThanksgivingDay":rrule(YEARLY,bymonth=11,byweekday=TH(4),dtstart=beginDate)}
	
	PaperCrisisRule = rrule(WEEKLY,bymonth=(6,7,8,9,10,11,12),byweekday=(WE),dtstart=datetime.datetime(1968,6,6),until=datetime.datetime(1969,1,1))
	PaperCrisisSet = rruleset()
	PaperCrisisSet.rrule(PaperCrisisRule)
	PaperCrisisSet.exdate(datetime.datetime(1968,6,5))
	PaperCrisisSet.exdate(datetime.datetime(1968,7,3))
	PaperCrisisSet.exdate(datetime.datetime(1968,9,4))
	PaperCrisisSet.exdate(datetime.datetime(1968,11,6))
	PaperCrisisSet.exdate(datetime.datetime(1968,11,13))
	PaperCrisisSet.exdate(datetime.datetime(1968,11,27))
	Holidays["PaperCrisis"] = PaperCrisisSet
	
	exclude_weekends = rrule(DAILY,byweekday=(SA,SU),dtstart=beginDate)
	
	baseRuleSet.exrule(exclude_weekends)
	for holiday in Holidays.values():
		baseRuleSet.exrule(holiday)
	
	return baseRuleSet

AllTradingDays = BuildTradingDateRule() #builds the most conservative date rule - this tends to be slow to access!

class Year(object):
	""" Represents a financial year and provides convienience operations to derive information based on financial years. """
	def __init__(self, seedDate):
		""" Right now assumes a datetime date, but really most of these Year and Quarter types are going to have to do a lot of
		isinstance stuff to resolve all sorts of dates into a single format. """
		self.value = seedDate.year
	
	def __repr__(self):
		return str(self.value)
	
	def getValue(self):
		return self.value
	
class Quarter(object):
	""" Represents a financial year and provides convieneince opteraions to derive information based on financial quarters. """
	Quarters = [(0,4,1),(0,7,1),(0,10,1),(1,1,1)] #used for base quarter calcuations
	QuarterStrings = {1:"First Quarter",2:"Second Quarter",3:"Third Quarter",4:"Fourth Quarter"}
	def __init__(self, seedDate):
		""" Right now assumes a datetime date, but really msot of these Year and Quarter types rae going to have to do a lot of
		isinstance stuff to resolve all sorts of dates into a single format. """ 
		self.date = seedDate
		quarterFinder = FuzzyPolicy(FuzzyPolicy.RoundUp())
		closestQuarter = quarterFinder.advice(seedDate, Quarter.genQuarters(Year(seedDate)))
		self.value = Quarter.genQuarters(Year(seedDate)).index(closestQuarter) + 1
		
	@staticmethod
	def genQuarters(year):
		return [datetime.date(yearmod+year.getValue(),month,day) for (yearmod,month,day) in Quarter.Quarters]
	
	def __repr__(self):
		return Quarter.QuarterStrings[self.value]
		

class DatePolicy(object):
	"""
	 A date policy is a class that provides date advice when faced with a single date that potentially falls somewhere
	between a group of other dates.  The resolution is what date can be substituted for the passed in date, given the range in
	the group of other dates.
	"""
	def advice(self, aDate, dateList):
		"""
		This function dates in a date and a list of other dates and returns a date.  The date it returns is the 'resolved' date,
		or, the date which this policy believes can be substituted for the passed in date, given the group of other dates.
		"""
		raise ImplementationError("DatePolicy is an abstract class")

class StrictPolicy(DatePolicy):
	"""
	A strict policy basically says that no date is substitutable and that only the passed in date can stand for itself.
	"""
	def advice(self, aDate, dateList):
		"""
		Since no date is substitutable for any other, StrictPolicy advice simply returns the passed in date as the only
		date that can stand for the passed in date.  aDate is a datetime.date, while dateList is a list of datetime.dates
		in sorted order (latest dates last).
		
		Returns the date that is passed in even if it doesn't exist in the dateList:
		>>> dp = StrictPolicy()
		>>> dp.advice(datetime.date(2000,1,1), [datetime.date(2001,1,1),datetime.date(2001,1,2), datetime.date(2001,2,1)])
		datetime.date(2000, 1, 1)
		
		Or, alternatively, if it does:
		>>> dp.advice(datetime.date(2005,3,4), [datetime.date(2005,3,1), datetime.date(2005,3,2), datetime.date(2005,3,4)])	
		datetime.date(2005, 3, 4)
		
		pre:
			isinstance(aDate, datetime.date)
			all(isinstance(x, datetime.date) for x in dateList)
		
		post[]:
			isinstance(__return__,datetime.date)
		"""
		return aDate
		
class FuzzyPolicy(DatePolicy):
	"""
	Fuzzy policy dictates that one of the dates in the passed in list may be substitutable for the single passed in date.
	There are multiple kinds of FuzzyPolicies, created via dependency injection, based on Rounding rules.
	
	inv:
		self._roundRule is not None
		isinstance(self._roundRule,FuzzyPolicy.RoundRule)
	
	"""
	
	class RoundRule(object):
		""" RoundRules are basically sub policies that advice FuzzyPolicy on how to act, whether to round to a later
		date, an earlier date, or the closest date. """
		def __class__(self, aDate, dateList):
			""" Rounding rules are used as functors and must overload the call function. """
			raise ImplementationErrror("RoundRule is an abstract class")
	   
	
	class RoundUp(RoundRule):
		"""
		 The RoundUp rounding rule takes the date that is just 'above', or later, than the date passed in.  The closest date
		that is AFTER the date passed in is returned.  RoundUp uses function object semantics.  If no date exists which is
		larger(later) than the date passed in, RoundUp returns None.
		
		Returns the closest date that's after the one passed in:
		>>> dp = FuzzyPolicy(FuzzyPolicy.RoundUp())
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2003,12,30), datetime.date(2004,1,1), datetime.date(2004,6,2)])
		datetime.date(2004, 6, 2)
		
		Returns the first date if the date that's passed in is before all dates in the list:
		>>> dp.advice(datetime.date(2004,3,2), [datetime.date(2004,4,1), datetime.date(2004,7,1), datetime.date(2004,10,1), datetime.date(2005,1,1)])
		datetime.date(2004, 4, 1)
		
		Returns the date passed in if it exists in the dateList:
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2004,1,1), datetime.date(2004,1,2), datetime.date(2004,2,3)])
		datetime.date(2004, 1, 2)
		
		Returns None if there is no date later than the date passed in:
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2003,12,30), datetime.date(2003,12,31), datetime.date(2004,1,1)]) == None
		True
		
		""" 
		def __call__(self, aDate, dateList):	
			"""
			RoundUp uses function object semantics.  For help, please see the RoundUp object's documentation. This
			call expects a datetime.date to be passed for aDate, and a list of datetime.dates to be passed for dateList. 
		    aDate is a datetime.date, while dateList is a list of datetime.dates in sorted order (latest dates last).
			
			pre:
				dateList == sorted(dateList)
				isinstance(aDate, datetime.date)
				all(isinstance(x, datetime.date) for x in dateList)
		
			post[]:
				isinstance(__return__,datetime.date) or __return__ is None
			 
		"""
		  	dateList = [datetime.date(1900,1,1)] + sorted(dateList)
			toReturn = [upperBound for (lowerBound,upperBound) in zip(dateList[:-1],dateList[1:]) if lowerBound < aDate < upperBound]
			if toReturn:
				return toReturn[0]
			else:
				return None
	
	class RoundDown(RoundRule):
		"""
		The RoundDown rounding rule takes in the date that is just 'below', or before, the date passed in.  The closest date
		that is BEFORE the date passed in is returned.  RoundDown uses function object semantics.  If no date exists which is
		smaller(earlier) than the date passed in, RoundDown returns None.
		
		Returns the closest date that's before the one passed in:
		>>> dp = FuzzyPolicy(FuzzyPolicy.RoundDown())
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2003,6,30), datetime.date(2004,1,3), datetime.date(2004,6,2)])
		datetime.date(2003, 6, 30)
		
		Returns the date passed in if it exists in the dateList:
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2004,1,1), datetime.date(2004,1,2), datetime.date(2004,2,3)])
		datetime.date(2004, 1, 2)
		
		Returns the last date if the date passed in after all dates in the list:
		>>> dp.advice(datetime.date(2005,1,2), [datetime.date(2004,1,1), datetime.date(2004,1,2), datetime.date(2004,2,3)])
		datetime.date(2004, 2, 3)
		
		Returns None if there is no date earlier than the date passed in:
		>>> dp.advice(datetime.date(2003,12,31), [datetime.date(2004,1,1), datetime.date(2004,1,2), datetime.date(2004,1,3)]) == None
		True
				
		"""
		def __call__(self, aDate, dateList):
			"""
			RoundDown uses function object semantics.  For help, please see the RoundDown object's documentation.  This
			call expects a datetime.date to be passed in for aDate, and a list of datetime.dates to be passed for dateList.
			aDate is a datetime.date, while dateList is a list of datetime.dates in sorted order (latest dates last).
			
			pre:
				dateList == sorted(dateList)
				isinstance(aDate, datetime.date)
				all(isinstance(x, datetime.date) for x in dateList)
		
			post[]:
				isinstance(__return__,datetime.date) or __return__ is None
			
			"""	
			dateList = sorted(dateList) + [datetime.date(2100,1,1)]
			toReturn = [lowerBound for (lowerBound,upperBound) in zip(dateList[:-1],dateList[1:]) if lowerBound < aDate < upperBound]
			if toReturn:
				return toReturn[0]
			else:
				return None		
	
	class RoundClose(RoundRule):
		"""
		The RoundClose rounding rule simply takes the closes available date in the list of dates passed in.  It uses function
		object semantics.  RoundClose is the safest Rounding rule as it will never return None.
		
		Returns the closest date that's to the one passed in:
		
		>>> dp = FuzzyPolicy(FuzzyPolicy.RoundClose())
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2003,6,30), datetime.date(2004,1,3), datetime.date(2004,6,2)])
		datetime.date(2004, 1, 3)
		
		Whether that date is higher or lower:
		
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2003,6,30), datetime.date(2004,1,1), datetime.date(2004,6,2)])
		datetime.date(2004, 1, 1)
		
		Returns the date passed in if it exists in the dateList:
		
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2004,1,1), datetime.date(2004,1,2), datetime.date(2004,2,3)])
		datetime.date(2004, 1, 2)
		
		Never returns None:
		
		>>> dp.advice(datetime.date(1990,12,31), [datetime.date(2004,1,1), datetime.date(2004,1,2), datetime.date(2004,1,3)])
		datetime.date(2004, 1, 1)
		
		>>> dp.advice(datetime.date(2010,2,28), [datetime.date(2004,1,1), datetime.date(2004,1,2), datetime.date(2004,1,3)])
		datetime.date(2004, 1, 3)		
		""" 
		def __call__(self, aDate, dateList):
			"""
			RoundClose uses function object semantics.  For help, please see the RoundClose object's documentation.  This
			call expects a datetime.date to be passed in for aDate, and a list of datetime.dates to be passed in for dateList
			aDate is a datetime.date, while dateList is a list of datetime.dates in sorted order (latest dates last).
			
			pre:
				dateList == sorted(dateList)
				isinstance(aDate, datetime.date)
				all(isinstance(x, datetime.date) for x in dateList)
		
			post[]:
				isinstance(__return__,datetime.date) or __return__ is None
			
			"""	
			diffs = [aDate-otherDate for otherDate in dateList]
			#print diffs
			absoluteDiffs = [abs(timediff.days) for timediff in diffs]
			#print absoluteDiffs
			minimumTimeDifferent = min(absoluteDiffs)
			#print minimumTimeDifferent
			minimumIndex = absoluteDiffs.index(minimumTimeDifferent)
			#print minimumIndex
			return dateList[minimumIndex]
	
	
	def __init__(self, roundRule):
		"""
		Fuzzy policy requires a rounding rule to be passed in for dependency injection.  By default, this is 
		RoundDown.  The round rule is expected to be default constructable and passed in as a class.
		
		pre:
			isinstance(roundRule,FuzzyPolicy.RoundRule)
		"""
		
		self._roundRule = roundRule
		
	def advice(self, aDate, dateList):
		"""
		Fuzzy policy returns the best date in the list of dates passed in to substitute for the single passed in date argument.  Of
		course, if the single date is also in the list of dates, the single date itself is quickly returned.  Otherwise, the
		fuzzy policy invokes its rounding rule to decide between the list of dates which is best suited to substitute for
		the passed in date.   aDate is a datetime.date, while dateList is a list of datetime.dates in sorted order (latest dates last).
		
		pre:
			isinstance(aDate, datetime.date)
			all(isinstance(x, datetime.date) for x in dateList)
		
		post[]:
			isinstance(__return__,datetime.date) or __return__ is None
		
		"""
		dateList = sorted(dateList)
		if aDate in dateList:
			return aDate
		return self._roundRule(aDate, dateList)