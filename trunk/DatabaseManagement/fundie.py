import re, datetime, urllib2, copy
from scipy import stats

dateparse = re.compile(r"[0-9]{4,4}-[0-9]{2,2}-[0-9]{2,2}")
webparse = re.compile(r"(5[0-9] weeks Ending)|((1[0-2]|[1-9]) months Ending)|(As of)")
moneyparse = re.compile(r"(-?([0-9]{0,3},?)*[0-9]{0,3}\.[0-9]{0,2})|(-)")
moneyparseslim = re.compile(r"-?([0-9]{0,3},?)*[0-9]{0,3}\.[0-9]{0,2}")


incomeStatementWords = 	["Revenue", "Other Revenue, Total", "Total Revenue", "Cost of Revenue, Total", "Gross Profit", r"Selling/General/Admin. Expenses, Total", "Research & Development", r"Depreciation/Amortization", r"Interest Expense(Income) - Net Operating", "Unusual Expense (Income)", "Other Operating Expenses, Total", "Total Operating Expense", "Operating Income", r"Interest Income(Expense), Net Non-Operating", "Gain (Loss) on Sale of Assets", "Other, Net", "Income Before Tax", "Income After Tax", "Minority Interest", "Equity In Affiliates", r"Net Income Before Extra. Items", "Accounting Change", "Discontinued Operations", "Extraordinary Item", "Net Income", "Preferred Dividends", r"Income Available to Common Excl. Extra Items", r"Income Available to Common Incl. Extra Items", "Basic Weighted Average Shares", "Basic EPS Excluding Extraordinary Items", "Basic EPS Including Extraordinary Items", "Dilution Adjustment", "Diluted Weighted Average Shares", "Diluted EPS Excluding Extraordinary Items", "Diluted EPS Including Extraordinary Items", r"Dividends per Share - Common Stock Primary Issue", "Gross Dividends - Common Stock", "Net Income after Stock Based Comp. Expense", "Basic EPS after Stock Based Comp. Expense", "Diluted EPS after Stock Based Comp. Expense", "Depreciation, Supplemental", "Total Special Items", "Normalized Income Before Taxes", "Effect of Special Items on Income Taxes", "Income Taxes Ex. Impact of Special Items", "Normalized Income After Taxes", "Normalized Income Avail to Common", "Basic Normalized EPS", "Diluted Normalized EPS"]

balanceSheetWords = ["Cash & Equivalents", "Short Term Investments", "Cash and Short Term Investments", r"Accounts Receivable - Trade, Net", "Receivables - Other", "Total Receivables, Net", "Total Inventory", "Prepaid Expenses", "Other Current Assets, Total", "Total Current Assets", r"Property/Plant/Equipment, Total - Gross", "Goodwill, Net", "Intangibles, Net", "Long Term Investments", "Other Long Term Assets, Total", "Total Assets", "Accounts Payable", "Accrued Expenses", "Notes Payable/Short Term Debt", r"Current Port. of LT Debt/Capital Leases", "Other Current liabilities, Total", "Total Current Liabilities", "Long Term Debt", "Capital Lease Obligations", "Total Long Term Debt", "Total Debt", "Deferred Income Tax", "Minority Interest", "Other Liabilities, Total", "Total Liabilities", "Redeemable Preferred Stock, Total", "Preferred Stock - Non Redeemable, Net", "Common Stock, Total", r"Additional Paid-In Capital", "Retained Earnings (Accumulated Deficit)", r"Treasury Stock - Common", "Other Equity, Total", "Total Equity", "Total Liabilities & Shareholders' Equity", "Shares Outs - Common Stock Primary Issue", "Total Common Shares Outstanding"]

cashFlowsWords = [r"Net Income/Starting Line", r"Depreciation/Depletion", "Amortization", "Deferred Taxes", r"Non-Cash Items", "Changes in Working Capital", "Cash from Operating Activities", "Capital Expenditures", "Other Investing Cash Flow Items, Total", "Cash from Investing Activities", "Financing Cash Flow Items", "Total Cash Dividends Paid", "Issuance (Retirement) of Stock, Net", "Issuance (Retirement) of Debt, Net", "Cash from Financing Activities", "Foreign Exchange Effects", "Net Change in Cash", "Cash Interest Paid, Supplemental", "Cash Taxes Paid, Supplemental"]

class WebAccessError(Exception):
	def __init__(self, args, symbol="Unknown"):
		self.args = args
		self.symbol = symbol
	def __str__(self):
		return repr(self.args)

class WebDataError(Exception):
	def __init__(self, args):
		self.args = args
	def __str__(self):
		return repr(self.args)

class WebInfoNotFound(Exception):
	def __init__(self, args, symbol="Unknown"):
		self.args = args
		self.symbol = symbol
	def __str__(self):
		return repr(self.args)

def isValid(symbol):
	url = "http://finance.yahoo.com/q?s=" + symbol

	try:
		table = urllib2.urlopen(url).read()
	except urllib2.URLError, e:
		raise WebAccessError("Network down.", symbol)
	except httplib.BadStatusLine, e:
		raise WebAccessError("Bad Status.", symbol)

	if "is not a valid ticker symbol" in table or "is no longer valid. It has changed to" in table:
#		print symbol + " is invalid"
		return False
	else:
		return True

def getLatestPrices(symbol, fromDate, toDate):
	prices = {}

	url = "http://ichart.finance.yahoo.com/table.csv?s=" + symbol + "&d=" + str(toDate.month-1) +\
			"&e=" + str(toDate.day) + "&f=" + str(toDate.year) + "&g=d&a=" + str(fromDate.month-1) +\
			"&b=" + str(fromDate.day) + "&c=" + str(fromDate.year) + "&ignore=.csv"


	try:
		table = urllib2.urlopen(url).read()
	except urllib2.HTTPError, e:
		raise WebInfoNotFound("Information on " + symbol + " cannot be found", symbol)
	except urllib2.URLError, e:
		raise WebAccessError("Network down.", symbol)
	if "Historical quote data is unavailable for the specified date range." in table:
		raise WebInfoNotFound("Information on " + symbol + " from " + str(fromDate) + " to " + str(toDate) + " cannot be found")
	table = table.split('\n')
	table = table[1:-1]
	for element in table:
		date = element.split(',')
		data = {'open' : float(date[1]), 'high' : float(date[2]), 'low' : float(date[3]), \
				'close' : float(date[4]), 'volume' : float(date[5])}
		prices[convertDateYahoo(date[0])] = data
	return prices

def convertDateYahoo(string):
	toConvert = string.split('-')
	return datetime.date(int(toConvert[0]), int(toConvert[1]), int(toConvert[2]))

def checkBlank(stringToCheck, printme = True):
	if (moneyparseslim.search(stringToCheck)):
		if(moneyparseslim.search(stringToCheck).group() != '.'):
			b = float(moneyparseslim.search(stringToCheck).group().replace(',',''))
			return b
	return '-'

#new function
def getFinancialWebsite(symbol):
	url = "http://finance.google.com/finance?fstype=ii&q="+symbol

	try:
		webpage = urllib2.urlopen(url).read()
	except urllib2.HTTPError, e:
		raise WebInfoNotFound("Information on " + symbol + " cannot be found.")
	except urllib2.URLError, e:
		raise WebAccessError("Network down.")
	return webpage

def getAvailableDates(webpage, fromDelimiter, toDelimiter):
	webtemp = webpage
	dates = []
	mydates = []
	webtemp = webtemp[webpage.find(fromDelimiter):webpage.find(toDelimiter)]
	temp = webparse.search(webtemp)
	while(temp != None):
		webtemp = webtemp[temp.start()+len(temp.group()):]
		datetemp = dateparse.search(webtemp)
		dates.append(datetemp.group())
		temp = webparse.search(webtemp)

	for date in dates:
		mydates.append(datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])))
	return mydates		

def getIncomeDates(webpage):
	return getAvailableDates(webpage, "incannualdiv", "balinterimdiv")

def getBalanceDates(webpage):
	return getAvailableDates(webpage, "balannualdiv", "casinterimdiv")

def getCashDates(webpage):
	return getAvailableDates(webpage, "casannualdiv", r"</html>")


def getWebpageDates(webpage):
	webtemp = webpage
	dates = []
	mydates = []
	webtemp = webtemp[webpage.find("incannualdiv"):]
	temp = webparse.search(webtemp)
	while(temp != None):
		webtemp = webtemp[temp.start()+1:]
		datetemp = dateparse.search(webtemp)
#		print datetemp.group()
		dates.append(datetemp.group())
		temp = webparse.search(webtemp)
		if(temp.start() > webtemp.find("balinterimdiv")):
				temp = None


	for date in dates:
		mydates.append(datetime.date(int(date[0:4]), int(date[5:7]), int(date[8:10])))
	#removing duplicates
	fundbase = {}
	for date in mydates:
		if(date not in fundbase.keys()):
			fundbase[date] = []
			
	orderedkeys = fundbase.keys()
	orderedkeys.sort()
	orderedkeys.reverse()
	#print orderedkeys
	return orderedkeys

def seedFundamentals():
	toReturn = {}
	for word in incomeStatementWords:
		toReturn[word] = '-'
	for word in balanceSheetWords:
		toReturn[word] = '-'
	for word in cashFlowsWords:
		toReturn[word] = '-'
	
	return toReturn

def marshall(dictToMarshall):
	"Turns a fundamentals dictionary, like from seedFundamentals, into an array in proper order."
	toReturn = []
	for word in incomeStatementWords:
		#FIX THIS, right now your database left these two out somehow, so i have to rip them out of all additions.  I need to redo this such that
		#I can ask a 'fundamental website' if it has specific dates worth of specific peices of information, instead of scrolling through it.
		#that way i can update everyone's stuff that is missing.
		if word != r"Income Available to Common Incl. Extra Items" and word != "Basic EPS Excluding Extraordinary Items":
			toReturn.append(dictToMarshall[word])
		if word == r"Income Available to Common Incl. Extra Items" or word == "Basic EPS Excluding Extraordinary Items":
			pass
			#print word
			#TODO FIXTHIS, neither of these two fundamentals are included because you forgot them in your database.  you need to rewrite this
			#such that it will scan the fundamentals in the database and look for a specific spot that's missing, then search for that same
			#item in the webpage and update it.
	for word in balanceSheetWords:
		toReturn.append(dictToMarshall[word])
	for word in cashFlowsWords:
		toReturn.append(dictToMarshall[word])
	return toReturn

def getIncomeStatement(webpage, symbol, dateIndecies):
	incomeStatement = {}
	for date in dateIndecies:
		if(date[0]):
			incomeStatement[date[1]] = {}

	incomestatementindex = webpage.find("incannualdiv")
	balancesheetindex = webpage.find("balannualdiv")
	webtemp = webpage[incomestatementindex:balancesheetindex]

	for incomeWord in incomeStatementWords:
		webtemp = webtemp[webtemp.find(incomeWord)+len(incomeWord):] #find the word and pad it
		for date in dateIndecies:
			incomematch = moneyparse.search(webtemp)
			if(date[0]):
				incomeStatement[date[1]][incomeWord] = checkBlank(incomematch.group())
			webtemp = webtemp[incomematch.start()+len(incomematch.group()):] #pad it out by the numbers found
	

	#done
	return incomeStatement

def getBalanceSheet(webpage, symbol, dateIndecies):
	balanceSheet = {}
	for date in dateIndecies:
		if(date[0]):
			balanceSheet[date[1]] = {}

	balancesheetindex = webpage.find("balannualdiv")
	cashflowindex = webpage.find("casannualdiv")
	webtemp = webpage[balancesheetindex:cashflowindex]

	for balanceWord in balanceSheetWords:
		webtemp = webtemp[webtemp.find(balanceWord)+len(balanceWord):] #find the word and pad it
		for date in dateIndecies:
			balancematch = moneyparse.search(webtemp)
			if(date[0]):
				balanceSheet[date[1]][balanceWord] = checkBlank(balancematch.group())
			webtemp = webtemp[balancematch.start()+len(balancematch.group()):] #pad it out by the numbers found
	
	#done
	return balanceSheet

def getCashFlows(webpage, symbol, dateIndecies):
	cashFlows = {}
	for date in dateIndecies:
		if(date[0]):
			cashFlows[date[1]] = {}

	cashflowsindex = webpage.find("casannualdiv")
	endindex = webpage.find(r"<\html>")
	webtemp = webpage[cashflowsindex:endindex]

	for cashWord in cashFlowsWords:
		webtemp = webtemp[webtemp.find(cashWord)+len(cashWord):] #find the word and pad it
		for date in dateIndecies:
			cashmatch = moneyparse.search(webtemp)
			if(date[0]):
				cashFlows[date[1]][cashWord] = checkBlank(cashmatch.group())
			webtemp = webtemp[cashmatch.start()+len(cashmatch.group()):] #pad it out by the numbers found
	
	#done
	return cashFlows
