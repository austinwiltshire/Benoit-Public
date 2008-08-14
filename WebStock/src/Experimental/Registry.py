from Service import Service
import inspect

class Registry(object):
	""" Provides functions for mapping "Hosts" to "Interfaces".  Hosts are things that say they can provide a certain service
	given a certain contract, while Interfaces are items that need that service and also provide a certain contract/signature.
	Bloomberg does the job of matching up interfaces to hosts """
	
	registeredHosts = {}
	
	@staticmethod
	def getService(service, signatureMap, dbCache=None):
		""" A factory method that returns the __get__ method for a potential descriptor, in this case binding __get__ to a service
		call back to this registry, currently does not support arguments. """
		
		class ServiceDescriptor(object):
			def __init__(self, service):
				self.service = service
				self.signatureMap = signatureMap
			
			def __get__(self, inst, owner):
				if dbCache:
					if not getattr(inst, dbCache):
						serviceFunction = Registry.registeredHosts[self.service]
						#resolve arguments
						setattr(inst, dbCache, serviceFunction(**self.service.resolveArguments(self.signatureMap.bind(inst))))
					return getattr(inst, dbCache)
				else:
					serviceFunction = Registry.registeredHosts[self.service]
					#resolve arguments
					setattr(inst, dbCache, serviceFunction(**self.service.resolveArguments(self.signatureMap.bind(inst))))
					 
			
			def __set__(self, instance, value):
				raise Exception("Setting an immutable value")
			
			def __delete__(self, instance):
				raise Exception("Cannot delete immutable value")
			
		return ServiceDescriptor(service)
	
	@staticmethod
	def hostService(service, callback):
		""" This is used to register a service call with the Registry.  A potential host calls this method to register itself
		as a callback. """
		Registry.registeredHosts[service] = callback
		
class Callback(object):
	pass

class BoundMethod(Callback):
	""" Represents a bound method on a class. """
	def __init__(self, moduleName, className, unboundMethod):
		self.modulename = moduleName
		self.classname = className
		self.unboundMethod = unboundMethod
		self.instance = None
		
	def __call__(self, *args, **kwargs):
		if not self.instance:
			self.classBinding = getattr(__import__(self.modulename[:-3]), self.classname)
			self.instance = self.classBinding()
		return self.unboundMethod(self.instance, *args, **kwargs)

def Register(service):
	
	def decorator(func):
		classname = inspect.stack()[1][3]
		modulename = inspect.stack()[1][1]
		Registry.hostService(service, BoundMethod(modulename, classname, func))
		return func
	return decorator
		
	
