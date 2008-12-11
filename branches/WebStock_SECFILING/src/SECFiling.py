from Registry import Registry
import Website
from Service import Service
from Signature import Signature, SignatureMap
import copy
#import datetime
#from elixir import *
#from sqlalchemy import UniqueConstraint
#import copy
#from FinancialDate import toDate
import elixir
from elixir import Entity

#TODO: refactoring goals
#build a generic memoization framework 
#investigate PEAK and multimethods, and probably replace the registry with a more generic
#out-of-the-box callback mechanism.

class BService(object):
	def __init__(self, fieldType, *args, **kwargs):
		self.fieldType = fieldType
	
	def decorate(self, name, cls, service):
		self.addField(cls, name)
		self.addInitializer(cls, name)
		self.addAccessor(cls, name, service)
		
	def addInitializer(self, cls, name):
		initializerName = self.initializerName(name)
		initializerField = elixir.Field(elixir.Boolean())
		setattr(cls, initializerName, initializerField)
		
	def initializerName(self, name):
		return "".join(["__initialized__",name])
	
	def fieldName(self, name):
		return "".join(["_",name])
		
	def addAccessor(self, cls, name, service):
		setattr(cls, name, self.buildDescriptor(self.initializerName(name), self.fieldName(name), self.getFunction(name, service)))
	
	def addField(self, cls, name):
		fieldName = self.fieldName(name)
		setattr(cls, fieldName, copy.deepcopy(self.fieldType))
		
	def buildDescriptor(self, initializerName, fieldName, function):
		return ServiceDescriptor(initializerName, fieldName, function)
		
	def getFunction(self, name, filing):
		pass

class RegisteredService(BService):
	""" This sets a service such that asking for it does a look up. """
	
	def decorate(self, name, cls, filing):
		cls._registered_services_.append(name)
		super(RegisteredService,self).decorate(name, cls, filing)
	
	def getFunction(self, name, service):
		return Registry.getService(*service(name))

class AttributeService(BService):
	""" Sets the service assigned to basically be set-able, rather than looking up any function """
	
	def decorate(self, name, cls, filing):
		cls._attribute_services_.append(name)
		super(AttributeService,self).decorate(name, cls, filing)
	
	def getFunction(self, name, filing):
		return lambda inst: getattr(inst, self.fieldName(name))

class Bloomberg(object):
	
	@classmethod
	def ServicesDetected(cls):
		return [(service,getattr(cls,service)) for service in dir(cls) if isinstance(getattr(cls,service),BService)]
	
	@classmethod
	def DecorateServices(cls):
		cls._attribute_services_ = [] #[serviceName for serviceName,_ in cls._services_ if isinstance(getattr(cls,serviceName), AttributeService)]
		cls._registered_services_ = [] #[serviceName for serviceName,_ in cls._services_ if isinstance(getattr(cls,serviceName), RegisteredService)] 
		
	@classmethod
	def getServices(cls):
		return cls._services_
		
	def prefetch(self): 
		return dict([(serviceName, getattr(self,serviceName)) for serviceName,_ in self._registered_services_])
	
	def __init__(self, *args, **kwargs):
		#attribute service lookup SHOULD assume that attributes are passed in in the order that they are defined, or in the keywords.  but i should still expect them
		#to be in order
		args = list(args)
		for key in self._attribute_services_:
			try:
				setattr(self, key, kwargs.get(key, args.pop()))
			except IndexError:
				raise TypeError("__init__ takes exactly %d arguments, %d given" % (len(self._attribute_services_), len(args) + len(kwargs)))
		
	@classmethod
	def fetch(cls, *args, **kwargs):
		attributes = {}
		args = list(args)
		for key in cls._attribute_services_:
			try:
				attributes["".join(["_",key])] = kwargs.get(key, args.pop()) #ew...
			except IndexError:
				raise TypeError("fetch takes exactly %d arguments, %d given" % (len(cls._attribute_services_), len(args) + len(kwargs)))
		
		dbCache = cls.query.filter_by(**attributes).all()
		if not dbCache:
			return cls(symbol)
		else:
			if len(dbCache) > 1:
				raise Exception("Returned multiple results on query for: %s (%s)" % (cls, attributes))
			else:
				return dbCache[0]
		
class Periodic(Bloomberg):
	@classmethod
	def AvailableDates(cls, symbol):
		return [toDate(x.Date) for x in cls.query().filter_by(Symbol=symbol).all()]
#		
	@classmethod
	def WebDates(cls, symbol):
		return Registry.getServiceFunction(Service.Meta(cls.__document_name__ + "Dates"))(symbol)
#	
	@classmethod
	def NewDates(cls, symbol):
		available = set(cls.AvailableDates(symbol))
		onTheWeb = set(cls.WebDates(symbol))
		return list(onTheWeb - available)
	

#	#prefecth problems...
#	#prefetch method must be accessed via the 'fetch' method from market.symbol...., otherwise, multiple entries get put into 
#	#the database since that is the only way to get access to 'fetched' data.  i need to look further into enforcing uniqueness of
#	#data by symbol and date.  the constraints don't seem to be able to be enforced...


def MakePeriodical(service, prefix):
	def _(document):
		def ServiceFunction(name):
			return [service(name), SignatureMap({"symbol":"Symbol","date":"Date"})]
		
		document_name = CreateName(prefix, document)
		
		return decorate_(document, document_name, ServiceFunction)
	return _
	
Daily = MakePeriodical(Service.Daily,"Daily")
Annual = MakePeriodical(Service.Annually,"Annually")
Quarterly = MakePeriodical(Service.Quarterly, "Quarterly")

def Meta(document):
	
	def MetaService(name):
		return [Service.Meta(name), SignatureMap({"symbol":"Symbol"})]
	
	document_name = CreateName("Meta",document)
	
	return decorate_(document, document_name, MetaService)

class ServiceDescriptor(object):
	def __init__(self, initializerKey, cacheKey, function):	
		self.cacheKey = cacheKey
		self.initializerKey = initializerKey
		self.function = function
		
	def __get__(self, inst, owner):
		if not getattr(inst, self.initializerKey):
			try:
				setattr(inst, self.cacheKey, unicode(self.function(inst)))
				setattr(inst, self.initializerKey, True)
				elixir.session.commit()
			except KeyError:
				elixir.session.rollback()
				raise Exception("Service %s is not registered" % str(service))
		return getattr(inst, self.cacheKey)
	
	def __set__(self, inst, value):
		try:
			setattr(inst, self.cacheKey, value)
			elixir.session.commit()
		except:
			elixir.session.rollback()
			raise

#move this into a module because its basically a singleton builder class.
def decorate_(document, name, service):
#def SECFiling_Decorator(document):
	
	
	document = type(name,(document,Entity),{})
	
		
	document.DecorateServices()	
	services = document.ServicesDetected()

	for serviceName, bservice in services:
		#yet another reason my whole 'plugin framework' is horrendous.
		bservice.decorate(serviceName, document, service)
		
	#ugliness mostly due to Elixir's own 'dsl' style syntax which seems to assume you're using their silly syntax.  
	#todo: maybe look into a better way to do this but i'm not sure it exists.
	document._descriptor.tablename = name
	document._descriptor.polymorphic = False
	document._descriptor.inheritance = "concrete"
		
	return document
	
def CreateName(prefix, document, mix="_"):
	#return mix.join([prefix, document._descriptor.tablename])
	return mix.join([prefix, document.__name__])
	
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