import Portfolio

class MarketSimulation(object):
    def __init__(self, marketFactory):       
        self.myMarket = marketFactory.Market()       
        self.myPortfolio = Portfolio.LoggedPortfolio.CashPortfolio(10000, self.myMarket)
        self.myMarketCalender = marketFactory.MarketCalender()
        self.myInvestingStrategy = marketFactory.InvestingStrategy()
        self.myTrader = marketFactory.Trader()
        self.myPortfolioTheory = marketFactory.PortfolioTheory()
        self.myBroker = marketFactory.Broker()
        
    def __iter__(self):
        pass
    
    def run(self):
        pass
            
class BasicMarketSimulation(MarketSimulation):
    def __init__(self, marketFactory):
        super(BasicMarketSimulation, self).__init__(marketFactory)
        
    def step(self):
        self.myPortfolio = self.myBroker.balancePortfolio(self.myPortfolio)
        #print "calling next"
#        self.myMarketCalender.next()
        
    def __iter__(self):
        """ Used to iteratively see the output from a simulation run """
        for date in self.myMarketCalender:
            yield (date, self.myPortfolio)
            self.step()
            
    def run(self):
        """ Used just to get the final portfolio """
        for date in self.myMarketCalender:
            self.step()
        return self.myPortfolio
         
