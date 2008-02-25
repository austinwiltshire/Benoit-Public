import MarketFactory
import Broker
import Trader
import InvestingStrategy
import PortfolioTheory
import Market
import MarketDatabase
import MarketCalender
import Portfolio

class MarketFactoryBuilder:
    def __init__(self):
        pass
    
    def Wire(self, keyword, value):
        setattr(self, keyword, value)
        
    def Manufacture(self):
        return MarketFactory.MarketFactory(self.Broker, self.Trader, self.InvestingStrategy,\
                                           self.PortfolioTheory, self.Market, self.MarketDatabase,\
                                           self.MarketCalender, self.Portfolio)
    
    def ToolBasic(self):
        self.Wire("Broker", Broker.BasicBroker)
        self.Wire("Trader", Trader.BasicTrader)
        self.Wire("InvestingStrategy", InvestingStrategy.BasicInvestingStrategy)
        self.Wire("PortfolioTheory", PortfolioTheory.BasicPortfolioTheory)
        self.Wire("Market", Market.BasicMarket)
        self.Wire("MarketDatabase", MarketDatabase.MarketDatabase)
        self.Wire("MarketCalender", MarketCalender.BasicMarketCalender)
        self.Wire("Portfolio", Portfolio.Portfolio)
        
    @classmethod
    def PrebuiltBasic(cls):
        myMarketFactoryBuilder = cls()
        myMarketFactoryBuilder.ToolBasic()
        return myMarketFactoryBuilder