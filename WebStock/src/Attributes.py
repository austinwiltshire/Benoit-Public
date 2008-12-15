from elixir import Field, Boolean, session
from Registry import Registry

def DecorateServices(cls):
	cls._required_attributes_ = []
	cls._provided_attributes_ = [] 
	
def ServicesDetected(cls):
	return [(service,getattr(cls,service)) for service in dir(cls) if isinstance(getattr(cls,service),Attribute)]

def ProvidedAttributes(cls):
	return [name for name,obj in cls._provided_attributes_]

def RequiredAttributes(cls):
	return [name for name,obj in cls._required_attributes_]

class Attribute(object):
	def __init__(self, fieldType, *args, **kwargs):
		self.fieldType = fieldType
	
	def decorate(self, name, cls, service):
		self.register(cls, name)
		self.addField(cls, name)
		self.addAccessor(cls, name, service)
		
	def addInitializer(self, cls, name):
		initializerName = self.initializerName(name)
		initializerField = Field(Boolean())
		setattr(cls, initializerName, initializerField)
		
	def initializerName(self, name):
		return "".join(["__initialized__",name])
	
	def fieldName(self, name):
		return "".join(["_",name])
		
	def addAccessor(self, cls, name, service):
		setattr(cls, name, self.buildDescriptor(name, self.getFunction(name, service)))
	
	def addField(self, cls, name):
		fieldName = self.fieldName(name)
		setattr(cls, fieldName, Field(self.fieldType))
		
	def buildDescriptor(self, initializerName, fieldName, function):
		pass
		
	def getFunction(self, name, filing):
		pass

class Provided(Attribute):
	""" This sets a service such that asking for it does a look up. """
	def register(self, cls, name):
		cls._provided_attributes_.append((name,self))
	
	def decorate(self, name, cls, service):
		self.addInitializer(cls, name)
		super(Provided,self).decorate(name, cls, service)
	
	def getFunction(self, name, service):
		return Registry.getService(*service(name))
	
	def buildDescriptor(self, name, function):
		cache = self.fieldName(name)
		initializer = self.initializerName(name)
		
		class Descriptor(object):		
			def __get__(self, inst, owner):
				if not getattr(inst, initializer):
					try:
						setattr(inst, cache, function(inst))
						setattr(inst, initializer, True)
						session.commit()
					except KeyError:
						elixir.session.rollback()
						raise Exception("Service %s is not registered" % str(cache))
				return getattr(inst, cache)
		
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
					session.commit()
				except:
					session.rollback()
					raise
				
		return Descriptor()