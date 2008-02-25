import datetime, Database, CachePolicy, Query
#import SQL stuff.
#ORM might go here if you ever use it.
#nope, ORM is going to be hidden in MarketDatabase, which in turn is a layer above the actual
#sql.

class FlaggedResults(Exception):
    def __init__(self, price):
        self.price = price

def checkfordupe(tocheck):
    if isinstance(tocheck, list):
        return float(tocheck[0])
    return float(tocheck)

class MarketDatabase(object):
    def __init__(self, myCursor = None):
        self.myCursor = myCursor
        #make connection, set up
        #dummy database
        
        self.db = {'SBUX':10.00, 'IBM':25.00, 'IRBT':18.56,'GM':23.00}
            
    def getClosing(self, symbol, date):
        #how do i want to format this?
        #return {(symbol, date) : {'close':0.0}}
        return self.db[symbol]
    #you are already 'get closing', so you know its 'close' and dont need a dict
    #further, the caller also knows the symbol and date, so no worries there either.
    
    def getAllSymbols(self):
        return self.db.keys()
    
    def getAllDates(self):
        return [datetime.datetime(1,1,1), datetime.datetime(2,2,2), datetime.datetime(3,3,3)]
    
class SQLMarketDatabase(MarketDatabase):
    def __init__(self, host='austinwiltshire', user='root', password='password', db="STOCKINFO"):
        self.db = Database.SQLDatabase(host, user, password, db)
        self.stocktable = None
        self.datetable = None
        #self.db.cachePolicy.Append(CachePolicy.SimpleCachePolicy())
        self.localCache = {}
        self.today = None
        self.flaggedCache = {}

    def close(self):
	    self.db.closeConnection()

        
    def getClosing(self, symbol, date):
        #TODO: i'm also doing some cacheing at this level.  i need to figure out a better scheme.
        if date in self.localCache:
            if not symbol in self.localCache[date]:
                return 0.0
            elif date in self.flaggedCache:
                raise FlaggedResults(self.localCache[date][symbol])
            else:
                return self.localCache[date][symbol]
        else:
      #      print "populating local cache for date" + str(date)
            if len(self.localCache) >= 5:
                del self.localCache[min(self.localCache.keys())]
                
            try:
                self.localCache[date] = dict([(_symbol, checkfordupe(close)) for _symbol, close in\
                                    self.db.Select(['symbol','close'],['STOCKPRICES'],\
                                        ['date = \'%s\'' % date])])
                 #TODO: fix this.  some dates in the database don't  have anything in them?
                 #uh, so instead, I set this date to the last one.
                 #this is terrible! i'm a bad person! this reflects on my morality!
            except Exception, e:
                #print max(self.localCache.keys())
                print e
                self.localCache[date] = self.localCache[max(self.localCache.keys())]
                self.flaggedCache[date] = 1
        if not symbol in self.localCache[date]:
            return 0.0
#        print symbol, "*********"
 #       if symbol == 'PHI':
  #          print symbol, date, self.localCache[date][symbol]
        return self.localCache[date][symbol]
    
    def getFreeCashFlow(self, symbol, quarter):
        #i need a fuzzy date
        pair = self.db.Select(['cash_from_operating_activities','capital_expenditures'],\
                               ['STOCKFINANCIALS'],['symbol = \'%s\'' %symbol,\
                                'date = \'%s\'' % quarter], cast=float)
        freeCashFlow = pair[0] - pair[1]
        return freeCashFlow
    
    def getFreeCashFlows(self, symbol):
        triplets = self.db.Select(['date','cash_from_operating_activities','capital_expenditures'],\
                               ['STOCKFINANCIALS'],['symbol = \'%s\'' % symbol])
        cashflows = []
        if len(triplets) != 0 and isinstance(triplets[0], datetime.date):
            triplets = [triplets]
        for (date, cash_ops, capex) in triplets:
            cashflows.append((date, float(cash_ops+capex)))
            #capex is stored as a negative number, so really i want to add the two together to 
            # 'take' capex away from cash_ops.  
        cashflows.sort()
        
        return cashflows
    
    def setGBH_DCF(self, symbol, date, percentile):
        self.db.Replace('GBM_DCF', {'symbol':symbol, 'date':date, 'percentile':percentile})
        
    
    
    def getStockIssued(self, symbol, date):
        return self.db.Select(['total_common_shares_outstanding'], ['STOCKFINANCIALS'],\
                               ['symbol = \'%s\'' % symbol,'date = \'%s\'' % date], float)
        #TODO: what about fuzzy dates - return the latest date, in other words?
        
    def getYearsAvailable(self, symbol):
        return self.db.Select(['date'], ['STOCKFINANCIALS'], ['symbol = \'%s\'' % symbol])
    
    def getClosesForYear(self, symbol, thisyear):
        nextyear = thisyear + datetime.timedelta(366)
        return self.db.Select(['date','close'],['STOCKPRICES'],['symbol = \'%s\'' % symbol,\
                                            'date < \'%s\'' % nextyear, 'date > \'%s\'' % thisyear])
        
    def getWorkingCapital(self, symbol, year):
        currentAssets, currentLiabilities = self.db.Select(['total_current_assets',\
                                        'total_current_liabilities'],['STOCKFINANCIALS'],\
                                        ['symbol = \'%s\'' % symbol,'date = \'%s\'' % year])
        return float(currentAssets - currentLiabilities)

    def getAllSymbols(self):
        if not self.stocktable:
            self.stocktable = self.db.SelectAll(['symbol'], ['STOCKTABLE'])
        return self.stocktable
    
    def getAllDates(self):
        if not self.datetable:
            self.datetable = self.db.SelectAll(['date'], ['DATETABLE'])
            self.datetable.sort()
        return self.datetable
    

def updateDateTable():
    db = Database.SQLDatabase('austinwiltshire', 'root', 'password', 'stockinfo')
    massdates = db.SelectAll(['date'],['stockprices'])
    unique = list(set(massdates))
    unique.sort()
    for date in unique:
        db.Replace('datetable',{'date':date})
    db.commit()