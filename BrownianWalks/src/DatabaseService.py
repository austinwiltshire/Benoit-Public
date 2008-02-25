import MarketDatabase

from scipy import stats
import scipy
import math
import itertools
import pylab
import numpy
import datetime
import Query

class NoReturns(Exception):
    pass
    
def plotlines(*args):
    colors = itertools.cycle(['r','g','b','y'])
    plotargs = []
    for line,c in zip(args,colors):
        plotargs += [range(len(line)), line, c]
    pylab.plot(*plotargs)
    pylab.show()
        
class MarketService:
    pass

def GMB():
    return scipy.randn()
    #return scipy.random.lognormal(0.0,1.0)
    #returns a bell curve?

def percentstd(mean, dist):
    distfrommean = []
    for each in dist:
        print (each-mean)/mean
        distfrommean.append(pow((each-mean)/mean, 2))
    std = sum(distfrommean)
    std /= (len(dist)-1)
    #I don't think i need the geometric average.
 #   std = reduce(lambda x,y: x*y, distfrommean)
 #   std = pow(std, 1.0/(len(dist)))
    return math.sqrt(std)      
    
def geo_stats(distribution):
    mean = stats.gmean(distribution)
    
    #get geometric variance
    #geometric std is = the sum of (natural log of Ai - natrual log of the mean)^2 over n.
    # where Ai is the i'th member in the distribution and the mean is the geometric mean of the
    #distribution.  
    # take that number then take the square root, then take THAT number and raise e to the power of it.
    log_mean = math.log(mean)
    
    ans1 = (sum( [math.pow((math.log(x) - log_mean),2) for x in distribution] )) / len(distribution)
    #ans1 is temporary variable
    std = math.pow(math.e, math.sqrt(ans1))
    
    return std, mean
    
    

class GMB_DCF(MarketService):
    """ Geometric brownian motion walks into the future to produce a discounted cash flow analysis. "
    " Analysis is done by comparing a current price into a distribution and returning a percentile """
    def __init__(self, discountRate, years, defaultLongTermGrowthRate, number=10000, PDF=GMB, db = None):
        """ Set the distribution function, discount rate and years for this DCF """
        #TODO: should be passed in a marketDatabase..., or a normal database connection.
        self.PDF = PDF
        self.discountRate = discountRate
        self.years = years
        self.defaultLongTermGrowthRate = defaultLongTermGrowthRate
        if not db:
            db = MarketDatabase.SQLMarketDatabase()
        self.myDB = db
        self.number = number #granularity of distribution
        self.cachedDates = {}
    
    def setup(self):
        """ Original setup.  Produces a table of precalculated percentile fits for all prices. """
        
        #TODO: generalize this so that the year of the table I'm making is a variable and 
        #not just assumed to be the 'last one'.  that is currently how i'm getting my 
        #base variable and my stockIssued variable.
        self.myDB.db.CreateTable({'symbol':str, 'date':datetime.date, 'percentile':float}, "GBM_DCF")
        
        for symbol in self.myDB.getAllSymbols():
            #TODO: make sure the below is sorted at the myDB level
            answer = self.myDB.getFreeCashFlows(symbol)
            #(years,freeCashFlows) = zip(*self.myDB.getFreeCashFlows(symbol))
            yearCashPairs = self.myDB.getFreeCashFlows(symbol)
            print "Calculating %s" % symbol
                       
            if len(yearCashPairs) == 0:
                print "Not enough data"
                continue
            
            (years, freeCashFlows) = zip(*yearCashPairs)
            #get first year's working capital to approximate underlying 'asset'
            #TODO: my really bad understanding of accounting(check with grant) is the following
            #all free cash flows are converted into 3 things:
            #stock buy backs, dividends, or saved off as additional current assets.
            #current assets in turn may be turned into long term assets via aqcuisitions and the like
            #or they could be used to pay off long term debt
            #so i'm going to take simple working capital from the first year as the 'underlying
            #asset'.  all changes in working capital in the next years that i'm taking
            #cash flow i'm going to attribute entirely to using cash to pay off debt or 
            #turn into long term assets.
            
            if len(years) < 5:
                print "Not enough data."
                #not enough sample points, ignore this one.
                continue
            
            
            #so far i need 3 services, closing, free cash flows and working capital
            #these in turn would need to call at least 4 others, operating cash flow and capex
            #and current assets and current liabilities.
            
            #TODO: put database format in some XML file maybe?
            #maybe login info too?
            #can refer and tailor that to whoever's computer i'm on

            year = years[-1]

            #new idea.  take the average growth in absolute terms.  put that over the average
            #value in absolute terms.  we'll use that as my drift.  we'll plot this to see 
            #if it makes sense.

            avg_value = stats.mean(freeCashFlows)
            abs_growth = [x-y for (x,y) in zip(freeCashFlows[1:],freeCashFlows[:-1])]
            avg_growth = stats.mean(abs_growth)
            std_growth = stats.std(abs_growth)
            avg = avg_growth / avg_value
            avg = avg + 1.0
            #this is a huge fucking guess.  this is the weakest part of the whole damned thing.

            std = std_growth / avg_value    
           
            #for plotting, we're assuming 'avg value' is in the middle.
#            middle = len(freeCashFlows)/2
 #           print middle, len(freeCashFlows)
  #          toplotabs = []
   #         toplotabsstd1 = []
    #        toplotabsstd2 = []
     #       for x in range(len(freeCashFlows)):
      #          val = ((x-middle) * avg_growth) + avg_value
#                print val
          #      toplotabs.append(val)
         #       toplotabsstd1.append(val+std_growth)
        #        toplotabsstd2.append(val-std_growth)
                
       #     toplotgrow = []
      #      toplotgrowstd1 = []
     #       toplotgrowstd2 = []
    #        for x in range(len(freeCashFlows)):
   #             growth = pow(1+percentGrowth, (x-middle))
  #              val1 = (avg_value * pow(1+percentGrowth,(x-middle)))
 #               print val1
#                toplotgrow.append(val1)
#                toplotgrowstd1.append(val1 + (avg_value * percentStd))
#                toplotgrowstd2.append(val1 - (avg_value * percentStd))

            if std < 0.0 or avg < 1.0:
                print "Negative growth, ignoring"
                continue
            #leave out those who aren't even growing on average  duh.
            #could put them in later if you wanted to aggressively short sell.
            
            potentialFutures = [self.genFuture(freeCashFlows[-1], std, avg)\
                                 for x in range(self.number)]

            summedFutures = [sum(x)+perp for x,perp in potentialFutures]
            for x in range(len(summedFutures)):
                if summedFutures[x] < 0.0:
                    summedFutures[x] = 0.0
            summedFutures.sort()
            
            #screw working capital idea
#            workingCapitalProxy = [workingCapital+freeCashFlows[0]]
#            for x in range(len(freeCashFlows)-1):
#                workingCapitalProxy.append(workingCapitalProxy[x] + freeCashFlows[x+1])
                #TODO: see above comment about asking grant              
#            FCFGrowth = [1.0 + (x-y)/y for (x,y) in zip(workingCapitalProxy[1:],workingCapitalProxy[:-1])]
#            print FCFGrowth
#            print workingCapitalProxy
#            std, avg = stats.std(FCFGrowth),geo_stats(FCFGrowth)[1]
            #we're using the normal standard deviation, and the geometric average growth.            
#            potentialFutures = [self.genFuture(freeCashFlows[-1], std, avg)\
 #                                for x in range(self.number)]
#            potentialFutures = [self.genFuture(workingCapitalProxy[-1], std, avg)\
#                                for x in range(self.number)]
            #trying to pass in working capital
#            workingCapitalDiscount = [self.grow(workingCapital, 1.05, year) for year in\
#                                      range(len(potentialFutures[0]))]
#           
#            for future in range(len(potentialFutures)):
#                for year in range(len(workingCapitalDiscount)):
#                    potentialFutures[future][year] -= workingCapitalDiscount[year]            
            #now i need to strip working capital back out
                          
            stockIssued = self.myDB.getStockIssued(symbol,year)
            if stockIssued == 0:
                print "No stock issued"
                continue
            
#            plotlines(*potentialFutures)
                
            
#            return potentialFutures
            priceCurve = [summedFuture / stockIssued for summedFuture in summedFutures]
            #TODO: histogram would be nice to see shape of ending distribution
            
#            print symbol, potentialFutures
            
            #now, for this distribution, I have to fit each price into it and return a percentile            
            percentiles = [(date, self.getPercentile(float(price), priceCurve))\
                            for (date,price) in self.myDB.getClosesForYear(symbol, year)]
            
#            print symbol, percentiles

            for (date,percentile) in percentiles:
                self.myDB.setGBH_DCF(symbol, date, percentile)
            self.myDB.db.commit()
                #put the values back in my database
            
            #TODO: make a 'distribution' class that will keep itself ordered even as I add points
            #and return to me a percentile I plug into it
            
    def getPercentile(self, price, priceCurve):
        index = 0
        while index < len(priceCurve) and price > priceCurve[index]:
            index += 1
        return 100.00 * (float(index) / float(len(priceCurve)))

    def grow(self, principle, rate, year):
        """ Opposite of discount """
        return principle * pow(rate,year)

    def genFuture(self, principle, shock, drift, timescale = 1.0):
        #set up first year
        potentialFlows = [principle * scipy.random.normal(drift, shock)]
        
        #we've already seeded the first year
        for x in range(self.years-1):
#            print 'current principle', potentialFlows[-1]
#            other = drift + shock * self.PDF()
#            modifier = scipy.random.normal(drift, shock)
#            shock = shock * self.PDF()
#            modifier = drift + shock
#            print modifier,
            try:
                modifier = scipy.random.normal(drift,shock)
            except:
                print drift, shock
                raise "boogie"
            
 #           print 'drift * shock', modifier
 #           print "other ", other
#            potentialFlows.append(potentialFlows[-1] + potentialFlows[-1] * (drift * timescale) *\
 #                                 (shock * self.PDF() * math.sqrt(timescale)))
            potentialFlows.append(potentialFlows[-1] * modifier)
            #ah jeez.  ok now i have the geometric average as the drift, and the geometric 
            #variance as the 'shock'.  but how do i generate some random log_normal number?
            perpetuity = self.calcPerpetuity(potentialFlows, drift, shock)
            perpetuity = self.discount(perpetuity, self.discountRate, self.years)
            #TODO: discount rate ought to be related to the variance in the cash flows.
            discountedFlows = []
            for (year, value) in enumerate(potentialFlows):
                #enumerate starts with year 0, but we need to start with year 1
                discountedFlows.append(self.discount(value, self.discountRate, year+1))
        return discountedFlows,perpetuity
#        return sum(potentialFlows)
        #what about perpetuity?
        
    def calcPerpetuity(self, cashflows, drift, shock):
        final = cashflows[-1]
        basediscount = self.discountRate - 1.0
        baselongterm = self.defaultLongTermGrowthRate - 1.0
        return (final * self.defaultLongTermGrowthRate) / (basediscount - baselongterm)
    
    
    def discount(self, principle, rate, years):
        """ Returns the value of the principle in years if discount rate is rate "
        " assumes that rate is in 1.x format, i.e., 5 percent would be 1.05 """
        return principle / pow(rate, years)
    
    def getGBM_DCF(self, symbol, date):
        #I'm going to cache here.
        if not self.checkCache(date):
            self.addCache(date)
        return self.getCache(date,symbol)
    
    def checkCache(self, date):
        if date in self.cachedDates.keys():
            return True
        else:
            return False
        
    def addCache(self, date):
  #      print date, "in add"
        DBReturns = self.myDB.db.Select(['symbol','percentile'],['GBM_DCF'],\
                                      ['date = \'%s\'' % date])
        if DBReturns == [] or DBReturns == None:
 #           print "null results, adding empty dictionary"
            self.cachedDates[date] = {}
            if len(self.cachedDates.keys()) >= 5:
                del self.cachedDates[min(self.cachedDates.keys())]
            return
        if isinstance(DBReturns[0],str):
            DBReturns = [DBReturns]
        
        cache = dict([(symbol, percentile) for symbol,percentile in DBReturns])
        self.cachedDates[date] = cache
        if len(self.cachedDates.keys()) >= 5:
            del self.cachedDates[min(self.cachedDates.keys())]
    
    def getCache(self, date, symbol):
        #assumes DATE is in CACHE
        if symbol not in self.cachedDates[date].keys():
            raise NoReturns()
        else:
            return self.cachedDates[date][symbol]

class distribution(object):
    def __init__(self, array):
        self.array = array
    
    def percentile(self, value):
        #figure out where in the array this value fits with percentiles...
        pass

    