"""

This lab is dedicated to simply pulling data out of the mysql database.

"""

#DONE
#first, get sqlalchemy
#first connect to the database

#DOING
#get free cash flows

#TODO


from bloomberg import SESSION as BB
from financials import CashFlowStatement as CFS
from basics import HistoricalPrices as Prices
from financials import BalanceSheet as BS
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, aliased, join
import datetime
import itertools
import table
import FinancialDate
from named_tuple import namedtuple

#min for cashflows is 2004,12,26
#max is 2009, 1, 31

#we need to pair up cash flow growth of:
# 2006 (2006 - 2005 / 2005) with price growth of 2007 (2007 - 2006 / 2006)
# 2007 with 2008
# 2008 with 2009

##YEARS_TO_CHECK = [2005, 2006, 2007, 2008, 2009]



#the cash flow growth should be paired up with the price growth of 2007, and so
#on

#TODO: haven't gathered dividends! aren't properly figuring out price growth!
#TODO: and price growth ain't growth! you want market cap growth! number of shares could change...

def closest_date(date, dates):
    """ Given a date and list of other dates, returns the closest date in that list to the date passed in. """
    
    differences = [date - dt for dt in dates]
    index = differences.index(min(differences))
    return dates[index]

class Study(object):
    """ Gathering the data for the correlation of cash flow growth of year n
    with the price growth of year n+1. """
    
    def __init__(self):
    	self.years_to_check = [2005, 2006, 2007, 2008, 2009]
        self.cf_engine = None
        self.cf_sessionmaker = None
        self.cf_session = None
        
        self.p_engine = None
        self.p_sessionmaker = None
        self.p_session = None
        
        self.metadata = None

    def get_free_cash_flows(self, dbase, cfs):
        """ Returns results of a query to get free cash flows from db's
        cfs table (assumes db is a database and cfs is the cash flow 
        statement table) """
        
        free_cash_flow = ((cfs.CashFromOperatingActivities - 
                           cfs.CapitalExpenditures)
                          .label("FreeCashFlow"))
        
        return\
        (dbase.query(cfs.Symbol, #get symbol, date and free cash flow
                     cfs.Date,
                     free_cash_flow)
              .filter(cfs.CashFromOperatingActivities!=None) #where cash from
                                                             #ops is defined 
              .filter(cfs.CapitalExpenditures!=None) #where capex is defined
              .order_by(cfs.Symbol) #ordered by symbol
              .order_by(cfs.Date) #subordered by date
              .all())
        
    def get_free_cash_flow_growth(self, groups):
        """ Returns a dict keyed to symbol and with values of pairs where the
        first element is the date of reported growth (retrospective) and the
        second element is the growth itself """
        
        CashFlowGrowth = namedtuple("CashFlowGrowth", "date growth")
        
        grouped_growths = {}
        for key, values in groups.iteritems():
            
            base_free_cash_flows = [value.FreeCashFlow for value in values[1:]]
            base_dates = [value.Date for value in values[1:]]
            retrospective_free_cash_flows = [value.FreeCashFlow for value in values[:-1]]
            
            growths = [growth(base, retrospective) 
                       for base in base_free_cash_flows
                       for retrospective in retrospective_free_cash_flows]
            
            grouped_growths[key] =  [CashFlowGrowth(date=date, growth=growth)
                                     for date in base_dates
                                     for growth in growths]
        
        return grouped_growths
        
        
    def run(self):
        """ Runs the study """
        
        
        free_cash_flows = self.get_free_cash_flows(BB, CFS)         
        grouped_free_cash_flows = group_into_dict(free_cash_flows,
                                                  lambda x: x.Symbol)
        
        #assert: dates are in order earliest to latest
        assert all(in_order(values) 
                   for values in grouped_free_cash_flows.itervalues())
        
        #put in order according to date, earliest date first, calculate retrospective growth - growth for 2005 is growth *since* 2004 to 2005.
        free_cash_flow_growths = \
            self.get_free_cash_flow_growth(grouped_free_cash_flows)      	
            
        #pseudocode
        #total_value_growths = \
        #   self.get_total_value_growth(BB, CFS)
        # total value = dividends for a year + growth in market cap
        # those two things can be found using functions below
        	
        #DONE: (but you should review)
        #made a capital gains function work in way X, then a dividends function work in way Y.  I'm not sure how cap gains works any more
        #since i haven't looked at it.  however, dividends works in a better way through glueing functions together, which in turn finally
        #just are held in an object that represents the query.
        #TODO:
        #you can either drive the algorithm forward, or refactor some things since i think hiding the query inside an object is probably
        #the best thing ot do.  you can re-apply this pattern to each query such that the query itself is nice and neat, but you get
        #OO'ish wrapper around it so i don't have to crane my head so much.
        #if you want to drive the algorithm forward more, basically you need to add capital gains and dividends per share together to get
        #total value.  
        #this needs to be grouped by stock, and then by year.  it needs to be correlated such that the RETROSPECTIVE cash flow growth
        #is compared to the PROSPECTIVE total growth (dividends + capital gains)
        #also, could introduce objects along the same lines as dividends getter (where the pattern is the object just represents
        #controlled and sensible access to a query run in the __init__ function) for free cash flow growth, total gains, and then
        #an object that just creates one of each and that becomes your 'study'
        
        
        #then group the findings by symbol, iterate for each symbol and you'll get dividends per share on that symbol by passing in 
        #the query findings for that symbol.  Assumes a named tuple format.
        
                    
        #you've made a capital gains function.  holy crap next time you do one of these labs you have to test things interactively as you build 
        #them.  try downloading ipython since it's more difficult to do things in the normal shell and keep things reloaded in ipython and well
        #factored in the lab.
        #now you neeed to make a dividends function that takes in dates and gives me the dividends paid out that year / number of shares out.  
        #we'll add that to the overall capital gains to get a total return.  suggest putting dividends in a seperate function, then finally putting
        #both called from yet another function that returns total return.
        #also suggest for next lab testing the hell out of things both interactively, debugging, and assertions.  i dont know how i got so lazy!
        #also suggest keeping the next lab pylint clean from the begining.
        #also suggest stripping this lab for refactoring parts like the capital gains and dividends.  stop cutting and pasting you asshole.  move it 
        #out into a common file inside stock lab.
        
#            return  psession.query(alias2.Symbol,
#                           alias2.Date, 1.0 + ((alias2.Close-alias1.Close)/alias1.Close)) \
#                    .select_from(join(alias1, alias2, alias1.Symbol==alias2.Symbol)) \
#                    .filter(alias1.Date==first_day_base) \
#                    .filter(alias2.Date==first_day_next).all()

def total_value(symbol, begin_date, end_date):
    """
    Returns the overall increase in value for symbol from date to date.
    """
    
    average_dividends_date = begin_date + ((begin_date - end_date) / 2)
    
    
    dividends = ALL_DIVIDENDS.dividends_per_share(symbol,
                                                  average_dividends_date)
    
    market_cap = 
     

def in_order(lst, key_func=lambda x:x): 
    """ Predicate returns true if the lst is in order """
    return sorted(lst, key=key_func) == lst 

def first_trading_day_after(date_):
    """ Returns the first trading day after the date given.  If the date given is a valid trading day, returns the date given. """
    #TODO: move this to financial date
    return FinancialDate.NthTradingDayAfter(date_, 0)


def value_for_year(date, all_values, date_func, value_func):
    """
    Given a list of values, returns the value most appropriate for the passed in date.  Requires a date_func that gets the date for
    any particular value, and a value_func that gets the value for any particular value.
    """
    
    as_dict = dict([(date_func(value), value_func(value)) for value in all_values])
    
    appropriate_date = closest_date(date, [date_func(value) for value in all_values])
    
    return as_dict[appropriate_date]

def dividends_for_year(date, all_dividends):
    """
    Given a list of all the dividends for a stock, returns the dividends most appropriate for a given date. 
    """
    
    return value_for_year(date, all_dividends, lambda val: val.Date, lambda val: val.TotalCashDividendsPaid)


def shares_out_for_year(date, all_shares_out):
    """
    Given a list of all the shares out for a stock, returns the shares outstanding most appropriate for the given date.
    """
    
    return value_for_year(date, all_shares_out, lambda val: val.Date, lambda val: val.TotalCommonSharesOutstanding)

def dividends_per_share(date, dividends_for_year, shares_out_for_year):
    """
    Given a function that returns the dividends for a year, and given a function that returns the number of shares outstanding for a year,
    and given a year, returns the dividends per share for that year.
    """
    
    return dividends_for_year(date) / shares_out_for_year(date)

class dividends_getter(object):
    
    def __init__(self):
        all_shares_out = \
                (BB.query(BS.Symbol, #get symbol, date and shares out
                          BS.Date,
                          BS.TotalCommonSharesOutstanding)
                   .order_by(BS.Symbol) #ordered by symbol
                   .order_by(BS.Date) #subordered by date
                   .all())
        self.all_shares_out = group_into_dict(all_shares_out, lambda x: x.Symbol)

        all_dividends = \
            (BB.query(CFS.Symbol,
                      CFS.Date,
                      CFS.TotalCashDividendsPaid)
               .order_by(CFS.Symbol)
               .order_by(CFS.Date)
               .all())
        self.all_dividends = group_into_dict(all_dividends, lambda x: x.Symbol)
            
    def dividends_per_share(self, symbol, date):
        div_per_year_func = lambda d: dividends_for_year(d, self.all_dividends[symbol])
        shares_out_func = lambda d: shares_out_for_year(d, self.all_shares_out[symbol])
        
        return dividends_per_share(date, div_per_year_func, shares_out_func)

ALL_DIVIDENDS = dividends_getter()




def capital_gains(symbol, dates):
    """ Returns the capital_gains for a stock for the given dates in the form of a dictionary indexed by closest available trading day
    to each date in dates.  Capital gains is calculated by multiplying the stocks closing price on that day by total common shares outstanding
    (or an approximation thereof) of the stock on that day.  This calculation takes into account stock splits, buybacks and the like. """
    
    #REFACTOR:
    #have a new idea.  this whole thing would be a lot cleaner if i could just get some functions out of here
    #i need a function 'price_on_date' that takes in a date and returns a closing price
    #and i need a function that is 'shares_out_on_date' that takes in a date and returns the number of shares outstanding
    #then i can make this function simply take in a date and those two functions and it gives me back the market cap
    
    #both of those functions could be ripped out from the below and simply be little more than accesses to dictionaries. 
    #the price_on_date function would need to have a dict full of all prices both today and in a year i will look for market caps on
    #and then the shares out one will just be access to the balance sheet dictionary combined with the 'find nearest' functionality below
    
    #so how at the outside do i still do my query of looking for dates that only have pairs?
    #probably similar to the way i look below but i can at least pull out the procedure a bit.  maybe something will occur to me once things
    #are more pulled apart.
    
    #NOTE: finds PROSPECTIVE capital gains, so for date x, finds capital gains you would have made from date x till a year from then.
    #might way to generalize this to take a timedelta parameter?
       
    one_year = datetime.timedelta(365)
    
    #get the trading dates for dates (they aren't necessarily valid trading days)
    trading_dates = [first_trading_day_after(dt) for dt in dates]
    
    #need to also get the prices for a year after
    year_later_trading_days = [first_trading_day_after(dt + one_year) 
                               for dt in trading_dates]
    
    next_year_backwards = dict([(key, value) for key in year_later_trading_days
                                             for value in trading_dates])
    
    
    #get prices for those dates   
    begin_prices = (BB.query(Prices.Date,
                             Prices.Close)
                      .filter(Prices.Symbol == symbol)
                      .filter(Prices.Date.in_(trading_dates))
                      #.filter(Prices.Date + one_year != None) don't know if this would work
                      .order_by(Prices.Date)
                      .all())
    
    end_prices = (BB.query(Prices.Date,
                           Prices.Close)
                      .filter(Prices.Symbol == symbol)
                      .filter(Prices.Date.in_(year_later_trading_days))
                      .order_by(Prices.Date)
                      .all())
    
    #get the dates i didn't find
    end_dates_not_found = set(year_later_trading_dates) - set([dt.Date for dt in end_prices])
    
    #which renders their beginings invalid
    invalid_begin_dates = [next_year_backwards[dt] for dt in list(end_dates_not_found)]
    
    #sorted leaves them sorted by date, earliest first
    valid_begin = sorted([(dt.Date, dt.Close) for dt in begin_prices if dt.Date not in invalid_begin_dates])
    end_prices = sorted([(dt.Date, dt.Close) for dt in end_prices])
    
    #assert that all the begins are exactly (or within two days at most of) one year apart
    assert all([((end - begin) - one_year <= 2)
                for end in end_prices
                for begin in valid_begin])
    
    assert len(valid_begin) == len(end_prices)
    
    #now we need to get the available balance sheet dates and shares out 
    #TODO: this would be more accurate if we used quarterly information
    shares_outs = (BB.query(BS.Date,
                            BS.TotalCommonSharesOutstanding)
                     .filter(BS.Symbol==symbol)
                     .order_by(BS.Date)
                     .all())
    
    #organized by date
    shares_outs = dict([(shares_out.Date, shares_out.TotalCommonSharesOutstanding) for shares_out in shares_out])
    bs_dates = shares_outs.keys()
    
    def market_cap(price, date, shares_out):
        
        closest_bs_date = closest_date(date, shares_out.keys())
        
        return price * shares_out[closest_bs_date]
         
    begin_market_caps = [(dt, market_cap(close, dt, shares_outs)) for dt, close in valid_begin]
    end_market_caps = [(dt, market_cap(close, dt, shares_outs)) for dt, close in end_prices]
    
    def growth(begin, end):
        return (begin - end) / begin
    
    return dict([(dt_1, growth(mkcp_1, mkcp_2)) for dt_1, mkcp_1 in begin_market_caps
                                                for dt_2, mkcp_2 in end_market_caps])
        
def group_into_dict(lst, func):
    """ Groups values in list according key found in func, and returns the 
    result as a dictionary. """
    
    groups = itertools.groupby(lst, func)
    return dict((key, list(values)) for key, values in groups)
    
    

#first we grab names, dates, cash from operating activities and capital expenditures from the database.
#they're grouped by symbol and ordered by date
results = session.query(symbol, date, cash_from_ops, capex).order_by(symbol).order_by(date)

#we organize them by symbol
results = itertools.groupby(results, lambda x: x._Symbol)

#we build our groups into dictionaries
results = dict((key, list(values)) for key, values in results)

#we remove all the results that provide less than 4 years of information
#this works out to 3 years of differences for each symbol
results = dict((key, values) for key, values in results.iteritems() if len(values) > 4 and values[0]._Date.month > 11)

#dates in each group are stored in order from oldest to newest.
def assert_dates_in_order(values):
    difference_values = itertools.izip(values[:-1], values[1:])
    for old, new in difference_values:
        assert old < new
        
for key, value in results.iteritems():
    assert_dates_in_order(value)
    
    
    #CLEAR ALL THE ONES WITH NONES IN CAPEX OR NET INCOME
#print len(results)

#now i need to go through each one and calulate the free cash flow for each one


def has_cash_flows(values):
    for _, _, operating, capex_ in values:
        if not operating or not capex_:
            return False
    return True

def free_cash_flows(values):
    new_values = []
    for _, date_, operating, capex_ in values:
        new_values.append((date_.year, operating-capex_))
    return new_values

results = dict((key, free_cash_flows(values)) for key, values in results.iteritems() if has_cash_flows(values))    
print len(results)

#just making sure here all our cash flows are valid
assert all((cash_flows != None) for _, values in results.iteritems() for _, cash_flows in values)

class Result(object):
    def __init__(self, a_symbol, cash_flow_growth):
        self.symbol = a_symbol
        self.cash_flow_growth = cash_flow_growth
        self.price_growth = {}
        
    def pair(self):
        
        the_results = {}
        couldntfind = []
        
        for a_date, cfgrowth in self.cash_flow_growth.iteritems():
            if a_date+1 in self.price_growth.keys():
                the_results[date] = (date, cfgrowth, a_date+1, self.price_growth[a_date+1])
            else:
                couldntfind.append(a_date+1)
        
        return FinalResult(self.symbol, the_results, couldntfind)
        
        
    def __str__(self):
        return "Symbol %s\n Cash Flow Growth: \n%s\n Price Growth: \n%s\n" % (self.symbol,
                                                                              "\n".join(str(date) + " " + str(value) for date, value 
                                                                                                               in self.cash_flow_growth.iteritems()),
                                                                              "\n".join(str(date) + " " + str(value) for date, value
                                                                                                               in self.price_growth.iteritems()))

class FinalResult(object):
    def __init__(self, the_symbol, the_results, couldntfind):
        self.symbol = the_symbol
        self.results = the_results
        self.couldntfind = couldntfind
        
    def __str__(self):
        return_ = ""
        for dictkey, values in self.results.iteritems():
            return_ += (str(dictkey) + " " + str(values) + "\n")
            
        return "Symbol " + self.symbol + "Values \n" + return_ + " and couldn't find \n" + str(self.couldntfind)
    


#now need to find cash flow growths    
results = dict((key, Result(key, dict([(date2[0], (date2[1]-date1[1]) / date1[1]) for date1, date2 in itertools.izip(value[1:], value[:-1])]))) for key, value in results.iteritems())


#for result in results.itervalues():
#    print result
#now i need to add price information to all of this...

#need to get the first trading day of the year,,,

def first_trading_day(for_year):
    dt = datetime.datetime(for_year, 1, 1)
    
    actual_first_trading_day = FinancialDate.NthTradingDayAfter(dt, 0)
    
    return datetime.date(actual_first_trading_day.year, actual_first_trading_day.month, actual_first_trading_day.day)

def price_growth(for_year):
    first_day_base = first_trading_day(for_year-1)
    first_day_next = first_trading_day(for_year)
    
    alias1 = aliased(table.Prices)
    alias2 = aliased(table.Prices)
    
    return  psession.query(alias2.Symbol,
                           alias2.Date, 1.0 + ((alias2.Close-alias1.Close)/alias1.Close)) \
                    .select_from(join(alias1, alias2, alias1.Symbol==alias2.Symbol)) \
                    .filter(alias1.Date==first_day_base) \
                    .filter(alias2.Date==first_day_next).all()
        
     
for year in YEARS_TO_CHECK:
    print "Checking year...", year
    price_growth_for_year = price_growth(year)
    
    for symbol, dates in itertools.groupby(price_growth_for_year, lambda x: x.Symbol):
        if symbol in results.keys():
            results[symbol].price_growth.update(dict([(date.year, growth) for _, date, growth in dates]))


import pickle

f = open("lab1output.dat", "w")

results = dict([(key, value.pair()) for key, value in results.iteritems()])

pickle.dump(results, f)

for result in results.itervalues():
    print result.pair()
            
            
#ok i imagine the new price growth query looking something like...
# below gets market cap per year (but excludes times when a company releases stuff on a non trading day, if that ever happens.  might be an interesting
#inspection to see
# session.query(bs.Symbol, bs.Date, bs.StockOutstanding * p.Close).select_from(join(bs, p, bs.Symbol == p.Symbol & bs.Date == p.Date))
#can't think of a way to calculate growth in the database right nwo but the above should be good enough
#  below gets dividends per year
# session.query(bs.Symbol, bs.Date, bs.DividendsPaid / bs.StockOutstanding)
   

#need to match up the results with the cash flows...

#alias1 = aliased(table.Prices)
#alias2 = aliased(table.Prices)
#
#for symbol, date, growth in psession.query(alias2.Symbol, 
#                                           alias2.Date, 1.0 + ((alias2.Close-alias1.Close)/alias1.Close)) \
#                                    .select_from(join(alias1, alias2, alias1.Symbol==alias2.Symbol)) \
#                                    .filter(alias1.Date==datetime.date(2001,4,20)) \
#                                    .filter(alias2.Date==datetime.date(2002,4,22))[:10]:
#    print symbol, date, growth
