""" Bloomberg works with the Attributes module to fully decorate a 'bloomberg' class, that is, a class that provides stock info in some way.  The whole framework
consists of a system of registered generic functions, type data for storage, and a name.  The name is a UID for the stock information, while the generic function
defines how to find it 'first time' and the type information defines how to persist it. 

Implementation Notes:
This ought to be combined with Attributes and pulled into a real metaclass rather than these global functions.

There is one single metaclass that all other configuration types inherit from, i.e., meta, annual, daily, etc.  These work with the attributes found
on a class being passed into them.  Metaclasses will be used not via the __metaclass__ hook but instead by explicitly calling them, similar to the way it is done now
except instead of annual being a function, it would be a metaclass inheriting from bloomberg.
"""

from elixir import Field, Boolean, session, Entity, EntityMeta, using_options
import Registry
from Attributes import Require, Provide, AttributeBuilder
from sqlalchemy import UniqueConstraint
from sqlalchemy import Integer
from Adapt import Adapt
import datetime
from Cached import cached

class PersistantHostMeta(type):	
	def __new__(cls, doc):
		oldname = doc.__name__
		newname = cls.getName(oldname)
		

		
		document = cls.create_type(newname)
		
#		document = type(newname, (PersistantHost,Entity), attrs)
		
		for attributeName, attribute in cls.AttributesDetected(doc):
			#if attribute is Provide:
			#	print "!!!!!"
			#if attribute is Require:
				#print "******"
			#setattr(document, attributeName, attribute(attributeName, document, cls.getFunction(attributeName)))
			setattr(document, attributeName, attribute(attributeName, document, cls.getName(attributeName)))
			
		#ugliness mostly due to Elixir's own 'dsl' style syntax which seems to assume you're using their silly syntax.  
		#todo: maybe look into a better way to do this but i'm not sure it exists.
		#we can't use normal syntax because Elixir expects us to be _inside_ their own class using their class setters.
		#the better way to do it might be in looking at how SQLAlchemy sets things up 
		document._descriptor.tablename = document.__name__
		document._descriptor.polymorphic = False
		document._descriptor.inheritance = "concrete"
		document._descriptor.table_args = list([UniqueConstraint(*cls.getConstraints())])
		#document._descriptor.auto_primarykey = 
			
		
		return document
	
	@classmethod
	def create_type(cls, newname):
		
		attrs = {}
		attrs["_required_attributes_"] = []
		attrs["_provided_attributes_"] = []
		
		return type(newname, (PersistantHost, Entity), attrs)
	
	def __init__(cls, name, bases, dct):
		return super(PHMeta,cls).__init__(cls, name, bases, dct)
	
	@classmethod
	def AttributesDetected(cls, doc):
		#we use the hidden 'order' of the attribute to determine where it is in the class.  hack shamelessly stolen from django.
		return sorted([(service,doc.__dict__[service]) for service in doc.__dict__.keys() if isinstance(doc.__dict__[service],AttributeBuilder)], cmp= lambda x,y: cmp(x[1],y[1]))
	
	@classmethod
	def getFunction(cls, name):
		try:
			return Registry.Get(cls.getName(name))
		#TODO: fix this
		except: #hack to drop looks for keys i dont have
			return None
	
	
	
class Annual(PersistantHostMeta):
	
	#as for this new mixin stuff, it'd make sense if i could actually figure out the inheritance structure such that i could mix date and symbol naturally and pull
	#out their funcationality into other metaclasses, i.e., such that annual inherited from both symbol and dated meta, but 'meta' only inherited from symbol
	#for now, i'm just doing it manually
	@classmethod
	def getConstraints(cls):
		return ["_Symbol","_Date"]
	
#	@classmethod
#	def create_type(cls, newname):			
#		attrs = {}
#		attrs["_required_attributes_"] = []
#		attrs["_provided_attributes_"] = []
#		
#		return type(newname, (DatedPersistantHost, Entity), attrs)
		
	
	@classmethod
	def getName(cls, name):
		return "".join(["Annual",name])
	
class Quarterly(PersistantHostMeta):
	
	@classmethod
	def getConstraints(cls):
		return ["_Symbol","_Date"]

	@classmethod
	def getName(cls, name):
		return "".join(["Quarterly",name])
	
	
class Daily(PersistantHostMeta):
	
	@classmethod
	def getConstraints(cls):
		return ["_Symbol","_Date"]
	
	@classmethod
	def getName(cls, name):
		return "".join(["Daily",name])
	
class Meta(PersistantHostMeta):
	
	@classmethod
	def getConstraints(cls):
		return ["_Symbol"]
	
	@classmethod
	def getName(cls, name):
		return name
	
#	@classmethod
#	def getFunction(cls, name):
#		return Registry.Get(name)


#TODO:
# persistnat host ought to be a flyweight, however, both entity and persistant host (who i'm multiply inheriting from, could override _new_.  
class PersistantHost(object):
	""" This represents an object that is stored in a database, similar to Elixir's own entities.  But it adds on a few things to help with lookups, such as
	defining 'required attributes' that are used in the initializer list to do a look up or create a new entry dynamically. """
	
	@classmethod
	def ProvidedAttributeNames(cls):
		""" Returns the names of all attributes 'provided' by a class. """
		return [name for name,obj in cls._provided_attributes_]

	@classmethod
	def RequiredAttributeNames(cls):
		""" Returns the names of all attributes 'required' by a class """
		return [name for name,obj in cls._required_attributes_]

	@classmethod
	def RequiredAttributes(cls):
		""" Returns the attributes 'required' by a class.  """
		return cls._required_attributes_

	@classmethod
	def ProvidedAttributes(cls):
		return cls._provided_attributes_ 
	
	def prefetch(self): 
		""" A convenience function that calls all provided attributes of this object, which will as a side effect pre-load them via the web
		or via the database.  Calling prefetch on many different objects will download their data from the web into the database. """
		 
		return dict([(attribute, getattr(self,attribute)) for attribute in self.ProvidedAttributeNames()])
	
	@classmethod
	def new(cls, *args, **kwargs):
		work = cls(*args, **kwargs)
		for name, attr in cls.ProvidedAttributes():
			attr.set(name, work)
		
		return work
	
	def __init__(self, *args, **kwargs):
		""" Initializer is not 'type safe' naturally so we have to do some checking, otherwise it expects all 'Required Attributes' to be given either
		as positional or keyword arguments, in the order they were defined in the user of this class. 
		
		Implementation Notes:
		A safer __init__ function can be constructed by the metaclass such that argument checking is only done at one time.
		"""
		
		argsList = list(args)
		argsList.reverse()
		for key in self.RequiredAttributeNames():
			try:
				setattr(self, key, kwargs.get(key, argsList.pop()))
			except IndexError:
				raise TypeError("__init__ takes exactly %d arguments, %d given" % (len(self.RequiredAttributes()), len(args) + len(kwargs)))
			
	@classmethod
	def buildQuery(cls, query, *args, **kwargs):
		""" Acts at the class level to build up a query to the database based on Required Attributes.  It does this as a collaboration with the attribute objects
		still on the class itself. Helper function expects an SQLAlchemy query to be given to it to modify.  """

		argsList = list(args)
		argsList.reverse()
		for name, attribute in cls.RequiredAttributes():
			argument = kwargs.get(name, argsList.pop())
			query = attribute.buildQuery(cls, query, name, argument)
		return query
		
	@classmethod
	@cached(20)
	def fetch(cls, *args, **kwargs):
		""" A class creation method similar to __init__ that does a lookup in the database using SQLAlchemy, returning a query that represents the class with 
		required attributes filled in.  If such a class does not exist, fetch creates it. """
		
		query = cls.query
		query = cls.buildQuery(query, *args, **kwargs)		
		dbCache = query.first()

		if not dbCache:
			return cls(*args, **kwargs)
		return dbCache

	
#class DatedPersistantHost(PersistantHost):	
##	@Lazy
	#@classmethod
	#def AvailableDates(cls, symbol):
#		return sorted([Adapt(x.Date,datetime.date) for x in cls.query().filter_by(_Symbol=symbol).all()])
	
#	id = Field(Integer, nullable=True, autoincrement=True)
#	using_options(auto_primarykey=False)