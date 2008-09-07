from Service import Service
from Signature import Signature, SignatureMap
import datetime
from elixir import *
from Registry import Registry
from sqlalchemy import UniqueConstraint
import copy

class Bloomberg(object):
	""" Provides functions for mapping "Hosts" to "Interfaces".  Hosts are things that say they can provide a certain service
	given a certain contract, while Interfaces are items that need that service and also provide a certain contract/signature.
	Bloomberg does the job of matching up interfaces to hosts """


def initfunction(cls):
	def init(self, symbol, date):
#		super(cls,self).__init__()
		#i dont quite understand what this line is supposed to do.  who's init function is 
		#this supposed to call anyway?
#		print "calling init, symbol = ", symbol, "date = ", date
#		self.Symbol = symbol
#		self.Date = date
		pass
	return init

#class BloombergEntry(Entity):
#	Symbol = Field(Unicode(10))
#	Date = Field(Unicode(10))
#	using_options(UniqueConstraint("Symbol","Date"))
#	using_options(inheritance="single")
	
def buildServiceDict(services, filing):
	dictbuilt = {}
	for serviceName, fieldType in services:
		fieldkey = "".join(["_",serviceName])
		fieldval = copy.deepcopy(fieldType)
		print "in buildsd loop", fieldType
		propertykey = serviceName
		propertyval = Registry.getService(*filing.buildService(serviceName))
		dictbuilt[fieldkey] = fieldval
		dictbuilt[propertykey] = propertyval
	print "in build servicedict ", dictbuilt
	return dictbuilt

def ServicesSupported(cls):
	#print cls, [type(x) for x in dir(cls)], "inside _services supported"
	return [(service,getattr(cls,service)) for service in dir(cls) if isinstance(getattr(cls,service),Field)]
	
class SECFiling_(EntityMeta):
	class ATABLE(object):
		#TODO: add this at the outside scope, to be passed in.
		constraints = [UniqueConstraint("Symbol","Date")]
#		Symbol = Field(Unicode(10))
#		Date = Field(DateTime)		
		
#		using_options(inheritance="multi")
#		using_table_options(useexisting=True)
		for constraint in constraints:
			using_options(constraint)
			
	def __new__(cls, name, bs, filing):
		bases = []
		dct = {}
		
		bases = (Entity, SECFiling_.ATABLE, SECFiling)
		
#		def init(self, symbol, date):
#			print self, cls
#			# You are here.  how do i call super when the type isn't created yet?
#			super(cls, self).__init__()
#			self.Symbol = symbol
#			self.Date = date
		
#		dictbuild = []
		
		dct.update(buildServiceDict(ServicesSupported(bs), filing))
		dct["__init__"] = initfunction(cls)
		dct["Symbol"] = Field(Unicode(10))
		dct["Date"] = Field(DateTime)
#		cls.Symbol = Field(Unicode(10))
#		cls.Date = Field(DateTime)
		
		return super(SECFiling_, cls).__new__(cls, name, bases, dct)

	def __init__(cls, name, bs, filing):
		
#		dictbuild = []
#		for service,sig in bs.services.items():
#			fieldkey = "".join(["_",service])
#			fieldval = sig()
#			propertykey = service
#			propertyval = Registry.getService(*filing.buildService(service))
#			dictbuild.append((fieldkey,fieldval))
#			dictbuild.append((propertykey,propertyval))
#		dictbuilt = dict(dictbuild)
#		dct.update(dictbuilt)
		
#		bases = list(bases)
#		bases.append(SECFiling)
#		bases.append(Entity)
#		bases.append(BuilderMeta.ATABLE)
#		bases = tuple(bases)

		bases = (SECFiling, Entity, SECFiling_.ATABLE)
		dct = {}
		dct.update(buildServiceDict(ServicesSupported(bs), filing))
		dct["__init__"] = initfunction(cls)
		dct["Symbol"] = Field(Unicode(10))
		dct["Date"] = Field(DateTime)
		
		print dir(cls), "before init"
		super(SECFiling_, cls).__init__(name, bases, dct)
		print dir(cls),  "after init"
		
#		cls.Symbol = Field(Unicode(10))
#		cls.Date = Field(DateTime)

#	@classmethod
#	def Builder(cls, name, bs, filing):
#		dictbuild = []
#		for service,sig in bs.services.items():
#			fieldkey = "".join(["_",service])
#			fieldval = sig()
#			propertykey = service
#			propertyval = Registry.getService(*filing.buildService(service))
#			dictbuild.append((fieldkey,fieldval))
#			dictbuild.append((propertykey,propertyval))
#		dictbuilt = dict(dictbuild)
		
#		return cls(name, (), {}, bs, filing)

		# you are here.  move the below function into the meta class.
		# then figure out whether you can, at this point in __init__, introspect the class before its returned and
		# set up registry stuff HERE.  it makes sense that you'd be able to.
		# then quarterly and annual balance sheet cna do inheritance from BalanceSheet proper, like i think elixir expects
		# but their registered functions WILL be, in fact, pointed at different services(one getting the quarterly info, etc)
		# i should probably make it multi inheritance since i dont want date/symbol conflicts on the begining of each year
		

class SECFiling(Bloomberg):
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
	def buildService(cls, serviceName, cache=None):
		""" Builds a very common argument list for the caller, based around the name of the service being built.  By 
		convention, if cache(the name of the dbCache field) is not given, all we do is append a _ to the front.  This
		is assumed to be an attribute on the calling class."""
		
		if not cache:
			cache = "".join(["_",serviceName])
		
		return [Service(serviceName, Signature((unicode,"symbol"),(datetime.date,"date")),cls.getConfig()), 
			 	SignatureMap({"symbol":"Symbol", "date":"Date"}), cache]
		
	@staticmethod
	def getConfig():
		raise Exception("Not Implemented")
	
class QuarterlyFiling(SECFiling_, SECFiling):
	def __new__(cls, name, bs):
		return super(QuarterlyFiling, cls).__new__(cls, name, bs, QuarterlyFiling)
	
	def __init__(cls, name, bs):
		return super(QuarterlyFiling, cls).__init__(name, bs, QuarterlyFiling)
	
	@staticmethod
	def getConfig():
		return {"frequency":"quarterly"}

class AnnualFiling(SECFiling_, SECFiling):
	def __new__(cls, name, bs):
		return super(AnnualFiling, cls).__new__(cls, name, bs, AnnualFiling)
	
	def __init__(cls, name, bs):
		return super(AnnualFiling, cls).__init__(name, bs, AnnualFiling)
	
	@staticmethod
	def getConfig():
		return {"frequency":"annually"}
	
	