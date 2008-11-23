from Service import Service
from Signature import Signature, SignatureMap
import datetime
from elixir import *
from Registry import Registry
from sqlalchemy import UniqueConstraint
import copy
from FinancialDate import toDate

#TODO: refactoring goals
#build a generic memoization framework 
#investigate PEAK and multimethods, and probably replace the registry with a more generic
#out-of-the-box callback mechanism.

class Bloomberg(object):
	""" Provides functions for mapping "Hosts" to "Interfaces".  Hosts are things that say they can provide a certain service
	given a certain contract, while Interfaces are items that need that service and also provide a certain contract/signature.
	Bloomberg does the job of matching up interfaces to hosts """
	pass

#	#prefecth problems...
#	#prefetch method must be accessed via the 'fetch' method from market.symbol...., otherwise, multiple entries get put into 
#	#the database since that is the only way to get access to 'fetched' data.  i need to look further into enforcing uniqueness of
#	#data by symbol and date.  the constraints don't seem to be able to be enforced...

def Daily(document):
	
	return SECFiling(DailyMixin)(document)

def Annual(document):
	
	return SECFiling(AnnualMixin)(document)

def Quarterly(document):
	
	return SECFiling(QuarterlyMixin)(document)

def Meta(document):
	
	return SECFiling(MetaMixin)(document)
					
class SECFiling(Bloomberg):
	
	def __init__(self, filing):
		self.filing = filing
	
	def __call__(self, document):
		
		name = self.filing.createName(document.__name__)
		
		dct = self.buildServiceDict(self.ServicesSupported(document))
		dct.update(self.filing.buildDct(name))
		dct.update({"commit_on_change":True})
		
		return EntityMeta(name, (self.filing,), dct)
		
	def ServicesSupported(self, document):
		return [(service,getattr(document,service)) for service in dir(document) if isinstance(getattr(document,service),Field)]
	
	def initializerKey(self, name):
		return "".join(["__initialized__",name])
	
	def cacheKey(self, name):
		return "".join(["_",name])
	
	def ServiceDictBuilder(self, serviceName, field):
		initializerKey = self.initializerKey(serviceName)
		cacheKey = self.cacheKey(serviceName)
		function = Registry.getService(*self.buildService(serviceName))
		
		class ServiceDescriptor(object):	
			def __get__(self, inst, owner):
				if not getattr(inst, initializerKey):
					try:
						inst.__dict__[cacheKey] = function(inst)
						inst.__dict__[initializerKey] = True
					except KeyError:
						raise Exception("Service %s is not registered" % str(service))
				return inst.__dict__[cacheKey]
	
		return {initializerKey : Field(Boolean()),
		  	cacheKey : copy.deepcopy(field),
		  	serviceName : ServiceDescriptor() }
		
	def buildServiceDict(self, services):
		dictbuilt = {}
		for serviceName, fieldType in services:
			dictbuilt.update(self.ServiceDictBuilder(serviceName, fieldType))

		dictbuilt["prefetch"] = self.buildPrefetchMethod([serviceName for serviceName,_ in services])
		return dictbuilt

	def buildPrefetchMethod(self, services):
		def _(self):
			return dict([(service, getattr(self,service)) for service in services])
		return _	
		
	def buildService(self, serviceName):
		return self.filing.getService(serviceName)

#i have not yet figured out how to do entity inheritance yet in a way that doesn't reload the whole database each time.
class DateMixin(object):

#it may make sense to put a 'state' pattern inside the date mixin which allows or disallows certain access?
	def __init__(self, symbol, date=None):
		self.Symbol = symbol
		self.Date = date
		
	@classmethod
	def AvailableDates(cls, symbol):
		return [toDate(x.Date) for x in cls.query().filter_by(Symbol=symbol).all()]
	
	@classmethod	
	def buildDct(cls, documentName):
		
		@classmethod
		def WebDates(cls, symbol):
			return Registry.getServiceFunction(Service.Meta(documentName + "Dates"))(symbol)
		
		return {"WebDates": WebDates}
	
	@classmethod
	def NewDates(cls, symbol):
		available = set(cls.AvailableDates(symbol))
		onTheWeb = set(cls.WebDates(symbol))
		return list(onTheWeb - available)

	@classmethod
	def getService(cls, serviceName):
		return [cls.getSubService(serviceName), SignatureMap({"symbol":"Symbol","date":"Date"})]
	
	@classmethod
	def fetch(cls, symbol, date):
		dbCache = cls.query.filter_by(Symbol=symbol,Date=date).all()
		if not dbCache:
			return cls(symbol, date)
		else:
			if len(dbCache) > 1:
				raise Exception("Returned multiple results on query for: %s (%s %s)" % (cls, symbol, str(date)))
			else:
				return dbCache[0]

class QuarterlyMixin(DateMixin, Entity):
	Symbol = Field(Unicode(10))
	Date = Field(DateTime)
		
	@staticmethod
	def getSubService(serviceName):
		return Service.Quarterly(serviceName)
	
	@classmethod
	def createName(cls, name):
		return "".join(["Quarterly",name])

class AnnualMixin(DateMixin, Entity):
	Symbol = Field(Unicode(10))
	Date = Field(DateTime)
	
	@classmethod
	def getSubService(cls, serviceName):
		return Service.Annually(serviceName)
	
	@classmethod
	def createName(cls, name):
		return "".join(["Annual",name])

class DailyMixin(DateMixin, Entity):	
	Symbol = Field(Unicode(10))
	Date = Field(DateTime)

	@classmethod
	def getSubService(cls, serviceName):
		return Service.Daily(serviceName)
	
	@classmethod
	def createName(cls, name):
		return "".join(["Daily",name])
	
class MetaMixin(Entity):
	Symbol = Field(Unicode(10))
	
	@classmethod
	def buildDct(cls, documentName):
		return {}
	
	def __init__(self, symbol):
		self.Symbol = symbol
	
	@classmethod
	def getService(cls, serviceName):
		return [Service.Meta(serviceName), SignatureMap({"symbol":"Symbol"})]
	
	@classmethod
	def createName(cls, name):
		return "".join(["Meta",name])
	
	@classmethod
	def fetch(cls, symbol):
		dbCache = cls.query.filter_by(Symbol=symbol).all()
		if not dbCache:
			return cls(symbol)
		else:
			if len(dbCache) > 1:
				raise Exception("Returned multiple results on query for: %s (%s)" % (cls, symbol))
			else:
				return dbCache[0]	

#TODO: do a protocol implementation that maps FinancialDate.Quarter to just a datetime.date