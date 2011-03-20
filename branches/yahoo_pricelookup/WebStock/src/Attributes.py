""" These attributes work in tandem with the Bloomberg metaclass framework (which is currently implemented as free functions rather than a proper metaclass).  They
describe different patterns of use on Bloomberg objects that provide stock information.  They encompass both first time access, via the web, for instance, and 
persistance using the Elixir declarative ORM. 

Implementation Notes:

Much of this ought to be combined with the Bloomberg module in a proper metaclass.  """

from elixir import Field, Boolean, session, DateTime, Float
#from sqlalchemy import desc, asc
from SafeFloat import SafeFloat
import WebsiteExceptions
#import Registry
#import Website

class AttributeBuilder(object):
	
	#used to maintain ordering because python won't :( learned it from django! go django!
	counter = 0
	
	
	def __init__(self, attributeType, fieldType):
		self.attributeType = attributeType
		self.fieldType = fieldType
		self.order = AttributeBuilder.counter
		AttributeBuilder.counter += 1
		
	def __call__(self, name, cls, function):
		return self.attributeType(self.fieldType, name, cls, function)
	
	def __cmp__(self, other):
		return cmp(self.order, other.order)

Provide = lambda x: AttributeBuilder(Provided,x)
Require = lambda x: AttributeBuilder(Required,x)

class Attribute(object):
	""" Defines a generic attribute on a stock info yielding object.  Attributes provide a framework both for first time use via web calls, persistance and 
	declarative-style use. """
	
	def __init__(self, fieldType, name, cls, function):#, *args, **kwargs):
		""" Returns the fieldType this attribute will be stored in the database and cast as. """
		self.fieldType = fieldType
		self.name = name
		self.cls = cls
		self.register(cls, name)
	   	self.function = function
		self.addField(cls, name)
		
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
		return query.filter_by(**{fieldName:value})

class Provided(Attribute):
	""" This represents an attribute that, given all required attributes on this class are given, this class can provide to the user, usually via a web interface. """
	def __init__(self, fieldType, name, cls, function):
		self.addInitializer(cls, name)
		super(Provided,self).__init__(fieldType, name, cls, function)
		
	def register(self, cls, name):
		""" Function adds this attribute to the list of attributes on the class. """
		cls._provided_attributes_.append((name,self))
	
	def __get__(self, inst, owner):
		if not inst:
			#stupid SQL calling everything :(
			return None
		
		cache = self.fieldName(self.name)
		initializer = self.initializerName(self.name)
		cleanup = self.cleanup
				
		if not getattr(inst, initializer):
			try:
				val = self.function(inst)
				setattr(inst, cache, val)
				setattr(inst, initializer, True)
				session.commit()
			except KeyError:
				elixir.session.rollback()
				session.close()
				raise Exception("Service %s is not registered" % str(cache))
			except WebsiteExceptions.DateNotFound: #these two errors don't work well with rollback due to a misunderstanding on my part.
   	   	   	   	   	session.commit()
   	   	   	   	   	inst.delete()
   	   	   	   	   	raise
			except WebsiteExceptions.SymbolNotFound:
					session.commit()
					inst.delete()
					raise
#					except Web stuff.  i need to detect if i just can't get on the web and NOT delete stuff.
		return cleanup(getattr(inst, cache))
	
	def __set__(self, name, inst):
		raise Exception("Setting a constant value")
	
	def set(self, name, inst):
		cache = self.fieldName(name)
		initializer = self.initializerName(name)
		try:
			val = self.function(inst)
			setattr(inst, cache, val)
			setattr(inst, initializer, True)
		except:
			session.rollback()
			session.close()
			raise
	

class Required(Attribute):
	""" Signifies an attribute that is expected to be provided by the user.  In other words, its required for the construction of the stock info providing object."""
	
	def register(self, cls, name):
		""" Appends this attribute to the list of required attributes on this class. """
		cls._required_attributes_.append((name,self))
		
	def addField(self, cls, name):
		""" Helper function that adds the field to the passed in class such that the Elixir ORM framework will detect it. """
		fieldName = self.fieldName(name)
		setattr(cls, fieldName, Field(self.fieldType, primary_key=True))
		
	def __get__(self, inst, owner):
		if not inst:
			return None #sqlalchemy likes to call everything :(
		
		cache = self.fieldName(self.name)
		
		if not getattr(inst, cache):
			raise Exception("Attribute %s is required on initialization" % cache)
		return getattr(inst, cache)
	
	def __set__(self, inst, value):
		cache = self.fieldName(self.name)
		
		if getattr(inst, cache):
			raise Exception("Attribute %s is already set." % cache)
		try:
			setattr(inst, cache, value)
		except:
			session.rollback()
			session.close()