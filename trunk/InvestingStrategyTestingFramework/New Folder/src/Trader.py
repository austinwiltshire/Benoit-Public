#import copy
import Position
import Transaction
import logging

def ComissionedTrader(trader, _comission):
    return lambda x,y: trader(x, comission=_comission)

class Trader(object):
    """ Currently a dumb trader.   Detect buys and sells could do better """
    def __init__(self, myMarket, comission):
        self.myMarket = myMarket
        self.myComission = comission
    
    def match(self, newPortfolio, oldPortfolio):
        """ Takes in a preferred portfolio and an actual portfolio, engages in trades to match as close as possible the two """
        pass
                
class BasicTrader(Trader):
    """ Currently a dumb trader.   Detect buys and sells could do better """
    
    def __init__(self, myMarket, comission):
        super(BasicTrader, self).__init__(myMarket, comission)
        self.antijitterTolerance = 2
    
    def match(self, newPortfolio, oldPortfolio):
        """ Takes in a preferred portfolio and an actual portfolio, engages in trades to match as close as possible the two """
        #oldPortfolio = copy.copy(oldPortfolio)
        #get rid of the copy since it might be taking up space since portfolios can get big...
        #print "In trader, holdings before trade: ", str(oldPortfolio.getSymbols())
   #     print "In trader, ideal: ", str(newPortfolio.getSymbols())
        #do sells first to liberate cash
   #     stocksToSell = [(x,-(newPortfolio.getProportion(x)-y)) for (x,y) in oldPortfolio.getAllProportions().items()]
   
       # stocksToSell = [(symbol, -(newPortfolio.getProportion(symbol)-newProportion-oldPortfolio.getProportion(symbol)) for\
         #               (symbol, newProportion) in newPortfolio.getAllProportions().items()]
   
        #print "In trader, current holdings proportion: ", str(oldPortfolio.getAllProportions())
        
        allSymbols = set(oldPortfolio.getSymbols() + newPortfolio.getSymbols())
        
        
        sizeHelper = oldPortfolio.getNumberPositions()
 #       print newPortfolio.getAllProportions()
 #       print oldPortfolio.getAllProportions()
   
        trades = [(symbol, (newPortfolio.getProportion(symbol) -\
                 oldPortfolio.getProportion(symbol))) for symbol in allSymbols]
        stocksToBuy = [(symbol, proportion) for (symbol, proportion) in trades if (proportion >= 0.0 and symbol != self.myMarket.CASH and symbol.sharesEquivalent(proportion * oldPortfolio.getTotalValue()) > self.antijitterTolerance)]
        stocksToSell = [(symbol, -proportion) for (symbol, proportion) in trades if (proportion < 0.0 and symbol != self.myMarket.CASH and symbol.sharesEquivalent(proportion * oldPortfolio.getTotalValue()) > self.antijitterTolerance)]
        #find the difference in proportions between the ideal portfolio and this new one.
        
  #      print "before everything, trades :", str(trades)
  #      print "before jitter correction, buys ", str(stocksToBuy)
  #      print "before jitter correction, sells ", str(stocksToSell)
        
        stocksToBuy = [(symbol, symbol.sharesEquivalent(proportion*oldPortfolio.getTotalValue()))\
                              for (symbol, proportion) in stocksToBuy]
        stocksToSell = [(symbol, symbol.sharesEquivalent(proportion*oldPortfolio.getTotalValue()))\
                               for (symbol, proportion) in stocksToSell]
        #find the equivalent shares
        

        
        #anti jitter buys
        stocksToRemove = []
        for i in range(len(stocksToBuy)):
            (symbol, shares) = stocksToBuy[i]
            if shares <= self.antijitterTolerance:
                print "boogie woogie!!!!"
    #            print "removing buy jitter, was ", str((symbol,shares)), " is now ", str((symbol,'0'))
                stocksToRemove.append((symbol, shares))
                #reduces buys of 1,2...
                
        for (symbol,shares) in stocksToRemove:
            stocksToBuy.remove((symbol,shares))        

        stocksToRemove = []        
        for i in range(len(stocksToSell)):
            (symbol, shares) = stocksToSell[i]
            if shares <= self.antijitterTolerance:
                print "rippity pippity!!!"
     #           print "removing sell jitter, was ", str((symbol,shares)), " is now ", str((symbol,'0'))
                stocksToRemove.append((symbol,shares))
                #reduces sells of 1,2...
            elif (oldPortfolio[symbol].getQuantity() - shares) <= self.antijitterTolerance:
      #          print "bumping up sales for jitter, was ", str((symbol,shares)), " is now ", str((symbol, oldPortfolio[symbol].getQuantity()))
                stocksToSell[i] = (symbol, oldPortfolio[symbol].getQuantity())
                #reduces sells that sell all BUT 1,2...
        
        for (symbol,shares) in stocksToRemove:
            stocksToSell.remove((symbol,shares))        
        
                
    #    print "In trader, stocks to buy : ", str(stocksToBuy)
        #print "other stocks to sell helper : ", str(stocksToSell)
        #print "trades :", str(trades)
    #    print "In trader, stocks to sell : ", str(stocksToSell)
        totalCash = oldPortfolio.getTotalValue()

        
       # print "In trader" + str(stocksToSell)
        #liberate cash
        for (symbol, shares) in stocksToSell:
            #TODO: why are there negative percents in here?
            #because you had the weirdest, most innacurate way of calculating those...
            #ammount = symbol.sharesEquivalent(percent * totalCash) #necessary to take comissions into account with each trade
            #oldPortfolio.sell(Position.Position(symbol, ammount, self.myMarket), self.myComission)
            #print Transaction.Sell(symbol, ammount, self.myMarket, self.myComission)
            logging.info("In trader, selling %d shares of %s", shares, str(symbol))
            oldPortfolio.sell(Transaction.Sell(symbol, shares, self.myMarket, self.myComission))
        #make purchases       
        for (symbol, shares) in stocksToBuy:
            #ammount = symbol.sharesEquivalent(percent * (oldPortfolio.getTotalValue() - self.myComission))
            #oldPortfolio.buy(Position.Position(symbol, ammount, self.myMarket), self.myComission)
            #print Transaction.Buy(symbol, ammount, self.myMarket, self.myComission)
            if symbol.getPrice() * shares < oldPortfolio.getCash():
                logging.info("In trader, buying %d shares of %s", shares, str(symbol))
                oldPortfolio.buy(Transaction.Buy(symbol, shares, self.myMarket, self.myComission))
        #turn proportions from above into actual number of stocks.  There WILL be 'negative' ammounts of stocks
        #these represent sells! this also puts the ammounts before the symbols so i can sort on 
        #ammounts below...
        
   #     print "In Trader, holdings after trade: ", str(oldPortfolio.getSymbols())
        #print "In Trader, turnover is: ", str(len(stocksToSell)), " / ", str(sizeHelper-1)
        return oldPortfolio
    
    #NOTE: Btw, array[:] returns a copy of an array.
                
#===============================================================================
#    def buy(self, symbol, ammount, portfolio):
#        """ Buys a certain number of shares """
# 
#        stockValue = symbol.getValue(ammount)
# 
#        #do I have enough cash to buy this ammount?
#        if stockValue > portfolio.getCash():
#            raise "Something"
#            
#        #if this ever gets multithreaded or anything, next two steps need to be atomic
#        portfolio[symbol] += Position(symbol, ammount, self.myMarket)
#        portfolio[self.myMarket.getCash()] -= Position(self.myMarket.CASH, stockValue)
#        #figure out 'dict' like access.  make sure in the portfolio that this buy/sell is logged!
#        #should the portfolio log?  certainly i want portfolios to log behind the scenes...
#        #but I may  need another object to handle the logging responsibilities.  Maybe a type of portfolio or a wrapped portfolio...
#        #should I go with a single consistent interface instead of getCash rather go with Symbol.CASH?
#        
#        return portfolio
#    
#    def sell(self, symbol, ammount, portfolio):
#        
#        #do I have enough shares to sell this ammount?
#        if ammount > portfolio[symbol].getQuantity():
#            raise "Something"
#        
#        stockValue = symbol.getValue(ammount)
#        
#        #like buy, next two steps should be atomic if possible
#        portfolio[symbol] -= Position(symbol, ammount, self.myMarket)
#        portfolio[Symbol.CASH] +=  Position(self.myMarket.CASH, stockValue)
#        
#        return portfolio
#===============================================================================