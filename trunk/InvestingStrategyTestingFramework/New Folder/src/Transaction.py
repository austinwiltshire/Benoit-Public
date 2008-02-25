""" Used to represent buys and sells.  """

class Transaction(object):
    def __init__(self, symbol, quantity, market, fees):
        self.date = market.getDate()
        self.symbol = symbol
        self.quantity = quantity
        self.price = symbol.getPrice()
        self.fees = fees
        
    def __str__(self):
        return " ".join(map(str, [self.date, self.getType(), self.quantity, "SHARES OF", self.symbol,\
                    "AT", self.price]))
        
    def __repr__(self):
        return " ".join(map(str, [self.date, self.getType(), self.quantity, "SHARES OF",\
                        self.symbol,"AT", self.price]))
        
    def getType(self):
        pass
    
    def getSymbol(self):
        return self.symbol
    
    def getAmmount(self):
        return self.quantity
    
    def getPrice(self):
        return self.price
    
    def getFees(self):
        return self.fees

        
class Buy(Transaction):
    def getType(self):
        return "BUY"
    
class Sell(Transaction):
    def getType(self):
        return "SELL"
