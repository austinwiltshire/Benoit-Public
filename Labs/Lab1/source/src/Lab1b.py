"""
I can't understand why I wrote lab1 the way I did.

To reform the purpose of this study: Does *retrospective* growth in free cash flow predict *prospective* total return,
where total return is defined as dividends + capital gains.

We will take two annual, consecutive cash flow statements which should be approximately a year apart.
The oldest one's date will hereafter be known as the 'past cash flow statement' date.  The most recent will hereafter
be known as the 'present cash flow statement' date.  Growth in free cash flow will be derived between them as a 
percent.

This will be considered our retrospective free cash flow growth.

From the present cash flow date, we will find the nearest valid future trading date, hereafter referred to as the 
'present trading date' and find the nearest valid future trading date in precisely one year's time, hereafter 
referred to as the 'future trading date'.

This is the time horizon for which we will calculate our total return.  To calculate dividends received over this time
period, we will take the total common shares outstanding (as found in the balance sheet) and dividends distributed
(found on the cash flow statement) on the balance sheet and cash flow statement from the respective sheets/statements
nearest to our trading dates (hereafter referred to as the present balance sheet and future balance sheet, and 
present cash flow statement and future cash flow statement).  Divideds per share for each date will be simply dividing
dividends distributed by total common shares outstanding.  Dividends per share *over* the period will be the average
of these two values.

Next, we will calculate capital gains by finding the differences between the closing on the present trading date and 
the closing on the ending trading date, *adjusted* such that the present trading date's value is expressed in terms
of total common shares outstanding on the ending trading date.  The total common shares outstanding will be derived
from the closest available future annual balance sheet to the trading date.

thus capital_gains = (future_closing_price - adjusted_present_closing_price)
where
adjusted_present_closing_price = 
    (present_closing_price * (future_total_shares_outstanding / present_total_shares_outstanding))

Capital gains in this case means, roughly, how much we would have seen a stock's price rise had we bought it at the 
present trading date and sold it at the future trading date, *adjusting* for splits and buybacks.

After we find the prospective capital gains for a stock, we add it to its dividends per share, and then derive that
value, the total absolute return (expressed in dollars) into the total relative return (expressed as a percent) by
dividing it by the original, non-adjusted present_closing_price.

That will be considered our prospective total return.

Finally, we will group these values as pairs (retrospective free cash flow growth, prospective total return) and
use them as data points to search for correlations.
"""

#REFACTOR:
#add NextAnnualBalanceSheetIssueDate, PreviousAnnualBalanceSheetIssueDate, ... for CFS and IncS on price table
#that would make this WHOLE THING so much easier.


import datetime
import SnP500
from bloomberg import SESSION as DBCON
from financials import CashFlowStatement as CFS
from basics import HistoricalPrices as HPRICE
from financials import BalanceSheet as BS
from FinancialDate import NthTradingDayAfter

def closest_date_after(date, dates):
    """
    Given a date and list of other dates, returns the closest date in the list after the date passed in.
    """
    
    #precondition: date is a datetime.date
    #precondition: dates is a list of datetime.dates thats sorted
    
#    for index, date in enumerate(dates[:-1]):
#        if dates[index] < date and date > dates[index+1]:
#            return dates[index+1]
#    
#    return None

#    postcondition: if ret is a datetime.date then ret in dates and ret > date else ret is None

def closest_date(date, dates):
    """ Given a date and list of other dates, returns the closest date in that list to the date passed in. """
    
    differences = [date - dt for dt in dates]
    index = differences.index(min(differences))
    return dates[index]

def first_trading_day_after(date):
    """
    Returns the first valid trading day after date.
    
    spec'd 4/19/2010
    """
    
    #preconditions:
    type_check(date, datetime.date)
    
    #where ret is the first trading day after date
    
    #postconditions:
    type_check(ret, datetime.date)

ONE_YEAR = datetime.timedelta(365)

STRICT_CHECKING = True

def one_trading_year_later(date):
    """
    Returns the trading date approximately one year later.  Assumes date is a datetime.date, and ensures that
    return value is no more than 367 days newer than date.
    
    partially spec'd 4/15/10
    """
    #type_check(date, datetime.date)
    
    #ret = NthTradingDayAfter(date, 365)
    
    #assert ret - date < datetime.timedelta(2)

def sanity_check(sanity_passed, msg="Failed sanity check."):
    """
    Similar to an assert but only gives a warning if STRICT_CHECKING global
    variable is false.
    """
    
    global STRICT_CHECKING
    
    if STRICT_CHECKING:
        assert sanity_passed, msg
    elif not sanity_passed:
        print "Warning! Sanity check failed. " + msg       

def predicate(func):
    """
    A type checking decorator that ensures a check for a functions return value always takes place to ensure it's
    a boolean.
    """
    
    #preconditions:
    assert callable(func), \
        "Decorators only work on callable objects."
    
    def decorated_function(*args, **kwargs):
        """
        A newly decorated function that checks all output from func to ensure it's a boolean.
        """
        answer = func(*args, **kwargs)
        
        #postconditions:
        type_check(answer, bool)
        
        return answer
    
    return decorated_function


@predicate
def is_date_reasonable(date):
    """
    Helper predicate checks to ensure dates are in a reasonable range.
    """
    return datetime.date(1998, 1, 1) < date < datetime.date.today()

def type_check(obj, type_):
    """
    Runs a type checking assertion that object is an instance of type_
    """
    assert isinstance(obj, type_), \
        "Type Violation: %s must be of type %s" % (str(obj), str(type_))
    
    return True

#REFACTOR:
#add assertion to first_trading_day_after that the day found must be within 4 trading days after the day requested.

#FIXME: add 'n' to list of protected names on pylint
#FIXME: increase method name size to 40 on pylint

@predicate
def is_approximately_n_days_older(future, past, n, tolerance=datetime.timedelta(5)):
    """
    Predicate returns true if future is rougly n days more recent than past, where roughly is defined by tolernace.
    The default tolerance is five days.
    """
    
    #preconditions
    type_check(future, datetime.date)
    type_check(past, datetime.date)
    type_check(n, datetime.timedelta)
    type_check(tolerance, datetime.timedelta)
    
    assert future > past, "Assumes %s is more recent than %s" % (str(future), str(past))
    
    #doc
    #where answer is whether or not future is approximately n days older than past, within tolerance
    
    #design
    #return (future - past) < tolerance

class Database(object):
    """
    Encapsulates all database access, allowing prefetching of what I think I'll need.
    """
    
    def __init__(self):
        """
        spec'ed 4/14/2010
        further spec'ed 4/19/2010
        designed 4/19/2010
        """
        
        #doc:
        #where self._supported_symbols equals SnP500 list
        #where self._price_table is a query for symbols, dates and closing prices on all symbols
        #where self._bs_table is a query for symbol, date, shares outstanding
        #where self._cfs_table is a query for symbol, date, operating cash flow and capital expenditures and total
        #cash dividends paid
        
        #design:
        #the below should effectively precache anything I need later.
         
#        self._supported_symbols = SnP500.symbols
#                return\
        
        #REFACTOR: calculate free cash flow in DB, see lab 1.
#        cfs_table = (DBCON.query(CFS.Symbol, #get symbol, date and free cash flow
#                                 CFS.Date,
#                                 CFS.CashFromOperatingActvities,
#                                 CFS.CapitalExpenditures,
#                                 CFS.TotalCashDividendsPaid)
#                          .filter(CFS.CashFromOperatingActivities!=None) #where cash from ops is defined 
#                          .filter(CFS.CapitalExpenditures!=None) #where capex is defined
#                          .order_by(CFS.Symbol) #ordered by symbol
#                          .order_by(CFS.Date) #subordered by date
#                          .all())
#        self._cfs_table = group_into_dict(cfs_table, lambda x: x.Symbol)
#
#        bs_table = (DBCON.query(BS.Symbol,
#                                BS.Date,
#                                BS.TotalCommonSharesOutstanding)
#                         .filter(BS.TotalCommonSharesOutstanding!=None) #where total shares is defined
#                         .order_by(BS.Symbol)
#                         .order_by(BS.Date)
#                         .all())
#        self._bs_table = group_into_dict(bs_table, lambda x: x.Symbol)
#
#        price_table = {}
#        for symbol in self._symbols_supported:
#            dates_of_interest = [elem.Date for elem in itertools.chain(self._bs_table[symbol],
#                                                                       self._cfs_table[symbol])]
#            dates_of_interest.extend([one_trading_year_later(date) for date in dates_of_interest])
#            
#            price_table[symbol] = (DBCON.query(HPRICE.Symbol,
#                                               HPRICE.Date,
#                                               HPRICE.Close)
#                                        .filter(HPRICE.Date.in_(dates_of_interest))
#                                        .order_by(HPRICE.Symbol)
#                                        .order_by(HPRICE.Date)
#                                        .all())
#        self._price_table = price_table

            
        
        #invariant:
        type_check(self._price_table, dict)
        type_check(self._bs_table, dict)
        type_check(self._cfs_table, dict)
        
        assert all([type_check(price.Symbol, basestring) for price in self._price_table.values()]), \
            "Symbols should all be strings."
        assert all([type_check(price.Close, float) for price in self._price_table.values()]), \
            "Closing prices should all be floats."
        assert all([type_check(cfs.Symbol, basestring) for cfs in self._cfs_table.values()]), \
            "Cash flow statement symbols should be strings."
        assert all([type_check(cfs.Date, datetime.date) for cfs in self._cfs_table.values()]), \
            "Cash flow statement dates should be datetime.dates."
        assert all([type_check(cfs.CashFromOperatingActvities, float) or cfs.CashFromOperatingActvities is None 
                    for cfs in self._cfs_table.values()]), \
            "Cash flow statement operating cash flow should be a float or None."
        assert all([type_check(cfs.CapitalExpenditures, float) or cfs.CapitalExpenditures is None
                    for cfs in self._cfs_table.values()]), \
            "Cash flow statement capital expenditures should be a float or None."
        assert all([type_check(cfs.TotalCashDividendsPaid, float) or cfs.TotalCashDividendsPaid is None
                    for cfs in self._cfs_table.values()]), \
            "Cash flow statement total cash dividends paid should be a float or None."
        assert all([type_check(bs.Symbol, basestring) for bs in self._bs_table.values()]), \
            "Balance sheet symbols should be strings."
        assert all([type_check(bs.Date, datetime.date) for bs in self._bs_table.values()]), \
            "Balance sheet dates should be datetime.dates"
        assert all([type_check(bs.TotalCommonSharesOutstanding, float) for bs in self._bs_table.values()]), \
            "Balance sheet total common shares outstanding should be a float."
        sanity_check(all([len(symbol) <= 8 for symbol in self._supported_symbols]),
                     "All symbols are of reasonable length in official symbol table.")
        sanity_check(all([len(symbol) <= 8 for symbol in self._cfs_table.keys()]),
                     "All symbols are of reasonable length in cash flow statement.")
        sanity_check(all([len(symbol) <= 8 for symbol in self._price_table.keys()]),
                     "All symbols are of reasonable length in price table.")
        sanity_check(all([len(symbol) <= 8 for symbol in self._bs_table.keys()]),
                     "All symbols are of reasonable length in balance sheet.")
        sanity_check(all([price.Close >= 0.0 for price in self._price_table.values()]),
                     "All closing prices should be above $0.00 in price table.")
        sanity_check(all([bs.TotalCommonSharesOutstanding >= 0.0 for bs in self._bs_table.values()]),
                     "All total common shares outstanding are above 0 shares.")
        sanity_check(all([is_date_reasonable(price.Date) for price in self._price_table]),
                     "All dates in price table are past 1998 and before today.")
        sanity_check(all([is_date_reasonable(cfs.Date) for price in self._cfs_table]),
                     "All dates in price table are past 1998 and before today.")
        sanity_check(all([is_date_reasonable(bs.Date) for bs in self._bs_table]),
                     "All dates in price table are past 1998 and before today.")
        
        assert len(self._price_table.keys()) == len(self._bs_table.keys()) == len(self._cfs_table.keys()) != 0, \
            "All tables should be loaded and have all the keys." 
        assert (set(self._price_table.keys()) == set(self._bs_table.keys()) == set(self._cfs_table.keys()) == 
                self._supported_symbols), "All tables support the same symbols."
                
        sanity_check(len(self._price_table) != 0, "Price table should be fully loaded.")
        sanity_check(len(self._bs_table) != 0, "Balance Sheet table should be fully loaded.")
        sanity_check(len(self._cfs_table) != 0, "Cash Flow Statement table should be fully loaded.")
    
    def cfs_dates(self, symbol):
        """
        Returns a list of the dates of all annual cash flow statements the database supports for symbol
        
        spec'd 4/12/2010
        design 4/19/2010
        """
        
        #preconditions:
        type_check(symbol, basestring)
        assert self.has_symbol(symbol), \
            "Database supports the symbol being queried."
            
        #doc:
        #where ret is the issue dates of cash flow statements for symbol
        
        #design:
        #ret = [cfs.Date for cfs in self._cfs_table[symbol]]
            
        #postconditions:
        type_check(ret, list)
        assert all(type_check(element, datetime.date) for element in ret), \
            "List should be made up of dates." 
        assert all(self.has_cfs_for_date(symbol, date) for date in ret), \
            "All returned dates should be valid cfs dates."
        sanity_check(len(ret) < 10, "Shouldn't have more than 10 dates being returned in cfs_dates")
        sanity_check(all(is_date_reasonable(element) for element in ret),
                     "Dates shouldn't be unreasonable in cfs_dates")
        
    
    @property
    def supported_symbols(self):
        """
        Return a list of all the symbols this database supports querying.
        
        spec 4/12/2010
        design 4/12/2010
        ref 4/15/2010
        """
        
        #DOC:
        #where ret is the symbols the database supports
        
        #DESIGN:
        #ret = self._supported_symbols
        
        #REFACTOR:
        #move invariants into a method to be called
        
        #postconditions
        sanity_check(len(ret) < 600, "Should be less than 600 symbols the database supports.")
        type_check(ret, list)
        assert all(type_check(element, basestring) for element in ret), \
            "All elements of the return list should be strings."
        sanity_check(all(len(element) < 8 for element in ret),
                     "All strings in return list ought to be less than 8 characters.")
    
    @predicate
    def has_cfs_for_date(self, symbol, date):
        """
        Predicate returns true if there was a cash flow statement issues on date.
        
        designed 4/19/2010
        """
        
        #preconditions:
        type_check(symbol, basestring)
        type_check(date, datetime.date)
        
        self.has_symbol(symbol), \
            "Requires that we have this symbol, %s, in our database." % symbol
        
        #design:
        #ret = date in [cfs.Date for cfs in self._cfs_table[symbol]]
        
    def prior_cfs_for_date(self, symbol, date):
        """
        Returns the cfs issued approximately one year before the date passed in.
        
        Assumes cfs exists for date, as well as prior date and symbol.
        
        spec'ed 4/19/2010
        """
        
        #preconditions:
        #assert  self.has_cfs_for_date(symbol, date)
        #assert has_prior_cfs_for_date(symbol, date)
        #assert has_symbol(symbol)
        
        #doc:
        #prior_cfs = prior cash flow statement
        # should support Symbol and Date properties
        
        #design:
        #cfs_dates = sorted([cfs.Date for cfs in self._cfs_table[symbol]])
        #current_date_index = cfs_dates.index(date)
        #assert current_date_index != 0, "Double check that there is actually a previous cash flow statement available."
        #previous_date = cfs_dates[current_date_index - 1]             
        #prior_cfs = self._cfs_table[symbol][previous_date]
        
        #postcondition
        assert prior_cfs.Symbol == symbol, "Ensures Cash Flow statements are from the same stock." 
        assert is_approximately_n_days_older(date, prior_cfs.Date, n=ONE_YEAR), "Ensures cash flow statements are" \
            " approximately one year apart."
        assert date < prior_cfs.Date, "Ensures date is more recent than the prior cfs's issue date."
        
               
    @predicate
    def has_prior_cfs_for_date(self, symbol, date):
        """
        Predicate returns true if there was a cash flow statement issued prior to this one, approximately a year
        earlier.  Assumes a cfs exists for date.
        
        designed 4/19/2010
        """
        
        #preconditions
        type_check(symbol, basestring)
        type_check(date, datetime.date)
        
        assert self.has_cfs_for_date(symbol, date), \
            "Require that we have a cash flow statement issued on %s for %s" % (str(date), symbol)
        assert self.has_symbol(symbol), \
            "Require that we be tracking %s in our database of symbols." % (symbol)
            
        #design:
        #dates = sorted([cfs.Date for cfs in self._cfs_table[symbol]]) #we're assuming in ascending order where
        #more recent is later in the list
        #ret = dates.index(date) != 0
        
        
        
        
    @predicate
    def cfs_has_ocf(self, symbol, date):
        """
        Predicate returns true if the cash flow statement for symbol on date has an operating cash flow value not
        null (0.0 is ok).
        Assumes there is a cash flow statement for symbol on date.
        
        designed 4/19/2010
        """
        
        #REFACTOR:
        #given that we can prove this is always true given the construction of the original query, consier removing
        #this check
        
        #precondition
        assert self.has_symbol(symbol), \
            "Require that we're tracking %s in our symbol database." % symbol
        assert self.has_cfs_for_date(symbol, date), \
            "Require that we have cash flow statements for %s on %s" % (symbol, str(date))
            
        #design:
        #ret = self._cfs_table[symbol].CashFromOperatingActivities != None
    
    @predicate
    def cfs_has_capex(self, symbol, date):
        """
        Predicate returns true if the cash flow statement for this symbol on date has capital expenditures reported,
        or not null.  0.0 is ok.
        Assumes there is a cash flow statement for symbol on date.
        
        designed 4/19/2010
        """
        
        #preconditions
        assert self.has_symbol(symbol), \
            "Require that we're tracking %s in our symbol database." % symbol
        assert self.has_cfs_for_date(symbol, date), \
            "Require that we have a valid cash flow statement for %s on %s." % (symbol, str(date))
            
        #design:
        #ret = self._cfs_table[symbol].CapitalExpenditures is not None
        
    @predicate
    def prior_cfs_has_ocf(self, symbol, date):
        """
        Predicate returns true if the annual cash flow statement issued roughly one year prior to the date passed in
        has operating cash flow supported.
        Assumes that the date passed in is a valid cash flow statement report date for symbol, and that a cash flow
        statement was issued prior to the date passed in.
        """
        
        #preconditions
        type_check(symbol, basestring)
        type_check(date, datetime.datetime)
        
        assert self.has_symbol(symbol), \
            "Require that we're tracking %s in our symbol database." % symbol
        assert self.has_cfs_for_date(symbol, date), \
            "Require that we have the cash flow statement for %s on %s" % (symbol, str(date))
        assert self.has_prior_cfs_for_date(symbol, date), \
            "Require that we have a cash flow statement issued prior to the one issued on %s for %s" % \
            (str(date), symbol)
        
        #doc
        #prior_cfs = prior cash flow statement
        # should support Symbol and Date properties
        
        #design
        #prior_cfs = prior_cfs_for_date(self, symbol, date)
        #ret = prior_cfs.CashFromOperatingActivities is not None
        
        #postcondition
        assert prior_cfs.Symbol == symbol, "Ensures Cash Flow statements are from the same stock." 
        assert is_approximately_n_days_older(date, prior_cfs.Date, n=ONE_YEAR), "Ensures cash flow statements are" \
            " approximately one year apart."
        assert date < prior_cfs.Date, "Ensures date is more recent than the prior cfs's issue date."

    @predicate
    def prior_cfs_has_capex(self, symbol, date):
        """
        Predicate returns true if the cash flow statement issued roughly one year before date has capital expenditures
        reported, or is not null.  0.0 is valid.
        Assumes that there is a cash flow statement issued for date, and that one exists roughly one year prior to date
        as well. 
        """
        
        #preconditions
        type_check(symbol, basestring)
        type_check(date, datetime.date)
        assert self.has_cfs_for_date(symbol, date), \
            "Require that we have a cash flow statement issued for %s on %s" % (symbol, str(date))
        assert self.has_prior_cfs_for_date(symbol, date), \
            "Require that we have a cash flow statement issued roughly one year before %s for %s" % (str(date), symbol)
        
        #prior_cfs = prior cash flow statement
        # should support Symbol and Date properties
        
        #design
        #prior_cfs = prior_cfs_for_date(self, symbol, date)
        #ret = prior_cfs.CapitalExpenditures is not None
        
        #postcondition
        assert prior_cfs.Symbol == symbol, "Ensures Cash Flow statements are from the same stock." 
        assert is_approximately_n_days_older(date, prior_cfs.Date, n=ONE_YEAR), "Ensures cash flow statements are" \
            " approximately one year apart."
        assert date < prior_cfs.Date, "Ensures date is more recent than the prior cfs's issue date."
    
    @predicate
    def is_trading_date(self, symbol, date):
        """
        Predicate returns true if date has trading information available for symbol on date.
        Assumes symbol is a tracked symbol.
        
        designed 4/19/2010
        """
        
        #preconditions:
        type_check(symbol, basestring)
        type_check(date, datetime.date)
        
        assert self.has_symbol(symbol), "Requires that the database tracks %s" % symbol
        
        #design:
        #ret = date in [price.Date for price in self._price_table[symbol]]
    
    @predicate    
    def bs_reported_within_a_year_after(self, symbol, date):
        """
        Predicate returns true if symbol has a balance sheet that was issued after date, but no more than
        a year (367 days) later.
        Assumes we track symbol, and that date is a valid trading date.
        """
        
        #preconditions:
        type_check(symbol, basestring)
        type_check(date, datetime.date)
        
        assert self.has_symbol(symbol)
        assert self.is_trading_date(symbol, date)
        
        #doc
        #we take in a trading date, we need to find the first BS date AFTER that trading date.
       
        #design
        #bs_dates = sorted([bs.Date for bs in self._bs_table[symbol]])
        #bs_date = closest_date_after(date, bs_dates)
        #return bs_date is not None and bs_date - date < datetime.timedelta(367)
        
    @predicate   
    def cfs_reported_within_a_year_after(self, symbol, date):
        """
        Predicate returns true if symbol has a cash flow statement that was issued after date, but no more than
        a year later.
        Assumes we track symbol and that date is a valid trading date.
        """
        
        #preconditions:
        type_check(symbol, basestring)
        type_check(date, datetime.date)
        
        #cfs_dates = sorted([cfs.Date for cfs in self._cfs_table[symbol]])
        #cfs_date = closest_date_after(date, cfs_dates)
        #return cfs_date is not None and cfs_date - date < datetime.timedelta(367)
        
        assert self.has_symbol(symbol)
        assert self.is_trading_date(symbol, date)
        
    @predicate
    def has_symbol(self, symbol):
        """
        Predicate returns true if we have the following information on this symbol:
            - Some trading information available
            - At least one balance sheet, cash flow statement, and income statement available for this symbol.
            
            designed 4/19/2010
        """
        
        #preconditions
        type_check(symbol, basestring)
        sanity_check(len(symbol) <= 8, "Symbol length should be reasonable")
        
        #ret = symbol in self._supported_symbols
        
        #postconditions
        assert symbol in self._supported_symbols if ret else True, \
            "Returning true should indicate the symbol is in our supported symbols."
            
    def fcf_for_date(self, symbol, today):
        """
        Returns the free cash flow, as defined by operating cash flow - capex, for today.
        
        Assumes that today is a valid cash flow statement date, that symbol is supported, and that capex and operating
        cash flow for date is well defined.
        """
        pass
        
    def prior_fcf_for_date(self, symbol, today):
        """
        Returns the free cash flow, as defined by operating cash flow - capex, for the cash flow statement issued prior
        to today.  Assumes today is a valid cash flow statement date, and that one exists roughly a year prior to this
        one.
        
        Assumes that symbol is supported and that capex and operating cash flow are well defined on the cash flow
        statement issued prior to this one.
        """
        pass

DATABASE = Database()

def retrospective_cash_flow_growth(symbol, today):
    """
    Returns the cash flow growth between roughly a year ago and today for symbol.
    Assumes today is the issue date of a cash flow statement, also assumes that an annual cash flow statement is 
    available from roughly a year ago.
    """
    
    #preconditions
    type_check(symbol, basestring)
    type_check(today, datetime.date)
    
    assert DATABASE.has_symbol(symbol), \
        "Requires that the database have %s available." % symbol
    assert DATABASE.has_cfs_for_date(symbol, today), \
        "Requires we have a cash flow statement available for %s " % str(today)
    assert DATABASE.has_prior_cfs_for_date(symbol, today), \
        "Requires we have a cash flow statement prior to %s" % str(today)
    assert DATABASE.cfs_has_ocf(symbol, today), \
        "Requires that the Cash flow statement has reported operating cash flow for %s on %s" % (symbol, str(today))
    assert DATABASE.cfs_has_capex(symbol, today), \
        "Requires that the cash flow statement has reported capital capital expenditures for %s on %s" % \
        (symbol, str(today))
    assert DATABASE.prior_cfs_has_ocf(symbol, today), \
        "Requires that the cfs issued one year prior to %s report operating cash flow for %s" % (str(today), symbol)
    assert DATABASE.prior_cfs_has_capex(symbol, today), \
        "Requires that the cfs issued one year prior to %s report capital expenditures for %s" % (str(today), symbol)
      
    #REFACTOR: change 'today' to 'present_cash_flow_statement' and 'prior_cfs' to 'past_cash_flow_statement'  
    #prior_cfs_free_cash_flow = prior year's cash flow statement's free cash flow as calculated by operating cash
    #flow - capital expenditures    
    
    #process invariant
    assert prior_cfs_free_cash_flow != 0.0, \
        "Previous year's free cash flow is $0.0, thus growth is impossible to calculate"
        
    #where answer is the retrospective cash flow growth for symbol on today
    
    #design
    #today_fcf = self.fcf_for_date(symbol, today)
    #prior_fcf = self.prior_fcf_for_date(symbol, today)
    #ret = (today_fcf - prior_fcf) / prior_fcf
    
    #postconditions:
    type_check(answer, float)
    
def prospective_total_return(symbol, today):
    """
    Returns the total return of a symbol if bought today and held for roughly one year.  
    Assumes today is a valid trading day, and that a valid trading day exists roughly one year from now.
    Assumes that a balance sheet, used for total shares outstanding is issued prior to today, as well as prior to
    the future trading date.
    Assumes that a cash flow statement, used for dividends distributed, has been issued prior to today, as well as
    prior to one year from now.
    Assumes closing price is available on present_trading_date
    Assumes closing price is available on future_trading_date   
    
    thus capital_gains = (future_closing_price - adjusted_present_closing_price)
    where
    adjusted_present_closing_price = 
    (present_closing_price * (future_total_shares_outstanding / present_total_shares_outstanding))
    
    To calculate dividends received over this time
    period, we will take the total common shares outstanding (as found in the balance sheet) and dividends distributed
    (found on the cash flow statement) on the balance sheet and cash flow statement from the respective 
    sheets/statements
    nearest to our trading dates (hereafter referred to as the present balance sheet and future balance sheet, and 
    present cash flow statement and future cash flow statement).  Divideds per share for each date will be simply 
    dividing
    dividends distributed by total common shares outstanding.  Dividends per share *over* the period will be the 
    average
    of these two values.
        
    """
    
    #REFACTOR: change 'today' to say 'present_trading_date'
    
    #preconditions
    type_check(symbol, basestring)
    type_check(today, datetime.date)
    
    assert DATABASE.has_symbol(symbol), \
        "Requires %s be tracked in database." % symbol
    assert DATABASE.is_trading_date(symbol, today), \
        "Requires %s must be a valid trading day for %s" % (str(today), symbol)
    assert DATABASE.bs_reported_within_a_year_after(symbol, today), \
        "Requires that %s must have a balance sheet reported after %s" % (symbol, str(today))
    assert DATABASE.cfs_reported_within_a_year_after(symbol, today), \
        "Requires that %s must have a cash flow statement reported after %s" % (symbol, str(today))
        
    #where future_trading_date = first_trading_day_after(today + ONE_YEAR)
    #use one_trading_year_later (and refactor the name)
    
    
    #design:
    #prospective_total_return = prospective_capital_growth(symbol, today) + prospective_div_yield(symbol, today)
    
    assert DATABASE.is_trading_date(symbol, future_trading_date), \
        "Requires %s must be a valid trading day for %s" % (str(today), symbol)
    assert DATABASE.bs_reported_within_a_year_after(symbol, future_trading_date), \
        "Requires %s must have a balance sheet reported after %s" % (symbol, str(future_trading_date))
    assert DATABASE.cfs_reported_within_a_year_after(symbol, future_trading_date), \
        "Requires %s must have a cash flow statement reported after %s" % (symbol, str(future_trading_date))
        
    #process invariant
    #where present_bs.TotalCommonSharesOutstanding = present balance sheet's total common shares outstanding
    #and present_bs.Date
    assert present_bs.TotalCommonSharesOutstanding != 0.0, \
        "Total common shares outstanding for %s on %s must not be 0.0" % (symbol, str(present_bs.Date))
        
    #where answer is prospective total return starting at present_trading_date
    
    #postconditions:
    type_check(answer, float)

def prospective_capital_growth(symbol, today):
    """
    Returns the prospective capital gains growth for symbol starting at today until approximately one year from now.
    
    Assumes that trading dates exist for today and a date approximately one year from now, and that a balance sheet
    exists prior to today and prior to approximately one year from now, both of which must support 
    total common shares outstanding.
    
    Capital growth is calculated as the total change in market cap, which is closing price on date * total
    common shares outstanding for date.
    """
    pass

def dividend_yield_for(symbol, today):
    """
    Returns the dividend yield that would occur over a year for symbol if held from today for approximately a year.
    
    Assumes that trading dates exist for today and approximately a year from now, as well as cash flow statements
    that describe total dividends issued.  Finally, shares outstanding from the balance sheet must also be available.
    
    Dividend yield is calculated as dividends per share / closing price.  Dividends per share is calculated as
    total dividends issued / total common shares outstanding.
    """
    pass


def pair_rfcfg_and_ptr_for(symbol, present_cfs_date):
    """
    Return a pair - the retrospective free cash flow growth and prospective total return, for symbol, given 
    a present cash flow statement date.
    Assumes that retrospective free cash flow can be calculated using present_cfs_date as a base date.
    Assumes that prospective total return can be calculated using the nearest future trading date from 
    present_cfs_statement as a base date.
    
    designed 4/12
    further specified 4/12
    """
    
    #preconditions:
    type_check(symbol, basestring)
    type_check(present_cfs_date, datetime.date)
    
    sanity_check(is_reasonable_date(present_cfs_date))
    
    assert DATABASE.has_symbol(symbol), \
        "Requires that the database be tracking %s" % symbol
    
    assert rfcfg_exists_for(symbol, present_cfs_date), \
        "Requires that retrospective free cash flow growth can be calculated for %s using %s as a base date." % \
        (symbol, str(present_cfs_date))
    
    #DOC:
    #where present_trading_date = first_trading_day_after(present_cfs_date)
    
    #DESIGN:
    #present_trading_date = first_trading_day_after(present_cfs_date)    
    
    #process invariant:
    type_check(present_trading_date, datetime.date)
    
    assert ptr_exists_for(symbol, present_trading_date), \
        "Requires that prospective total return can be calculated for %s using %s as a base date." % \
        (symbol, str(present_trading_date))
    
    sanity_check(is_reasonable_date(present_trading_date), 
                 "present_trading_date in pair_rfcfg_and_ptr_for should be a reasonable date.")
        
    #DOC:
    #where answer is a pair consisting of the retrospective free cash flow growth and prospective total return with
    #with base date for the former of present_cfs_date and base date for the latter = present_trading_date
    
    #DESIGN:
    #answer = (retrospective_cash_flow_growth(symbol, present_cfs_date,
    #          prospective_total_return(symbol, present_trading_date))
    
    #REFACTOR:
    #use a named_tuple here
    
    #postconditions:
    type_check(answer, tuple)
    assert len(answer) == 2, \
        "Ensures length of answer tuple is 2, i.e., is a pair."
    type_check(answer[0], float)
    type_check(answer[1], float)
    
    sanity_check(-10000.00 < answer[0] < 10000.00, "Retrospective cash flow growth ought to be between -100x and 100x")
    sanity_check(0.0 < answer[1] < 10000.00, "Prospective total return should not be below 0 or above 100x.")
    
    #DESIGN:
    #return answer

@predicate    
def rfcfg_exists_for(symbol, present_cfs_date):
    """
    Predicate returns true if retrospective free cash flow growth can be calculated for symbol using present_cfs_date
    as the base date.
    Assumes present_cfs_date is a valid cash flow statement date for symbol.
    
    designed 4/15/10
    """
    
    #preconditions:
    type_check(symbol, basestring)
    type_check(present_cfs_date, datetime.date)
    
    assert DATABASE.has_symbol(symbol), \
        "Requires that symbol %s be in the database." % symbol
    assert DATABASE.has_cfs_for_date(symbol, present_cfs_date), \
        "Requires that our base date, %s, be a valid cash flow statement reporting date for %s" % \
        (str(present_cfs_date), symbol)
        
    #ret = cfs_has_ocf(symbol, present_cfs_date) and
    #      cfs_has_capex(symbol, present_cfs_date) and
    #      has_prior_cfs_for_date(symbol, present_cfs_date) and
    #      prior_cfs_has_ocf(symbol, present_cfs_date) and
    #      prior_cfs_has_capex(symbol, present_cfs_date)
        
@predicate
def ptr_exists_for(symbol, present_trading_date):
    """
    Predicate returns true if prospective total return can be calculated for symbol using present_trading_date as our
    base date.
    Assumes present_trading_date is a valid trading date.
    
    designed 4/15/10
    """
    
    #REFACTOR: note this assumption and trace your assumptions back up to the callers - do the callers guarantee these
    #assumptions? for instance, ptr_exists_For is called in pair_rfcfg_and_ptr_for, however the caller uses a function
    # first_trading_day_after that uses a calendar system to figure out trading days and does not verify with the 
    #database, meaning that we might have broken an assumption.  We need to add an assertion there to ensure that,
    #and probably an assertion after any use of the nth_trading_day_after functions.
    
    #preconditions:
    type_check(symbol, basestring)
    type_check(present_trading_date, datetime.date)
    
    assert DATABASE.has_symbol(symbol), \
        "Requires that symbol %s be in the database." % symbol
    assert DATABASE.is_trading_date(symbol, present_trading_date), \
        "Requires that our base date for the prospective total return calculation, %s, be a valid trading date" \
        "for %s" % (str(present_trading_date), symbol)
        
    #future_trading_day = one_trading_year_after(present_trading_date)
    #return (DATABASE.bs_reported_within_a_year_after(present_trading_day) and
    #        DATABASE.cfs_reported_within_a_year_after(present_trading_day) and
    #        DATABASE.is_trading_date(future_trading_day) and
    #        DATABASE.bs_reported_within_a_year_after(present_trading_day) and
    #        DATABASE.cfs_reported_within_a_year_after(present_trading_day))
    
 
@predicate       
def rfcfg_and_ptr_exist_for(symbol, present_cfs_date):
    """
    Predicate returns true if retrospective cash flow growth and prospective total return can be calculated using
    present_cfs_date for the first, and the nearest future trading date for the other.
    Assumes that symbol is tracked, and present_cfs_date is the date of a valid cash flow statement.
    
    designed 4/12
    """
    
    #preconditions:
    type_check(symbol, basestring)
    type_check(present_cfs_date, datetime.date)
    
    sanity_check(is_date_reasonable(present_cfs_date),
                 "present_cfs_date should be reasonable in rfcfg_and_ptr_exist_for")
    
    assert DATABASE.has_symbol(symbol), \
        "Requires %s Must be tracked by the database." % symbol
    assert DATABASE.has_cfs_for_date(symbol, present_cfs_date), \
        "Requires that %s must be a valid cash flow statement report date for %s" % (str(present_cfs_date), symbol)

    #DESIGN:
    #present_trading_date = first_trading_date_after(present_cfs_date)
    
    #process invariant
    sanity_check(is_date_reasonable(present_trading_date), 
                 "present_trading_date found in rfcfg_and_ptr_exist_for should be reasonable.")
    
    assert DATABASE.is_trading_date(symbol, present_trading_date), \
        "Invariant that the date %s we find for symbol %s is recorded in the database." % (symbol, present_trading_date)

    #DESIGN:
    #ret = rfcfg_exists_for(symbol, present_cfs_date) and ptr_exists_for(symbol, present_trading_date)

    #postconditions:
    assert ptr_exists_for(symbol, present_trading_date), \
        "Ensures that the prospective total return can be calculated for %s with %s as a base date." % \
        (symbol, str(present_trading_date))
    assert rfcfg_exists_for(symbol, present_cfs_date), \
        "Ensures that the retrospective free cash flow growth can be calculated for %s with %s as a base date." % \
        (symbol, str(present_cfs_date))
    
    #DESIGN:
    #return ret
    
        
def list_valid_study_dates_for(symbol):
    """
    Returns a list of valid dates to calcluate retrospective free cash flow growth and prospective total return for
    symbol.
    Assumes symbol is a valid tracked stock.
    
    designed 4/12
    """
    
    #preconditions
    assert DATABASE.has_symbol(symbol), \
        "Requires that %s is tracked by the database." % symbol
    
    #DESIGN:
    #trial_study_dates = DATABASE.cfs_dates(symbol)
    #list_of_valid_study_dates = [date for date in trial_study_dates if rfcfg_and_ptr_exist_for(symbol, date)]
    
    #DOC:
    #where list_of_valid_study_dates is a list of the valid study dates for symbol where retrospective free cash flow
    #growth and prospective total return can be calculated using the dates in the list as present_cfs_date base dates.
    
    #postconditions
    type_check(list_of_valid_study_dates, list)
    assert all(type_check(element, datetime.date) for element in list_of_valid_study_dates), \
        "Study dates should all be of type datetime.date"
    
    assert all([rfcfg_and_ptr_exist_for(symbol, date) for date in list_of_valid_study_dates]), \
        "Ensures all dates provided are valid study dates for %s" % symbol
        
    sanity_check(len(list_of_valid_study_dates) < 10, 
                 "list_of_valid_study_dates should be of reasonable size in list_valid_study_dates_for")
    sanity_check(is_reasonable_date(date) for date in list_of_valid_study_dates)
    
    
    #DESIGN:   
    #return list_of_valid_study_dates

#pseudocode
def run_study():
    """
    Runs the study described in the module's docstring
    """
    #results = []
    #for symbol in DATABASE.supported_symbols:
    #    for present_cfs_date in list_valid_study_dates_for(symbol):
    #        results.append(pair_rfcfg_and_ptr_for(symbol, present_cfs_date))
    #return results
    pass