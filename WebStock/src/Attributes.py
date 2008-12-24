from elixir import Field, Boolean, session, DateTime, Float
from sqlalchemy import desc, asc
from SafeFloat import SafeFloat
import Registry
import Website

def DecorateServices(cls):
	cls._required_attributes_ = []
	cls._provided_attributes_ = [] 
	
def ServicesDetected(cls):
	return [(service,getattr(cls,service)) for service in dir(cls) if isinstance(getattr(cls,service),Attribute)]

def ProvidedAttributeNames(cls):
	return [name for name,obj in cls._provided_attributes_]

def RequiredAttributeNames(cls):
	return [name for name,obj in cls._required_attributes_]

def RequiredAttributes(cls):
	return cls._required_attributes_

class Attribute(object):
	def __init__(self, fieldType, *args, **kwargs):
		self.fieldType = fieldType
	
	def decorate(self, name, cls, document_type):
		self.register(cls, name)
		self.addField(cls, name)
		self.addAccessor(cls, name, document_type)
		
	def addInitializer(self, cls, name):
		initializerName = self.initializerName(name)
		initializerField = Field(Boolean())
		setattr(cls, initializerName, initializerField)
		
	def initializerName(self, name):
		return "".join(["__initialized__",name])
	
	def fieldName(self, name):
		return "".join(["_",name])
		
	def addAccessor(self, cls, name, document_type):
		setattr(cls, name, self.buildDescriptor(name, self.getFunction(name, document_type)))
	
	def addField(self, cls, name):
		fieldName = self.fieldName(name)
		setattr(cls, fieldName, Field(self.fieldType))
		
	def cleanup(self, arg):
		if isinstance(self.fieldType, Float):
			return SafeFloat(arg)
		else:
			return arg
		
	def buildQuery(self, cls, query, key, value):
		#hack
		fieldName = self.fieldName(key)
#		if self.fieldType is DateTime and fieldName == "_Date":
#			print "date", value
#			field = getattr(cls, fieldName)
	#		print value
#			return query.filter(field <= value).order_by(desc(field))
#		  	return query
#		else:
#			print "symbol", value
		return query.filter_by(**{fieldName:value})
		
	def buildDescriptor(self, initializerName, fieldName, function):
		pass
		
	def getFunction(self, name, document_type):
		pass

class Provided(Attribute):
	""" This sets a service such that asking for it does a look up. """
	def register(self, cls, name):
		cls._provided_attributes_.append((name,self))
	
	def decorate(self, name, cls, document_type):
		self.addInitializer(cls, name)
		super(Provided,self).decorate(name, cls, document_type)
	
	def getFunction(self, name, document_type):
		if document_type is "Meta":
			return Registry.Get(name)
		else:
			realname = "".join([document_type,name])
			return Registry.Get(realname)
	
	def buildDescriptor(self, name, function):
		cache = self.fieldName(name)
		initializer = self.initializerName(name)
		cleanup = self.cleanup
		
		class Descriptor(object):		
			def __get__(self, inst, owner):
				if not getattr(inst, initializer):
					try:
						val = function(inst)
#						if val != '-':
						setattr(inst, cache, val)
#						else:
#							setattr(inst, cache, None)
						setattr(inst, initializer, True)
						session.commit()
					except KeyError:
						elixir.session.rollback()
						raise Exception("Service %s is not registered" % str(cache))
					except Website.DateNotFound:
						#if date doesn't exist for today then, well, it probably doesn't exist at all.  right now we're gonna go ahead and delete it.
						#but we have to make sure its committed.
	   	   	   	   	   	session.commit()
	   	   	   	   	   	inst.delete()
	   	   	   	   	   	raise
					except Website.SymbolNotFound:
						#same with this, see above.  if we dont find the symbol then it probably doesn't exist at all.
						#inst.delete()
						#but we have to make sure its committed.
						session.commit()
						inst.delete()
						raise
#					except Web stuff.  i need to detect if i just can't get on the web and NOT delete stuff.
						
#						inst.
#						entity.
				return cleanup(getattr(inst, cache))
		
		return Descriptor()

class Required(Attribute):
	""" Sets the service assigned to basically be set-able, rather than looking up any function """
	def register(self, cls, name):
		cls._required_attributes_.append((name,self))
	
	def buildDescriptor(self, name, function):
		cache = self.fieldName(name)
		
		class Descriptor(object):			
			def __get__(self, inst, owner):
				if not getattr(inst, cache):
					raise Exception("Attribute %s is required on initialization" % cache)
				return getattr(inst, cache)
			
			def __set__(self, inst, value):
				if getattr(inst, cache):
					raise Exception("Attribute %s is already set." % cache)
				try:
					setattr(inst, cache, value)
#					session.commit()
				except:
					session.rollback()
#					raise
				
		return Descriptor()