import Transaction

class Position(object):
    """ Basic wrapper around holdings in the stock market, including a symbol, and ammount of stock
    " held.  Could be expanded to support short sells, futures and option positions """
    def __init__(self, symbol, ammount, market):
        self.mySymbol = symbol
        self.myAmmount = ammount
        self.myMarket = market
        
    def getQuantity(self):
        return self.myAmmount
    
    def setQuantity(self, newQuantity):
        self.myAmmount = newQuantity
        
    def getSymbol(self):
        return self.mySymbol
        
    def __add__(self, other):
        if isinstance(other, Transaction.Transaction):
            return self.__addTransaction__(other)
        elif isinstance(other, Position):
            return self.__addPosition__(other)
        else:
            raise "Invalid type to add"
        
    def __addTransaction__(self, other):
        if self.mySymbol == self.myMarket.CASH:

            toReturn = Position(self.mySymbol, self.myAmmount, self.myMarket)
            toReturn.myAmmount += ((other.getAmmount() * other.getPrice()) - other.getFees())
            
            if toReturn < 0.0:
                raise "Not enough cash to cover transaction"
            
            return toReturn
        else:
            if other.getSymbol() != self.mySymbol:
                raise "Unmatching stock symbols"

            toReturn = Position(self.mySymbol, self.myAmmount, self.myMarket)
            toReturn.myAmmount += other.getAmmount()
            
            return toReturn
        
    def __addPosition__(self, other):
        if other.mySymbol != self.mySymbol:
            raise "Non matching symbols"
        if other.myMarket is not self.myMarket:
            raise "Non matching markets"
        
        toReturn = Position(self.mySymbol, self.myAmmount, self.myMarket)
        toReturn.myAmmount += other.myAmmount
    
        return toReturn
    
    def __sub__(self, other):
        if isinstance(other, Transaction.Transaction):
            return self.__subTransaction__(other)
        elif isinstance(other, Position):
            return self.__subPosition__(other)
        else:
            raise "Invalid type to sub"
        
    
    def __subPosition__(self, other):
        if other.mySymbol != self.mySymbol:
            raise "Non matching symbols"
        if other.myMarket is not self.myMarket:
            raise "Non matching markets"
        
        toReturn = Position(self.mySymbol, self.myAmmount, self.myMarket)
        toReturn.myAmmount -= other.myAmmount
        
        if toReturn.myAmmount < 0:
            raise "Not enough stock to sell"
        
        return toReturn
    
    def __subTransaction__(self, other):
        if self.mySymbol == self.myMarket.CASH:
            toReturn = Position(self.mySymbol, self.myAmmount, self.myMarket)
            toReturn.myAmmount -= ((other.getAmmount() * other.getPrice()) + other.getFees())
            
            if toReturn.myAmmount < 0.0:
                
                raise "BOOBIES BOOBIES"
                raise Exception("Not enough cash to complete transaction")
            
            return toReturn
        else:
            if other.getSymbol() != self.mySymbol:
                raise "Unmatching stock symbols"

            toReturn = Position(self.mySymbol, self.myAmmount, self.myMarket)
            toReturn.myAmmount -= other.getAmmount()
            
            if toReturn.myAmmount < 0.0:
                raise "Not enough stock to complete transaction"
            
            return toReturn
    
    def dummyPosition(self):
        return Position(self.mySymbol, 0.0, self.myMarket)
        
    
    def getPrice(self):
        return self.mySymbol.getPrice()
    
    def getValue(self):
        y = self.getPrice()
        return self.getQuantity() * y
    
    def __str__(self):
        return "(" + str(self.mySymbol) + " Shares " + str(self.myAmmount) + " Price " + str(self.getPrice()) + " Value " + str(self.getValue()) + ")"
    
    def __repr__(self):
        return str(self)
    
class CashPosition(Position):
       pass
        