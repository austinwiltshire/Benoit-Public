""" This module works in tandem with the fundamentals module to define different ratios important in fundamental analysis. 

Implementation Note:
Both this and fundamentals 'belong' together, such that using and exercising the actual module system and folders would mean it'd make sense to put
them in the same module and have fundamentals refer to this as its 'definitions' file or something. """

#import Website
#import Yahoo
import FinancialDate
from Registry import Register
import Module2

#TODO:
#proper annual and quarterly logic here can clearup the 'preload' problem.  The problem is as follows:
#currently, all of these functions use the 'MostRevent' function on a stock.  That means that they will only query the database, not the web, so 
#they won't calculate correctly if the database has not been updated.
#this has to be done since these are usually calculated on a daily basis, and this could turn into a whole host of bad web calls.
#quarterly and annual logic, either here or in the MostRecent function itself, could give the app a hint as to whether it should check the web for new information.
#until then, we're expected to just make sure we get financial information in before calling/using these.

def PriceToEarnings(symbol, date):
	""" stock price / eps """	
	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	
	EPS = stock.Fundamentals.EarningsPerShare
	price = stock.Prices.Close	
	
	return price / EPS
Register("DailyPriceToEarnings",PriceToEarnings)

def EarningsPerShare(symbol, date):
	""" net revenues / outstanding shares """
		
	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	balanceSheet = stock.MostRecent(Module2.Financials.Annual.BalanceSheet)
	
	netRevenues = stock.Fundamentals.NetRevenues
	sharesOutstanding = balanceSheet.TotalCommonSharesOutstanding
	
	return netRevenues / sharesOutstanding
Register("DailyEarningsPerShare",EarningsPerShare)

def NetRevenues(symbol, date):
	""" net income - preferred dividends """
	
	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	incomeStatement = stock.MostRecent(Module2.Financials.Annual.IncomeStatement)
	
	netIncome = incomeStatement.NetIncome
	preferredDividends = incomeStatement.PreferredDividends or 0.0 #we assume none reported means none given out in this case.
	
	return netIncome - preferredDividends
Register("DailyNetRevenues",NetRevenues)