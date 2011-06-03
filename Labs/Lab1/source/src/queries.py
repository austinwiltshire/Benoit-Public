"""
Lab 1 - Correlation of retrospective (one year ago to today) free cash flow growth with prospective (today to one year
from today) total return, where total return is a combination of expected capital gains and dividends.

In other words, if you knew a company's free cash flow growth from last year to this year, can you tell whether you
should buy it?
"""

from bloomberg import D_SESSION as  DB
from financials import BalanceSheet as BS
from financials import CashFlowStatement as CFS
from basics import HistoricalPrices as PRICE

from sqlalchemy.orm import aliased

import FinancialDate

#TODO:
#now just need a way to group by the date, shoudl print out dates that aren't lined up for debug purposes.  once i 
#group the two things, i'm... done...  wow.
                
def first_trading_day_after(date):
    """
    Returns the first trading day after date.  If date is a trading day, returns date.
    
    move this into financial date.
    """
    
    
    return FinancialDate.NthTradingDayAfter(FinancialDate.toDatetime(date), 0)

def market_cap(price, balance_sheet):
    """
    Given a prices table and a balance sheet table, returns the sql term for market cap.
    """
    return price.Close * balance_sheet.TotalCommonSharesOutstanding

def growth(current, future):
    """
    Given two sql terms, returns a term representing the growth between them.
    """
    return 1.0 + ((future - current) / current)

def get_dates_available(symbol, table):
    """
    Returns the dates available for symbol, given a table that supports t.Date and t.Symbol
    """
    return [row.Date for row in (DB.query(table.Date)
                                   .filter(table.Symbol==symbol)
                                   .all())]

def equivalent_symbol(first_table, second_table):
    """
    Returns an on clause for an sql query that is true when the table's symbols are the same.
    """
    return first_table.Symbol == second_table.Symbol

def free_cash_flow(cash_flow_statement):
    """
    Returns a sqlalchemy term that calculates free cash flow given a cash flow statement term.
    Assumes capex is negative.
    """
    return (cash_flow_statement.CashFromOperatingActivities + cash_flow_statement.CapitalExpenditures)

def free_cash_flow_growth(symbol, cash_flow_statements, database):
    """
    Returns retrospective growth in free cash flow.  Returns a list of date and percentage pairs where the percentage
    represents the cash flow growth *one year up to* date.
    """
    
    past_cash_flow_statements = aliased(cash_flow_statements)
    
    current_free_cash_flow = free_cash_flow(cash_flow_statements)
    past_free_cash_flow = free_cash_flow(past_cash_flow_statements)
    growth_free_cash_flow = growth(past_free_cash_flow, current_free_cash_flow)
    
    return (database.query(cash_flow_statements.Date, growth_free_cash_flow)
                    .join((past_cash_flow_statements,
                           equivalent_symbol(cash_flow_statements, past_cash_flow_statements) &
                           (cash_flow_statements.PreviousIssueDate == past_cash_flow_statements.Date)))
                    .filter(cash_flow_statements.Symbol == symbol)
                    .order_by(cash_flow_statements.Date)
                    .all())

def total_growth(symbol, prices, balance_sheets, cash_flow_statements, database):
    """
    Calculates market cap growth for a symbol from all data available and returns growth in chronological order.
    
    Also takes into account dividends.
    
    Growth is perspective, returns a list of date percentage pairs where the percentage is the growth in the market
    cap from date until approx one year later.
    """
       
    dates = [first_trading_day_after(date) for date in get_dates_available(symbol, balance_sheets)]
    
    #dates currently datetimes, need to strip out just dates.
    dates = [datetime_.date() for datetime_ in dates]
    
    future_balance_sheets = aliased(balance_sheets)
    future_prices = aliased(prices)

    #dividends are always negative, i really want to add them below.
    dividended_future_market_cap = (market_cap(future_prices, future_balance_sheets) -
                                    cash_flow_statements.TotalCashDividendsPaid)
    
    current_market_cap = market_cap(prices, balance_sheets)   
    growth_market_cap = growth(current_market_cap, dividended_future_market_cap)
       
    dividended = (database.query(PRICE.Date, growth_market_cap, cash_flow_statements.TotalCashDividendsPaid) 
                    # get the current date and the prospective market cap growth
                    .join((BS, equivalent_symbol(PRICE, BS) & #when prices and balance sheets symbols are equal
                               (PRICE.PreviousBalanceSheetIssueDate == BS.Date)), #and price prev bs date points to bs
                          (future_balance_sheets, equivalent_symbol(BS, future_balance_sheets) &
                           #when bs and future bs symbols are equal
                                                  (BS.NextIssueDate == future_balance_sheets.Date)),
                                                  #and bs's next issue date is future bs
                          (cash_flow_statements, equivalent_symbol(future_balance_sheets, cash_flow_statements) &
                                                 (future_balance_sheets.ConcurrentCashFlowStatementIssueDate ==
                                                  cash_flow_statements.Date)),
                          (future_prices, 
                           equivalent_symbol(future_prices, future_balance_sheets) & 
                           #when future price and future bs symbol is equal
                           (future_prices.PreviousBalanceSheetIssueDate == future_balance_sheets.Date))) 
                           #and future date's prev bs issue is future bs
              .filter(PRICE.Symbol == symbol)
              .filter(PRICE.Date.in_(dates))
              .filter(future_prices.Date.in_(dates))
              .filter(cash_flow_statements.TotalCashDividendsPaid != None)
              .order_by(PRICE.Date)
              .all())
    
    #now grab things that don't have dividends
    future_market_cap = market_cap(future_prices, future_balance_sheets)
    current_market_cap = market_cap(prices, balance_sheets)   
    growth_market_cap = growth(current_market_cap, future_market_cap)
    
    non_dividended = (database.query(PRICE.Date, growth_market_cap)
                     # get the current date and the prospective market cap growth
                    .join((BS, equivalent_symbol(PRICE, BS) & #when prices and balance sheets symbols are equal
                               (PRICE.PreviousBalanceSheetIssueDate == BS.Date)), #and price prev bs date points to bs
                          (future_balance_sheets, equivalent_symbol(BS, future_balance_sheets) &
                          #when bs and future bs symbols are equal
                                                  (BS.NextIssueDate == future_balance_sheets.Date)), 
                                                  #and bs's next issue date is future bs
                          (cash_flow_statements, 
                           equivalent_symbol(future_balance_sheets, cash_flow_statements) &
                           (future_balance_sheets.ConcurrentCashFlowStatementIssueDate == cash_flow_statements.Date)),
                           (future_prices, equivalent_symbol(future_prices, future_balance_sheets) & 
                          #when future price and future bs symbol is equal
                          (future_prices.PreviousBalanceSheetIssueDate == future_balance_sheets.Date)))
                          #and future date's prev bs issue is future bs
              .filter(PRICE.Symbol == symbol)
              .filter(PRICE.Date.in_(dates))
              .filter(future_prices.Date.in_(dates))
              .filter(cash_flow_statements.TotalCashDividendsPaid == None)
              .order_by(PRICE.Date)
              .all())
    
    return sorted(dividended + non_dividended)

def find_retro_fcf_growth_and_pro_total_return(symbol):
    """
    Returns a list of tuples for symbol.  Each tuple consists of a date, retrospective free cash flow growth from one
    year prior to date, and prospective total return starting at date and ending one year after.
    """
    
    #growth = total_growth(symbol, PRICE, BS, CFS, DB)
    #fcf = free_cash_flow_growth(symbol, CFS, DB)
    
    #put both growth and fcf into dicts arranged by their dates
    
    #make a set of shared dates by taking the intersection between two sets consisting of the dates
    #for each date in the set, add a tuple of the date and the growth and fcf dict indexed by that date
    
    #return that list

if __name__ == "__main__":
    import datetime
    
    
    assert (total_growth(u"MSFT", PRICE, BS, CFS, DB) == 
            [(datetime.date(2005, 6, 30), 0.89457529443855699, -3545.0),
             (datetime.date(2006, 6, 30), 1.2061109836269901, -3805.0),
             (datetime.date(2007, 7, 2), 0.91682647645207704, -4015.0)])
    assert (free_cash_flow_growth(u"SBUX", CFS, DB) ==
            [(datetime.date(2006, 10, 1), 1.2889383187118), 
             (datetime.date(2007, 9, 30), 0.69608761965277999), 
             (datetime.date(2008, 9, 28), 1.0929961992617001)])
    
    
    