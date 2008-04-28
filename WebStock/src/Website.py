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

>>> scraper.getQuarterlyDeferredTaxes("YHOO") == {date(2008,3,31):29.64,\
												  date(2007,12,31):-78.16,\
												  date(2007,9,30):-43.75,\
												  date(2007,6,30):-48.54,\
												  date(2007,3,31):-42.30}
True

"""

#from BeautifulSoup import BeautifulSoup
import BeautifulSoup
import urllib2
import re
import datetime
import FinancialXML

from utilities import publicInterface, isString, isRegex

class SymbolNotFound(Exception):
	""" Raised when a symbol is not found or information for it cannot be found "
	
	inv:
		#typechecking
		self.symbol != None
		isinstance(self.symbol,str)
	"""
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isinstance(symbol,str)
		
		post:
			#typechecking
			isinstance(self.message, str) or isinstance(self.message, unicode)
		"""
		
		self.symbol = symbol
		super(SymbolNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not find symbol : \"%s\"" % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message
	
class SymbolHasNoFinancials(Exception):
	""" Raised when a symbol is a tracked company, but the company has no SEC documents
	available.
	
	inv:
		#typechecking
		self.symbol != None
		isinstance(self.symbol,str) or isinstance(self.symbol,unicode)
	
	"""
	
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isinstance(symbol,str) or isinstance(symbol,unicode)
		
		post:
			#typechecking
			isinstance(self.message, str) or isinstance(self.message, unicode)
		"""
		self.symbol = symbol
		super(SymbolHasNoFinancials,self).__init__(*args, **kwargs)
		
		self.myMessage = "Symbol does not support financials: \"%s\""  % (self.symbol)
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message
	
class DateNotFound(Exception):
	""" Raised when a requested date is not available for a peice of information on
	a stock. 
	
	inv:
		#typechecking
		self.symbol != None
		isinstance(self.symbol,str)
		self.date != None
		isinstance(self.date,datetime.date)
	"""
	
	def __init__(self, symbol, date, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isinstance(symbol,str)
			isinstance(date,datetime.date)
			
		post:
			#typechecking
			isinstance(self.message, str) or isinstance(self.message, unicode)
		"""
		
		self.symbol = symbol
		self.date = date
		super(DateNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Symbol \"%s\" does not support date : %s" % (self.symbol, str(self.date))
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message
	
class SectorInformationNotFound(Exception):
	""" Raised when a symbol does not support Sector information "
	
	inv:
		#typechecking
		self.symbol != None
		isString(self.symbol)
	"""
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isString(symbol)
		
		post:
			#typechecking
			isString(self.message)
		"""
		
		self.symbol = symbol
		super(SectorInformationNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not find Sector Information for symbol: \"%s\"" % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message

class IndustryInformationNotFound(Exception):
	""" Raised when a symbol does not support Industry Information "
	
	inv:
		#typechecking
		self.symbol != None
		isString(self.symbol)
	"""
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isString(symbol)
		
		post:
			#typechecking
			isString(self.message)
		"""
		
		self.symbol = symbol
		super(IndustryInformationNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not find Industry Information for symbol: \"%s\"" % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message

class CurrencyInformationNotFound(Exception):
	""" Raised when a Currency Information for this symbol is not supported "
	
	inv:
		#typechecking
		self.symbol != None
		isString(self.symbol)
	"""
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isString(symbol)
		
		post:
			#typechecking
			isString(self.message)
		"""
		
		self.symbol = symbol
		super(CurrencyInformationNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not find Currency Information for symbol: \"%s\"" % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message
	

class Bloomberg(object):
	""" A Bloomberg is a stock information service provider.  It can host any number of "
	" services depending on what is available, such as price, volume, etc. information for "
	" any stock and any date """
	pass 

class Website(Bloomberg):
	""" Website is a Bloomberg that gets its information from a particular website. """
	pass

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
														   date(2007,6,30):-0.01,\
														   date(2007,3,31):-0.03,\
														   date(2006,12,31):0.11}
	True
	
	When searching for a stock that has no SEC data, an exception is raised:
	
	>>> scraper.getAnnualForeignExchangeEffects("NTDOY")
	Traceback (most recent call last):
		...
	SymbolHasNoFinancials: Symbol does not support financials: \"NTDOY\"
	
	Or, when searching for a symbol that does not exist at all:
	
	>>> scraper.getAnnualCashInterestPaid("CHEESE")
	Traceback (most recent call last):
		...
	SymbolNotFound: Could not find symbol : \"CHEESE\"
	
	Or, when looking for information on a stock that DOES exist, but a date 
	that doesnt:
	
	>>> scraper.getAnnualDeferredTaxes("CFC", date(2007,12,30))
	Traceback (most recent call last):
		...
	DateNotFound: Symbol \"CFC\" does not support date : 2007-12-30
	
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
	
	To see what the stock IS traded in, use
	
	>>> scraper.getCurrencyReported("IBN")
	u'INR'
	
	Even though it may be traded on an American stock exchange;
	
	>>> scraper.getExchange("INR")
	u'NYSE'
	
	inv:
		isinstance(self._SECCache,dict)
		isinstance(self._metaCache,dict)
		all(isinstance(x,str) for x in self._SECCache.keys())
		all(isinstance(x,str) for x in self._metaCache.keys())
		all(isinstance(x,Google.SECData) for x in self._SECCache.values())
		all(isinstance(x,Google.Metadata) for x in self._metaCache.values())
	""" 


	class SECData(object):
		""" Helper for Google website. After passing a beautifulSoup object, 
		the SECData object encapsulates the instance of BeautifulSoup 
		and the parsing know-how to get	different peices of information, such 
		as SEC financials, out.
	
		The behavior thereafter is similar to the Google Object, but it is not
		optimized for heavy use and can only 'look' at one stock symbol at a time.
		
		It should generally only be used by the Google interface object.
		
		
		inv:
			#these should be constant class variables
			self.otherKW != None
			self.regexs != None
			self.divs != None
			self.sec_docs != None
			self.numberRe != None
			self.dateRe != None
			
			self.otherKW == Google.SECData.otherKW
			self.regexs == Google.SECData.regexs
			self.divs == Google.SECData.divs
			self.sec_docs == Google.SECData.sec_docs
			self.numberRe == Google.SECData.numberRe
			self.dateRe == Google.SECData.dateRe
			
			isinstance(self.otherKW, dict)
			isinstance(self.regexs, dict)
			isinstance(self.divs, dict)
			isinstance(self.sec_docs, dict)
			isinstance(self.numberRe,type(re.compile(""))) #finding the type of a regex seems to be difficult...
			isinstance(self.dateRe,type(re.compile("")))
			
			#check to make sure regexs always work right
			self.numberRe.match("-1234567890.12") != None
			self.dateRe.match("12 months Ending 2006-12-12") != None
			
			#ensure that class variables always exist
			self.quarterlyDates != None
			self.annualDates != None
			self.datesCache != None
			
			isinstance(self.quarterlyDates,list)
			isinstance(self.annualDates,list)
			isinstance(self.datesCache, dict)
			
			hasattr(self,"labels") if not self.isPrototype else True
			self.labels.has_key("BalanceSheet") if hasattr(self,"labels") else True 
			self.labels.has_key("IncomeStatement") if hasattr(self,"labels") else True
			self.labels.has_key("CashFlowStatement") if hasattr(self,"labels") else True
			self.labels.has_key("Dates") if hasattr(self,"labels") else True
			
			self.sec_docs.has_key("BalanceSheet")
			self.sec_docs.has_key("CashFlowStatement")
			self.sec_docs.has_key("IncomeStatement")
			
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
			we simply return a prototype to get access to SECData's interface.
			
			pre:
				#type check
				isinstance(soup,BeautifulSoup.BeautifulSoup) if soup != None else True
			
			post[self]:
				#do a check to make sure I've added my attributes correctly
				#but only in the case that this isn't a prototype
				
				hasattr(self,"getAnnualRevenue") if soup else True
				callable(self.getAnnualRevenue) if (hasattr(self,"getAnnualRevenue") and not self.isPrototype) else True
				not hasattr(self,"labels") if self.isPrototype else True
				
			
			"""
				
			self.quarterlyDates = []
			self.annualDates = []
			self.supportedInformation = []
			self.datesCache = {}
			#assumes that across balance sheet, cash flows, etc... same dates are used.
			
			self.isPrototype = True
			
			for name,_ in self.regexs.items():
				self._declareAttribute(name)
			
			if not soup:
				self.isPrototype = True
				return #used to get a prototype
	
			self.isPrototype = False
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
				self._addAttribute(name,searchRe)
				
		def _declareAttribute(self, name):
			""" Helper private function to build up this objects interface.  Loads 
			what properties this Bloomberg can view from an XML file, who's names are
			then sent in here.
			
			pre:
				#typechecking
				isinstance(name,BeautifulSoup.NavigableString) or isinstance(name,str) or isinstance(str,unicode)
				
				#make sure the name i'm declaring is NOT already declared
				not hasattr(self,"getAnnual"+name)
				not hasattr(self,"getQuarterly"+name)
				
			post[self,name]:
			
				#make sure class has been mutated
				hasattr(self,"getAnnual"+name)
				hasattr(self,"getQuarterly"+name)
			
			"""
	
			annualMethodName = "getAnnual%s" % name
			quarterlyMethodName = "getQuarterly%s" % name
			
			self.__setattr__(annualMethodName, self._badHack)
			self.__setattr__(quarterlyMethodName, self._badHack)
			
		def _badHack(self):
			""" This is baaad.  Used to fake 'callable' on the prototype's interface.  """
			pass
				
		def _getSECDoc(self, name):
			""" Returns the name of the SEC document that any particular financial keyword
			is found in.  Generally only used as a private, helper function.
			
			Example: #For testing purposes only
			
			>>> example = Google.SECData()
			>>> example._getSECDoc("Revenue")
			'IncomeStatement'
			
			pre:
				#typecheck
				isinstance(name,str) or isinstance(name, unicode)
				
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
			
		def _addAttribute(self, name, regEx):
			""" Adds a new method, assuming this new method supports the retrieval of some stock
				information.  Also appends this new method to the list of supported information.
				Generally used as a private, helper function.  Used in conjunction with 
				declareAttribute.
				
				pre:
					#TYPECHECK
					isinstance(name,str) or isinstance(name,unicode)
					isinstance(regEx,str) or isinstance(regEx,unicode)
				
					#ensure I'm only getting class defined regex's
					regEx in self.regexs.values()
					
					#ensure that the methods and variables I'm about to define are not already
					#defined
					not callable(getattr(self,"getAnnual%s" % name)) or getattr(self,"getAnnual%s" % name) == self._badHack
					not callable(getattr(self,"getQuarterly%s" % name)) or getattr(self,"getQuarterly%s" % name) == self._badHack
					
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
			
			secDoc = self._getSECDoc(name)
			
			annualMethodName = "getAnnual%s" % name
			quarterlyMethodName = "getQuarterly%s" % name
			
			annualVariableName = "annual%s" % name
			quarterlyVariableName = "quarterly%s" % name
			
			annualDiv = self.labels[secDoc]['Annual']
			quarterlyDiv = self.labels[secDoc]['Quarterly']
			
			annualDateKey = "annual%s" % secDoc
			quarterlyDateKey = "quarterly%s" % secDoc
				
			searchRe = re.compile(regEx)
			
			annualMethod = lambda : self._webparse(annualVariableName, searchRe\
												  , annualDiv, self._getDates(annualDiv, annualDateKey))
			quarterlyMethod = lambda : self._webparse(quarterlyVariableName, searchRe\
												  , quarterlyDiv, self._getDates(quarterlyDiv, quarterlyDateKey))
			
			self.__setattr__(annualMethodName, annualMethod)
			self.__setattr__(quarterlyMethodName, quarterlyMethod)
			self.__setattr__(annualVariableName, None)
			self.__setattr__(quarterlyVariableName, None)
			
		def _getRows(self, div, searchRe):
			""" Get the rows associated with the regular expression searchRe.  Generally used
			as a private, helper function. 
			
			We're assuming that searchRe is a regex found within our established regex's from our XML file
			because the only thing that should call this function is another SECData function.
			
			pre:
				#typecheck
				div != None
				isinstance(searchRe,type(re.compile("")))
				
			
			post[]:
				#typecheck
				isinstance(__return__,list)
				all([x == '-' or isinstance(x,float) for x in __return__])
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
		
		def _webparse(self, variableName, searchRe, division, dates):
			""" Used as a private helper function to be called by delegation via a 
			lambda.  Also cache's any attribute that's been looked up in the SECData
			object such that look up does not have to occur again. 
			
			pre:
				#typecheck
				isinstance(variableName,str) or isinstance(variableName,unicode)
				isinstance(searchRe,type(re.compile("")))
				division != None
				isinstance(dates,list)
				all([isinstance(x,datetime.date) for x in dates])
			
			post[]:
				#typecheck
				isinstance(__return__,dict)
				all([isinstance(x,datetime.date) for x in __return__.keys()])
				all([isinstance(x,float) or x=='-' for x in __return__.values()])
			"""
			
			if not self.__getattribute__(variableName):
					self.__setattr__(variableName, self._getRows(division, searchRe))
			return dict(zip(dates, self.__getattribute__(variableName)))
		 
		def _getDates(self, div, key=None):
			""" Returns dates found in a BeautifulSoup division.  If key is not provided, 
			the function simply returns dates found.  If a key is provided, the function 
			cache's the dates on that key as an optimization. 
			
			pre:
				#typecheck
				div != None
				(isinstance(key,str) or isinstance(key,unicode)) if key != None else True
			
			post[key,self]:
				#type check return value
				isinstance(__return__,list)
				all([isinstance(x,datetime.date) for x in __return__])
				self.datesCache.has_key(key)
			"""
			
			if not key:
				return self._getDatesFromDiv(div)
					
			if not self.datesCache.has_key(key):
				self.datesCache[key] = self._getDatesFromDiv(div)
				
			return self.datesCache[key]
		
		def _getDatesFromDiv(self, div):
			""" Helper private function for the getDates function.  Actually does the physical
			parsing of a BeautifulSoup object.
			
			pre:
				div != None
			
			post[]:
				isinstance(__return__,list)
				all([isinstance(x,datetime.date) for x in __return__])
			"""
			  
			tds = div.findAll('td')
			tds = [self.dateRe.search(str(td)) for td in tds if self.dateRe.search(str(td))]
			dates = [datetime.date(int(td.group('year')), int(td.group('month')), int(td.group('day'))) for td in tds]
			return dates

	
	class Metadata:
		"""
		
		inv:
			#typechecking
			isinstance(self.factory, Google.SoupFactory)
			isinstance(self.soup, BeautifulSoup.BeautifulSoup)
			isinstance(self.currencyReported, str) or isinstance(self.currencyReported, unicode)
			isString(self.exchange)
			isinstance(self.competitors, list)
			all(isString(x) for x in self.competitors)
			isString(self.industry)
			isString(self.symbol)
			isString(self.properName)
			
			#check that regex's work properly
			isRegex(self.currencyRe)
			isRegex(self.exchangeRe)
			isRegex(self.sectorRe)
			isRegex(self.industryRe)
			
			self.currencyRe.search("(In millions of JPY)") is not None
			self.exchangeRe.search("(Public, NASDAQ:GOOG)") is not None
			self.sectorRe.search("Sector:") is not None
			self.industryRe.search("Industry:") is not None
			
			self.currencyRe == Google.Metadata.currencyRe
			self.exchangeRe == Google.Metadata.exchangeRe
			self.sectorRe == Google.Metadata.sectorRe
			self.industryRe == Google.Metadata.industryRe
			
			
		"""
		
		currencyRe = re.compile("\(In millions of (?P<currency>[A-Z]+)\)")
		exchangeRe = re.compile("\(([A-z]+, )?(?P<exchange>[A-Z]+):(?P<symbol>[A-Z0-9]+)\)")
		sectorRe = re.compile("Sector:")
		industryRe = re.compile("Industry:")
		
		def __init__(self, soup, factory):
			""" Metadata's constructor.
			
			pre:
				isinstance(soup,BeautifulSoup.BeautifulSoup)
				isinstance(factory,Google.SoupFactory)
			"""
			
			self.soup = soup
			self.factory = factory
			self.currencyReported = ""
			self.exchange = ""
			self.competitors = []
			self.sector = ""
			self.industry = ""
			self.symbol = ""
			self.properName = ""
		
		def getCurrencyReported(self):
			""" Returns a unicode character string that signifies the currency 
			that this stock is reported to the SEC in.  This is a service provided
			to the Google class.
			
			For example:
			
			>>> scraper = Google()
			>>> scraper.getCurrencyReported("IRBT")
			u'USD'
			
			#US dollar
			
			>>> scraper.getCurrencyReported("MTU")
			u'JPY'
			
			#japanese yen
			
			Throws a SEC documents not found error if the symbol does not have
			SEC data.
			>>> scraper.getCurrencyReported("SATR")
			Traceback (most recent call last):
				...
			CurrencyInformationNotFound: Could not find Currency Information for symbol: \"SATR\"
							
			pre:
				self.factory.hasMeta(self.getSymbol())
#				self.factory.hasSEC(self.getSymbol())
			#TODO: this needs to be checked one place.  right now i throw an exception but i kind of want to enforce this too...
			#thoughts: i suppose since it's a public function, it SHOULD throw an exception instead of just checking constraints.
							
			post[]:
				#typechecking
				isinstance(__return__,unicode)
				
				#symbol should be cached
				self.currencyReported != ""
			
			"""
			if not self.currencyReported:
				if not self.hasCurrencyReported():
					raise CurrencyInformationNotFound(self.getSymbol())
				financialDiv = self.soup.find('div', id='financials')
				while not self.currencyReported:
					if self.currencyRe.search(str(financialDiv)):
						self.currencyReported = unicode(self.currencyRe.search(str(financialDiv)).group('currency'))
					else:
						financialDiv = financialDiv.next
			return self.currencyReported
		#TODO: there is a beautiful soup construct for searching for regular expressions that i should use instead of this.
		#there's some weirdness with navigable strings that i never really figured out.
			
		def hasCurrencyReported(self):
			""" Returns whether or not this page supports Currency information.
			
			>>> scraper = Google()
			>>> scraper.hasCurrencyReported("MTU")
			True
			
			>>> scraper.hasCurrencyReported("SATR")
			False
			
			pre:
				self.factory.hasMeta(self.getSymbol())
				
			post[]:
				#typechecking
				isinstance(__return__,bool)
			"""
			if self.currencyReported:
				return True
			elif not self.factory.hasSEC(self.getSymbol()):
				return False
			
			financialDiv = self.soup.find('div', id='financials')
			if not financialDiv:
				return False
			
			finding = None
			while financialDiv:
				if self.currencyRe.search(str(financialDiv)):
					return True
				else:
					financialDiv = financialDiv.next
			return False
		
		def getExchange(self):
			""" Returns the name of the exchange this symbol is traded upon
			or list of exchanges if the symbol returns multiple exchanges.
			This is a service provided to the Google class.
			
			For example:
			>>> scraper = Google()
			>>> scraper.getExchange("IRBT")
			u'NASDAQ'
			
			>>> scraper.getExchange("NTDOY")
			u'OTC'
			
			>>> scraper.getExchange("IBM")
			u'NYSE'

			pre:
				#typechecking
				self.factory.hasMeta(self.getSymbol())
			
			post[self.exchange]:
				#typechecking
				isString(__return__)
				
				#check cacheing
				self.exchange != __old__.self.exchange if __old__.self.exchange == "" else True
				
				
				
			"""
			if not self.exchange:
				exchangeHeader = self.soup.find('table',id='companyheader').h1.nextSibling.string
				self.exchange = self.exchangeRe.search(exchangeHeader).group('exchange')
			return self.exchange
		
		def hasExchange(self):
			""" Returns whether this page supports exchange information.
			TODO: can i actually find an example of where this would be false?
			For example:
			>>> scraper = Google()
			>>> scraper.hasExchange("IRBT")
			True
			
			>>> scraper.hasExchange("NTDOY")
			True
			
			>>> scraper.hasExchange("IBM")
			True
			
			pre:
				self.factory.hasMeta(self.getSymbol())
			
			post[]:
				#typechecking
				isinstance(__return__,bool)
			"""
			if self.exchange:
				return True
			exchangeHeader = self.soup.find("table",id="companyheader").h1.nextSibling.string
			if self.exchangeRe.search(exchangeHeader).group('exchange'):
				return True
			else:
				return False
			#TODO: add failure cases
		def getSymbol(self):
			""" Is a reflective function that will return the symbol this MetaSoup
			is currently pointed at. 
			
			For example:
			>>> scraper = Google()
			>>> scraper.getSymbol("ADBE")
			u'ADBE'
			
#			pre:
#				self.factory.hasMeta(self.getSymbol())
			#TODO: the above logic is sound, i just can't call it in that way.  getsymbol ought to only be called on things that HAVE
			meta information, but symbol doesn't know itself... hrm... should symbol be passed in?
			
			post[self.symbol]:
				#typechecking
				isinstance(__return__,unicode)
				
				#cache check
				self.symbol != __old__.self.symbol if __old__.self.symbol == "" else True
			"""
			if not self.symbol:
				symbolHeader = self.soup.find('table',id='companyheader').h1.nextSibling.string
				self.symbol = self.exchangeRe.search(symbolHeader).group('symbol')
			return self.symbol
		
		def hasSymbol(self):
			""" Returns whether or not this page has symbol information.
			TODO: is there a case where this is false?
			For example:
			>>> scraper = Google()
			>>> scraper.hasSymbol("ADBE")
			True
			
			post[]:
				isinstance(__return__,bool)
			"""
			if self.symbol:
				return True
			symbolHeader = self.soup.find('table',id='companyheader').h1.nextSibling.string
			if self.exchangeRe.search(symbolHeader).group('symbol'):
				return True
			else:
				return False
			#TODO: does this even make sense?  what is a page without a symbol?
			
		
		def getCompetitors(self):
			""" Returns a list of symbols that are competitors to the
			company the passed in symbol represents.  This is a service provided
			to the Google class.
			
			For example:
			>>> scraper = Google()
			>>> x = scraper.getCompetitors("MSFT")
			>>> x.sort()
			>>> print x
			[u'AAPL', u'ADBE', u'GOOG', u'HPQ', u'IBM', u'JAVA', u'NOVL', u'ORCL', u'QUIK', u'YHOO']
	
			pre:
				self.factory.hasMeta(self.getSymbol())
				
			post[self.competitors]:
				#typechecking
				isinstance(__return__,list)
				all([isinstance(x,unicode) for x in __return__])
				
				#cache check
				self.symbol != __old__.self.competitors if __old__.self.competitors == [] else True
				
			"""	
			if not self.competitors:   
				compDiv = self.soup.find("div",id="related")
				compLink = re.compile("rct-[0-9]+")
				for link in compDiv.findAll('a',id=compLink):
					if link.string != self.getSymbol():
						self.competitors.append(link.string)
			return self.competitors
				
		def hasCompetitors(self):
			""" Returns whether this page supports Competitor information.
			TODO: does this have a false case?
			For example:
			>>> scraper = Google()
			>>> scraper.hasCompetitors("MSFT")
			True
			
			pre:
				self.factory.hasMeta(self.getSymbol())
				
			post[]:
				#typecheck
				isinstance(__return__, bool)
			"""
			if self.competitors:
				return True
			compDiv = self.soup.find("div",id="related")
			compLink = re.compile("rct-[0-9]+")
			for link in compDiv.findAll('a',id=compLink):
				if link.string != self.getSymbol():
					return  True
			return False
				
			
		
		def getSector(self):
			""" Returns the name of the sector that the company represented
			by this symbol is considered a part of.  This is a service provided
			to the Google class.
			
			For example:
			>>> scraper = Google()
			>>> scraper.getSector("GOOG")
			u'Technology'
			
			>>> scraper.getSector("DOW")
			u'Basic Materials'
			
			>>> scraper.getSector("SATR")
			Traceback (most recent call last):
				...
			SectorInformationNotFound: Could not find Sector Information for symbol: \"SATR\"
			
			pre:
				self.factory.hasMeta(self.getSymbol())
				
			post[self.sector]:
				#typechecking
				isinstance(__return__,unicode)
				
				#cache check
				self.sector != __old__.self.sector if __old__.self.sector == "" else True
			"""
			if not self.sector:
				if not self.hasSector():
					raise SectorInformationNotFound(self.getSymbol())
			 	sectorDiv = self.soup.find("div",id='related').find("div",attrs={'class':'item'})
				if self.sectorRe.search(sectorDiv.next.string):
					self.sector = sectorDiv.next.next.string
			return self.sector
		
		def hasSector(self):
			""" Returns whether this page supports Sector information.
			
			For example:
			>>> scraper = Google()
			>>> scraper.hasSector("GOOG")
			True
			
			>>> scraper.hasSector("SATR")
			False
			
			pre:
				self.factory.hasMeta(self.getSymbol())
				
			post[]:
				#typecheck
				isinstance(__return__,bool)
			"""
			if self.sector:
				return True
			sectorDiv = self.soup.find("div",id="related").find("div",attrs={'class':'item'})
			if sectorDiv and self.sectorRe.search(sectorDiv.next.string):
				return True
			else:
				return False
		
		def getIndustry(self):
			""" Returns the name of the industry that the company represented
			by this symbol is considered a part of.  This is a service provided
			to the Google class.
			
			For example:
			>>> scraper = Google()
			>>> scraper.getIndustry("GOOG")
			u'Computer Services'
			
			>>> scraper.getIndustry("DOW")
			u'Chemicals - Plastics & Rubber'
			
			>>> scraper.getIndustry("SATR")
			Traceback (most recent call last):
				...
			IndustryInformationNotFound: Could not find Industry Information for symbol: \"SATR\"
			
			pre:
				self.factory.hasMeta(self.getSymbol())
				
			post[self.industry]:
				isinstance(__return__,unicode)
				
				#cache check
				self.industry != __old__.self.industry if __old__.self.industry == "" else True
			"""
			if not self.industry:
				if not self.hasIndustry():
					raise IndustryInformationNotFound(self.getSymbol())
			 	industryDiv = self.soup.find("div",id='related').find("div",attrs={'class':'item'})
			 	industryDiv = industryDiv.next.next.next #skip ahead since 'sector' comes before 'industry'
				if self.industryRe.search(industryDiv.next.string):
					self.industry = industryDiv.next.next.string
			return self.industry
			
		def hasIndustry(self):
			""" Returns whether or not this page supports Industry information.
			
			For example:
			>>> scraper = Google()
			>>> scraper.hasIndustry("GOOG")
			True
			
			>>> scraper.hasIndustry("DOW")
			True
			
			>>> scraper.hasIndustry("SATR")
			False
			
			pre:
				self.factory.hasMeta(self.getSymbol())
				
			post[]:
				#type check
				isinstance(__return__,bool)
				
			"""
			
			if self.industry:
				return True
			industryDiv = self.soup.find("div",id="related").find("div",attrs={'class':'item'})
			
			#walk the divider making sure each 'next' is there.
			if not industryDiv:
				return False
			industryDiv = industryDiv.next
			if not industryDiv:
				return False
			industryDiv = industryDiv.next
			if not industryDiv:
				return False
			industryDiv = industryDiv.next
			if not industryDiv:
				return False
			
			if self.industryRe.search(industryDiv.next.string):
				return True
			else:
				return False
			
		def getProperName(self):
			""" Returns the proper name of the company represented by this 
			symbol.  This is a service provided to the Google class.
			
			For example:
			>>> scraper = Google()
			>>> scraper.getProperName("GOOG")
			u'Google Inc.'
			
			>>> scraper.getProperName("DOW")
			u'The Dow Chemical Company'
			
			pre:
				self.factory.hasMeta(self.getSymbol())
				
			post[self.properName]:
				#typechecking
				isinstance(__return__,unicode)
				
				#cache check
				self.properName != __old__.self.properName if __old__.self.properName == "" else True
				
			"""
			if not self.properName:
				self.properName = self.soup.find('table',id='companyheader').h1.string
			return self.properName

		def hasProperName(self):
			""" Returns whether or not this page supports a Proper Name 
			
			For example:
			>>> scraper = Google()
			>>> scraper.hasProperName("GOOG")
			True
			
			>>> scraper.hasProperName("DOW")
			True
			
			pre:
				self.factory.hasMeta(self.getSymbol())
				
			post[]:
				#typechecking
				isinstance(__return__,bool)	
			"""
			if self.properName:
				return True
			elif self.soup.find('table',id='companyheader') and self.soup.find('table',id='companyheader').h1.string:
				return True
			else:
				return False

	class SoupFactory:
		""" A helper class that builds Beautiful Soup objects and handles page look ups for the more specialized 
		soup parser objects inside Google.
		
		 
		inv:
			isRegex(self.invalidResultRe)
			isRegex(self.incomeLinkRe)
			
			self.incomeLinkRe.search("Income Statement") is not None
			self.invalidResultRe.search("Show all 12 companies") is not None
			
			self.incomeLinkRe == Google.SoupFactory.incomeLinkRe
			self.invalidResultRe == Google.SoupFactory.invalidResultRe
			
			#typecheck
			isinstance(self._metaCache, dict)
			isinstance(self._SECCache, dict)
			isinstance(self._basicCache, dict)
			
			all(isString(x) for x in self._metaCache.keys())
			all(isString(x) for x in self._SECCache.keys())
			all(isString(x) for x in self._basicCache.keys())
			
			all(isinstance(x, BeautifulSoup.BeautifulSoup) for x in self._metaCache.values())
			all(isinstance(x, BeautifulSoup.BeautifulSoup) for x in self._SECCache.values())
			all(isinstance(x, BeautifulSoup.BeautifulSoup) for x in self._basicCache.values())
			
		"""
		
		invalidResultRe = re.compile("(Show all [0-9]+ (companies|(mutual funds)))|([0-9]+ companies)|([0-9]+ funds)")
		invalidHeaderRe = re.compile("(All.*-.*[0-9]+ companies.*-.*[0-9] funds)", flags=re.DOTALL)
		incomeLinkRe = re.compile("Income.*Statement")
		
		
		def __init__(self):
			""" Soup factory's constructor """
			self._metaCache = {}
			self._SECCache = {}
			self._basicCache = {}
			
		def buildBasicSoup(self, symbol):
			""" Public function that takes in a symbol and returns a Beautiful Soup object of that symbol's 
			Basic information page parsed. This assumes nothing and is a way to capture search or 'symbol not found' pages.
			
			No examples because it'd be too complicated to show the soup returning, but that is enforced with a typechecking
			contract.
			TODO: test this via a unit test harness
			
			pre:
				#typecheck
				isinstance(symbol, str) or isinstance(symbol, unicode)
				
			post[self._basicCache, symbol]:
				#typecheck
				isinstance(__return__,BeautifulSoup.BeautifulSoup)
				
				#check cacheing
				symbol in self._basicCache if not symbol in __old__.self._basicCache else self._basicCache[symbol] == __old__.self._basicCache[symbol]
			"""
			
			if not self._basicCache.has_key(symbol):
				url = urllib2.urlopen(self._buildBaseURL(symbol))
				self._basicCache[symbol] = BeautifulSoup.BeautifulSoup(url)
			return self._basicCache[symbol]
									
		
		def buildMetaSoup(self, symbol):
			""" Public function that takes in a symbol and returns a Beautiful Soup object of that symbol's
			Meta information page parsed.  This assumes the symbol exists and will throw an error otherwise.
			
			No examples because it'd be too complicated to show the soup returning, but that is enforced with a typechecking
			contract.
			TODO: add an example, basically you have to exercise everything that Google does now for a single case and method call.
			
			pre:
				#typecheck
				isinstance(symbol, str) or isinstance(symbol, unicode)
				
			post[self._metaCache, symbol]:
				#typecheck
				isinstance(__return__,BeautifulSoup.BeautifulSoup)

				#check cache				
				symbol in self._metaCache if not symbol in  __old__.self._metaCache else self._metaCache[symbol] == __old__.self._metaCache[symbol]
				
			"""
			
			if not self._metaCache.has_key(symbol):
	   	   	   	if not self.hasBasic(symbol):
					raise SymbolNotFound(symbol)
	   	   	   	if not self.hasMeta(symbol):
					raise SymbolNotFound(symbol)
				else:
					self._metaCache[symbol] = self.buildBasicSoup(symbol) 
					
			return self._metaCache[symbol]
				
		def buildSECSoup(self, symbol):
			""" Public function that takes in a symbol and returns a Beautiful Soup object of that symbol's
			financial page parsed.
			
			No examples because it'd be too complicated to show the soup returning, but that is enforced with a typechecking
			contract.
			TODO: add an example, basically you have to exercise everything that Google does now for a single case and method call.
			
			pre:
				#typecheck
				isinstance(symbol, str) or isinstance(symbol, unicode)
				
			post[self._SECCache, symbol]:
				#typecheck
				isinstance(__return__,BeautifulSoup.BeautifulSoup)
				
				#cache check
				symbol in self._SECCache if not symbol in __old__.self._SECCache else self._SECCache[symbol] == __old__.self._SECCache[symbol]
				
			"""
			
			if not self._SECCache.has_key(symbol):
	   	   	   	if not self.hasBasic(symbol):
					raise SymbolNotFound(symbol)
	   	   	   	if not self.hasSEC(symbol):
					raise SymbolHasNoFinancials(symbol) 
				else:
					url = urllib2.urlopen(self._buildSECURL(symbol))
					self._SECCache[symbol] = BeautifulSoup.BeautifulSoup(url) 
			return self._SECCache[symbol]
		
		def _buildBaseURL(self, symbol):
			""" Used internally to soup factory to build a base URL for all soup objects 
			symbols looked up.
		
			Example: #For testing purposes only
		
			>>> example = Google.SoupFactory()
			>>> example._buildBaseURL('FDX')
			u'http://finance.google.com/finance?q=FDX'
			
			pre:
				#typecheck
				isinstance(symbol,str) or isinstance(symbol,unicode)
		
			post[]:
				#typechecking
				isinstance(__return__,str) or isinstance(__return__,unicode)
			
			
			"""
			return unicode("http://finance.google.com/finance?q=%s" % symbol)
		
		@staticmethod
		def _findSuffix(links, searchRe):
			""" Helper function to find a link that matches the search regex.  
			
			TODO: this is probably a re-implementation of something already in beautiful soup, you should investigate it.
			
			pre:
				#typecheck
				isRegex(searchRe)
			
			post:
				#typecheck
				isinstance(__return__, str) or isinstance(__return__, unicode)
			"""
			for link in links:
				if link.string and searchRe.search(link.string):
					return link['href']
			return None
		
		def _buildSECURL(self, symbol):
			""" Builds the proper URL for a particular stock symbol's SEC information 	
			Example: #For testing purposes only
		
			>>> example = Google.SoupFactory()
			>>> example._buildSECURL('FDX')
			u'http://finance.google.com/finance?fstype=ii&q=NYSE:FDX'
		
		
			pre:
				isinstance(symbol,str) or isinstance(symbol,unicode)
				self.hasSEC(symbol)
		
			post[]:
				#typechecking
				isinstance(__return__,str) or isinstance(__return__,unicode)
			
			
			
			
			"""			
			soup = self.buildBasicSoup(symbol)
			links = soup.findAll('a')
			suffix = self._findSuffix(links, self.incomeLinkRe)
		
			return unicode("".join(["http://finance.google.com/finance",suffix]))
		
		def hasSEC(self, symbol):
			""" A public predicate that returns whether or not this symbol supports lookup of SEC information.
			
			>>> x = Google.SoupFactory()
			>>> x.hasSEC("IRBT")
			True
			
			>>> x.hasSEC("NTDOY")
			False
			
			pre:
				#typecheck
				isinstance(symbol,unicode) or isinstance(symbol,str)
			
			post[]:
				#typecheck
				isinstance(__return__, bool)
			
			"""
			if not self.hasBasic(symbol):
				return False
			elif not self._isSECSoup(self.buildBasicSoup(symbol)):
				return False
			return True
			
		def hasMeta(self, symbol):
			""" A public predicate that returns whether or not this symbol supports lookup of meta information
			
			>>> x = Google.SoupFactory()
			>>> x.hasMeta("DD")
			True
			
			>>> x.hasMeta("FART")
			False
			
			pre:
				#typecheck
				isinstance(symbol,unicode) or isinstance(symbol, str)
				
			post[]:
				#typecheck
				isinstance(__return__,bool)
				
			"""
			
			if not self.hasBasic(symbol):
				return False
			elif not self._isMetaSoup(self.buildBasicSoup(symbol)):
				return False
			return True
			
		def hasBasic(self, symbol):
			""" A public predicate that returns whether or not this symbol supports basic lookup and is a symbol at all.
			
			>>> x = Google.SoupFactory()
			>>> x.hasBasic("NTDOY")
			True
			
			>>> x.hasBasic("MMMMM")
			False
			
			pre:
				isinstance(symbol,str) or isinstance(symbol,unicode)
				
			post[]:
				isinstance(__return__,bool)
				
			"""
			
			if not self._isBasicSoup(self.buildBasicSoup(symbol)):
				return False
			return True
		
		def _isSECSoup(self, soup):
			""" A predicate that returns whether or not this symbol has SEC information . Helper function to hasBasic
			
			pre:
				#typecheck
				isinstance(soup,BeautifulSoup.BeautifulSoup)
				
			post[]:
				#typecheck
				isinstance(__return__,bool)
			"""
			
			financialDiv = soup.find('div', id='financials')
			if not financialDiv:
				return False
			return True
		
		def _isMetaSoup(self, soup):
			""" A predicate that returns whether or not this symbol has meta information 
			
			pre:
				#typecheck
				isinstance(soup,BeautifulSoup.BeautifulSoup)
			
			post[]:
				#typecheck
				isinstance(__return__,bool)
			
			"""
			return self._isBasicSoup(soup)
		
		def _isBasicSoup(self, soup):
			""" A predicate that returns whether or not this symbol has basic information, helper function to
			isBasic.
			
			pre:
				#typecheck
				isinstance(soup,BeautifulSoup.BeautifulSoup)
				
			post[]:
				#typecheck
				isinstance(__return__,bool)
			 
			"""
			if soup.findAll(text=lambda x: "produced no matches" in x):
				return False #for flat out not found pages
			
			
			
			links = soup.findAll('a')
			for link in links:
				if link.string and self.invalidResultRe.search(link.string):
					return False #for search pages
			
			return True
		
	def _delegateInterface(self, interface, wrapper):
		""" Helper private function that implements my own little delegated interface idiom.
		Pushes the interface's methods on to this object, and sets all of the calls equal to 
		'wrapper' which gets passed in the method name and arguments.
		
		pre:
			#typechecking
			isinstance(dir(interface), list)
			all(isinstance(x, str) for x in dir(interface))
			callable(wrapper)
			
			#make sure i don't already have the attribute
			all(not hasattr(self,x) for x in publicInterface(interface))
			
		post[self]:
			#ensure that i've added the attributes
			all(hasattr(self,x) for x in publicInterface(interface))
			all(callable(getattr(self,x)) for x in publicInterface(interface))
			
			#has documentation string
			all(hasattr(getattr(self,x),'__doc__') for x in publicInterface(interface))
		
		"""
	   	for method in publicInterface(interface): 
	   	   	setattr(self,method, self._functionWrapper(wrapper,method))
	   	   	getattr(self,method).__doc__ = " This method is delegated to %s, check documentation there. " % interface
	   	   	

	def _functionWrapper(self, func, methodName):
		""" I can't use a lambda for this because lambda's don't bind to their arguments until they
		are called.  Meaning if i call lambda x: y(x), it call's whatever y is THEN, and if y has
		changed via a reference or something, then the lambda has completely changed! 
		
		pre:
			isinstance(methodName, str) or isinstance(methodName, unicode)
			callable(func)
			
		post[]:
			callable(__return__)
		
		"""
		def _(*args):
			return func(methodName, *args)
		return _
		
		
	def _metaWrapper(self, method, symbol):
		""" Wrapper function to call meta methods on an underlying, cached meta object 
		
		pre:
			#typechecking
			isinstance(method, str) or isinstance(method, unicode)
			isinstance(symbol, str) or isinstance(symbol, unicode)
			
		post[self._metaCache, symbol]:
			#check that symbol has been cached.
			symbol in self._metaCache if not symbol in __old__.self._metaCache else self._metaCache[symbol] == __old__.self._metaCache[symbol]
			
		"""
		if not self._metaCache.has_key(symbol):
			self._metaCache[symbol] = self.Metadata(self.factory.buildMetaSoup(symbol), self.factory)
		return getattr(self._metaCache[symbol],method)()
	
	def _SECWrapper(self, method, symbol, date=None):
		"""A wrapper used around calls to SECData.  This allows me to delegate SECData's entire interface
		onto Google at runtime.
		
		pre:
			#typechecking
			hasattr(self.SECData(), method)
			isinstance(date,datetime.date) or isinstance(x,datetime.datetime) if date else True
			isinstance(symbol, str) or isinstance(symbol, unicode)
			isinstance(method, str) or isinstance(method, unicode)
		
		post[self._SECCache]:
			#typechecking
			isinstance(__return__,dict) or isinstance(__return__, float)
			all(isinstance(x, datetime.date) for x in __return__.keys()) if isinstance(__return__,dict) else True
			all(isinstance(x, float) or isinstance(x,str) or isinstance(x,unicode) for x in __return__.values()) if isinstance(__return__,dict) else True
			symbol in self._SECCache if not symbol in __old__.self._SECCache else self._SECCache[symbol] == __old__.self._SECCache[symbol]
		"""
		
		if not self._SECCache.has_key(symbol):
			self._SECCache[symbol] = self.SECData(self.factory.buildSECSoup(symbol))
			
		#TODO: check to see if there's a valid name here
		results = getattr(self._SECCache[symbol], method)()	
			
		if date:
			try:
				results = results[date]
			except KeyError, e:
				raise DateNotFound(symbol,date)
		return results
			
	def __init__(self):
		""" Google's constructor.
		
		post[self]:
			#check to make sure attributes are added
			all([hasattr(self,x) for x in publicInterface(self.SECData())])
			
		"""

		prototype = self.SECData()  # SECData's interface doesn't get fully set until it's built so I need an instantiated object
		self.factory = self.SoupFactory()
		
		#add SEC info
	   	self._delegateInterface(prototype, self._SECWrapper) 
		self._SECCache = {}
		
		#add meta info
		self._delegateInterface(self.Metadata, self._metaWrapper)
		self._metaCache = {}
									
		#TODO: should also put this at the class level
		#TODO: this sort of 'information' stuff should be formalized in the bloomberg concept.
#		TODO: Investigate whether class inheritance interfaces are resolved at runtime
#		or compile time.
		#TODO: can get rid of "args", lambda's take default arguments.  even better would be having an explicit function creating 
		#function
#		Function can throw exceptions in two cases.
#		1. Function is given a symbol that flat out does not exist.
	   #TODO: USE THESE FOR UNIT TESTS FOR NEW META STUFF TO ENSURE IT THROWS THE PROPER EXCEPTIONS
#		
#		>>> example.getQuarterlyRevenue("fart")
#		Traceback (most recent call last):
#			...
#		SymbolNotFound: Could not find symbol : \"fart\"
#		
#		2. Function is given a symbol that returns search results
#		and does not exist directly.
#		
#		>>> example.getQuarterlyRevenue("happy")
#		Traceback (most recent call last):
#			...
#		SymbolNotFound: Could not find symbol : \"happy\"
		#TODO: figure out 'find' syntax for lists.  there ought to be a find for lists.
		#TODO: instead of filter, us decorate, find, undecorate.
		#TODO: might be able to put this all in the page.findAll method call
#			#make sure i haven't corrupted cache
#			len(self.cachedPages) >= len(__old__.self.cachedPages)
	   	   	#TODO: ADD TESTS TO CHECK THAT CACHE ISN'T CORRUPTED...
#		#TODO: due to my new implementation of this classes interface(i no longer use __getattr__)
#		# this function might be able to do better type checking and be more integrated into
#		# the rest of the class