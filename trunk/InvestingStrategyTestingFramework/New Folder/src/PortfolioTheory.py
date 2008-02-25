import Portfolio
import random
import Reccomendation
import logging



class PortfolioTheory(object):
    def __init__(self, market):
        self.market = market
        #connect to db?  might call this class a 'theorist' which in turn relies on 'theories' that
        #themselves come from a theory factory that's had it's database connection/calender set
    
    def rebalance(self, reccomendations):
        pass
    
    def getIdealSize(self):
        pass

class BasicPortfolioTheory(PortfolioTheory):
    def __init__(self, market):
        super(BasicPortfolioTheory, self).__init__(market)

    def rebalance(self, reccomendations, oldPortfolio):
        #reccomendations is a dict of {Symbol: Reccomendation}
        
        reccomendations = reccomendations.values()
        reccomendations.reverse()
        #print reccomendations
        reccomendations.sort()
        reccomendations = [x for x in reccomendations if isinstance(x, Reccomendation.Buy)]
        #print reccomendations
        total = float(len(reccomendations))
        
        proportions = dict([(x.getSymbol(),1.0/total) for x in reccomendations])
            
        return Portfolio.IdealPortfolio(proportions, self.market)
        
        #oldPortfolio is passed in because of sell signals against holds.  A dumb fundamentalist
        #theory might just pick the top 20 buys out of reccomendations and ignore oldportfolio
        #however, even a dumb technician theory needs to look for sell signals on any stocks
        #in the old portfolio before it sells them, otherwise it must reccomend buy or hold.
        
        #you know what'd be interesting is if portfolioTheories could be turned into function 
        #objects, with the above signature.  But instead of a whole bunch of different ones, there'd
        # be a few basic ones that could be added or subtracted from eachother...
        
        #basically figures out the proportions of different stocks vs. cash based on 
        #ratings.  then constructs a portfolio with those weightings based on actual values.
        #return Portfolio.Portfolio.ProportionPortfolio( {self.market.CASH:100}, self.market)
        
        #this is behavior that only applies to a simple broker
 #       advice = [x for x in advice if x.getSignal() == Reccomendation.Buy]
        #skim the top(at most) 20, or however many i need to fill in my portfolio
  #      advice = advice[:(20-portfolio.getPositions())]
  
class Hold20Buys(PortfolioTheory):
    def rebalance(self, reccomendations, oldPortfolio):
        """ Returns a portfolio of 20 stocks.  If any stock passed in is now reccomended to be "
        " 'sold', it is dropped.  It is replaced with a random 'buy' stock. """
        
        stockpicks = oldPortfolio.getSymbols()
        
        #print "In Portfolio Theory"
        
        allSymbols = self.market.getAllSymbols()
        
        #remove losers from current portfolio
        for symbol in oldPortfolio.getSymbols():
            if isinstance(reccomendations[symbol], Reccomendation.Sell):
                    stockpicks.remove(symbol)
                    allSymbols.remove(symbol)
                
        while(len(stockpicks) < self.getIdealSize() and len(allSymbols) > 0):
            potentialSymbol = allSymbols[random.randint(0, len(allSymbols)-1)]
            if isinstance(reccomendations[potentialSymbol], Reccomendation.Buy):
                stockpicks.append(potentialSymbol)
            allSymbols.remove(potentialSymbol)
                  
        ideal = Portfolio.IdealPortfolio(dict([(symbol, 1.0/float(len(stockpicks)))\
                                               for symbol in stockpicks]), self.market)
        return ideal
    
    def getIdealSize(self):
        return 25

class Hold8BuysOrCash(PortfolioTheory):
    def rebalance(self, reccomendations, oldPortfolio):
        """ Returns a portfolio of 8 stocks.  If any stock passed in is now reccomended to be "
        " 'sold', it is dropped.  It is replaced with a random 'buy' stock.  If 20 buys cannot "
        " be found, cash is used to fill the rest."""
        
        stockpicks = oldPortfolio.getSymbols()
        
        #print "In Portfolio Theory"
        
        allSymbols = self.market.getAllSymbols()
        
        #remove losers from current portfolio
        for symbol in oldPortfolio.getSymbols():
            if isinstance(reccomendations[symbol], Reccomendation.Sell):
                    stockpicks.remove(symbol)
                    allSymbols.remove(symbol)
                
        while(len(stockpicks) < self.getIdealSize() and len(allSymbols) > 0):
            potentialSymbol = allSymbols[random.randint(0, len(allSymbols)-1)]
            if isinstance(reccomendations[potentialSymbol], Reccomendation.Buy) and potentialSymbol not in stockpicks:
                stockpicks.append(potentialSymbol)
            allSymbols.remove(potentialSymbol)
            
        idealPortfolio = dict([(symbol, 1.0/float(self.getIdealSize())) for symbol in stockpicks])
        idealPortfolio[self.market.CASH] = 1.0 - (float(len(stockpicks)) / float(self.getIdealSize()))
        
        logging.info("ideal portfolio %s", str(idealPortfolio))
                  
        ideal = Portfolio.IdealPortfolio(idealPortfolio, self.market)
        return ideal
    
    def getIdealSize(self):
        return 9
                    