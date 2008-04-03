""" Used to download SEC financial information from finance.google.org

Examples:
>>> from datetime import date
>>> scraper = Google()
>>> round(scraper.getQuarterlyRevenue("MRK", datetime.date(2007,12,31)))
6243.0

>>> round(scraper.getQuarterlyGoodwill("IBM", date(2007,9,30)))
13843.0

>> round(scraper.getQuarterlyChangesInWorkingCapital("SBUX", date(2007,07,01)))
-4.00

Or, leave off the date and get whole dicts:

>>> scraper.getAnnualOtherRevenue("XOM") == {date(2007,12,31):14224.0,\
                                             date(2006,12,31):12168.0,\
                                             date(2005,12,31):11725.0,\
                                             date(2004,12,31):6783.0,\
                                             date(2003,12,31):9684.0,\
                                             date(2002,12,31):3557.0}
True

>>> scraper.getAnnualShortTermInvestments("CVX") == {date(2007,12,31):732.0,\
                                           date(2006,12,31):953.0,\
                                           date(2005,12,31):1101.0,\
                                           date(2004,12,31):1451.0,\
                                           date(2003,12,31):1001.0,\
                                           date(2002,12,31):824.0}
True

>>> scraper.getAnnualDeferredTaxes("RDS.A") == {date(2007,12,31):-773.00,\
                                                date(2006,12,31):1833.0,\
                                                date(2005,12,31):-1515.0,\
                                                date(2004,12,31):-1007.0}
True

Only difference between annual and quarterly data is in the name:

>>> scraper.getQuarterlyOtherRevenue("BP") == {date(2007,12,31):3938.0,\
                                               date(2007,6,30):1610.0,\
                                               date(2007,3,31):1076.0,\
                                               date(2006,12,31):602.0,\
                                               date(2006,9,30):2584.0}
True

>>> scraper.getQuarterlyShortTermInvestments("MSFT") == {date(2007,12,31):13616.0,\
                                                         date(2007,9,30):14937.0,\
                                                         date(2007,6,30):17300.0,\
                                                         date(2007,3,31):20625.0,\
                                                         date(2006,12,31):22014.0}
True

>>> scraper.getQuarterlyDeferredTaxes("YHOO") == {date(2007,12,31):-78.16,\
                                                  date(2007,9,30):-43.75,\
                                                  date(2007,6,30):-48.54,\
                                                  date(2007,3,31):-42.30}
True

"""

from BeautifulSoup import BeautifulSoup
import urllib2
import re
import datetime
import FinancialXML

class SymbolNotFound(Exception):
	""" Raised when a symbol is not found or information for it cannot be found """
	def __init__(self, symbol, *args, **kwargs):
		self.symbol = symbol
		super(SymbolNotFound,self).__init__(*args, **kwargs)
		
		
	def __repr__(self):
		return "Could not find symbol : %s \n%s" % (self.symbol, super(SymbolNotFound,self).__repr__())
	
class SymbolHasNoFinancials(Exception):
	""" Raised when a symbol is a tracked company, but the company has no SEC documents
	available.
	"""
	
	def __init__(self, symbol, *args, **kwargs):
		self.symbol = symbol
		super(SymbolHasNoFinancials,self).__init__(*args, **kwargs)
		
	def __repr__(self):
		return "Symbol does not support financials: %s \n%s"  % (self.symbol, super(SymbolHasNoFinancials,self).__repr__())
	
class DateNotFound(Exception):
	""" Raised when a requested date is not available for a peice of information on
	a stock. """
	
	def __init__(self, symbol, date, *args, **kwargs):
		self.symbol = symbol
		self.date = date
		super(DateNotFound,self).__init__(*args, **kwargs)
		
	def __repr__(self):
		return "Symbol %s does not support date : %s \n%s" % (self.symbol, self.date, super(DateNotFound,self).__repr__())

class Bloomberg(object):
	""" A Bloomberg is a stock information service provider.  It can host any number of "
	" services depending on what is available, such as price, volume, etc. information for "
	" any stock and any date """
	pass 

class Website(Bloomberg):
	""" Website is a Bloomberg that gets its information from a particular website. """
	pass

class GoogleSoup(object):
	""" Helper for Google website. After passing a beautifulSoup object, 
	the GoogleSoup object encapsulates the instance of BeautifulSoup 
	and the parsing know-how to get	different peices of information, such 
	as SEC financials, out.

	The behavior thereafter is similar to the Google Object, but it is not
	optimized for heavy use and can only 'look' at one stock symbol at a time.
	
	It should generally only be used by the Google interface object.
	
	
	
	"""
	
	otherKW = FinancialXML.xml_to_dict("google.xml")
	regexs = otherKW['regular_expressions']
	divs = otherKW['divisions']
	sec_docs = otherKW['sec_definition']
	
	#TODO: you are here.  i want to basically just create a table that will map different
	#attributes to their regex's, as well as define attributes automatically from this table
	#based on the name of the attribute, appended with 'quarterly' or 'annual'.
	#Google needs to inherit an interface similar to this one.  going to have to use 
	#getAttr[] heavily
	
	numberRe = re.compile(r"-?[\d{3,3},]*\d{0,3}\.\d+|-")
	dateRe = re.compile(r"((\d+ (months|weeks) Ending )|(As of ))(?P<year>\d{4,4})-(?P<month>\d{2,2})-(?P<day>\d{2,2})")	
	

	
	def __init__(self, soup=None):
		""" General constructor.  soup is an optional keyword, and if it is left out, 
		we simply return a prototype to get access to GoogleSoup's interface.
		
		post[self]:
			#do a check to make sure I've added my attributes correctly
			#but only in the case that this isn't a prototype
			hasattr(self,"getAnnualRevenue") if soup else True
		
		"""
			
		self.quarterlyDates = []
		self.annualDates = []
		self.supportedInformation = []
		self.datesCache = {}
		#assumes that across balance sheet, cash flows, etc... same dates are used.
		for name,_ in self.regexs.items():
			self.declareAttribute(name)
		
		if not soup:
			return #used to get a prototype
        #TODO: move prototype functionality out into a class method - the class itself should have these methods declared, not just
        #the objects!
		
		self.labels = {"BalanceSheet":{"Annual":soup.find('div', id=self.divs['BalanceSheet']['Annual']),\
									  "Quarterly":soup.find('div', id=self.divs['BalanceSheet']['Quarterly'])},\
					   "IncomeStatement":{"Annual":soup.find('div', id=self.divs['IncomeStatement']['Annual']),\
										  "Quarterly":soup.find('div', id=self.divs['IncomeStatement']['Quarterly'])},\
					   "CashFlowStatement":{"Annual":soup.find('div', id=self.divs['CashFlowStatement']['Annual']),\
											"Quarterly":soup.find('div', id=self.divs['CashFlowStatement']['Quarterly'])},\
					   "Dates":{"Annual":soup.find('div', id=self.divs['Dates']['Annual']),\
								"Quarterly":soup.find('div', id=self.divs['Dates']['Quarterly'])}}
		
		for name,searchRe in self.regexs.items():
			self.addAttribute(name,searchRe)
			
	def declareAttribute(self, name):
		""" Helper private function to build up this objects interface.  Loads 
		what properties this Bloomberg can view from an XML file, who's names are
		then sent in here."""

		annualMethodName = "getAnnual%s" % name
		quarterlyMethodName = "getQuarterly%s" % name
		
		self.__setattr__(annualMethodName, None)
		self.__setattr__(quarterlyMethodName, None)
		
		self.supportedInformation.append(annualMethodName)
		self.supportedInformation.append(quarterlyMethodName)
		
			
	def getSupportedInformation(self):
		""" Returns the information that this class provides, such as SEC data, in the form of 
			functions that can be called on it. """
			
		return self.supportedInformation
			
	def getSecDoc(self, name):
		""" Returns the name of the SEC document that any particular financial keyword
		is found in.  Generally only used as a private, helper function.
		
		Example: #For testing purposes only
		
		>>> example = GoogleSoup()
		>>> example.getSecDoc("Revenue")
		'IncomeStatement'
		
		pre:
			#ensure I'm passing in a valid name
			any([name in self.sec_docs['BalanceSheet'],\
				 name in self.sec_docs['IncomeStatement'],\
				 name in self.sec_docs['CashFlowStatement']])
		
		post[]:
			isinstance(__return__,str)
		
		"""
		
		
		if name in self.sec_docs['BalanceSheet']:
			return 'BalanceSheet'
		elif name in self.sec_docs['IncomeStatement']:
			return 'IncomeStatement'
		elif name in self.sec_docs['CashFlowStatement']:
			return 'CashFlowStatement'
		
	def addAttribute(self, name, regEx):
		""" Adds a new method, assuming this new method supports the retrieval of some stock
			information.  Also appends this new method to the list of supported information.
			Generally used as a private, helper function.  Used in conjunction with 
			declareAttribute.
			
			pre:
				#ensure I'm only getting class defined regex's
				regEx in self.regexs.values()
				
				#ensure that the methods and variables I'm about to define are not already
				#defined
				not callable(getattr(self,"getAnnual%s" % name))
				not callable(getattr(self,"getQuarterly%s" % name))
				
				#ensure that the variable names are not declared
				not hasattr(self,"annual%s" % name)
				not hasattr(self,"quarterly%s" % name)
			
			post[self]:
				#ensure that the methods have been properly defined
				callable(getattr(self,"getAnnual%s" % name))
				callable(getattr(self,"getQuarterly%s" % name))
				
				#ensure that the variable names are declared now
				hasattr(self,"annual%s" % name)
				hasattr(self,"quarterly%s" % name)
				
			
		"""
		
		secDoc = self.getSecDoc(name)
		
		annualMethodName = "getAnnual%s" % name
		quarterlyMethodName = "getQuarterly%s" % name
		
		annualVariableName = "annual%s" % name
		quarterlyVariableName = "quarterly%s" % name
		
		annualDiv = self.labels[secDoc]['Annual']
		quarterlyDiv = self.labels[secDoc]['Quarterly']
		
		annualDateKey = "annual%s" % secDoc
		quarterlyDateKey = "quarterly%s" % secDoc
			
		searchRe = re.compile(regEx)
		
		annualMethod = lambda : self.webparse(annualVariableName, searchRe\
											  , annualDiv, self.getDates(annualDiv, annualDateKey))
		quarterlyMethod = lambda : self.webparse(quarterlyVariableName, searchRe\
											  , quarterlyDiv, self.getDates(quarterlyDiv, quarterlyDateKey))
		
		self.__setattr__(annualMethodName, annualMethod)
		self.__setattr__(quarterlyMethodName, quarterlyMethod)
		self.__setattr__(annualVariableName, None)
		self.__setattr__(quarterlyVariableName, None)
		
		self.supportedInformation.append(annualMethodName)
		self.supportedInformation.append(quarterlyMethodName)
		
	def getRows(self, div, searchRe):
		""" Get the rows associated with the regular expression searchRe.  Generally used
		as a private, helper function. 
		
		post[]:
			isinstance(__return__,list)
		"""
		
		trs = div.findAll('tr')[1:]
		#get all trs, except the first because its just the dates.
		
		#why don't you just bite the bullet here and do a regex on the whole damned thing?
		tds = None
		for tr in trs:  
			tds = tr.findAll("td")
			if searchRe.search(str(tds[0])):
				break
			if tds[0].string and searchRe.search(tds[0].string) != None:
				break
			if tds[0].b and tds[0].b.string and searchRe.search(tds[0].b.string) != None: #important names are bolded
				break
			if tds[0].span and tds[0].span.string and searchRe.search(tds[0].span.string) != None:
				break
			if tds[0].b and tds[0].b.span and tds[0].b.span.string and searchRe.search(tds[0].b.span.string) != None:
				break
			#TODO: 'find' syntax again
		else: #didn't break out of the loop at all
			raise Exception("Couldn't find searchRe")
		
		#TODO: Why aren't you just using the regex over the whole damn thing instead of trying to narrow down whether its inside of 
		#a bold or a span?
		
		
		values = []
		for result in tds[1:]:
			
			#some random stuff is bolded.
			if result.find("b"):
				result = result.find("b")
			
			#if there is no result, google tends to put a '-' after a 'span' tag	
			if result.find("span"):
				val = result.find("span")
			else:
				val = result
				
			
			#check using a regex whether there is a number or a '-' in this td
			match = self.numberRe.search(val.string)
			if match:
				val = match.group()
			else:
				continue
			
			#clean up the string for storage
			val = val.replace(",","")
			
			val = float(val) if val != "-" else "-"
			
			#add it to results.
			values.append(val)
		
		return values
	
	def webparse(self, variableName, searchRe, division, dates):
		""" Used as a private helper function to be called by delegation via a 
		lambda.  Also cache's any attribute that's been looked up in the GoogleSoup
		object such that look up does not have to occur again. 
		
		post[]:
			isinstance(__return__,dict)
		"""
		
		if not self.__getattribute__(variableName):
				self.__setattr__(variableName, self.getRows(division, searchRe))
		return dict(zip(dates, self.__getattribute__(variableName)))
	 
	def getDates(self, div, key=None):
		""" Returns dates found in a BeautifulSoup division.  If key is not provided, 
		the function simply returns dates found.  If a key is provided, the function 
		cache's the dates on that key as an optimization. 
		
		post[]:
			#type check return value
			isinstance(__return__,list)
			all([isinstance(x,datetime.date) for x in __return__])
		"""
		
		if not key:
			return self.getDatesFromDiv(div)
				
		if not self.datesCache.has_key(key):
			tds = div.findAll('td')
			tds = [self.dateRe.search(str(td)) for td in tds if self.dateRe.search(str(td))]
			dates = [datetime.date(int(td.group('year')), int(td.group('month')), int(td.group('day'))) for td in tds]
			#TODO: replace this with getDatesFromDiv!
			self.datesCache[key] = dates
			
		return self.datesCache[key]
	
	def getDatesFromDiv(self, div):
		""" Helper private function for the getDates function.  Actually does the physical
		parsing of a BeautifulSoup object.
		"""
		  
		tds = div.findAll('td')
		tds = [self.dateRe.search(str(td)) for td in tds if self.dateRe.search(str(td))]
		dates = [datetime.date(int(td.group('year')), int(td.group('month')), int(td.group('day'))) for td in tds]
		return dates
		
		

class Google(Website):
	""" Google is the main class in this module, and supports a Bloomberg like use.
	Currently supports the retrieval of most SEC document information for the past 
	five years.
	
	You can get particular quarterlies:
	
	>>> from datetime import date
	>>> scraper = Google()
	>>> round(scraper.getQuarterlyOtherNet("CSCO", date(2008,01,26)))
	-28.0
	
	>>> round(scraper.getQuarterlyRetainedEarnings("CSCO", date(2008,01,26)))
	-1073.0
	
	>>> round(scraper.getQuarterlyIssuanceOfStock("CSCO", date(2008,01,26)))
	-3501.0
	
	Or annuals, simply switching a the name of the function:
	
	>>> round(scraper.getAnnualOtherNet("CSCO", date(2006,07,29)))
	-94.0
	
	>>> round(scraper.getAnnualRetainedEarnings("CSCO", date(2006,7,29)))
	-617.0
	
	>>> round(scraper.getAnnualIssuanceOfStock("CSCO", date(2005,07,30)))
	-9148.0
	
	If you leave out the date, you get a dict of all available information.

	>>> scraper.getQuarterlyTotalRevenue('S') == {date(2007,12,31):9847.0,\
												  date(2007,9,30):10044.0,\
	  										      date(2007,6,30):20255.0,\
												  date(2007,3,31):10091.0,\
												  date(2006,12,31):10438.0}
	True
	
	When information is unavailable to Google itself, a character dash is reported:
	
	>>> scraper.getQuarterlyOtherRevenue('S') == {date(2007,12,31):'-',\
                                                  date(2007,9,30):'-',\
                                                  date(2007,6,30):'-',\
                                                  date(2007,3,31):'-',\
                                                  date(2006,12,31):'-'}
	True

    These can sometimes be mixed:

	>>> scraper.getQuarterlyDilutionAdjustment('S') == {date(2007,12,31):0.00,\
                                                     	date(2007,9,30):'-',\
                                                     	date(2007,6,30):0.00,\
                                                     	date(2007,3,31):0.00,\
                                                     	date(2006,12,31):'-'}
	True
	
	A dash does not necesarilly mean zero, though.  Simply a lack of data.
    In fact, all data could exist, and still be zero!
    
	>>> scraper.getQuarterlyDividendsPerShare("IRBT") == {date(2007,12,29):0.0,\
                                                     	  date(2007,9,29):0.0,\
                                                     	  date(2007,6,30):0.0,\
                                                     	  date(2007,3,31):0.0,\
                                                     	  date(2006,12,30):0.0}
	True
    
    The data is accurate down to the hundredth, or at least as accurate as the 
    reporting company.
    
	>>> scraper.getQuarterlyDilutedNormalizedEPS('S') == {date(2007,12,31):-3.55,\
                                                     	  date(2007,9,30):0.05,\
                                                     	  date(2007,6,30):0.0,\
                                                     	  date(2007,3,31):-0.03,\
                                                     	  date(2006,12,31):0.11}
	True
    
    When searching for a stock that has no SEC data, an exception is raised:
    
    >>> scraper.getAnnualForeignExchangeEffects("NTDOY")
    Traceback (most recent call last):
    	...
    SymbolHasNoFinancials
    
    Or, when searching for a symbol that does not exist at all:
    
    >>> scraper.getAnnualCashInterestPaid("CHEESE")
    Traceback (most recent call last):
    	...
    SymbolNotFound
    
    Or, when looking for information on a stock that DOES exist, but a date 
    that doesnt:
    
	>>> scraper.getAnnualDeferredTaxes("CFC", date(2007,12,30))
	Traceback (most recent call last):
		...
	DateNotFound
	
    The scraper supports any stock that Google can search, including foreign stocks:
    
	>>> scraper.getAnnualNotesPayable("PIF.UN") == {date(2007,12,31):0.00,\
                                                    date(2006,12,31):0.00,\
                                                    date(2005,12,31):7.31,\
                                                    date(2004,12,31):2.97,\
                                                    date(2003,12,31):0.00,\
                                                    date(2002,12,31):0.00}
	True
    
    Or ADR's
    
	>>> scraper.getAnnualTotalAssets("IBN") == {date(2007,3,31):3943347.0,\
                                                date(2006,3,31):2772295.0,\
                                                date(2005,3,31):1784337.0,\
                                                date(2004,3,31):1409131.0,\
                                                date(2003,3,31):1180263.0,\
                                                date(2002,3,31):743362.0}
	True
	
	Beware though, stocks like these are not always reported in US Dollars!
	
	"""                                                

	def __init__(self):
		self.cachedPages = {}
		prototype = GoogleSoup()
		
		for functionName in prototype.getSupportedInformation():
			self.defineAttribute(functionName)
		
		#TODO: should also put this at the class level
		#TODO: this sort of 'information' stuff should be formalized in the bloomberg concept.
		
	def defineAttribute(self, name):
		""" Helper private function to add a new attribute to Google, based on the current
		interface of GoogleSoup.  Can't use inheritance there because I do not know at 
		'compile' what GoogleSoup's attributes are.
		
		TODO: Investigate whether class inheritance interfaces are resolved at runtime
		or compile time.
		
		Example Usage: #For testing purposes only
		
		>>> example = Google()
		>>> example.defineAttribute("myattribute")
		>>> hasattr(example, "myattribute")
		True
		
		"""
		
		self.__setattr__(name, lambda *args : self.__myGetAttr__(name, *args))
		
	def buildURL(self, symbol):
		""" Private helper function that builds website URL's for different
		symbols looked up.
		
		Example: #For testing purposes only
		
		>>> example = Google()
		>>> example.buildURL('FDX')
		u'http://finance.google.com/finance?fstype=ii&q=NYSE:FDX'
		
		Function can throw exceptions in two cases.
		1. Function is given a symbol that flat out does not exist.
		
		>>> example.getQuarterlyRevenue("fart")
		Traceback (most recent call last):
			...
		SymbolNotFound
		
		2. Function is given a symbol that returns search results
		and does not exist directly.
		
		>>> example.getQuarterlyRevenue("happy")
		Traceback (most recent call last):
			...
		SymbolNotFound
		
		post[]:
			isinstance(__return__,str) or isinstance(__return__,unicode)
    	
    	"""
		
		baseURL = "http://finance.google.com/finance?q=%s" % symbol
		page = urllib2.urlopen(baseURL)
		page = BeautifulSoup(page)
		
		if page.findAll(text=lambda x: "produced no matches" in x):
			raise SymbolNotFound(symbol)
		#for symbols that return nothing whatsoever
		
		inc = re.compile("Income.*Statement")
		invalidResultRe = re.compile("Show all [0-9]+ (companies|(mutual funds))")
		links = page.findAll('a')
		
		suffix=None
		for link in links:
			if not link.string:
				continue
			finding = inc.search(link.string)
			if invalidResultRe.search(link.string):
				raise SymbolNotFound(symbol)
			#for symbols that return a search page
			if not finding:
				continue
			suffix = link['href']
			break
		
		if not suffix:
			raise SymbolHasNoFinancials(symbol)
#		suffix = [x for x in inc.searchiter(x.string) if ]
		
 #	   suffix = filter(lambda x: x.string != None\
  #					   and inc.search(x.string) != None,links)[0]['href']
		return "".join(["http://finance.google.com/finance",suffix])
	
		#TODO: figure out 'find' syntax for lists.  there ought to be a find for lists.
		#TODO: instead of filter, us decorate, find, undecorate.
		#TODO: might be able to put this all in the page.findAll method call
		
	def buildSoup(self, symbol):
		""" Helper private function that turns a symbol string into a BeautifulSoup object
		
		
		post[]:
			#ensure type of returned object
			isinstance(__return__,BeautifulSoup) 
		"""
		
		url = self.buildURL(symbol)
		return BeautifulSoup(urllib2.urlopen(url))
	
	keywordRe = re.compile(r"get(Quarterly|Annual)(?P<keyword>[A-z]*)")
	
#	def __getattr__(self, name):
#   	""" Deprecated """
		#get the keyword - strip off 'get' and 'quarterly' or 'annual'
#		keyword = self.keywordRe.search(name).group('keyword') 
		
#		if GoogleSoup.regexs.has_key(keyword):
#			return lambda *args: self.__myGetAttr__(name, *args)
#		else: 
#			raise AttributeError()
		
	def __myGetAttr__(self, name, *args):
		""" Helper private function that turns a function call on Google to a call on
		an underlying GoogleSoup object.  It's used in lambdas as a delegated function.
		It expects a name argument that is a property that can be queried on the 
		underlying GoogleSoup, and then a symbol argument and a date argument, based
		on placement.  The date argument is optional, and if not given, this 
		function returns a dictionary of possible values.  
		
		Example: #For testing purposes only
		
		>>> from datetime import date
		>>> example = Google()
		>>> round(example.__myGetAttr__("getQuarterlyRevenue", "IRBT", date(2007,12,29)))
		99.0
		
		pre:
			#ensure arguments are well formed
			len(args) == 1 or len(args) == 2
			
			#first argument must be a string 
			isinstance(args[0],str)
			
			#second argument, if it exists, must be a datetime.date
			isinstance(args[1],datetime.date) if len(args) == 2 else True
		
		post[self.cachedPages]:
		
			#ensure that the page has been cached
			self.cachedPages.has_key(args[0])
			
			#ensure type of cache'ed object
			isinstance(self.cachedPages[args[0]], GoogleSoup)
			
			#proper return type, depending on the arguments provided
			isinstance(__return__,dict) if len(args) == 1 else isinstance(__return__,float)
		
		"""
		
		#do some type checking here
		
		#TODO: due to my new implementation of this classes interface(i no longer use __getattr__)
		# this function might be able to do better type checking and be more integrated into
		# the rest of the class
		
		symbol=None
		date=None
		
		#should have one/two arguments, one is a symbol string, one is a date 
#		if(len(args) == 0 or len(args) > 2):
#			raise AttributeError()
		
		#first should be a string
#		if not isinstance(args[0], str):
#			raise AttributeError()
		symbol = args[0]
		
		#second should be a date
		if(len(args) == 2):
#			if not isinstance(args[1], datetime.date):
#				raise AttributeError()
			date = args[1]
			
		if not self.cachedPages.has_key(symbol):
			self.cachedPages[symbol] = GoogleSoup(self.buildSoup(symbol))
			
		#TODO: check to see if there's a valid name here
		results = getattr(self.cachedPages[symbol], name)()	
			
		if date:
			try:
				results = results[date]
			except KeyError, e:
				raise DateNotFound(symbol,date)
		return results