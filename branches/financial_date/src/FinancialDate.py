"""
This module contains the beginings of a Financial Calendering API.  Currently it contains date policies, which
are standard, module helper classes for distinguishing date resolution.

Also contains stubs for Year and Quarter types, which should provide convienient, unified access to dates.

Implementation Notes:

Due to date rule construction, the first call to the date rule may be slow. A way around this might be to get an arbitrary date
during importation to cause the construction of the calendar.

Much of this may be deprecated given the Adaptation API built off of generic functions found in Adapt.  This will allow a function to define itself
off of either dates or datetimes and still work.  Annual and Quarterly helpers may still be useful, and certainly the overall calendering service - while slow -
contains a lot of valuable logic used in iterators.
"""

import datetime
from dateutil.rrule import *
import dateutil.relativedelta

class Calendar(object):
    """
    Provides calendaring services, a factory for financial datetimes.
    """
    
    def __init__(self):
        self._allTradingDays = AllTradingDays
    
    def NthTradingDayAfter(self, aDate, n):
        """ Finds the nth trading day after aDate.  Takes into account holidays and weekends. """
        
        if aDate in self._allTradingDays: #start so i'm always on a trading day.
            trialDate = aDate
        else:
            trialDate = self._allTradingDays.after(aDate) 
        
        if n==0: #in case we actually just want the trading day we passed in
            return FinancialDateTime(trialDate, self)
        
        for x in range(n):
            trialDate = self._allTradingDays.after(trialDate)
            
        return FinancialDateTime(trialDate, self)
    
    def NthTradingDayBefore(self, aDate, n):
        """ Finds the nth trading day before aDate.  Takes into account holidays and weekends. """
        trialDate = aDate
        
        if aDate in self._allTradingDays:
            trialDate = aDate
        else:
            trialDate = self._allTradingDays.before(aDate)
        
        if n==0: #in case we actually just want the trading day we passed in
               return FinancialDateTime(trialDate, self)
        
        for x in range(n):
            trialDate = self._allTradingDays.before(trialDate)
        return FinancialDateTime(trialDate, self)
    
    def FirstTradingDayBefore(self, aDate):
        """ Finds the first trading day before aDate, taking into account holidays and weekends. """
        return self.NthTradingDayBefore(aDate, 0)
    
    def FirstTradingDayAfter(self, aDate):
        """ Finds the first trading day after aDate, taking into account holidays and weekends. """
    
        return self.NthTradingDayAfter(aDate, 0)
    
    def IsTradingDay(self, aDate):
        """ Predicate returns true if aDate is a trading day, false otherwise. """
    
        return aDate in self._allTradingDays 

class FinancialDateTime(object):
    """
    Represents a datetime that is financially useful, i.e., during trading days and hours.
    """
    
    def __init__(self, date_, calendar):
        
        assert calendar.IsTradingDay(date_), "FinancialDateTimes only represent trading days!"
        
        if isinstance(date_, datetime.datetime):
            self._date = date_
        else: #assume datetime.date
            self._date = datetime.datetime(date_.year, date_.month, date_.day, 9, 0, 0) #assume 9 oclock am to make it a valid trading time   
            
    def toDatetime(self):
        return self._date
    
    def toDate(self):
        return self._date.date()
    
    def __eq__(self, rhs):
        return self._date == rhs     

def NthTradingDayAfter(aDate, n):
    """ Finds the nth trading day after aDate.  Takes into account holidays and weekends. """
    
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
    """ Finds the nth trading day before aDate.  Takes into account holidays and weekends. """
    trialDate = aDate
    
    if aDate in AllTradingDays:
        trialDate = aDate
    else:
        trialDate = AllTradingDays.before(aDate)
    
    if n==0: #in case we actually just want the trading day we passed in
           return trialDate
    
    for x in range(n):
        trialDate = AllTradingDays.before(trialDate)
    return trialDate

def FirstTradingDayBefore(aDate):
    """ Finds the first trading day before aDate, taking into account holidays and weekends. """
    
    return NthTradingDayBefore(aDate, 0)

def FirstTradingDayAfter(aDate):
    """ Finds the first trading day after aDate, taking into account holidays and weekends. """
    
    return NthTradingDayAfter(aDate, 0) 

def IsTradingDay(aDate):
    """ Predicate returns true if aDate is a trading day, false otherwise. """
    
    return aDate in AllTradingDays

#todo: remove positional args after beginDate.  Remove default to beginDate.  Move all dicts out to global scope such that they are only built once.
def BuildTradingDateRule():
    """ Helper function to build any local daily rule for iterator use.  Takes into account holidays and weekends.  Set beginDate to the first
    date available, the further back you go, the more strenuous performance. """
    
    #start on january 1st 1900
    beginDate = datetime.datetime(1900, 1, 1)
    
    days_of_mourning = {"Eisenhower":datetime.datetime(1969,3,31), #dead presidents
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
    
    acts_of_war = {"WorldTradeCenter1":datetime.datetime(2001,9,11), #knock knock
                   "WorldTradeCenter2":datetime.datetime(2001,9,12), #who's there?
                   "WorldTradeCenter3":datetime.datetime(2001,9,13), #september 11th
                   "WorldTradeCenter4":datetime.datetime(2001,9,14) } #september 11th who?
    #you said you'd never forget!
                
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
            
    for exception_day in exception_dates.values():
        tradingDates.exdate(exception_day)
    
    return tradingDates

AllTradingDays = BuildTradingDateRule() #builds the most conservative date rule - this tends to be slow to access!