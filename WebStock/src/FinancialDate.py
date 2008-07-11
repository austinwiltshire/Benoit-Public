"""
This module contains the beginings of a Financial Calendering API.  Currently it contains date policies, which
are standard, module helper classes for distinguishing date resolution.
"""

import datetime

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
			sorted(dateList) == dateList
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
		>>> dp = FuzzyPolicy(FuzzyPolicy.RoundUp)
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2003,12,30), datetime.date(2004,1,1), datetime.date(2004,6,2)])
		datetime.date(2004, 6, 2)
		
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
				sorted(dateList) == dateList
				isinstance(aDate, datetime.date)
				all(isinstance(x, datetime.date) for x in dateList)
		
			post[]:
				isinstance(__return__,datetime.date) or __return__ is None
			 
		"""
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
		>>> dp = FuzzyPolicy(FuzzyPolicy.RoundDown)
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2003,6,30), datetime.date(2004,1,3), datetime.date(2004,6,2)])
		datetime.date(2003, 6, 30)
		
		Returns the date passed in if it exists in the dateList:
		>>> dp.advice(datetime.date(2004,1,2), [datetime.date(2004,1,1), datetime.date(2004,1,2), datetime.date(2004,2,3)])
		datetime.date(2004, 1, 2)
		
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
				sorted(dateList) == dateList
				isinstance(aDate, datetime.date)
				all(isinstance(x, datetime.date) for x in dateList)
		
			post[]:
				isinstance(__return__,datetime.date) or __return__ is None
			
			"""	
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
		>>> dp = FuzzyPolicy(FuzzyPolicy.RoundClose)
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
		
		pre:
			sorted(dateList) == dateList
			isinstance(aDate, datetime.date)
			all(isinstance(x, datetime.date) for x in dateList)
		
		post[]:
			isinstance(__return__,datetime.date) or __return__ is None
		
		""" 
		def __call__(self, aDate, dateList):
			"""
			RoundClose uses function object semantics.  For help, please see the RoundClose object's documentation.  This
			call expects a datetime.date to be passed in for aDate, and a list of datetime.dates to be passed in for dateList
			aDate is a datetime.date, while dateList is a list of datetime.dates in sorted order (latest dates last).
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
	
	
	def __init__(self, roundRule=RoundDown):
		"""
		Fuzzy policy requires a rounding rule to be passed in for dependency injection.  By default, this is 
		RoundDown.  The round rule is expected to be default constructable and passed in as a class.
		
		pre:
			isinstance(roundRule,type)
			roundRule == FuzzyPolicy.RoundDown or roundRule == FuzzyPolicy.RoundUp or roundRule == FuzzyPolicy.RoundClose
		"""
		self._roundRule = roundRule()
		
	def advice(self, aDate, dateList):
		"""
		Fuzzy policy returns the best date in the list of dates passed in to substitute for the single passed in date argument.  Of
		course, if the single date is also in the list of dates, the single date itself is quickly returned.  Otherwise, the
		fuzzy policy invokes its rounding rule to decide between the list of dates which is best suited to substitute for
		the passed in date.   aDate is a datetime.date, while dateList is a list of datetime.dates in sorted order (latest dates last).
		
		pre:
			sorted(dateList) == dateList
			isinstance(aDate, datetime.date)
			all(isinstance(x, datetime.date) for x in dateList)
		
		post[]:
			isinstance(__return__,datetime.date) or __return__ is None
		
		"""
		if aDate in dateList:
			return aDate
		return self._roundRule(aDate, dateList)