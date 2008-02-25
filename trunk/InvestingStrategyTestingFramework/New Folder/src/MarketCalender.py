#import datetime
#import copy
#import MarketDatabase
from MyExceptions import checkNotEmpty

#how do i I do singleton/borg in python?  Should only be one calender...
class MarketCalender(object):
    def __init__(self, myMarketDatabase):
        self.myMarketDatabase = myMarketDatabase
        #TODO: get rid of 'check not empty"
        self.dates = checkNotEmpty(self.myMarketDatabase.getAllDates())
        self.index = 0
        
    def getDates(self):
        return self.dates
            
    def today(self):
        pass
        
    def setNear(self, date):
        """ Takes in a date and sets the calender's index to that date or the first date AFTER that
        " date if the date is not available, except if it's later than the last date, then set
        " to the last date """
        pass
        
    def __iter__(self):
        """ Returns all dates, can iterate through those dates, or just use that as an enumeration
        " while .next'ing this """
        pass
        
class BasicMarketCalender(MarketCalender):

    def __init__(self, myMarketDatabase):
        super(BasicMarketCalender, self).__init__(myMarketDatabase)
            
    def today(self):
        return self.dates[self.index]
    
    def __iter__(self):
        for index in range(self.index, len(self.dates)):
            self.index = index
            yield self.today()
        
    def getQuarter(self, symbolString, date=None):
        allDates = self.myMarketDatabase.getAllFinancialDates(symbolString)
        #right now i don't support quarters, but i do support annuals, so do that
        
        #we want to find the lowest positive time difference between today and all my financial
        #dates, meaning, the financial date that was most recent in the past.
        if not date:
            date = self.today()
            
        diff = [(date - x,x) for x in allDates if (date - x).days > 0]
        #decorate -> sort -> undecorate
        diff.sort()
        
        return diff[0][1] 
    
        
    
        
    def setNear(self, date):
        """ Takes in a date and sets the calender's index to that date or the first date AFTER that
        " date if the date is not available, except if it's later than the last date, then set
        " to the last date """

        if date not in self.dates: # not very efficient
            newdates = copy.deepcopy(self.dates)
            newdates.append(date)
            newdates.sort()
            index = newdates.index(date)
            if(index < len(self.date)): #make sure date we're looking for isnt bigger than all dates we have
                self.index = index
            else:
                self.index = index-1
        else:
            self.index = self.dates.index(date)
        
#    def __iter__(self):
 #       """ Returns all dates, can iterate through those dates, or just use that as an enumeration
  #      " while .next'ing this """
   #     return self
        #how am I going to check for market day?
        # I could get 'market days' from the database.  I should probably just do that... base it 
        # on days I have data for the dji...
        
        #alternatively, if i wanted a database free model, I'd have to exclude weekends and holidays.
        #maybe I can get a list somewhere?
        #maybe a third party library has holidays listed?
    
        #check for dates out of bounds?