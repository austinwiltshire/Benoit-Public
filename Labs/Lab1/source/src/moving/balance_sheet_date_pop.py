"""
This script will populate the date fields on the balance sheet.

It will need to, for any stock, bring in that stock's balance sheets, income statements and cash flow statements, in 
sorted order with dates ascending.

First attempt may be to zip these three lists together, first asserting that there is an equal number of each 
statement (which isn't necessarily true and would necessitate another approach) and then asserting that for 
each group, the maximum distance between each group is within some tolerance, say, a month of eachother.

If both of those assertions are true, than for the balance sheet the current income and cash flow statements can simply 
be set as those dates found in its 'peer group'.  It's future is the next in it's peer group's dates, and it's previous
is the previous group in the list. For the first member in the list, it's previous is set to null, for the last, it's 
next is set to null.
"""

from bloomberg import SESSION as BB
from financials import CashFlowStatement as CFS
#from basics import HistoricalPrices as Prices
from financials import BalanceSheet as BS
from financials import IncomeStatement as IS
import datetime


def zip_financials(cash_flow_statements, balance_sheets, income_statements):
    """
    takes in three lists of financial statements and matches them up to return a list of 
    size = min(len(x) for x in lists), or the size of the smallest list.
    
    assumes they're sorted
    
    *also* assumes that each financial is issued on the same date.  this probably isn't true :(
    """

    is_dates = set([inc_s.Date for inc_s in income_statements])
    cfs_dates = set([cfs.Date for cfs in cash_flow_statements])
    bs_dates = set([bs.Date for bs in balance_sheets])

    min_dates = is_dates.intersection(cfs_dates.intersection(bs_dates))
    
    assert len(min_dates) != 0

    new_is = [inc_s for inc_s in income_statements if inc_s.Date in min_dates]
    new_bs = [bs for bs in balance_sheets if bs.Date in min_dates]
    new_cfs = [cfs for cfs in cash_flow_statements if cfs.Date in min_dates]

    assert len(new_is) == len(new_bs) == len(new_cfs) == len(min_dates)
    
    financials = zip(new_cfs, new_bs, new_is)
    
    tolerance = datetime.timedelta(31)
    
    for financial in financials:
        #should be within a month of eachother.
        assert max(issue.Date for issue in financial) - min(issue.Date for issue in financial) <= tolerance, \
            "%s doesn't have financials within date tolerance of eachother." % (balance_sheets[0].Symbol)
            
    return financials
    
    
def is_spot_check(symbol, date, dates):
    """
    simple test comparing the dates found for symbol, on date, to dates on the income statement
    """
    
    assert len(dates) == 8
    
    is_test = (BB.query(IS.NextIssueDate,
                     IS.PreviousIssueDate,
                     IS.ConcurrentBalanceSheetIssueDate,
                     IS.ConcurrentCashFlowStatementIssueDate,
                     IS.NextBalanceSheetIssueDate,
                     IS.PreviousBalanceSheetIssueDate,
                     IS.NextCashFlowStatementIssueDate,
                     IS.PreviousCashFlowStatementIssueDate)
              .filter(IS.Symbol == symbol)
              .filter(IS.Date == date)
              .all())

    assert len(is_test) == 1

    is_test = is_test[0]

    assert (is_test.NextIssueDate == dates[0] and
            is_test.PreviousIssueDate == dates[1] and
            is_test.ConcurrentBalanceSheetIssueDate == dates[2] and
            is_test.ConcurrentCashFlowStatementIssueDate == dates[3] and
            is_test.NextBalanceSheetIssueDate == dates[4] and
            is_test.PreviousBalanceSheetIssueDate == dates[5] and
            is_test.NextCashFlowStatementIssueDate == dates[6] and
            is_test.PreviousCashFlowStatementIssueDate == dates[7])
    

def cfs_spot_check(symbol, date, dates):
    """
    simple test comparing the dates found for symbol, on date, to dates
    """
    
    assert len(dates) == 8
    
    cfs_test = (BB.query(CFS.NextIssueDate,
                     CFS.PreviousIssueDate,
                     CFS.ConcurrentBalanceSheetIssueDate,
                     CFS.ConcurrentIncomeStatementIssueDate,
                     CFS.NextBalanceSheetIssueDate,
                     CFS.PreviousBalanceSheetIssueDate,
                     CFS.NextIncomeStatementIssueDate,
                     CFS.PreviousIncomeStatementIssueDate)
              .filter(CFS.Symbol == symbol)
              .filter(CFS.Date == date)
              .all())

    assert len(cfs_test) == 1

    cfs_test = cfs_test[0]

    assert (cfs_test.NextIssueDate == dates[0] and
            cfs_test.PreviousIssueDate == dates[1] and
            cfs_test.ConcurrentBalanceSheetIssueDate == dates[2] and
            cfs_test.ConcurrentIncomeStatementIssueDate == dates[3] and
            cfs_test.NextBalanceSheetIssueDate == dates[4] and
            cfs_test.PreviousBalanceSheetIssueDate == dates[5] and
            cfs_test.NextIncomeStatementIssueDate == dates[6] and
            cfs_test.PreviousIncomeStatementIssueDate == dates[7])

def bs_spot_check(symbol, date, dates):
    """
    simple test comparing the dates found for symbol, on date, to dates for balance sheets
    """
    
    assert len(dates) == 8
    
    bs_test = (BB.query(BS.NextIssueDate,
                     BS.PreviousIssueDate,
                     BS.ConcurrentCashFlowStatementIssueDate,
                     BS.ConcurrentIncomeStatementIssueDate,
                     BS.NextCashFlowStatementIssueDate,
                     BS.PreviousCashFlowStatementIssueDate,
                     BS.NextIncomeStatementIssueDate,
                     BS.PreviousIncomeStatementIssueDate)
              .filter(BS.Symbol == symbol)
              .filter(BS.Date == date)
              .all())

    assert len(bs_test) == 1

    bs_test = bs_test[0]

    assert (bs_test.NextIssueDate == dates[0] and
            bs_test.PreviousIssueDate == dates[1] and
            bs_test.ConcurrentCashFlowStatementIssueDate == dates[2] and
            bs_test.ConcurrentIncomeStatementIssueDate == dates[3] and
            bs_test.NextCashFlowStatementIssueDate == dates[4] and
            bs_test.PreviousCashFlowStatementIssueDate == dates[5] and
            bs_test.NextIncomeStatementIssueDate == dates[6] and
            bs_test.PreviousIncomeStatementIssueDate == dates[7])


#ALL_SYMBOLS = [u'SBUX', u'IBM', u'AMZN', u'BAC', u'DELL', u'LMT']

import SnP500

ALL_SYMBOLS = [unicode(s) for s in SnP500.symbols]

print "Starting"

for symbol in ALL_SYMBOLS:
    
    print "On %s" % (symbol)
    
    cash_flow_statements = (BB.query(CFS)
                            .filter(CFS.Symbol == symbol)
                            .order_by(CFS.Date)
                            .all())
      
    balance_sheets = (BB.query(BS)
                      .filter(BS.Symbol == symbol)
                      .order_by(BS.Date)
                      .all())

    income_statements = (BB.query(IS)
                         .filter(IS.Symbol == symbol)
                         .order_by(IS.Date)
                         .all())
    
    financials = zip_financials(cash_flow_statements, balance_sheets, income_statements)
    
    CASH_FLOW_STATEMENT = 0
    BALANCE_SHEET = 1
    INCOME_STATEMENT = 2
    
    #do body
    for index, financial in list(enumerate(financials))[1:-1]:
        #... because of the slicing, we can assume index-1 and index+1 always work.
               
        #cash flow statement
        
        
        financial[CASH_FLOW_STATEMENT].ConcurrentBalanceSheetIssueDate = financial[BALANCE_SHEET].Date       
        financial[CASH_FLOW_STATEMENT].ConcurrentIncomeStatementIssueDate = financial[INCOME_STATEMENT].Date
        
        financial[CASH_FLOW_STATEMENT].NextIssueDate = financials[index+1][CASH_FLOW_STATEMENT].Date
        financial[CASH_FLOW_STATEMENT].NextBalanceSheetIssueDate = financials[index+1][BALANCE_SHEET].Date
        financial[CASH_FLOW_STATEMENT].NextIncomeStatementIssueDate = financials[index+1][INCOME_STATEMENT].Date
        
        financial[CASH_FLOW_STATEMENT].PreviousIssueDate = financials[index-1][CASH_FLOW_STATEMENT].Date
        financial[CASH_FLOW_STATEMENT].PreviousBalanceSheetIssueDate = financials[index-1][BALANCE_SHEET].Date      
        financial[CASH_FLOW_STATEMENT].PreviousIncomeStatementIssueDate = financials[index-1][INCOME_STATEMENT].Date
        
        #do balance sheet
        financial[BALANCE_SHEET].ConcurrentCashFlowStatementIssueDate = financial[CASH_FLOW_STATEMENT].Date       
        financial[BALANCE_SHEET].ConcurrentIncomeStatementIssueDate = financial[INCOME_STATEMENT].Date
        
        financial[BALANCE_SHEET].NextIssueDate = financials[index+1][BALANCE_SHEET].Date
        financial[BALANCE_SHEET].NextCashFlowStatementIssueDate = financials[index+1][CASH_FLOW_STATEMENT].Date
        financial[BALANCE_SHEET].NextIncomeStatementIssueDate = financials[index+1][INCOME_STATEMENT].Date
        
        financial[BALANCE_SHEET].PreviousIssueDate = financials[index-1][BALANCE_SHEET].Date
        financial[BALANCE_SHEET].PreviousCashFlowStatementIssueDate = financials[index-1][CASH_FLOW_STATEMENT].Date
        financial[BALANCE_SHEET].PreviousIncomeStatementIssueDate = financials[index-1][INCOME_STATEMENT].Date
        
        #do income statement
        financial[INCOME_STATEMENT].ConcurrentCashFlowStatementIssueDate = financial[CASH_FLOW_STATEMENT].Date       
        financial[INCOME_STATEMENT].ConcurrentBalanceSheetIssueDate = financial[BALANCE_SHEET].Date
        
        financial[INCOME_STATEMENT].NextIssueDate = financials[index+1][INCOME_STATEMENT].Date
        financial[INCOME_STATEMENT].NextCashFlowStatementIssueDate = financials[index+1][CASH_FLOW_STATEMENT].Date
        financial[INCOME_STATEMENT].NextBalanceSheetIssueDate = financials[index+1][BALANCE_SHEET].Date
        
        financial[INCOME_STATEMENT].PreviousIssueDate = financials[index-1][INCOME_STATEMENT].Date
        financial[INCOME_STATEMENT].PreviousCashFlowStatementIssueDate = financials[index-1][CASH_FLOW_STATEMENT].Date
        financial[INCOME_STATEMENT].PreviousBalanceSheetIssueDate = financials[index-1][BALANCE_SHEET].Date
        
        #do prices
        
        
    
    #do tips
    #cash flow
    
    financials[0][CASH_FLOW_STATEMENT].ConcurrentBalanceSheetIssueDate = financials[0][BALANCE_SHEET].Date
    financials[0][CASH_FLOW_STATEMENT].ConcurrentIncomeStatementIssueDate = financials[0][INCOME_STATEMENT].Date
    
    financials[0][CASH_FLOW_STATEMENT].NextIssueDate = financials[1][CASH_FLOW_STATEMENT].Date
    financials[0][CASH_FLOW_STATEMENT].NextBalanceSheetIssueDate = financials[1][BALANCE_SHEET].Date
    financials[0][CASH_FLOW_STATEMENT].NextIncomeStatementIssueDate = financials[1][INCOME_STATEMENT].Date
    
    financials[-1][CASH_FLOW_STATEMENT].PreviousIssueDate = financials[-2][CASH_FLOW_STATEMENT].Date
    financials[-1][CASH_FLOW_STATEMENT].PreviousBalanceSheetIssueDate = financials[-2][BALANCE_SHEET].Date
    financials[-1][CASH_FLOW_STATEMENT].PreviousIncomeStatementIssueDate = financials[-2][INCOME_STATEMENT].Date
    
    financials[-1][CASH_FLOW_STATEMENT].ConcurrentBalanceSheetIssueDate = financials[-1][BALANCE_SHEET].Date
    financials[-1][CASH_FLOW_STATEMENT].ConcurrentIncomeStatementIssueDate = financials[-1][INCOME_STATEMENT].Date
    

    #balance sheet
    
    financials[0][BALANCE_SHEET].ConcurrentCashFlowStatementIssueDate = financials[0][CASH_FLOW_STATEMENT].Date
    financials[0][BALANCE_SHEET].ConcurrentIncomeStatementIssueDate = financials[0][INCOME_STATEMENT].Date
    
    financials[0][BALANCE_SHEET].NextIssueDate = financials[1][BALANCE_SHEET].Date
    financials[0][BALANCE_SHEET].NextCashFlowStatementIssueDate = financials[1][CASH_FLOW_STATEMENT].Date
    financials[0][BALANCE_SHEET].NextIncomeStatementIssueDate = financials[1][INCOME_STATEMENT].Date
    
    financials[-1][BALANCE_SHEET].ConcurrentCashFlowStatementIssueDate = financials[-1][CASH_FLOW_STATEMENT].Date
    financials[-1][BALANCE_SHEET].ConcurrentIncomeStatementIssueDate = financials[-1][INCOME_STATEMENT].Date
    
    financials[-1][BALANCE_SHEET].PreviousIssueDate = financials[-2][BALANCE_SHEET].Date
    financials[-1][BALANCE_SHEET].PreviousCashFlowStatementIssueDate = financials[-2][CASH_FLOW_STATEMENT].Date
    financials[-1][BALANCE_SHEET].PreviousIncomeStatementIssueDate = financials[-2][INCOME_STATEMENT].Date
    
    #income statement
    
    financials[0][INCOME_STATEMENT].ConcurrentCashFlowStatementIssueDate = financials[0][CASH_FLOW_STATEMENT].Date
    financials[0][INCOME_STATEMENT].ConcurrentBalanceSheetIssueDate = financials[0][BALANCE_SHEET].Date
    
    financials[0][INCOME_STATEMENT].NextIssueDate = financials[1][INCOME_STATEMENT].Date
    financials[0][INCOME_STATEMENT].NextCashFlowStatementIssueDate = financials[1][CASH_FLOW_STATEMENT].Date
    financials[0][INCOME_STATEMENT].NextBalanceSheetIssueDate = financials[1][BALANCE_SHEET].Date
    
    financials[-1][INCOME_STATEMENT].ConcurrentCashFlowStatementIssueDate = financials[-1][CASH_FLOW_STATEMENT].Date
    financials[-1][INCOME_STATEMENT].ConcurrentBalanceSheetIssueDate = financials[-1][BALANCE_SHEET].Date
    
    financials[-1][INCOME_STATEMENT].PreviousIssueDate = financials[-1][INCOME_STATEMENT].Date
    financials[-1][INCOME_STATEMENT].PreviousCashFlowStatementIssueDate = financials[-2][CASH_FLOW_STATEMENT].Date
    financials[-1][INCOME_STATEMENT].PreviousBalanceSheetIssueDate = financials[-2][BALANCE_SHEET].Date
    
    BB.commit()





cfs_spot_check(u"SBUX", datetime.date(2007, 9, 30), [datetime.date(2008, 9, 28),
                                                    datetime.date(2006, 10, 1),
                                                    datetime.date(2007,9,30),
                                                    datetime.date(2007,9,30),
                                                    datetime.date(2008, 9, 28),
                                                    datetime.date(2006, 10, 1),
                                                    datetime.date(2008, 9, 28),
                                                    datetime.date(2006, 10, 1)])

cfs_spot_check(u"IBM", datetime.date(2007, 12, 31), [datetime.date(2008, 12, 31),
                                                    datetime.date(2006, 12, 31),
                                                    datetime.date(2007, 12, 31),
                                                    datetime.date(2007, 12, 31),
                                                    datetime.date(2008, 12, 31),
                                                    datetime.date(2006, 12, 31),
                                                    datetime.date(2008, 12, 31),
                                                    datetime.date(2006, 12, 31)])

bs_spot_check(u"AMZN", datetime.date(2007, 12, 31), [datetime.date(2008, 12, 31),
                                                    datetime.date(2006, 12, 31),
                                                    datetime.date(2007, 12, 31),
                                                    datetime.date(2007, 12, 31),
                                                    datetime.date(2008, 12, 31),
                                                    datetime.date(2006, 12, 31),
                                                    datetime.date(2008, 12, 31),
                                                    datetime.date(2006, 12, 31)])

bs_spot_check(u"BAC", datetime.date(2007, 12, 31), [datetime.date(2008, 12, 31),
                                                   datetime.date(2006, 12, 31),
                                                   datetime.date(2007, 12, 31),
                                                   datetime.date(2007, 12, 31),
                                                   datetime.date(2008, 12, 31),
                                                   datetime.date(2006, 12, 31),
                                                   datetime.date(2008, 12, 31),
                                                   datetime.date(2006, 12, 31)])

is_spot_check(u"DELL", datetime.date(2008, 2, 1), [datetime.date(2009, 1, 30),
                                                  datetime.date(2007, 2, 2),
                                                  datetime.date(2008, 2, 1),
                                                  datetime.date(2008, 2, 1),
                                                  datetime.date(2009, 1, 30),
                                                  datetime.date(2007, 2, 2),
                                                  datetime.date(2009, 1, 30),
                                                  datetime.date(2007, 2, 2)])

is_spot_check(u"LMT", datetime.date(2007, 12, 31), [datetime.date(2008, 12, 31),
                                                   datetime.date(2006, 12, 31),
                                                   datetime.date(2007, 12, 31),
                                                   datetime.date(2007, 12, 31),
                                                   datetime.date(2008, 12, 31),
                                                   datetime.date(2006, 12, 31),
                                                   datetime.date(2008, 12, 31),
                                                   datetime.date(2006, 12, 31)])



BB.close()
print "Finished"


#notes:
#ok, so there's a few items that didn't completely take.  ANF, for example, has 4 cash flows, income statements, etc...
#but its cash flows are one year in advance of everything else.  weird.  i don't want to download new data right now
#so i'm not going to fix this.  but it's out of sync, yes.
#
#one thing to look into is making this smarter such that it only updates values which were null to begin with.
#looking for null values not only would make it faster, but also more smartly look for things that the current script
#misses due to its inadequacies.
    
    #don't commit until test programs work!
    
    
    #TODO: consider refactoring common stuff out of 'do body' and 'do tips'.  could also consider another layer of
    #recursive zips, maybe evena property map.
    #for testing, just print out a single one until it works right, then maybe print out 10 to confirm, then run the whole thing to 
    #ensure none of the assertions trigger.