class MarketFactory:
    """ This factory is wired up by some sort of factory factory, and produces simulation ready
    "   broker's and whatever else.  This factory assumes you pass in the classes you want to 
    "    wire things up with, but also passes in an ACTIVE database connection as myDatabaseCursor """
    def __init__(self, myBrokerClass, myTraderClass, myInvestingStrategyClass,\
                 myPortfolioTheoryClass, myMarketClass, myMarketDatabaseClass,\
                 myMarketCalenderClass, myPortfolioClass):
        self.myBrokerClass = myBrokerClass
        self.myTraderClass = myTraderClass
        self.myInvestingStrategyClass = myInvestingStrategyClass
        self.myPortfolioTheoryClass = myPortfolioTheoryClass
        self.myMarketClass = myMarketClass
        self.myMarketDatabaseClass = myMarketDatabaseClass
        self.myMarketCalenderClass = myMarketCalenderClass
        self.myPortfolioClass = myPortfolioClass
        
        self.myMarket = None # replaces singletons?
        self.myMarketDatabase = None
        self.myMarketCalender = None

    def close(self):
	self.myMarketDatabase.close()
    
    def Broker(self):
        return self.myBrokerClass(self.InvestingStrategy(), self.Trader(), self.PortfolioTheory(),\
                                  self.Market())
    
    def InvestingStrategy(self):
        return self.myInvestingStrategyClass(self.Market())
    
    def Trader(self):
        #assumes 0 comissions
        return self.myTraderClass(self.Market(), 0.0)
    
    def PortfolioTheory(self):
        return self.myPortfolioTheoryClass(self.Market())
    
    def Market(self):
        #print "!!!"
        if not self.myMarket:
            self.myMarket = self.myMarketClass(self.MarketDatabase(), self.MarketCalender())
        return self.myMarket
        #return self.myMarketClass(self.MarketDatabase(), self.MarketCalender())
    
    def MarketDatabase(self):
        if not self.myMarketDatabase:
            self.myMarketDatabase = self.myMarketDatabaseClass()
        return self.myMarketDatabase
    
    def MarketCalender(self):
        if not self.myMarketCalender:
            self.myMarketCalender = self.myMarketCalenderClass(self.MarketDatabase())
        return self.myMarketCalender
        #return self.myMarketCalenderClass(self.MarketDatabase())       
