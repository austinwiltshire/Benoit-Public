""" A reimagination of the Google Website object """

from Registry import Register
import datetime
from SECFiling import Bloomberg
from Service import Service
from Signature import Signature

import sys
sys.path.append(r"C:\Users\John\Workspace\Webstock\src")
import Website
import Yahoo

#class Website(Bloomberg):
#	""" Website not only provides Bloomberg functions, but also provides access to BeautifulSoup and urllib2 stuff.  It also
#	denotes that the object is a singleton - all websites are singletons.  There are no mutators. """ 
#	pass

#I have to seed google to run once.
Website.Google().getQuarterlyCashAndEquivalents("IRBT", datetime.date(2008,6,28)) #hack to get this google's stuff registered

#===============================================================================
# class Google(Website):
#	""" Google is the Website financial.google.com, in fact there may be a few websites in here but right now this just
#	maps to my current Google implementation. It is a Bloomberg.Host, meaning it provides services given a fulfilled contract. """
#	
#	def __init__(self):
#		self.scraper = Website2.Google()
#		
#	@Register(Service("CashAndEquivalents",Signature((unicode,"symbol"),(datetime.date,"date")),{"frequency":"annually"}), "Google", "Google")
#	def AnnualCashAndEquivalents(self, symbol, date):
#		return self.scraper.getAnnualCashAndEquivalents(symbol, date)
#	
#	@Register(Service("CashAndEquivalents",Signature((unicode,"symbol"),(datetime.date,"date")),{"frequency":"quarterly"}), "Google", "Google")
#	def QuarterlyCashAndEquivalents(self, symbol, date):
#		""" This is just, right now, a mapping down to the old Google for prototyping purposes.  It also registers itself
#		as a host, meaning if someone's looking for "CashAndEquivalents" and they provide the given signature, then
#		Bloomberg can map the two together """
#		return self.scraper.getQuarterlyCashAndEquivalents(symbol, date)
#	
#	@Register(Service("Revenue",Signature((unicode,"symbol"),(datetime.date,"date")),{"frequency":"annually"}), "Google", "Google")
#	def AnnualRevenue(self, symbol, date):
#		return self.scraper.getAnnualRevenue(symbol, date)
#	
#	@Register(Service("Revenue",Signature((unicode,"symbol"),(datetime.date,"date")),{"frequency":"quarterly"}), "Google", "Google")
#	def QuarterlyRevenue(self, symbol, date):
#		return self.scraper.getQuarterlyRevenue(symbol, date)
#===============================================================================
	
	
	#TODO: do a protocol implementation that maps FinancialDate.Quarter to just a datetime.date
	


