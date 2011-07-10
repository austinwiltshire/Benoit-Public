"""
Can retrospective free cash flow growth predict prospective total return?
"""

from sqlalchemy.orm import aliased

import basics
import financials
import FinancialDate
from bloomberg import SESSION
   
import result

ANNUAL = 1

result.create_table()
  
CURRENT_BALANCE_SHEET = financials.BalanceSheet
NEXT_BALANCE_SHEET = aliased(financials.BalanceSheet)

PREVIOUS_CASH_FLOW_STATEMENT = aliased(financials.CashFlowStatement)
CURRENT_CASH_FLOW_STATEMENT = financials.CashFlowStatement
NEXT_CASH_FLOW_STATEMENT = aliased(financials.CashFlowStatement)

def average_common_shares(current_balance_sheet, next_balance_sheet):
    """
    Returns the average number of shares between two balance sheets.
    """
    return (current_balance_sheet.TotalCommonSharesOutstanding + next_balance_sheet.TotalCommonSharesOutstanding) / 2.0

def has_available_price(symbol, date):
    """
    Returns true if 'symbol' supports price information on 'date'
    """
    
    assert symbol != None and date != None
    
    calendar = FinancialDate.Calendar()
    date = calendar.FirstTradingDayAfter(date)
    
    historical_prices = basics.HistoricalPrices
    
    val = (SESSION.query(historical_prices.Close).filter(historical_prices.Symbol == symbol) 
                  .filter(historical_prices.Date == date.toDatetime()).first())
    return val != None

def next_available_price(symbol, date):
    """
    Returns the next available closing price for 'symbol' on 'date'.
    
    If 'date' is a valid trading day, returns the closing price for 'date'.
    """
    
    
    assert symbol != None and date != None
    
    calendar = FinancialDate.Calendar()
    date = calendar.FirstTradingDayAfter(date)
    
    historical_prices = basics.HistoricalPrices
    
    val = (SESSION.query(historical_prices.Close).filter(historical_prices.Symbol == symbol)
                  .filter(historical_prices.Date == date.toDatetime()).first())
    assert val != None, "%s does not support date %s" % (symbol, str(date.toDatetime()))
    
    return val[0]

def total_return(cur_price, cur_shares, next_price, next_shares, div):
    """
    Returns the total return, that is, the total market cap growth + dividends
    """

    #total return is cap gains (market cap growth) + avg div yield
    assert div >= 0.0, "dividends can't be negative %f" % div
    return market_cap_growth(cur_price, cur_shares, next_price, next_shares) + (div / ((cur_price + next_price) / 2))

def market_cap_growth(cur_price, cur_shares, next_price, next_shares):
    """
    Returns the market capitalization growth of a stock as caluclated by price * shares outstanding
    """
    
    assert cur_price != None and cur_shares != None and next_price != None and next_shares != None
     
    cur_market_cap = cur_price * cur_shares
    
    return ((next_price * next_shares) - cur_market_cap) / cur_market_cap

def free_cash_flow(cash_flow_statement):
    """
    Calculates free cash flow given a cash flow statement where free cash flow is
    cash from operating activities + capital expenditures
    """
    #capex is negative
    
    return cash_flow_statement.CashFromOperatingActivities + cash_flow_statement.CapitalExpenditures

#results = [FreeCashFlowGrowth(*row) for row in SESSION.query(current_cfs.Symbol,
#                         previous_cfs.Date,
#                         current_cfs.Date,
#                         (free_cash_flow(current_cfs) - free_cash_flow(previous_cfs)) / 
#                          free_cash_flow(previous_cfs)) \
#                  .filter(current_cfs.Symbol == previous_cfs.Symbol) \
#                  .filter(current_cfs.PreviousIssueDate == previous_cfs.Date)
#                  .filter(current_cfs.CapitalExpenditures != None)
#                  .filter(current_cfs.Period == ANNUAL)
#                  .filter(previous_cfs.Period == ANNUAL)
#                  .filter(previous_cfs.CapitalExpenditures != None)]
#


def total_return2(cur_price, cur_shares, next_price, next_shares, div):

    assert cur_price != None and cur_shares != None and next_price != None and next_shares != None

    if not div:
        div = 0.0
        
    #total return is cap gains (market cap growth) + avg div yield
    assert div >= 0.0, "dividends can't be negative %f" % div
    
    avg_shares = (cur_shares + next_shares) / 2.0
    avg_price = (cur_price + next_price) / 2.0
    
    div_per_share = div / avg_shares
    div_yield = div_per_share / avg_price
    
    cur_market_cap = cur_price * cur_shares
    next_market_cap = next_price * next_shares
    
    market_cap_growth = (next_market_cap - cur_market_cap) / cur_market_cap
    
    return market_cap_growth + div_yield

def fcf_growth(cur_cash_from_ops, cur_capex, past_cash_from_ops, past_capex):
    """
    Calculates the free cash flow growth in a stock.
    """
    
    assert cur_cash_from_ops != None and past_cash_from_ops != None
    
    if not cur_capex:
        cur_capex = 0.0
        
    if not past_capex:
        past_capex = 0.0
        
    cur_fcf = cur_cash_from_ops + cur_capex
    past_fcf = past_cash_from_ops + past_capex
    
    return (cur_fcf - past_fcf) / (past_fcf)


#results = [Result(symbol, curr_bs_date, prev_cfs_date, next_bs_date, 
#            fcf_growth(cur_cash_from_ops, cur_capex, past_cash_from_ops, past_capex),
#            total_return2(next_available_price(symbol, curr_bs_date), cur_shares, next_available_price(symbol, next_bs_date), next_shares, dividends))
#            for symbol, curr_bs_date, prev_cfs_date, next_bs_date, cur_cash_from_ops, cur_capex, past_cash_from_ops, past_capex, cur_shares, next_shares, dividends in
#            SESSION.query(current_bs.Symbol, 
#                          current_bs.Date,
#                          previous_cfs.Date, 
#                          next_bs.Date,
#                          current_cfs.CashFromOperatingActivities,
#                          current_cfs.CapitalExpenditures,
#                          previous_cfs.CashFromOperatingActivities,
#                          previous_cfs.CapitalExpenditures,
#                          current_bs.TotalCommonSharesOutstanding,
#                          next_bs.TotalCommonSharesOutstanding,
#                          -next_cfs.TotalCashDividendsPaid)
#                   .filter(current_bs.Symbol == current_cfs.Symbol)
#                   .filter(current_bs.Symbol == next_bs.Symbol)
#                   .filter(current_bs.NextIssueDate == next_bs.Date)
#                   .filter(current_bs.ConcurrentCashFlowStatementIssueDate == current_cfs.Date)
#                   .filter(current_cfs.Symbol == previous_cfs.Symbol)
#                   .filter(current_cfs.Symbol == next_cfs.Symbol)
#                   .filter(current_cfs.PreviousIssueDate == previous_cfs.Date)
#                   .filter(current_cfs.NextIssueDate == next_cfs.Date)
#                   .filter(current_bs.Period == ANNUAL)
#                   .filter(next_bs.Period == ANNUAL)
#                   .filter(current_cfs.Period == ANNUAL)
#                   .filter(next_cfs.Period == ANNUAL)
#                   .filter(previous_cfs.Period == ANNUAL) if has_available_price(symbol, curr_bs_date) and has_available_price(symbol, next_bs_date)]
#
#print len(results)
#print results
#
#MEMORY_SESSION.add_all(results)
#MEMORY_SESSION.commit()

#for dividend paying stocks
#results_with_dividends = [(symbol, cur_date, next_date, total_return(next_available_price(symbol, cur_date), cur_shares, next_available_price(symbol, next_date), next_shares, div))
#                          for symbol, cur_date, next_date, cur_shares, next_shares, div in SESSION.query(current_bs.Symbol,
#                                        current_bs.Date,
#                                        next_bs.Date,
#                                        current_bs.TotalCommonSharesOutstanding,
#                                        next_bs.TotalCommonSharesOutstanding,
#                                        - (next_cfs.TotalCashDividendsPaid / average_common_shares(current_bs, next_bs))) #average dividends for the period
#                                 .filter(current_bs.Symbol == next_bs.Symbol)
#                                 .filter(current_bs.NextIssueDate == next_bs.Date)
#                                 .filter(next_bs.Date == next_cfs.Date)
#                                 .filter(current_bs.Symbol == next_cfs.Symbol)
#                                 .filter(current_bs.Period == ANNUAL)
#                                 .filter(next_bs.Period == ANNUAL)
#                                 .filter(next_cfs.Period == ANNUAL)
#                                 .filter(next_cfs.TotalCashDividendsPaid != None) if has_available_price(symbol, cur_date) and has_available_price(symbol, next_date)]
#
#results_without_dividends = [(symbol, cur_date, next_date, total_return(next_available_price(symbol, cur_date), cur_shares, next_available_price(symbol, next_date), next_shares, 0.0))
#                             for symbol, cur_date, next_date, cur_shares, next_shares in SESSION.query(current_bs.Symbol,
#                                        current_bs.Date,
#                                        next_bs.Date,
#                                        current_bs.TotalCommonSharesOutstanding,
#                                        next_bs.TotalCommonSharesOutstanding)
#                                 .filter(current_bs.Symbol == next_bs.Symbol)
#                                 .filter(current_bs.NextIssueDate == next_bs.Date)
#                                 .filter(next_bs.Date == next_cfs.Date)
#                                 .filter(current_bs.Period == ANNUAL)
#                                 .filter(next_bs.Period == ANNUAL)
#                                 .filter(current_bs.Symbol == next_cfs.Symbol)
#                                 .filter(next_cfs.TotalCashDividendsPaid == None) if has_available_price(symbol, cur_date) and has_available_price(symbol, next_date)]

#print results_with_dividends + results_without_dividends


#generate all new tables as sqllite tables

#create a function that, given a date, returns market cap growth of a stock one year from that date (or throws exception if doesn't exist?)
#preferably inside the database
#create a function that, given a date, returns dividend yield for that stock one year from that date
#preferably inside the database
#create a function that adds those two
#preferably inside the database
#generate a table of total return with begin date, end date, symbol and total return
#generate table from join the two tables where fcf growth end date = total return begin date,
#run a regression  
