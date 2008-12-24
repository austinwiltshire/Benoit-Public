from Registry import Registry
import Website
#rom Service import Service
#from Signature import Signature, SignatureMap
import copy
#import datetime
#from elixir import *
#from sqlalchemy import UniqueConstraint
#import copy
#from FinancialDate import toDate
import elixir
from elixir import Entity, Field

from Bloomberg import Required, Provided, Attribute, PersistantHost, DecorateServices, ServicesDetected, DecoratePersistantHost
from Periodic import AvailableDates

#TODO: refactoring goals
#build a generic memoization framework 
#investigate PEAK and multimethods, and probably replace the registry with a more generic
#out-of-the-box callback mechanism.

#	#prefecth problems...
#	#prefetch method must be accessed via the 'fetch' method from market.symbol...., otherwise, multiple entries get put into 
#	#the database since that is the only way to get access to 'fetched' data.  i need to look further into enforcing uniqueness of
#	#data by symbol and date.  the constraints don't seem to be able to be enforced...

def MakePeriodical(document_type):
	def _(document):
		
		document_name = "".join([document_type,document.__name__])
		document = type(document_name,(document,Entity),{})
		
		staticHost = DecoratePersistantHost(document, document_type)
		#staticHost.AvailableDates = AvailableDates
		return staticHost
	return _

def Meta(document):
	
	document = type(document.__name__,(document,Entity),{})
	
	return DecoratePersistantHost(document, "Meta")

Daily = MakePeriodical("Daily")
Annual = MakePeriodical("Annual")
Quarterly = MakePeriodical("Quarterly")

	
#def CreateName(prefix, document, mix=""):
	#return mix.join([prefix, document._descriptor.tablename])
#	return mix.join([prefix, document.__name__])
	
#def SECFiling(filing, document):
#		name = filing.createName(document.__name__)
#		
#		services = document.ServicesSupported()
#		print services, "services"
#		
#		dct = {}
#		for serviceName, fieldType in services:
#			
#			initializerKey = buildInitializerKey(serviceName)
#			cacheKey = buildCacheKey(serviceName)
#			function = Registry.getService(*filing.getService(serviceName))
#			
#			dct[initializerKey] = Field(Boolean())
#			dct[cacheKey] = Field(fieldType.fieldType)
#			dct[serviceName] = buildServiceDescriptor(initializerKey, cacheKey, function)
#		
#		def prefetch(self):
#			return dict([(serviceName, getattr(self,serviceName)) for serviceName,_ in services])
#		
#		dct["prefetch"] = prefetch
#		dct["__document_name__"] = name
##		dct.update(filing.buildDct(name))
#		if '_Industry' in dct:
#			print "LOOOOOOOOOOOOOKING FOR INDUSTRY"
#			print type(dct['_Industry'])
#		return EntityMeta(name, (filing,Entity), dct)

#i have not yet figured out how to do entity inheritance yet in a way that doesn't reload the whole database each time.
#class DateMixin(object):
#
##it may make sense to put a 'state' pattern inside the date mixin which allows or disallows certain access?
#	def __init__(self, symbol, date=None):
#		self.Symbol = symbol
#		self.Date = date
#		
#	@classmethod
#	def AvailableDates(cls, symbol):
#		return [toDate(x.Date) for x in cls.query().filter_by(Symbol=symbol).all()]
#		
#	@classmethod
#	def WebDates(cls, symbol):
#		return Registry.getServiceFunction(Service.Meta(cls.__document_name__ + "Dates"))(symbol)
#	
#	@classmethod
#	def NewDates(cls, symbol):
#		available = set(cls.AvailableDates(symbol))
#		onTheWeb = set(cls.WebDates(symbol))
#		return list(onTheWeb - available)
#
#	@classmethod
#	def getService(cls, serviceName):
#		return [cls.getSubService(serviceName), SignatureMap({"symbol":"Symbol","date":"Date"})]
#	
#	@classmethod
#	def fetch(cls, symbol, date):
#		dbCache = cls.query.filter_by(Symbol=symbol,Date=date).all()
#		if not dbCache:
#			return cls(symbol, date)
#		else:
#			if len(dbCache) > 1:
#				raise Exception("Returned multiple results on query for: %s (%s %s)" % (cls, symbol, str(date)))
#			else:
#				return dbCache[0]
#
#class QuarterlyMixin(DateMixin, Entity):
#	Symbol = Field(Unicode(10))
#	Date = Field(DateTime)
#		
#	@staticmethod
#	def getSubService(serviceName):
#		return Service.Quarterly(serviceName)
#	
#	@classmethod
#	def createName(cls, name):
#		return "".join(["Quarterly",name])
#
#class AnnualMixin(DateMixin, Entity):
#	Symbol = Field(Unicode(10))
#	Date = Field(DateTime)
#	
#	@classmethod
#	def getSubService(cls, serviceName):
#		return Service.Annually(serviceName)
#	
#	@classmethod
#	def createName(cls, name):
#		return "".join(["Annual",name])
#
#class DailyMixin(DateMixin, Entity):	
#	Symbol = Field(Unicode(10))
#	Date = Field(DateTime)
#
#	@classmethod
#	def getSubService(cls, serviceName):
#		return Service.Daily(serviceName)
#	
#	@classmethod
#	def createName(cls, name):
#		return "".join(["Daily",name])
	
	
#get rid of the mixin concept, init and fetch can be replaced by somethign querying for 'attribute' and 'registered' services
#as can prefetch
#name can just be a property of the decorator.
#class MetaMixin(object):
#	Symbol = Field(Unicode(10))
	
#	def __init__(self, symbol):
#		print type(self), symbol, "*@!#*@!(#@!(#@!(#@(!#(@!#(@!#(@!"
#		self.Symbol = symbol
	
#	@classmethod
#	def getService(cls, serviceName):
#		return [Service.Meta(serviceName), SignatureMap({"symbol":"Symbol"})]
	
#	@classmethod
#	def createName(cls, name):
#		return "".join(["Meta",name])
	
#	@classmethod
#	def xfetch(cls, symbol):
#		print cls
#		dbCache = cls.query.filter_by(_Symbol=symbol).all()
#		if not dbCache:
#			print "db cache miss"
#			print cls, "(((((((((((((((((((((((((((((((((((((((((("
#			return cls(symbol)
#		else:
#			print "HIT!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
#			if len(dbCache) > 1:
#				raise Exception("Returned multiple results on query for: %s (%s)" % (cls, symbol))
#			else:
#				return dbCache[0]	

#TODO: do a protocol implementation that maps FinancialDate.Quarter to just a datetime.date