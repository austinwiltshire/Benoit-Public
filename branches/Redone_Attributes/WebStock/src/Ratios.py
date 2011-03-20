""" This module works in tandem with the fundamentals module to define different ratios important in fundamental analysis. 

Implementation Note:
Both this and fundamentals 'belong' together, such that using and exercising the actual module system and folders would mean it'd make sense to put
them in the same module and have fundamentals refer to this as its 'definitions' file or something. """

#import Website
#import Yahoo
import FinancialDate
from Registry import Register, Get, InlineRegister, RegisterWithName
import Module2
from SafeFloat import SafeFloat
from WebsiteExceptions import DateNotFound
from decorators import Handles

#TODO:
#proper annual and quarterly logic here can clearup the 'preload' problem.  The problem is as follows:
#currently, all of these functions use the 'MostRevent' function on a stock.  That means that they will only query the database, not the web, so 
#they won't calculate correctly if the database has not been updated.
#this has to be done since these are usually calculated on a daily basis, and this could turn into a whole host of bad web calls.
#quarterly and annual logic, either here or in the MostRecent function itself, could give the app a hint as to whether it should check the web for new information.
#until then, we're expected to just make sure we get financial information in before calling/using these.


@InlineRegister
def DailyFundamentalsDates(symbol):

	beginDate = min([Get("AnnualIncomeStatementDates")(symbol)[0],
					 Get("AnnualCashFlowStatementDates")(symbol)[0],
					 Get("AnnualBalanceSheetDates")(symbol)[0]])	
	
	return [_date for _date in Get("DailyPricesDates")(symbol) if _date >= beginDate]
#Register("DailyFundamentalsDates",DailyFundamentalsDates)

@InlineRegister
def QuarterlyDerivedDates(symbol):
	return sorted(list(set(Get("QuarterlyIncomeStatementDates")(symbol) + Get("QuarterlyCashFlowStatementDates")(symbol) + Get("QuarterlyBalanceSheetDates")(symbol))))	
#Register("QuarterlyDerivedDates",QuarterlyDerivedDates)

@InlineRegister
def AnnualDerivedDates(symbol):
	return sorted(list(set(Get("AnnualIncomeStatementDates")(symbol) + Get("AnnualCashFlowStatementDates")(symbol) + Get("AnnualBalanceSheetDates")(symbol))))
#Register("AnnualDerivedDates",AnnualDerivedDates)

@InlineRegister
@Handles(DateNotFound,returns=SafeFloat(None))
def QuarterlyFreeCashFlow(symbol, date):
	""" Operating Cash Flow - Capital Expenditures """

	stock = Module2.Symbol(symbol).Date(date.month, date.day, date.year)

#	try:
	OperatingCashFlow = stock.Financials.Quarter.CashFlowStatement.CashFromOperatingActivities
	CapitalExpenditures = stock.Financials.Quarter.CashFlowStatement.CapitalExpenditures
#	except DateNotFound:
		#some derived financial stuff exists, some doesn't, depending on the date, because financials are so goofy.  its not a huge waste just to store a null
#		return SafeFloat(None)
		
	

	
	#capital expenditures are stored as negative numbers (since they're expenditures) so we're actually adding below
	return OperatingCashFlow + CapitalExpenditures
#Register("QuarterlyFreeCashFlow",QuarterlyFreeCashFlow)

@InlineRegister
@Handles(DateNotFound,returns=SafeFloat(None))
def AnnualFreeCashFlow(symbol, date):
	""" Operating Cash Flow - Capital Expenditures """

	stock = Module2.Symbol(symbol).Date(date.month, date.day, date.year)
	
	OperatingCashFlow = stock.Financials.Annual.CashFlowStatement.CashFromOperatingActivities
	CapitalExpenditures = stock.Financials.Annual.CashFlowStatement.CapitalExpenditures

#	if not OperatingCashFlow or not CapitalExpenditures:
#		return SafeFloat(None)

	#capital expenditures are stored as negative numbers (since they're expenditures) so we're actually adding below	
	return OperatingCashFlow + CapitalExpenditures

#Register("AnnualFreeCashFlow",AnnualFreeCashFlow)

@RegisterWithName("DailyPriceToEarnings")
@Handles(DateNotFound,returns=SafeFloat(None))
def PriceToEarnings(symbol, date):
	""" stock price / eps """	
	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	
	EPS = stock.MostRecent(Module2.Financials.Annual.Derived).EarningsPerShare
	price = stock.Prices.Close	
	
	return price / EPS

@RegisterWithName("DailyPriceToFreeCashFlow")
@Handles(DateNotFound,returns=SafeFloat(None))
def PriceToFreeCashFlow(symbol, date):
	""" stock price / FCF per share """	

	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	
	FCFPS = stock.MostRecent(Module2.Financials.Annual.Derived).FreeCashFlowPerShare
	price = stock.Prices.Close	
	
	return price / FCFPS

@InlineRegister
@Handles(DateNotFound,returns=SafeFloat(None))
def AnnualFreeCashFlowPerShare(symbol, date):

	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	balanceSheet = stock.MostRecent(Module2.Financials.Annual.BalanceSheet)
	
	if not balanceSheet:
		return SafeFloat(None)
	
	freeCashFlow = stock.Financials.Annual.Derived.FreeCashFlow
	sharesOutstanding = balanceSheet.TotalCommonSharesOutstanding
	
	return freeCashFlow / sharesOutstanding

@InlineRegister
@Handles(DateNotFound,returns=SafeFloat(None))
def QuarterlyFreeCashFlowPerShare(symbol, date):

	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	balanceSheet = stock.MostRecent(Module2.Financials.Annual.BalanceSheet)
	
	if not balanceSheet:
		return SafeFloat(None)
	
	freeCashFlow = stock.Financials.Quarter.Derived.FreeCashFlow
	sharesOutstanding = balanceSheet.TotalCommonSharesOutstanding
	
	return freeCashFlow / sharesOutstanding

@InlineRegister
@Handles(DateNotFound,returns=SafeFloat(None))
def AnnualEarningsPerShare(symbol, date):
	""" Operating Cash Flow - Capital Expenditures """

	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	balanceSheet = stock.MostRecent(Module2.Financials.Annual.BalanceSheet)
	
	if not balanceSheet:
		return SafeFloat(None)
	
	netRevenues = stock.Financials.Annual.Derived.NetRevenues
	sharesOutstanding = balanceSheet.TotalCommonSharesOutstanding
	
	return netRevenues / sharesOutstanding

@InlineRegister
@Handles(DateNotFound,returns=SafeFloat(None))
def QuarterlyEarningsPerShare(symbol, date):
	""" Operating Cash Flow - Capital Expenditures """

	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	balanceSheet = stock.MostRecent(Module2.Financials.Quarter.BalanceSheet)
	
	if not balanceSheet:
		return SafeFloat(None)
	
	netRevenues = stock.Financials.Quarter.Derived.NetRevenues
	sharesOutstanding = balanceSheet.TotalCommonSharesOutstanding
	
	return netRevenues / sharesOutstanding

@InlineRegister
@Handles(DateNotFound,returns=SafeFloat(None))
def AnnualNetRevenues(symbol, date):
	""" net income - preferred dividends """
	
	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	incomeStatement = stock.MostRecent(Module2.Financials.Annual.IncomeStatement)
	
	if not incomeStatement:
		return SafeFloat(None)
	
	netIncome = incomeStatement.NetIncome
	preferredDividends = incomeStatement.PreferredDividends or 0.0 #we assume none reported means none given out in this case.
	
	return netIncome - preferredDividends

@InlineRegister
@Handles(DateNotFound,returns=SafeFloat(None))
def QuarterlyNetRevenues(symbol, date):
	""" net income - preferred dividends """
	
	stock = Module2.Symbol(symbol).Date(date.month,date.day,date.year)
	incomeStatement = stock.MostRecent(Module2.Financials.Quarter.IncomeStatement)
	
	if not incomeStatement:
		return SafeFloat(None)
	
	netIncome = incomeStatement.NetIncome
	preferredDividends = incomeStatement.PreferredDividends or 0.0 #we assume none reported means none given out in this case.
	
	return netIncome - preferredDividends