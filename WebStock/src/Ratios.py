import Website
import Yahoo
import FinancialDate
from Registry import Register
import Module2

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
	
	netIncome = incomeStatement.NetIncome or 0.0
	preferredDividends = incomeStatement.PreferredDividends or 0.0
	
	return netIncome - preferredDividends
Register("DailyNetRevenues",NetRevenues)