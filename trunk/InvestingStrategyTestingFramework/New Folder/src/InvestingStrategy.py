import Reccomendation
import datetime
from MyExceptions import EmptyReturns
import MarketDatabase
import DatabaseService
import logging

class InvestingStrategy(object):
    def __init__(self, market):
#        if not market:
#            market = Market.Market()
        self.market = market
        #basically undefined.  do whatever.  in basic one, might do nothing.  most
        #probably will connect to their own analyst of sorts, which might in turn connect
        #to the database or ORM.
    
    def getAdvice(self, symbol): 
        pass
    
    def __getitem__(self, symbol):
        return self.getAdvice(symbol)
    
class BasicInvestingStrategy(InvestingStrategy):
    def __init__(self, market):
        super(BasicInvestingStrategy, self).__init__(market)

    def getAdvice(self, symbol): #in design, put calender in here.  but i'm making calender global?
        #but analysts have their own connection to the database.  how are they going to get calender?
        #make calender singlton again?  or factory method with calender set?
        
        #right nwo, advice does not rely on any other calender date other than today, so this is
        #fine
        
        #returns a Reccomendation
        if symbol == self.market.getSymbol('GM') and self.market.getDate() == datetime.datetime(1,1,1):
            return Reccomendation.Buy(symbol, 1.5)
        elif symbol == self.market.getSymbol('IRBT') and self.market.getDate() == datetime.datetime(1,1,1):
            return Reccomendation.Buy(symbol, 2.0)
        elif symbol == self.market.getSymbol('GM') and self.market.getDate() == datetime.datetime(2,2,2):
            return Reccomendation.Sell(symbol, 5.0)
        elif symbol == self.market.getSymbol('IBM') and self.market.getDate() == datetime.datetime(2,2,2):
            return Reccomendation.Buy(symbol, 2.3)
        else:
            return Reccomendation.Hold(symbol, 1.0)
        
class GBM_DCF(InvestingStrategy):
    """ Derives a discounted cash flow analysis using geometric brownian motion of the free cash "
    " flows.  Returns a percentile for today and generally reccomends buying low percentile stocks."""
    def __init__(self, market):
        super(GBM_DCF, self).__init__(market)
        self.service = DatabaseService.GMB_DCF(None,None,None,None, market.myDatabase)
        
    def getAdvice(self, symbol):
        day = self.market.getDate()

        try:
            percentile = float(self.service.getGBM_DCF(str(symbol),day))
        except DatabaseService.NoReturns, e:
            return Reccomendation.Sell(symbol, 5.0)
        
        if percentile >= 60.0 or percentile < 10.0:
            return Reccomendation.Sell(symbol, 5.0)
            logging.info("advice to sell on %s, percentile at %f",symbol,percentile)
        elif percentile >= 10.0 and percentile <= 45.0:
            logging.info("advice to buy on %s, percentile at %f", symbol,percentile)
#            print "advice on : ", symbol, percentile
            return Reccomendation.Buy(symbol, 5.0)
        elif percentile > 45.0 and percentile < 60.0:
            logging.info("advice to hold on %s, percentile at %f", symbol, percentile)
            return Reccomendation.Hold(symbol, 5.0)
        else: #huh?
            
            return Reccomendation.Sell(symbol, 5.0)
        
class YesterdayUp(InvestingStrategy):
    """ Gives a high buy to any stock that went up yesterday.  A high sell to any stock that went down yesterday. """
    
    def __init__(self, market):
        print "THIS SHOULD NOT PRINT"
        super(YesterdayUp, self).__init__(market)
        self.dates = self.market.getCalender().getDates()
    
    def getAdvice(self, symbol):
        #get yesterday's date
        todaysIndex = self.dates.index(self.market.getCalender().today())
        
        if todaysIndex == 0 or todaysIndex == 1:
            return Reccomendation.Hold(symbol, 5.0)
            
        
        yesterdaysDate = self.dates[todaysIndex-1]
        twodaysagoDate = self.dates[todaysIndex-2]#to judge change between prices

        
        #TODO: need to check to make sure i'm not at the begining of the dates array.
        try:
            yesterdaysPrice = self.market.getPrice(symbol, yesterdaysDate)
            twodaysagoPrice = self.market.getPrice(symbol, twodaysagoDate)
        except EmptyReturns, e: #stock is not traded yet.
            print e
            return Reccomendation.Hold(symbol, 5.0)
        except MarketDatabase.FlaggedResults, e:
            print e
            return Reccomendation.Hold(symbol, 5.0)
            
        #print yesterdaysPrice, twodaysagoPrice, symbol, yesterdaysDate
        #TODO: get rid of duplicates in your database
        if isinstance(yesterdaysPrice, list):
            yesterdaysPrice = yesterdaysPrice[0]
        if isinstance(twodaysagoPrice, list):
            twodaysagoPrice = twodaysagoPrice[0]
        #EVIL HACK
            
 #       print "Today is :", self.market.getCalender().today()
  #      print "Symbol is :", symbol
   #     print "Yesterday was : ", yesterdaysDate, " and its price was : ", yesterdaysPrice
    #    print "Two days ago was : ", twodaysagoDate, " and its price was : ", twodaysagoPrice
        
        diff = yesterdaysPrice - twodaysagoPrice #!!!  should be based on what happened yesterday, not two days ago...
#	diff = symbol.getPrice() - yesterdaysPrice
            
        if(diff > 0.0):
 #           print "Reccomending buy"
            return Reccomendation.Buy(symbol, 5.0)
        elif(diff == 0.0):
 #           print "Reccomending hold"
            return Reccomendation.Hold(symbol, 5.0)
        elif(diff < 0.0):
 #           print "Reccomending sell"
            return Reccomendation.Sell(symbol, 5.0)
