class Broker(object):
    def __init__(self, investingStrategy,trader, portfolioTheory, market):
        self.myInvestingStrategy = investingStrategy
        self.myTrader = trader
        self.myPortfolioTheory = portfolioTheory
        self.myMarket = market
        
    def balancePortfolio(self, portfolio):
        """ Takes in a portfolio and returns a portfolio with cash converted into new positions """
        pass
        
class BasicBroker(Broker):
    def __init__(self, investingStrategy,trader, portfolioTheory, market):
        super(BasicBroker, self).__init__(investingStrategy, trader, portfolioTheory, market)
        
    def balancePortfolio(self, portfolio):
        """ Takes in a portfolio and returns a portfolio with cash converted into new positions """
       
#        advice = {}
 #       for symbol in self.myMarket.getAllSymbols():
  #          advice[symbol] = self.myInvestingStrategy.getAdvice(symbol)
      #precalculating advice is inefficient.  i should just produce advice for the theroist when he needs it
        
        balancedPortfolio = self.myPortfolioTheory.rebalance(self.myInvestingStrategy, portfolio)
        
        portfolio = self.myTrader.match(balancedPortfolio, portfolio)
        return portfolio
                               
        #learn the deocrate, sort, undecorate idiom
        #learn how to take apart dicts.
        #learn how to initialize dict's above.
        #extrude the commonalities of the above into a common function.
    
    