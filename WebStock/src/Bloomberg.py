from elixir import Field, Boolean, session, Entity
from Registry import Registry
from Attributes import Required, Provided, Attribute, DecorateServices, ServicesDetected, ProvidedAttributes, RequiredAttributes

def DecoratePersistantHost(document, name, service):
	
	document = type(name,(document,Entity),{})
	
		
	DecorateServices(document)	
	services = ServicesDetected(document)

	for serviceName, bservice in services:
		bservice.decorate(serviceName, document, service)
		
	#ugliness mostly due to Elixir's own 'dsl' style syntax which seems to assume you're using their silly syntax.  
	#todo: maybe look into a better way to do this but i'm not sure it exists.
	document._descriptor.tablename = name
	document._descriptor.polymorphic = False
	document._descriptor.inheritance = "concrete"
		
	return document

class PersistantHost(object):
	def prefetch(self): 
		return dict([(attribute, getattr(self,attribute)) for attribute in ProvidedAttributes(self)])
	
	def __init__(self, *args, **kwargs):
		argsList = list(args)
		for key in RequiredAttributes(self):
			try:
				setattr(self, key, kwargs.get(key, argsList.pop()))
			except IndexError:
				raise TypeError("__init__ takes exactly %d arguments, %d given" % (len(RequiredAttributes(self)), len(args) + len(kwargs)))
		
	@classmethod
	def fetch(cls, *args, **kwargs):
		attributes = {}
		argsList = list(args)
		for key in RequiredAttributes(cls):
			try:
				attributes["".join(["_",key])] = kwargs.get(key, argsList.pop()) #ew...
			except IndexError:
				raise TypeError("fetch takes exactly %d arguments, %d given" % (len(RequiredAttributes(cls)), len(args) + len(kwargs)))
		
		dbCache = cls.query.filter_by(**attributes).all()
		if not dbCache:
			return cls(*args, **kwargs)
		else:
			if len(dbCache) > 1:
				raise Exception("Returned multiple results on query for: %s (%s)" % (cls, attributes))
			else:
				return dbCache[0]
	
