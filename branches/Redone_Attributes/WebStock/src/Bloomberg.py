""" Bloomberg works with the Attributes module to fully decorate a 'bloomberg' class, that is, a class that provides stock info in some way.  The whole framework
consists of a system of registered generic functions, type data for storage, and a name.  The name is a UID for the stock information, while the generic function
defines how to find it 'first time' and the type information defines how to persist it. 

Implementation Notes:
This ought to be combined with Attributes and pulled into a real metaclass rather than these global functions.

There is one single metaclass that all other configuration types inherit from, i.e., meta, annual, daily, etc.  These work with the attributes found
on a class being passed into them.  Metaclasses will be used not via the __metaclass__ hook but instead by explicitly calling them, similar to the way it is done now
except instead of annual being a function, it would be a metaclass inheriting from bloomberg.
"""

from elixir import Field, Boolean, session, Entity
from Registry import Registry
from Attributes import Required, Provided, Attribute, DecorateServices, ServicesDetected, ProvidedAttributeNames, RequiredAttributeNames, RequiredAttributes, ProvidedAttributes

def DecoratePersistantHost(document, document_type):
	""" This helper function works similar to a metaclass, and configures the document class passed into it with information found from the document_type. 
	A persistant host is currently what all users of this must inherit from.  It's useful and makes sense, I just hate the name."""
	
	DecorateServices(document)	
	services = ServicesDetected(document)

	for serviceName, bservice in services:
		bservice.decorate(serviceName, document, document_type)
		
	#ugliness mostly due to Elixir's own 'dsl' style syntax which seems to assume you're using their silly syntax.  
	#todo: maybe look into a better way to do this but i'm not sure it exists.
	#we can't use normal syntax because Elixir expects us to be _inside_ their own class using their class setters.
	#the better way to do it might be in looking at how SQLAlchemy sets things up 
	document._descriptor.tablename = document.__name__
	document._descriptor.polymorphic = False
	document._descriptor.inheritance = "concrete"
		
	return document

class PersistantHost(object):
	""" This represents an object that is stored in a database, similar to Elixir's own entities.  But it adds on a few things to help with lookups, such as
	defining 'required attributes' that are used in the initializer list to do a look up or create a new entry dynamically. """
	
	def prefetch(self): 
		""" A convenience function that calls all provided attributes of this object, which will as a side effect pre-load them via the web
		or via the database.  Calling prefetch on many different objects will download their data from the web into the database. """
		 
		return dict([(attribute, getattr(self,attribute)) for attribute in ProvidedAttributeNames(self)])
	
	@classmethod
	def new(cls, *args, **kwargs):
		work = cls(*args, **kwargs)
		for name, attr in ProvidedAttributes(cls):
			attr.set(name, work)
		
		return work
	
	def __init__(self, *args, **kwargs):
		""" Initializer is not 'type safe' naturally so we have to do some checking, otherwise it expects all 'Required Attributes' to be given either
		as positional or keyword arguments, in the order they were defined in the user of this class. 
		
		Implementation Notes:
		A safer __init__ function can be constructed by the metaclass such that argument checking is only done at one time.
		"""
		
		argsList = list(args)
		for key in RequiredAttributeNames(self):
			try:
				setattr(self, key, kwargs.get(key, argsList.pop()))
			except IndexError:
				raise TypeError("__init__ takes exactly %d arguments, %d given" % (len(RequiredAttributes(self)), len(args) + len(kwargs)))
			
	@classmethod
	def buildQuery(cls, query, *args, **kwargs):
		""" Acts at the class level to build up a query to the database based on Required Attributes.  It does this as a collaboration with the attribute objects
		still on the class itself. Helper function expects an SQLAlchemy query to be given to it to modify.  """
		
		argsList = list(args)
		for name, attribute in RequiredAttributes(cls):
			argument = kwargs.get(name, argsList.pop())
			query = attribute.buildQuery(cls, query, name, argument)
		return query
		
	@classmethod
	def fetch(cls, *args, **kwargs):
		""" A class creation method similar to __init__ that does a lookup in the database using SQLAlchemy, returning a query that represents the class with 
		required attributes filled in.  If such a class does not exist, fetch creates it. """
		
		query = cls.query
		query = cls.buildQuery(query, *args, **kwargs)		
		dbCache = query.first()

		if not dbCache:
			return cls(*args, **kwargs)
		return dbCache