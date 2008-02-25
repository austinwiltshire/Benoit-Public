#Market is a factory for symbols.
import MarketDatabase

class Symbol(object):
    #My attempt at a flyweight pattern.  
    allSymbols = {}
    def __new__(cls, stringSymbol, **kwords):
        if not(stringSymbol in Symbol.allSymbols):
            Symbol.allSymbols[stringSymbol] = object.__new__(cls, stringSymbol)
        return Symbol.allSymbols[stringSymbol]
            
    def __init__(self, stringSymbol, myMarket):
            self.stringSymbol = stringSymbol
            self.myMarket = myMarket
    
    def getPrice(self):
        try:
        #TODO: get rid of duplicates in the database
            checkForDuplicate = self.myMarket.getPrice(self)
      #  print checkForDuplicate,
        except MarketDatabase.FlaggedResults, e:
            checkForDuplicate = e.price
        if isinstance(checkForDuplicate, list):
            return checkForDuplicate[0]
        return checkForDuplicate
        
    def getCashFlow(self):
            return self.myMarket.getCashFlow(self)
        
    def getValue(self, ammount):
        return self.getPrice() * ammount
    
    def sharesEquivalent(self, money, truncate=True):
        """ Returns the shares equivalent to 'money' sum of money.  For example, passing in 100.00 "
        " when the price is 5.00 will return 20.00.  If 'truncate' is true, returns a truncated, "
        " rounded down integer, to prevent partial shares from being returned. """
       #check for divide by zero
       #TODO: Find out why stocks that are not traded yet are being flagged by my portfolio theorist.
        try:
           if truncate:
       #     print money, self.getPrice()
               return int(money / self.getPrice())
           else:
               return money / self.getPrice()
        except Exception, e:
            return 0.0
            
        
    def __str__(self):
        return self.stringSymbol
    
    def __repr__(self):
        return self.stringSymbol
    
    def __eq__(self, other):
        return self.stringSymbol == other.stringSymbol
    
    def getStringRep(self):
        return self.stringSymbol
        
class Cash(Symbol):
    def __new__(cls, **kwords):
        toReturn = super(Cash, cls).__new__(cls, 'CASH')
        return toReturn
    
    def __init__(self, myMarket):
        self.stringSymbol = "CASH"
        self.myMarket = myMarket
            
    def __hash__(self):
        return hash("CASH")
    
    def getPrice(self):
        return 1.0
    
    def getValue(self, ammount):
        return ammount
        
#to avoid singletons, and possibly even flyweights, think about the following:
# add a factory or abstract factory that is set by actual database connection/market and calender
#all symbols flowing from that factory are going to be initialized on those two things.
#could allow the ability to use the same broker to analyze two different days at the same time,
#using two different database connections.
        