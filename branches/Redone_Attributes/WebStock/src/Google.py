""" Used to download SEC financial information from finance.google.org

Examples:
>>> from datetime import date
>>> round(getQuarterlyRevenue("MRK", date(2007,12,31)))
6243.0

>>> round(getQuarterlyGoodwill("IBM", date(2008,9,30)))
18861.0

>> round(getQuarterlyChangesInWorkingCapital("SBUX", date(2008,09,28)))
-75.00

>>> round(getQuarterlyOtherNet("CSCO", date(2008,01,26)))
22.0

>>> round(getQuarterlyRetainedEarnings("CSCO", date(2008,01,26)))
-1073.0

>>> round(getQuarterlyIssuanceOfStock("CSCO", date(2008,04,26)))
-1526.0

>>> round(getAnnualOtherNet("CSCO", date(2006,07,29)))
-94.0

>>> round(getAnnualRetainedEarnings("CSCO", date(2006,7,29)))
-617.0

>>> round(getAnnualIssuanceOfStock("CSCO", date(2005,07,30)))
-9148.0

Some information is not provided by google, showing up as a '-' on the website.  We return it as None.

>>> getQuarterlyOtherRevenue('S', date(2007,12,31)) is None
True

>>> getQuarterlyDilutionAdjustment('S', date(2007,12,31))
0.0

>>> getAnnualDilutionAdjustment('S', date(2007,12,31)) is None
True

>>> int(getQuarterlyDilutedNormalizedEPS('S', date(2007,12,31)))
-3

If a stock does not have public financials, like a foriegn company, or simply doesn't exist, we get a Financials not supported error.

>>> getAnnualForeignExchangeEffects("NTDOY", date(2007,12,31))
Traceback (most recent call last):
	...
SymbolHasNoFinancials: Symbol does not support financials: \"NTDOY\"

>>> getAnnualCashInterestPaid("CHEESE", date(2007,9,30))
Traceback (most recent call last):
	...
SymbolNotFound: Could not find symbol : \"CHEESE\"

Or if the date is invalid:

>>> getAnnualDeferredTaxes("BAC", date(2007,12,30))
Traceback (most recent call last):
	...
DateNotFound: Symbol \"BAC\" does not support date : 2007-12-30

Foreign exchanges that Google supports are accessible.

>>> round(getAnnualNotesPayable("PIF.UN", date(2007,12,31)))
0.0

Or ADR's

>>> round(getAnnualTotalAssets("IBN", date(2007,3,31)))
3943347.0

But this might not be in American dollars!

>>> getCurrencyReported("IBN")
u'INR'

Even though its traded on an American stock exchange

>>> getExchange("IBN")
u'NYSE'

"""

from Registry import Register
import urllib
from urlparse import urlunparse
from urllib2 import urlopen, HTTPError
from Adapt import Adapt
from datetime import date, datetime
from SymbolLookup import SymbolLookup
from utilities import head, tail
from Cached import cached
import re
from OrderedDict import OrderedDict

from WebsiteExceptions import DateNotFound, SymbolNotFound, SymbolHasNoFinancials

from BeautifulSoup import BeautifulSoup

#curry urlencode to always decode lists
urlencode = lambda dct: urllib.urlencode(dct, True)

resolver = SymbolLookup()

schema = 'http'
basePage = 'finance.google.com'
path = 'finance'

def financialsURL(dct):
	return (schema, basePage, path, '', urlencode(dct), '')

@cached(100)
def getFinancials(symbol,exchange=None,doit=True):
	#currently don't use exchange but can/should in the future if it's provided.
	
	#resolve to google style symbols
	symbol = resolver.getGoogle(symbol)
	
	args = {}
	args['fstype'] = 'ii'
	
	#this symbol may need to be added to it's exchange ala NASDAQ:IRBT instead of just IRBT...
	args['q'] = symbol
		
	url = financialsURL(args)
	raw_url = urlunparse(url)
	
	#print raw_url
	
	try:
		if doit:
			return ParsedFinancials(urlopen(raw_url))
		else:
			return BeautifulSoup(urlopen(raw_url))
	except HTTPError, e:
		raise SymbolNotFound(symbol)
	except IndexError, e:
		raise SymbolHasNoFinancials(symbol)
	
class ParsedFinancials(object):
	
	numberRe = re.compile(r"-?[\d{3,3},]*\d{0,3}\.\d+|-")
	dateRe = re.compile(r"((\d+ (months|weeks) ending )|(As of ))(?P<year>\d{4,4})-(?P<month>\d{2,2})-(?P<day>\d{2,2})")
	#dateRe = re.compile(r"((\d+ (months|weeks) Ending )|(As of ))(?P<year>\d{4,4})-(?P<month>\d{2,2})-(?P<day>\d{2,2})")
	#as of 2/9/09 the 'Ending' went to 'ending'	
	
	QuarterlyIncomeDiv = 'incinterimdiv'
	AnnualIncomeDiv = 'incannualdiv'
	QuarterlyBalanceDiv = 'balinterimdiv'
	AnnualBalanceDiv = 'balannualdiv'
	QuarterlyCashDiv = 'casinterimdiv'
	AnnualCashDiv = 'casannualdiv'
	
	def __init__(self, rawHTML):
		soup = BeautifulSoup(rawHTML)
		
		#these look ups must be ordered as they appear here for findNextSibling to work.  and findNextSibling more closely resembles a linear search rather than
		#a random look up each time.  13% speedup right there.
		div = soup.find("div",id=ParsedFinancials.QuarterlyIncomeDiv)
		
		self.QuarterlyIncomeStatement = ParsedFinancials.ParsedIncomeStatement(div)
		self.exportElementsFrom(self.QuarterlyIncomeStatement,"Q_")
		
		div = div.findNextSibling("div",id=ParsedFinancials.AnnualIncomeDiv)
		self.AnnualIncomeStatement = ParsedFinancials.ParsedIncomeStatement(div)
		self.exportElementsFrom(self.AnnualIncomeStatement,"A_")
		
		div = div.findNextSibling("div",id=ParsedFinancials.QuarterlyBalanceDiv)
		self.QuarterlyBalanceSheet = ParsedFinancials.ParsedBalanceSheet(div)
		self.exportElementsFrom(self.QuarterlyBalanceSheet,"Q_")
		
		div = div.findNextSibling("div",id=ParsedFinancials.AnnualBalanceDiv)
		self.AnnualBalanceSheet = ParsedFinancials.ParsedBalanceSheet(div)
		self.exportElementsFrom(self.AnnualBalanceSheet,"A_")
		
		div = div.findNextSibling("div",id=ParsedFinancials.QuarterlyCashDiv)
		self.QuarterlyCashFlow = ParsedFinancials.ParsedCashFlowStatement(div)
		self.exportElementsFrom(self.QuarterlyCashFlow, "Q_")
		
		div = div.findNextSibling("div",id=ParsedFinancials.AnnualCashDiv)
		self.AnnualCashFlow = ParsedFinancials.ParsedCashFlowStatement(div)
		self.exportElementsFrom(self.AnnualCashFlow, "A_")

	def exportElementsFrom(self, parsedFinancialStatement,addName=""):
		""" Takes elements from the passed in financial statement and adds them to this top level one for easy access.
		
		Ex:
		
		>> pf = getFinancials("DD")
		>> pf.Revenue == pf.AnnualIncomeStatement.Revenue
		True
		
		"""
		
		for element in parsedFinancialStatement.getElements().keys():
			setattr(self,"".join([addName,element]),getattr(parsedFinancialStatement,element))
				
	class ParsedFinancialStatement(object):
		def __init__(self, soup):
			
			#while we can use just a random access style .find on any soup, doing these specific things in the order they are presented using .findNext
			#represents a more than doubling in speed.  since this class is built for all stocks on what could be a daily basis, it's important that we don't
			#spend too much time text processing and parsing.
			
			self.dates, div = self.findDates(soup)			
					
			for elem,regex in self.getElements().items():
				div = div.findNext(text=regex)
				found = self.findElem2(div)
				lst = self.findNumberList(found)
							
				self.setElem(elem, lst)
		
		def getDates(self):
			return sorted(self.dates)
				
		def findDates(self, soup):
			parsedDates = soup.findAll("td",valign="top",align=lambda elem: elem != "left")
			dateiterhelper = parsedDates[-1]
			foundDates = [ParsedFinancials.dateRe.search(parsedDate.string) for parsedDate in parsedDates]
			return ([self.buildDateFromParse(foundDate) for foundDate in foundDates], dateiterhelper)
		
		def buildDateFromParse(self, regexedDate):
			return date(int(regexedDate.group("year")), int(regexedDate.group("month")), int(regexedDate.group("day")))
		
		def findElem(self, regex, soup):
			return soup.find(text=regex).findParent("td").findNextSiblings("td")
		
		def findElem2(self, soup):
			return soup.findParent("td").findNextSiblings("td")
		
		def findNumberList(self, soups):
			string_list = [soup.find(text=ParsedFinancials.numberRe) for soup in soups]
			parsed_strings = [ParsedFinancials.numberRe.search(txt).group() for txt in string_list]
			clean_strings = [txt.replace(",","") for txt in parsed_strings]
			return [float(txt) if txt != '-' else None for txt in clean_strings] #need to account for '-'
		
		def setElem(self, elem, lst):
			setattr(self,elem, dict((date,number) for date,number in zip(self.dates,lst)))
	
	class ParsedIncomeStatement(ParsedFinancialStatement):	
		
		_elements = OrderedDict(("Revenue",re.compile("(?!(Other |Total |st of ))Revenue")),
							 	("OtherRevenue",re.compile("Other Revenue, Total")),
							 	("TotalRevenue",re.compile("Total Revenue")),
							 	("CostOfRevenue",re.compile("Cost of Revenue, Total")),
							 	("GrossProfit",re.compile("Gross Profit")),
							 	("SGAExpenses",re.compile("Selling/General/Admin[.] Expenses, Total")),
							 	("ResearchAndDevelopment",re.compile("Research & Development")),
							 	("DepreciationAmortization",re.compile("Depreciation/Amortization")),
							 	("InterestNetOperating",re.compile("Interest Expense\(Income\) - Net Operating")),
							 	("UnusualExpense",re.compile("Unusual Expense \(Income\)")),
							 	("OtherOperatingExpenses",re.compile("Other Operating Expenses, Total")),
							 	("TotalOperatingExpense",re.compile("Total Operating Expense")),
							 	("OperatingIncome",re.compile("Operating Income")),
							 	("InterestIncome",re.compile("Interest Income\(Expense\), Net Non-Operating")),
							 	("GainOnSaleOfAssets",re.compile("Gain \(Loss\) on Sale of Assets")),
							 	("OtherNet",re.compile("Other, Net")),
							 	("IncomeBeforeTax",re.compile("Income Before Tax")),
							 	("IncomeAfterTax",re.compile("Income After Tax")),
							 	("MinorityInterest_Inc",re.compile("Minority Interest")),
							 	("EquityInAffiliates",re.compile("Equity In Affiliates")),
							 	("NetIncomeBeforeExtraItems",re.compile("Net Income Before Extra[.] Items")),
							 	("AccountingChange",re.compile("Accounting Change")),
							 	("DiscontinuedOperations",re.compile("Discontinued Operations")),
							 	("ExtraordinaryItem",re.compile("Extraordinary Item(?!(s))")),
							 	("NetIncome",re.compile("Net Income(?!(([/]Starting Line)|( Before Extra[.] Items)|( after Stock Based Comp[.] Expense)))")),
							 	("PreferredDividends",re.compile("Preferred Dividends")),
							 	("IncomeAvailToCommonExclExtraItems",re.compile("Income Available to Common Excl[.] Extra Items")),
							 	("IncomeAvailToCommonInclExtraItems",re.compile("Income Available to Common Incl[.] Extra Items")),
							 	("BasicWeightedAverageShares",re.compile("Basic Weighted Average Shares")),
							 	("BasicEPSExclExtraItems",re.compile("Basic EPS Excluding Extraordinary Items")),
							 	("BasicEPSInclExtraItems",re.compile("Basic EPS Including Extraordinary Items")),
							 	("DilutionAdjustment",re.compile("Dilution Adjustment")),
							 	("DilutedWeightedAverageShares",re.compile("Diluted Weighted Average Shares")),
							 	("DilutedEPSExclExtraItems",re.compile("Diluted EPS Excluding Extraordinary Items")),
							 	("DilutedEPSInclExtraItems",re.compile("Diluted EPS Including Extraordinary Items")),
							 	("DividendsPerShare",re.compile("Dividends per Share - Common Stock Primary Issue")),
							 	("GrossDividends",re.compile("Gross Dividends - Common Stock")),
							 	("NetIncomeAfterCompExp",re.compile("Net Income after Stock Based Comp[.] Expense")),
							 	("BasicEPSAfterCompExp",re.compile("Basic EPS after Stock Based Comp[.] Expense")),
							 	("DilutedEPSAfterCompExp",re.compile("Diluted EPS after Stock Based Comp[.] Expense")),
							 	("DepreciationSupplemental",re.compile("Depreciation, Supplemental")),
							 	("TotalSpecialItems",re.compile("Total Special Items")),
							 	("NormalizedIncomeBeforeTaxes",re.compile("Normalized Income Before Taxes")),
							 	("EffectsOfSpecialItemsOnIncomeTaxes",re.compile("Effect of Special Items on Income Taxes")),
							 	("IncomeTaxesExSpecialItems",re.compile("Income Taxes Ex[.] Impact of Special Items")),
							 	("NormalizedIncomeAfterTaxes",re.compile("Normalized Income After Taxes")),
							 	("NormalizedIncomeAvailableCommon",re.compile("Normalized Income Avail to Common")),
							 	("BasicNormalizedEPS",re.compile("Basic Normalized EPS")),
							 	("DilutedNormalizedEPS",re.compile("Diluted Normalized EPS")))
		
		
		def getElements(self):
			return self._elements
			
	class ParsedCashFlowStatement(ParsedFinancialStatement):
		
		_elements = OrderedDict(("NetIncomeStartingLine",re.compile("Net Income/Starting Line")),
							 	("DepreciationDepletion",re.compile("Depreciation/Depletion")),
							 	("Amortization",re.compile("Amortization")),
							 	("DeferredTaxes",re.compile("Deferred Taxes")),
							 	("NonCashItems",re.compile("Non-Cash Items")),
							 	("ChangesInWorkingCapital",re.compile("Changes in Working Capital")),
							 	("CashFromOperatingActivities",re.compile("Cash from Operating Activities")),
							 	("CapitalExpenditures",re.compile("Capital Expenditures")),
							 	("OtherInvestingCashFlow",re.compile("Other Investing Cash Flow Items, Total")),
							 	("CashFromInvestingActivities",re.compile("Cash from Investing Activities")),
							 	("FinancingCashFlowItems",re.compile("Financing Cash Flow Items")),
							 	("TotalCashDividendsPaid",re.compile("Total Cash Dividends Paid")),
							 	("IssuanceOfStock",re.compile("Issuance \(Retirement\) of Stock, Net")),
							 	("IssuanceOfDebt",re.compile("Issuance \(Retirement\) of Debt, Net")),
							 	("CashFromFinancingActivities",re.compile("Cash from Financing Activities")),
							 	("ForeignExchangeEffects",re.compile("Foreign Exchange Effects")),
							 	("NetChangeInCash",re.compile("Net Change in Cash")),
							 	("CashInterestPaid",re.compile("Cash Interest Paid, Supplemental")),
							 	("CashTaxesPaid",re.compile("Cash Taxes Paid, Supplemental")))
		
		def getElements(self):
			return self._elements
	
	class ParsedBalanceSheet(ParsedFinancialStatement):
		
		_elements = OrderedDict(("CashAndEquivalents",re.compile("Cash & Equivalents")),
					 	 	   	("ShortTermInvestments",re.compile("Short Term Investments")),
					 			("CashAndShortTermInvestments",re.compile("Cash and Short Term Investments")),
					 			("AccountsReceivableTrade",re.compile("Accounts Receivable - Trade, Net")),
					 			("ReceivablesOther",re.compile("Receivables - Other")),
					 			("TotalReceivablesNet",re.compile("Total Receivables, Net")),
					 			("TotalInventory",re.compile("Total Inventory")),
					 			("PrepaidExpenses",re.compile("Prepaid Expenses")),
					 			("OtherCurrentAssetsTotal",re.compile("Other Current Assets, Total")),
					 			("TotalCurrentAssets",re.compile("Total Current Assets")),
					 			("PPE",re.compile("Property/Plant/Equipment, Total - Gross")),
					 			("Goodwill",re.compile("Goodwill, Net")),
					 			("Intangibles",re.compile("Intangibles, Net")),
					 			("LongTermInvestments",re.compile("Long Term Investments")),
					 			("OtherLongTermAssets",re.compile("Other Long Term Assets, Total")),
					 			("TotalAssets",re.compile("Total Assets")),
					 			("AccountsPayable",re.compile("Accounts Payable")),
					 			("AccruedExpenses",re.compile("Accrued Expenses")),
					 			("NotesPayable",re.compile("Notes Payable/Short Term Debt")),
					 			("CurrentPortLTDebtToCapital",re.compile("Current Port[.] of LT Debt/Capital Leases")),
					 			("OtherCurrentLiabilities",re.compile("Other Current liabilities, Total")),
					 			("TotalCurrentLiabilities",re.compile("Total Current Liabilities")),
					 			("LongTermDebt",re.compile("Long Term Debt")),
					 			("CapitalLeaseObligations",re.compile("Capital Lease Obligations")),
					 			("TotalLongTermDebt",re.compile("Total Long Term Debt")),
					 			("TotalDebt",re.compile("Total Debt")),
					 			("DeferredIncomeTax",re.compile("Deferred Income Tax")),
					 			("MinorityInterest_Bal",re.compile("Minority Interest")),
					 			("OtherLiabilities",re.compile("Other Liabilities, Total")),
					 			("TotalLiabilities",re.compile("Total Liabilities")),
					 			("RedeemablePreferredStock",re.compile("Redeemable Preferred Stock, Total")),
					 			("PreferredStockNonRedeemable",re.compile("Preferred Stock - Non Redeemable, Net")),
					 			("CommonStock",re.compile("Common Stock, Total")),
					 			("AdditionalPaidInCapital",re.compile("Additional Paid-In Capital")),
					 			("RetainedEarnings",re.compile("Retained Earnings \(Accumulated Deficit\)")),
					 			("TreasuryStock",re.compile("Treasury Stock - Common")),
					 			("OtherEquity",re.compile("Other Equity, Total")),
					 			("TotalEquity",re.compile("Total Equity")),
					 			("TotalLiabilitiesAndShareholdersEquity",re.compile("Total Liabilities & Shareholders' Equity")),
					 			("SharesOuts",re.compile("Shares Outs - Common Stock Primary Issue")),
					 			("TotalCommonSharesOutstanding",re.compile("Total Common Shares Outstanding")))
			
		def getElements(self):	
			return self._elements	
	
#translates key errors into date errors on Google Financial Functions
def ThrowsDateError(func):
	def _(symbol, date):
		try:
			return func(symbol, date)
		except KeyError, e:
			raise DateNotFound(symbol, date)
	return _

#this saves me a bit of typing and allows me to change how all the functions work
def GoogleFinancialsFunction(attr):
	def _(symbol, date):
		financials = getFinancials(symbol)
		val = getattr(financials,attr)
		return val[date]
	return ThrowsDateError(_)
GFF = GoogleFinancialsFunction

#date functions

def getAnnualIncomeStatementDates(symbol):
	return getFinancials(symbol).AnnualIncomeStatement.getDates()

def getAnnualBalanceSheetDates(symbol):
	return getFinancials(symbol).AnnualBalanceSheet.getDates()

def getAnnualCashFlowStatementDates(symbol):
	return getFinancials(symbol).AnnualCashFlow.getDates()

def getQuarterlyIncomeStatementDates(symbol):
	return getFinancials(symbol).QuarterlyIncomeStatement.getDates()

def getQuarterlyBalanceSheetDates(symbol):
	return getFinancials(symbol).QuarterlyBalanceSheet.getDates()

def getQuarterlyCashFlowStatementDates(symbol):
	return getFinancials(symbol).QuarterlyCashFlow.getDates()

#quarterly income statement functions

getQuarterlyRevenue = GFF("Q_Revenue")
getQuarterlyOtherRevenue = GFF("Q_OtherRevenue")
getQuarterlyTotalRevenue = GFF("Q_TotalRevenue")
getQuarterlyCostOfRevenue = GFF("Q_CostOfRevenue")
getQuarterlyGrossProfit = GFF("Q_GrossProfit")
getQuarterlySGAExpenses = GFF("Q_SGAExpenses")
getQuarterlyResearchAndDevelopment = GFF("Q_ResearchAndDevelopment")
getQuarterlyDepreciationAmortization = GFF("Q_DepreciationAmortization")
getQuarterlyInterestNetOperating = GFF("Q_InterestNetOperating")
getQuarterlyUnusualExpense = GFF("Q_UnusualExpense")
getQuarterlyOtherOperatingExpenses = GFF("Q_OtherOperatingExpenses")
getQuarterlyTotalOperatingExpense = GFF("Q_TotalOperatingExpense")
getQuarterlyOperatingIncome = GFF("Q_OperatingIncome")
getQuarterlyInterestIncome = GFF("Q_InterestIncome")
getQuarterlyGainOnSaleOfAssets = GFF("Q_GainOnSaleOfAssets")
getQuarterlyOtherNet = GFF("Q_OtherNet")
getQuarterlyIncomeBeforeTax = GFF("Q_IncomeBeforeTax")
getQuarterlyIncomeAfterTax = GFF("Q_IncomeAfterTax")
getQuarterlyMinorityInterest_Inc = GFF("Q_MinorityInterest_Inc")
getQuarterlyEquityInAffiliates = GFF("Q_EquityInAffiliates")
getQuarterlyNetIncomeBeforeExtraItems = GFF("Q_NetIncomeBeforeExtraItems")
getQuarterlyAccountingChange = GFF("Q_AccountingChange")
getQuarterlyDiscontinuedOperations = GFF("Q_DiscontinuedOperations")
getQuarterlyExtraordinaryItem = GFF("Q_ExtraordinaryItem")
getQuarterlyNetIncome = GFF("Q_NetIncome")
getQuarterlyPreferredDividends = GFF("Q_PreferredDividends")
getQuarterlyIncomeAvailToCommonExclExtraItems = GFF("Q_IncomeAvailToCommonExclExtraItems")
getQuarterlyIncomeAvailToCommonInclExtraItems = GFF("Q_IncomeAvailToCommonInclExtraItems")
getQuarterlyBasicWeightedAverageShares = GFF("Q_BasicWeightedAverageShares")
getQuarterlyBasicEPSExclExtraItems = GFF("Q_BasicEPSExclExtraItems")
getQuarterlyBasicEPSInclExtraItems = GFF("Q_BasicEPSInclExtraItems")
getQuarterlyDilutionAdjustment = GFF("Q_DilutionAdjustment")
getQuarterlyDilutedWeightedAverageShares = GFF("Q_DilutedWeightedAverageShares")
getQuarterlyDilutedEPSExclExtraItems = GFF("Q_DilutedEPSExclExtraItems")
getQuarterlyDilutedEPSInclExtraItems = GFF("Q_DilutedEPSInclExtraItems")
getQuarterlyDividendsPerShare = GFF("Q_DividendsPerShare")
getQuarterlyGrossDividends = GFF("Q_GrossDividends")
getQuarterlyNetIncomeAfterCompExp = GFF("Q_NetIncomeAfterCompExp")
getQuarterlyBasicEPSAfterCompExp = GFF("Q_BasicEPSAfterCompExp")
getQuarterlyDilutedEPSAfterCompExp = GFF("Q_DilutedEPSAfterCompExp")
getQuarterlyDepreciationSupplemental = GFF("Q_DepreciationSupplemental")
getQuarterlyTotalSpecialItems = GFF("Q_TotalSpecialItems")
getQuarterlyNormalizedIncomeBeforeTaxes = GFF("Q_NormalizedIncomeBeforeTaxes")
getQuarterlyEffectsOfSpecialItemsOnIncomeTaxes = GFF("Q_EffectsOfSpecialItemsOnIncomeTaxes")
getQuarterlyIncomeTaxesExSpecialItems = GFF("Q_IncomeTaxesExSpecialItems")
getQuarterlyNormalizedIncomeAfterTaxes = GFF("Q_NormalizedIncomeAfterTaxes")
getQuarterlyNormalizedIncomeAvailableCommon = GFF("Q_NormalizedIncomeAvailableCommon")
getQuarterlyBasicNormalizedEPS = GFF("Q_BasicNormalizedEPS")
getQuarterlyDilutedNormalizedEPS = GFF("Q_DilutedNormalizedEPS")

#quarterly balance sheet functions

getQuarterlyCashAndEquivalents = GFF("Q_CashAndEquivalents")
getQuarterlyShortTermInvestments = GFF("Q_ShortTermInvestments")
getQuarterlyCashAndShortTermInvestments = GFF("Q_CashAndShortTermInvestments")
getQuarterlyAccountsReceivableTrade = GFF("Q_AccountsReceivableTrade")
getQuarterlyReceivablesOther = GFF("Q_ReceivablesOther")
getQuarterlyTotalReceivablesNet = GFF("Q_TotalReceivablesNet")
getQuarterlyTotalInventory = GFF("Q_TotalInventory")
getQuarterlyPrepaidExpenses = GFF("Q_PrepaidExpenses")
getQuarterlyOtherCurrentAssetsTotal = GFF("Q_OtherCurrentAssetsTotal")
getQuarterlyTotalCurrentAssets = GFF("Q_TotalCurrentAssets")
getQuarterlyPPE = GFF("Q_PPE")
getQuarterlyGoodwill = GFF("Q_Goodwill")
getQuarterlyIntangibles = GFF("Q_Intangibles")
getQuarterlyLongTermInvestments = GFF("Q_LongTermInvestments")
getQuarterlyOtherLongTermAssets = GFF("Q_OtherLongTermAssets")
getQuarterlyTotalAssets = GFF("Q_TotalAssets")
getQuarterlyAccountsPayable = GFF("Q_AccountsPayable")
getQuarterlyAccruedExpenses = GFF("Q_AccruedExpenses")
getQuarterlyNotesPayable = GFF("Q_NotesPayable")
getQuarterlyCurrentPortLTDebtToCapital = GFF("Q_CurrentPortLTDebtToCapital")
getQuarterlyOtherCurrentLiabilities = GFF("Q_OtherCurrentLiabilities")
getQuarterlyTotalCurrentLiabilities = GFF("Q_TotalCurrentLiabilities")
getQuarterlyLongTermDebt = GFF("Q_LongTermDebt")
getQuarterlyCapitalLeaseObligations = GFF("Q_CapitalLeaseObligations")
getQuarterlyTotalLongTermDebt = GFF("Q_TotalLongTermDebt")
getQuarterlyTotalDebt = GFF("Q_TotalDebt")
getQuarterlyDeferredIncomeTax = GFF("Q_DeferredIncomeTax")
getQuarterlyMinorityInterest_Bal = GFF("Q_MinorityInterest_Bal")
getQuarterlyOtherLiabilities = GFF("Q_OtherLiabilities")
getQuarterlyTotalLiabilities = GFF("Q_TotalLiabilities")
getQuarterlyRedeemablePreferredStock = GFF("Q_RedeemablePreferredStock")
getQuarterlyPreferredStockNonRedeemable = GFF("Q_PreferredStockNonRedeemable")
getQuarterlyCommonStock = GFF("Q_CommonStock")
getQuarterlyAdditionalPaidInCapital = GFF("Q_AdditionalPaidInCapital")
getQuarterlyRetainedEarnings = GFF("Q_RetainedEarnings")
getQuarterlyTreasuryStock = GFF("Q_TreasuryStock")
getQuarterlyOtherEquity = GFF("Q_OtherEquity")
getQuarterlyTotalEquity = GFF("Q_TotalEquity")
getQuarterlyTotalLiabilitiesAndShareholdersEquity = GFF("Q_TotalLiabilitiesAndShareholdersEquity")
getQuarterlySharesOuts = GFF("Q_SharesOuts")
getQuarterlyTotalCommonSharesOutstanding = GFF("Q_TotalCommonSharesOutstanding")

#quarterly cash flow functions

getQuarterlyNetIncomeStartingLine = GFF("Q_NetIncomeStartingLine")
getQuarterlyDepreciationDepletion = GFF("Q_DepreciationDepletion")
getQuarterlyAmortization = GFF("Q_Amortization")
getQuarterlyDeferredTaxes = GFF("Q_DeferredTaxes")
getQuarterlyNonCashItems = GFF("Q_NonCashItems")
getQuarterlyChangesInWorkingCapital = GFF("Q_ChangesInWorkingCapital")
getQuarterlyCashFromOperatingActivities = GFF("Q_CashFromOperatingActivities")
getQuarterlyCapitalExpenditures = GFF("Q_CapitalExpenditures")
getQuarterlyOtherInvestingCashFlow = GFF("Q_OtherInvestingCashFlow")
getQuarterlyCashFromInvestingActivities = GFF("Q_CashFromInvestingActivities")
getQuarterlyFinancingCashFlowItems = GFF("Q_FinancingCashFlowItems")
getQuarterlyTotalCashDividendsPaid = GFF("Q_TotalCashDividendsPaid")
getQuarterlyIssuanceOfStock = GFF("Q_IssuanceOfStock")
getQuarterlyIssuanceOfDebt = GFF("Q_IssuanceOfDebt")
getQuarterlyCashFromFinancingActivities = GFF("Q_CashFromFinancingActivities")
getQuarterlyForeignExchangeEffects = GFF("Q_ForeignExchangeEffects")
getQuarterlyNetChangeInCash = GFF("Q_NetChangeInCash")
getQuarterlyCashInterestPaid = GFF("Q_CashInterestPaid")
getQuarterlyCashTaxesPaid = GFF("Q_CashTaxesPaid")

#Annual income statement functions

getAnnualRevenue = GFF("A_Revenue")
getAnnualOtherRevenue = GFF("A_OtherRevenue")
getAnnualTotalRevenue = GFF("A_TotalRevenue")
getAnnualCostOfRevenue = GFF("A_CostOfRevenue")
getAnnualGrossProfit = GFF("A_GrossProfit")
getAnnualSGAExpenses = GFF("A_SGAExpenses")
getAnnualResearchAndDevelopment = GFF("A_ResearchAndDevelopment")
getAnnualDepreciationAmortization = GFF("A_DepreciationAmortization")
getAnnualInterestNetOperating = GFF("A_InterestNetOperating")
getAnnualUnusualExpense = GFF("A_UnusualExpense")
getAnnualOtherOperatingExpenses = GFF("A_OtherOperatingExpenses")
getAnnualTotalOperatingExpense = GFF("A_TotalOperatingExpense")
getAnnualOperatingIncome = GFF("A_OperatingIncome")
getAnnualInterestIncome = GFF("A_InterestIncome")
getAnnualGainOnSaleOfAssets = GFF("A_GainOnSaleOfAssets")
getAnnualOtherNet = GFF("A_OtherNet")
getAnnualIncomeBeforeTax = GFF("A_IncomeBeforeTax")
getAnnualIncomeAfterTax = GFF("A_IncomeAfterTax")
getAnnualMinorityInterest_Inc = GFF("A_MinorityInterest_Inc")
getAnnualEquityInAffiliates = GFF("A_EquityInAffiliates")
getAnnualNetIncomeBeforeExtraItems = GFF("A_NetIncomeBeforeExtraItems")
getAnnualAccountingChange = GFF("A_AccountingChange")
getAnnualDiscontinuedOperations = GFF("A_DiscontinuedOperations")
getAnnualExtraordinaryItem = GFF("A_ExtraordinaryItem")
getAnnualNetIncome = GFF("A_NetIncome")
getAnnualPreferredDividends = GFF("A_PreferredDividends")
getAnnualIncomeAvailToCommonExclExtraItems = GFF("A_IncomeAvailToCommonExclExtraItems")
getAnnualIncomeAvailToCommonInclExtraItems = GFF("A_IncomeAvailToCommonInclExtraItems")
getAnnualBasicWeightedAverageShares = GFF("A_BasicWeightedAverageShares")
getAnnualBasicEPSExclExtraItems = GFF("A_BasicEPSExclExtraItems")
getAnnualBasicEPSInclExtraItems = GFF("A_BasicEPSInclExtraItems")
getAnnualDilutionAdjustment = GFF("A_DilutionAdjustment")
getAnnualDilutedWeightedAverageShares = GFF("A_DilutedWeightedAverageShares")
getAnnualDilutedEPSExclExtraItems = GFF("A_DilutedEPSExclExtraItems")
getAnnualDilutedEPSInclExtraItems = GFF("A_DilutedEPSInclExtraItems")
getAnnualDividendsPerShare = GFF("A_DividendsPerShare")
getAnnualGrossDividends = GFF("A_GrossDividends")
getAnnualNetIncomeAfterCompExp = GFF("A_NetIncomeAfterCompExp")
getAnnualBasicEPSAfterCompExp = GFF("A_BasicEPSAfterCompExp")
getAnnualDilutedEPSAfterCompExp = GFF("A_DilutedEPSAfterCompExp")
getAnnualDepreciationSupplemental = GFF("A_DepreciationSupplemental")
getAnnualTotalSpecialItems = GFF("A_TotalSpecialItems")
getAnnualNormalizedIncomeBeforeTaxes = GFF("A_NormalizedIncomeBeforeTaxes")
getAnnualEffectsOfSpecialItemsOnIncomeTaxes = GFF("A_EffectsOfSpecialItemsOnIncomeTaxes")
getAnnualIncomeTaxesExSpecialItems = GFF("A_IncomeTaxesExSpecialItems")
getAnnualNormalizedIncomeAfterTaxes = GFF("A_NormalizedIncomeAfterTaxes")
getAnnualNormalizedIncomeAvailableCommon = GFF("A_NormalizedIncomeAvailableCommon")
getAnnualBasicNormalizedEPS = GFF("A_BasicNormalizedEPS")
getAnnualDilutedNormalizedEPS = GFF("A_DilutedNormalizedEPS")

#Annual balance sheet functions

getAnnualCashAndEquivalents = GFF("A_CashAndEquivalents")
getAnnualShortTermInvestments = GFF("A_ShortTermInvestments")
getAnnualCashAndShortTermInvestments = GFF("A_CashAndShortTermInvestments")
getAnnualAccountsReceivableTrade = GFF("A_AccountsReceivableTrade")
getAnnualReceivablesOther = GFF("A_ReceivablesOther")
getAnnualTotalReceivablesNet = GFF("A_TotalReceivablesNet")
getAnnualTotalInventory = GFF("A_TotalInventory")
getAnnualPrepaidExpenses = GFF("A_PrepaidExpenses")
getAnnualOtherCurrentAssetsTotal = GFF("A_OtherCurrentAssetsTotal")
getAnnualTotalCurrentAssets = GFF("A_TotalCurrentAssets")
getAnnualPPE = GFF("A_PPE")
getAnnualGoodwill = GFF("A_Goodwill")
getAnnualIntangibles = GFF("A_Intangibles")
getAnnualLongTermInvestments = GFF("A_LongTermInvestments")
getAnnualOtherLongTermAssets = GFF("A_OtherLongTermAssets")
getAnnualTotalAssets = GFF("A_TotalAssets")
getAnnualAccountsPayable = GFF("A_AccountsPayable")
getAnnualAccruedExpenses = GFF("A_AccruedExpenses")
getAnnualNotesPayable = GFF("A_NotesPayable")
getAnnualCurrentPortLTDebtToCapital = GFF("A_CurrentPortLTDebtToCapital")
getAnnualOtherCurrentLiabilities = GFF("A_OtherCurrentLiabilities")
getAnnualTotalCurrentLiabilities = GFF("A_TotalCurrentLiabilities")
getAnnualLongTermDebt = GFF("A_LongTermDebt")
getAnnualCapitalLeaseObligations = GFF("A_CapitalLeaseObligations")
getAnnualTotalLongTermDebt = GFF("A_TotalLongTermDebt")
getAnnualTotalDebt = GFF("A_TotalDebt")
getAnnualDeferredIncomeTax = GFF("A_DeferredIncomeTax")
getAnnualMinorityInterest_Bal = GFF("A_MinorityInterest_Bal")
getAnnualOtherLiabilities = GFF("A_OtherLiabilities")
getAnnualTotalLiabilities = GFF("A_TotalLiabilities")
getAnnualRedeemablePreferredStock = GFF("A_RedeemablePreferredStock")
getAnnualPreferredStockNonRedeemable = GFF("A_PreferredStockNonRedeemable")
getAnnualCommonStock = GFF("A_CommonStock")
getAnnualAdditionalPaidInCapital = GFF("A_AdditionalPaidInCapital")
getAnnualRetainedEarnings = GFF("A_RetainedEarnings")
getAnnualTreasuryStock = GFF("A_TreasuryStock")
getAnnualOtherEquity = GFF("A_OtherEquity")
getAnnualTotalEquity = GFF("A_TotalEquity")
getAnnualTotalLiabilitiesAndShareholdersEquity = GFF("A_TotalLiabilitiesAndShareholdersEquity")
getAnnualSharesOuts = GFF("A_SharesOuts")
getAnnualTotalCommonSharesOutstanding = GFF("A_TotalCommonSharesOutstanding")

#Annual cash flow functions

getAnnualNetIncomeStartingLine = GFF("A_NetIncomeStartingLine")
getAnnualDepreciationDepletion = GFF("A_DepreciationDepletion")
getAnnualAmortization = GFF("A_Amortization")
getAnnualDeferredTaxes = GFF("A_DeferredTaxes")
getAnnualNonCashItems = GFF("A_NonCashItems")
getAnnualChangesInWorkingCapital = GFF("A_ChangesInWorkingCapital")
getAnnualCashFromOperatingActivities = GFF("A_CashFromOperatingActivities")
getAnnualCapitalExpenditures = GFF("A_CapitalExpenditures")
getAnnualOtherInvestingCashFlow = GFF("A_OtherInvestingCashFlow")
getAnnualCashFromInvestingActivities = GFF("A_CashFromInvestingActivities")
getAnnualFinancingCashFlowItems = GFF("A_FinancingCashFlowItems")
getAnnualTotalCashDividendsPaid = GFF("A_TotalCashDividendsPaid")
getAnnualIssuanceOfStock = GFF("A_IssuanceOfStock")
getAnnualIssuanceOfDebt = GFF("A_IssuanceOfDebt")
getAnnualCashFromFinancingActivities = GFF("A_CashFromFinancingActivities")
getAnnualForeignExchangeEffects = GFF("A_ForeignExchangeEffects")
getAnnualNetChangeInCash = GFF("A_NetChangeInCash")
getAnnualCashInterestPaid = GFF("A_CashInterestPaid")
getAnnualCashTaxesPaid = GFF("A_CashTaxesPaid")

@cached(100)
def getMetadata(symbol):
	
	#resolve to google style symbols
	symbol = resolver.getGoogle(symbol)
	
	args = {}
	args['q'] = symbol
		
	url = financialsURL(args)
	raw_url = urlunparse(url)
	
	#print raw_url
	
	try:
		return ParsedMetadata(urlopen(raw_url))
	except HTTPError, e:
		raise SymbolNotFound(symbol)
	
class ParsedMetadata(object):
	
	currencyRe = re.compile("\(In millions of (?P<currency>[A-Z]+)\)")
	exchangeRe = re.compile("\(([A-z]+, )?(?P<exchange>[A-Z]+):(?P<symbol>[A-Z0-9]+)\)")
	sectorRe = re.compile("Sector:")
	industryRe = re.compile("Industry:")
	competitorRe = re.compile("rct-[0-9]")
	
	def __init__(self, rawHTML):
		soup = BeautifulSoup(rawHTML)
		
		#if this type of lookup is still too slow, ordering them and using the previously found item may speed things up.  thesse are currently not ordered.
		self.currency = ParsedMetadata.currencyRe.search(soup.find(text=ParsedMetadata.currencyRe)).group("currency")
		self.exchange = ParsedMetadata.exchangeRe.search(soup.find(text=ParsedMetadata.exchangeRe)).group("exchange")
		self.sector = soup.find(text=lambda navstr: "Sector:" in navstr).next.string
		self.industry = soup.find(text=lambda navstr: "Industry:" in navstr).next.string
		self.properName = soup.find('div',attrs={'class':'tophdg'}).h1.string
		self.symbol = ParsedMetadata.exchangeRe.search(soup.find(text=ParsedMetadata.exchangeRe)).group("symbol")
		self.competitors = [competitor.string for competitor in soup.findAll("a",id=ParsedMetadata.competitorRe)]

def getCurrencyReported(symbol):
	return getMetadata(symbol).currency

def getExchange(symbol):
	return getMetadata(symbol).exchange

def getSector(symbol):
	return getMetadata(symbol).sector

def getIndustry(symbol):
	return getMetadata(symbol).industry

def getProperName(symbol):
	return getMetadata(symbol).properName

def getSymbol(symbol):
	return getMetadata(symbol).symbol

def getCompetitors(symbol):
	return getMetadata(symbol).competitors

Register("Industry",getIndustry)
Register("QuarterlyCashFlowStatementDates",getQuarterlyCashFlowStatementDates)
Register("QuarterlyBalanceSheetDates",getQuarterlyBalanceSheetDates)
Register("QuarterlyIncomeStatementDates",getQuarterlyIncomeStatementDates)
Register("AnnualCashFlowStatementDates",getAnnualCashFlowStatementDates)
Register("AnnualBalanceSheetDates",getAnnualBalanceSheetDates)
Register("AnnualIncomeStatementDates",getAnnualIncomeStatementDates)

Register("AnnualPreferredDividends",getAnnualPreferredDividends)
Register("QuarterlyPreferredDividends",getQuarterlyPreferredDividends)
Register("AnnualNetIncome",getAnnualNetIncome)
Register("QuarterlyNetIncome",getQuarterlyNetIncome)
Register("AnnualRevenue",getAnnualRevenue)
Register("QuarterlyRevenue",getQuarterlyRevenue)
Register("AnnualUnusualExpense",getAnnualUnusualExpense)
Register("QuarterlyUnusualExpense",getQuarterlyUnusualExpense)

Register("QuarterlyCashAndEquivalents",getQuarterlyCashAndEquivalents)
Register("AnnualCashAndEquivalents",getAnnualCashAndEquivalents)
Register("AnnualTotalCommonSharesOutstanding",getAnnualTotalCommonSharesOutstanding)
Register("QuarterlyTotalCommonSharesOutstanding",getQuarterlyTotalCommonSharesOutstanding)

Register("QuarterlyNetIncomeStartingLine", getQuarterlyNetIncomeStartingLine)
Register("AnnualNetIncomeStartingLine", getAnnualNetIncomeStartingLine)