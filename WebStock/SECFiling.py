from Service import Service
from Signature import Signature, SignatureMap
import datetime
from elixir import *
from Registry import Registry
from sqlalchemy import UniqueConstraint
import copy

#TODO: refactoring goals
#build a generic memoization framework 
#investigate PEAK and multimethods, and probably replace the registry with a more generic
#out-of-the-box callback mechanism.

class Bloomberg(object):
	""" Provides functions for mapping "Hosts" to "Interfaces".  Hosts are things that say they can provide a certain service
	given a certain contract, while Interfaces are items that need that service and also provide a certain contract/signature.
	Bloomberg does the job of matching up interfaces to hosts """
	pass


#ef initfunction():
#def init(self, symbol, date):
#		super(cls,self).__init__()
		#i dont quite understand what this line is supposed to do.  who's init function is 
		#this supposed to call anyway?

#	self.Symbol = symbol
#	self.Date = date
#return init

#class BloombergEntry(Entity):
#	Symbol = Field(Unicode(10))
#	Date = Field(Unicode(10))
#	using_options(UniqueConstraint("Symbol","Date"))
#	using_options(inheritance="single")
	
def buildServiceDict(services, filing):
	dictbuilt = {}
	for serviceName, fieldType in services:
		fieldInitKey = "".join(["_initialized_",serviceName])
		fieldkey = "".join(["_",serviceName])
		fieldval = copy.deepcopy(fieldType)
		propertykey = serviceName
		propertyval = Registry.getService(*filing.buildService(serviceName))
		dictbuilt[fieldkey] = fieldval
		dictbuilt[propertykey] = propertyval
		dictbuilt[fieldInitKey] = Field(Boolean())
		
		
	#prefecth problems...
	#prefetch method must be accessed via the 'fetch' method from market.symbol...., otherwise, multiple entries get put into 
	#the database since that is the only way to get access to 'fetched' data.  i need to look further into enforcing uniqueness of
	#data by symbol and date.  the constraints don't seem to be able to be enforced...
	dictbuilt["prefetch"] = buildPrefetchMethod([serviceName for serviceName,_ in services])
	
	return dictbuilt

def buildPrefetchMethod(services):
	def _(self):
		return dict([(service, getattr(self,service)) for service in services])
	return _

def ServicesSupported(cls):
	return [(service,getattr(cls,service)) for service in dir(cls) if isinstance(getattr(cls,service),Field)]
	
class SECFiling(EntityMeta):
	def __new__(cls, name, document, filingType):
		bases = []
		dct = {}
		
		bases = (Entity, filingType)
		
		dct.update(buildServiceDict(ServicesSupported(document), filingType))
		dct.update(filingType.buildDct(name))
		
		return super(SECFiling, cls).__new__(cls, name, bases, dct)

	def __init__(cls, name, document, filingType):
		super(SECFiling, cls).__init__(name, (), {})
		# you are here.  move the below function into the meta class.
		# then figure out whether you can, at this point in __init__, introspect the class before its returned and
		# set up registry stuff HERE.  it makes sense that you'd be able to.
		# then quarterly and annual balance sheet cna do inheritance from BalanceSheet proper, like i think elixir expects
		# but their registered functions WILL be, in fact, pointed at different services(one getting the quarterly info, etc)
		# i should probably make it multi inheritance since i dont want date/symbol conflicts on the begining of each year
		

class SECFiling_(Bloomberg):
#	using_options(inheritance="multi")
#	constraints = [UniqueConstraint("Symbol","Date")]
#	for constraint in constraints:
#		using_options(constraint)
	
	@classmethod
	def buildDct(cls, documentName):
		dct = {"__init__" : SECFiling_.buildInitFunction(),
			   "Symbol" : copy.deepcopy(Field(Unicode(10))),
			   "Date" : copy.deepcopy(Field(DateTime)) }
		dct = cls.buildDatesFunction(dct, documentName)
	 #YOU ARE HERE: somehow i need to do this without having a cache'ed variable and i need a standard
		#sig map too.
		return copy.deepcopy(dct)	
	
	@classmethod
	def buildDatesFunction(cls, dct, documentName):
		name = documentName + "Dates"
		print name
		dct[name] = Registry.getStaticService(Service.Meta(name), SignatureMap({"symbol":"Symbol"}))
		return dct
		
	@staticmethod
	def buildInitFunction():
		def init(self, symbol, date):
			self.Symbol = symbol
			self.Date = date
		return init
	
	@classmethod
	def AvailableDates(cls, symbol):
		print cls
		return [x.Date for x in cls.query().filter_by(Symbol=symbol).all()]
	
	@classmethod
	def BuildDatesFunctionName(cls, documentName):
		return cls.prefix() + documentName + "Dates"
	
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
	
	@classmethod		
	def buildService(cls, serviceName, cache=None, initialized=None):
		""" Builds a very common argument list for the caller, based around the name of the service being built.  By 
		convention, if cache(the name of the dbCache field) is not given, all we do is append a _ to the front.  This
		is assumed to be an attribute on the calling class."""
		
		if not cache:
			cache = "".join(["_",serviceName])
			
		if not initialized:
			initialized = "".join(["_initialized_",serviceName])
		
		return [Service(serviceName, Signature((unicode,"symbol"),(datetime.date,"date")),cls.getConfig()), 
			 	SignatureMap({"symbol":"Symbol", "date":"Date"}), cache, initialized]
		
	@staticmethod
	def getConfig():
		raise Exception("Not Implemented")
	
class Quarterly(SECFiling_):
	@staticmethod
	def getConfig():
		return {"frequency":"quarterly"}

class Annual(SECFiling_):
	@staticmethod
	def getConfig():
		return {"frequency":"annually"}

class Daily(SECFiling_):
	@staticmethod
	def getConfig():
		return {"frequency":"daily"}
	
class Meta(SECFiling_):
	@staticmethod
	def getConfig():
		return {"meta":True}
	
	@staticmethod
	def buildInitFunction():
		def init(self, symbol):
			self.Symbol = symbol
		return init

	@staticmethod
	def buildDct(documentName):
		dct = {"__init__" : Meta.buildInitFunction(),
			   "Symbol" : Field(Unicode(10))}
		return dct
	
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
	
	@classmethod		
	def buildService(cls, serviceName, cache=None, initialized=None):
		""" Builds a very common argument list for the caller, based around the name of the service being built.  By 
		convention, if cache(the name of the dbCache field) is not given, all we do is append a _ to the front.  This
		is assumed to be an attribute on the calling class."""
		
		if not cache:
			cache = "".join(["_",serviceName])
			
		if not initialized:
			initialized = "".join(["_initialized_",serviceName])
			
		return [Service.Meta(serviceName), SignatureMap({"symbol":"Symbol"}), cache, initialized]
		
#	return [Service(serviceName, Signature((unicode,"symbol")),cls.getConfig()), 
#		 	SignatureMap({"symbol":"Symbol"}), cache]
	

#TODO: do a protocol implementation that maps FinancialDate.Quarter to just a datetime.date