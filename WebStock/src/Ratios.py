import Website
import Yahoo
import FinancialDate
from Registry import Register
from Service import Service

@Register(Service.Daily("PriceToEarnings"))
def PriceToEarnings(symbol, date):
	""" stock price / eps """
	
	eps = EarningsPerShare(symbol, date)
	
	price_scraper = Yahoo.Yahoo()
	price_on_day = price_scraper.getClose(symbol,date)
	
	return price_on_day / eps

def EarningsPerShare(symbol, date):
	""" net revenues / outstanding shares """
	financials_scraper = Website.Google()

	shares_outstanding_filing_date = AnnualBalanceSheetDate(symbol, date)
	
	shares_outstanding_filing_date = FinancialDate.toDate(shares_outstanding_filing_date)
	
	shares_outstanding = financials_scraper.getAnnualTotalCommonSharesOutstanding(symbol, shares_outstanding_filing_date)
	
	return NetRevenues(symbol, date) / shares_outstanding

def NetRevenues(symbol, date):
	""" net income - preferred dividends """
	financials_scraper = Website.Google()

	earnings_filing_date = AnnualIncomeStatementDate(symbol, date)
	
	earnings_filing_date = FinancialDate.toDate(earnings_filing_date)	
	
	earnings = financials_scraper.getAnnualNetIncome(symbol, earnings_filing_date)
		
	preferred_dividends_for_year = financials_scraper.getAnnualPreferredDividends(symbol, earnings_filing_date)
	
	if preferred_dividends_for_year == '-':
		net_revenues = earnings
	else:
		net_revenues = earnings - preferred_dividends_for_year
		
	return net_revenues

def AnnualIncomeStatementDate(symbol, date):
	financials_scraper = Website.Google()
	earnings_dates = financials_scraper.getAnnualIncomeStatementDates(symbol)
	
	fixed_date = FinancialDate.toDate(date)
	
	find_date = FinancialDate.FuzzyPolicy(FinancialDate.FuzzyPolicy.RoundDown())
	earnings_date = find_date.advice(fixed_date, earnings_dates)
	
	if not earnings_date:
		raise Website.DateNotFound(symbol,date)
	
	return FinancialDate.toDatetime(earnings_date)
	
def AnnualBalanceSheetDate(symbol, date):
	financials_scraper = Website.Google()
	earnings_dates = financials_scraper.getAnnualBalanceSheetDates(symbol)
	
	fixed_date = FinancialDate.toDate(date)
	
	find_date = FinancialDate.FuzzyPolicy(FinancialDate.FuzzyPolicy.RoundDown())
	earnings_date = find_date.advice(fixed_date, earnings_dates)
	
	if not earnings_date:
		raise Website.DateNotFound(symbol,date)
	
	return FinancialDate.toDatetime(earnings_date)	