import Symbol
#import copy
from MyExceptions import checkNotEmpty, EmptyReturns

class Market(object):
    def __init__(self, database, calender):
        self.myDatabase = database
        self.myCalender = calender
        self.CASH = self.getCash()
    
    def getSymbol(self, stringSymbol):
        pass
    
    def getCash(self):
        pass
    
    def getPrice(self, symbol, date=None):
        pass
    
    def getAllSymbols(self):
        pass
    
    def getAllSymbolStrings(self):
        pass
    
    def getCalender(self):
        pass
    
    def getDate(self):
        pass
    
#market may just provide simple interface for buys and sells and todays values.  different 
#market analyst objects might also have database connection and provide info to the strategies and
#theorists

class BasicMarket(Market):
    
    def __init__(self, database, calender):
        super(BasicMarket, self).__init__(database, calender)
        
    def getSymbol(self, stringSymbol):
        """ Factory method for symbols, all symbols must come from a market type """
        return Symbol.Symbol(stringSymbol, myMarket=self)
    
    def getCash(self):
        """ Factory method for cash"""
        return Symbol.Cash(myMarket=self)
    
    def getPrice(self, symbol, date=None): 
        """ Gets the _CLOSING_ price on each day """
        if not date:
            date = self.myCalender.today()
        try:
            price = checkNotEmpty(self.myDatabase.getClosing(str(symbol), date))
        except EmptyReturns, e:
            print e
            return 0.0
        else:
            return price
            
    
    def getCashFlow(self, symbol, quarter=None):
        if not quarter:
            quarter = self.myCalender.currentQuarter(str(symbol))
        return checkNotEmpty(self.myDatabase.getCashFlow(str(symbol), quarter))
             
    def getCalender(self):
        #returns a copy of the calender such that any operations on it doesnt affect the global calender
        #TODO: figure out why i can't deep copy calender.
        return self.myCalender
    
    def getAllSymbolStrings(self):
        """ Returns all symbols valid in to poll by this market """
        return checkNotEmpty(self.myDatabase.getAllSymbols())
    
    def getAllSymbols(self):
        return [self.getSymbol(x) for x in checkNotEmpty(self.getAllSymbolStrings())]
    
    def getDate(self):
        return self.myCalender.today()
