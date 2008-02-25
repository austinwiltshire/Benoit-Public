import Symbol
import Position
import Market
import pickle
#import copy
import Transaction

class Portfolio(object):
    def __init__(self, myMarket):
        self.positions = {}
        self.market = myMarket
        
    def getSymbols(self):
        return [x for x in self.positions.keys() if x is not self.market.CASH and self.positions[x] > 0.0]

        #return [x for x in self.positions.keys() if x is not self.market.CASH and self.positions[x].getQuantity() > 0.0]
#        toReturn = self.positions.keys()
 #       if self.market.CASH in toReturn:
  #          toReturn.remove(self.market.CASH)
   #     return toReturn
    
    def getProportions(self, symbol):
        pass
    
    def getAllProportions(self):
        return dict((x, self.getProportion(x)) for x in self.getSymbols())
    
    def getNumberPositions(self):
        return len(self.positions)
    
    def __getitem__(self, indexSymbol):
        return self.positions[indexSymbol]
    
    def __setitem__(self, indexSymbol, newPosition):
        if isinstance(newPosition, float):
            self.positions[indexSymbol].setQuantity(newPosition)
            return
        self.positions[indexSymbol] = newPosition
    
    def __str__(self):
        pass
        
    def __repr__(self):
        return str(self)

class TradingPortfolio(Portfolio):
    def buy(self, transaction):
        currentCash = self.positions[self.market.CASH]
        
        try:
            self.positions[self.market.CASH] -= transaction
            
            if transaction.getSymbol() not in self.positions :
                self.positions[transaction.getSymbol()] = Position.Position(transaction.getSymbol(), 0.0, self.market)
                
            self.positions[transaction.getSymbol()] += transaction
        except Exception, e:
 #           print e
#            raise e
            print "Probably not enough cash"
        
    def sell(self, transaction):
        currentCash = self.positions[self.market.CASH]
        
        try:
            self.positions[self.market.CASH] += transaction
            self.positions[transaction.getSymbol()] -= transaction
            if self.positions[transaction.getSymbol()].getQuantity() <= 0.01:
                del self.positions[transaction.getSymbol()]
                #stop tracking symbols i have no quantity for.
            
        except Exception, e:
            print e
            raise e
            self.positions[self.market.CASH] -= transaction #undo transaction
            print "Probably not enough stock"
    
    def getCash(self):
        return self.positions[self.market.CASH].getValue()
    
    def setCash(self, ammount):
        self.positions[self.market.CASH] = Position.Position(self.market.CASH, ammount, self.market)
    
    def getProportion(self, symbol):
        if symbol in self.positions:
            return float(self.positions[symbol].getValue()) / float(self.getTotalValue())
        else:
            return 0.0;
    
    def getTotalValue(self):
#        for pos in self.positions.values():
#            print str(pos)
   #     print sum(x.getValue() for x in self.positions.values()), "!!!!!!"
        x = sum(x.getValue() for x in self.positions.values())
        return x
        
    def __str__(self):
        return "Trading Portfolio { " + ",".join([str(x) for x in self.positions.values() if x.getQuantity() != 0.0]) + " } "
    
    @classmethod
    def CashPortfolio(cls, ammount, mymarket):
        toReturn = cls(mymarket)
        toReturn.setCash(ammount)
        return toReturn
    
class IdealPortfolio(Portfolio):
    """ Portfolio built completely by percentage, no real shares or money. Builds a portfolio from a 
        " dict of symbol : proportion pairs.  Proportions should add up "
        " to 100.00% but this is not assumed.  Instead, the proportion is assumed to be that of the "
        " whole.  If the dict {'irbt':10, 'gm':100} is passed in, then the percentage assigned to "
        " irbt will be 10/110, while the percentage assigned to gm will be 100/110.  As a bit of "
        " trivia, the value of 1,000,000 is used as a cash dummy to divide up the proportion of "
        " stocks.  It is assumed that the portfolio returned will be used for its proportions only "
        " and not for it's value or specific quantities. """
    def __init__(self, proportionSet, myMarket):
        super(IdealPortfolio, self).__init__(myMarket)
        
        totalUnits = float(sum([x for x in proportionSet.values()]))
        totalMoney = 1000000.00 # used to make percentages easier to calculate
      
        for (symbol, ammount) in proportionSet.iteritems():
            proportion = float(ammount) / totalUnits
#            self.positions[symbol] = Position.Position(symbol, symbol.sharesEquivalent(totalMoney * proportion), myMarket)        
            self.positions[symbol] = proportion
    
    def getSymbols(self):
        return self.positions.keys()
            
    def __getitem__(self, symbol):
        return self.positions.get(symbol, 0.0)
    
    def __setitem__(self):
        raise "Ideal portfolio is immutable"
    
    def getProportion(self, symbol):
        return self[symbol]
    
    def __str__(self):
        return "Ideal Portfolio { " + ",".join(["".join([str(x),": ",str(y),"%"])\
                                                for (x,y) in self.positions.items()]) + " } "
    
class LoggedPortfolio(TradingPortfolio):
    def __init__(self, myMarket):
        self.myHistory = []
        self.valueHistory = {}
        super(LoggedPortfolio, self).__init__(myMarket)
        
    def __len__(self):
        return len(self.myHistory)

    def save(self, filename):
	    #assumes DB is closed.  otherwise we run into major issues here...
	    saveto = open(filename, 'w')
	    pickle.dump(self, saveto)
	    saveto.close()

    @classmethod
    def load(cls, filename, myMarket=None):
	    openup = open(filename, 'r')
	    acls = pickle.load(openup)
	    openup.close()
	    #toreturn = cls(myMarket)
	    #toreturn.valueHistory = valueHistory
	    #toreturn.myHistory = history
	    #toreturn.positions = positions
	    return acls


        
    def buy(self, transaction):
        
        try:
            super(LoggedPortfolio, self).buy(transaction)
        except Exception, e:
            print e
            #don't logg the transaction as it didn't happen.
            raise "Transaction did not occur"
        else:
            self.myHistory.append(transaction)
            self.valueHistory[self.market.getCalender().today()] = self.getTotalValue()

    def sell(self, transaction):
        try:
            super(LoggedPortfolio, self).sell(transaction)
        except Exception, e:
            print e
            #don't logg the transaction as it didn't happen.
            raise "Transaction did not occur"
        else:
           self.myHistory.append(transaction)
           self.valueHistory[self.market.getCalender().today()] = self.getTotalValue()
            
    def getHistory(self):
        return self.myHistory     
    
    @staticmethod
    def buysOnly(transactionToCheck): #used for filtering functions
        """ Use: filter(transactions, Portfolio.buysOnly) """
        if isinstance(transactionToCheck, Transaction.Buy):
            return True
        else:
            return False
        
    @staticmethod
    def sellsOnly(transactionToCheck): #used for filtering functions
        """ Use: filter(transactions, Portfolio.sellsOnly) """
        if isinstance(transactionToCheck, Transaction.Sell):
            return True
        else:
            return False
