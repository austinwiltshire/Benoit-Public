import MarketSimulation
import MarketFactoryBuilder
import MarketDatabase
import InvestingStrategy
import PortfolioTheory
import Trader
import pickle
import datetime
import logging

logging.basicConfig(level=logging.NOTSET,
                    format = '%(asctime)s %(name)-12s %(levelname)-8s &(message)s',
                    datefmt='%m-%d %H:%M',
                    filename='debug.log',
                    filemode='w')

mfb = MarketFactoryBuilder.MarketFactoryBuilder.PrebuiltBasic()
#mfb.Wire("Trader", Trader.ComissionedTrader(Trader.BasicTrader, 7.99))
mfb.Wire("MarketDatabase", MarketDatabase.SQLMarketDatabase)
mfb.Wire("InvestingStrategy", InvestingStrategy.GBM_DCF)
mfb.Wire("PortfolioTheory", PortfolioTheory.Hold8BuysOrCash)
broke = mfb.Manufacture()
broke.MarketCalender().setNear(datetime.date(2006,12,27))
sim = MarketSimulation.BasicMarketSimulation(broke)

#simport = sim.run()
first = True

for (date, portfolio) in sim:
    #if first and len(portfolio.getSymbols()) != 0:
    #    if len(portfolio.getSymbols()) != 0:
    #        holdings = set(portfolio.getSymbols())
    #        first = False
    #elif first:
    #    continue
    #holdings = holdings.intersection(set(portfolio.getSymbols()))
    #print portfolio.getSymbols()
    #print "!!!!!!!!!!!!!!!!!!!!!!!!!", str(holdings), "!!!!!!!!!!!!!!!!!!!!!!!"
    print date, "Value :", portfolio.getTotalValue()
    print "Holdings :", [str(x) for x in portfolio.positions.values()]
    logging.info("SimDate :%s Value: %f Holdings :%s", str(date), portfolio.getTotalValue(), str([str(x) for x in portfolio.positions.values()]))
    

#    print "Holdings are ", str(portfolio.getSymbols())
#    print "Size is ", str(len(portfolio))

broke.close()
sim.myPortfolio.save('gbm6.ptf')
#    print date, portfolio, portfolio.getHistory()
 #   print date, "Value is ", portfolio.getTotalValue(), " Number of positions is ", portfolio.getNumberPositions(), \
  #  " Size is ", len(portfolio)
#    print "Holdings are ", portfolio.getSymbols()

