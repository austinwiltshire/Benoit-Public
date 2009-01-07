""" These attributes work in tandem with the Bloomberg metaclass framework (which is currently implemented as free functions rather than a proper metaclass).  They
describe different patterns of use on Bloomberg objects that provide stock information.  They encompass both first time access, via the web, for instance, and 
persistance using the Elixir declarative ORM. 

Implementation Notes:

Much of this ought to be combined with the Bloomberg module in a proper metaclass.  """

from elixir import Field, Boolean, session, DateTime, Float
from sqlalchemy import desc, asc
from SafeFloat import SafeFloat
import Registry
import Website

def DecorateServices(cls):
	""" Adds expected variables at the class level. """
	cls._required_attributes_ = []
	cls._provided_attributes_ = [] 
	
def ServicesDetected(cls):
	""" Returns all """
	return [(service,getattr(cls,service)) for service in dir(cls) if isinstance(getattr(cls,service),Attribute)]

def ProvidedAttributeNames(cls):
	""" Returns the names of all attributes 'provided' by a class. """
	return [name for name,obj in cls._provided_attributes_]

def RequiredAttributeNames(cls):
	""" Returns the names of all attributes 'required' by a class """
	return [name for name,obj in cls._required_attributes_]

def RequiredAttributes(cls):
	""" Returns the attributes 'required' by a class.  """
	return cls._required_attributes_

def ProvidedAttributes(cls):
	
	return cls._provided_attributes_ 

class Attribute(object):
	""" Defines a generic attribute on a stock info yielding object.  Attributes provide a framework both for first time use via web calls, persistance and 
	declarative-style use. """
	
	def __init__(self, fieldType):#, *args, **kwargs):
		""" Returns the fieldType this attribute will be stored in the database and cast as. """
		self.fieldType = fieldType
	
	def decorate(self, name, cls, document_type):
		""" Helper function that modifies the class handed in by adding this attribute's persistance and access layers to it. """
		self.function = self.getFunction(name, document_type)
		self.name = name
		self.register(cls, name)
		self.addField(cls, name)
		self.addAccessor(cls, name, document_type)
		
	def addInitializer(self, cls, name):
		""" Helper function that manages initialization of an attribute.  Some information is not available from the web and we must remember not to make new 
		webcalls every single time if information is not available, so we add an extra field to denote initialization. """
		initializerName = self.initializerName(name)
		initializerField = Field(Boolean())
		setattr(cls, initializerName, initializerField)
		
	def initializerName(self, name):
		""" This function represents the scheme used to access initializers, such that all initialization logic is kept in one place. """
		return "".join(["__initialized__",name])
	
	def fieldName(self, name):
		""" This function represents the scheme used to access fields themselves, such that all access logic is kept in one place and names can be 
		changed in one place. """
		return "".join(["_",name])
		
	def addAccessor(self, cls, name, document_type):
		""" Helper function that adds a descriptor to the passed in class that represents the unification of web and persistance access. """
		setattr(cls, name, self.buildDescriptor(name, self.getFunction(name, document_type)))
	
	def addField(self, cls, name):
		""" Helper function that adds the field to the passed in class such that the Elixir ORM framework will detect it. """
		fieldName = self.fieldName(name)
		setattr(cls, fieldName, Field(self.fieldType))
		
	def cleanup(self, arg):
		""" This function is unfortunately needed to remove any None's.  None's may be returned for information that does not exist via the web.  We wrap these 
		None's in an optional type mechanism similar to the Maybe Monad such that operations on None are safe and simply return None. """
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
		""" Virtual function defines how an implementing class defines its descriptor. """
		pass
		
	def getFunction(self, name, document_type):
		""" Virtual function defines how an implementing class gets its generic function. """
		pass

class Provided(Attribute):
	""" This represents an attribute that, given all required attributes on this class are given, this class can provide to the user, usually via a web interface. """
	
	def register(self, cls, name):
		""" Function adds this attribute to the list of attributes on the class. """
		cls._provided_attributes_.append((name,self))
	
	def decorate(self, name, cls, document_type):
		""" Provided attributes need initializers while required attributes do not. """
		self.addInitializer(cls, name)
		super(Provided,self).decorate(name, cls, document_type)
	
	def getFunction(self, name, document_type):
		""" Hack.  Uses the name of the document to do a generic function look up. """
		if document_type is "Meta":
			return Registry.Get(name)
		else:
			realname = "".join([document_type,name])
			return Registry.Get(realname)
	
	def buildDescriptor(self, name, function):
		""" Virtual function defines how a provided descriptor works - notice Set is not defined.  Provided descriptors are filled in via the framework, not the user.
		They should be considered immutable. """
		cache = self.fieldName(name)
		initializer = self.initializerName(name)
		cleanup = self.cleanup
		
		class Descriptor(object):		
			def __get__(self, inst, owner):
				if not getattr(inst, initializer):
					try:
						val = function(inst)
						setattr(inst, cache, val)
						setattr(inst, initializer, True)
						session.commit()
					except KeyError:
						elixir.session.rollback()
						raise Exception("Service %s is not registered" % str(cache))
					except Website.DateNotFound: #these two errors don't work well with rollback due to a misunderstanding on my part.
	   	   	   	   	   	session.commit()
	   	   	   	   	   	inst.delete()
	   	   	   	   	   	raise
					except Website.SymbolNotFound:
						session.commit()
						inst.delete()
						raise
#					except Web stuff.  i need to detect if i just can't get on the web and NOT delete stuff.
				return cleanup(getattr(inst, cache))
		
		return Descriptor()
	
	
	
	def set(self, name, inst):
		cache = self.fieldName(name)
		initializer = self.initializerName(name)
		try:
			val = self.function(inst)
			setattr(inst, cache, val)
			setattr(inst, initializer, True)
		except:
			session.rollback()
			raise

class Required(Attribute):
	""" Signifies an attribute that is expected to be provided by the user.  In other words, its required for the construction of the stock info providing object."""
	
	def register(self, cls, name):
		""" Appends this attribute to the list of required attributes on this class. """
		cls._required_attributes_.append((name,self))
	
	def buildDescriptor(self, name, function):
		""" This descriptor defines get and set, however, get is expected to be provided by the user.  There is no lookup process that takes place. """
		
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
				except:
					session.rollback()
				
		return Descriptor()