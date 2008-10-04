from Service import Service
import inspect
from elixir import session
from os import path

class Registry(object):
	""" Provides functions for mapping "Hosts" to "Interfaces".  Hosts are things that say they can provide a certain service
	given a certain contract, while Interfaces are items that need that service and also provide a certain contract/signature.
	Bloomberg does the job of matching up interfaces to hosts """
	
	registeredHosts = {}
	
	@staticmethod
	def getService(service, signatureMap, cacheName):
		""" A factory method that returns the __get__ method for a potential descriptor, in this case binding __get__ to a service
		call back to this registry, currently does not support arguments. """
		
		#TODO: it'd be nice if i could seperate this database memoization from the 
		# call to the service function.
		class ServiceDescriptor(object):	
			def __get__(self, inst, owner):
				if not getattr(inst, cacheName):
						serviceFunction = Registry.registeredHosts[service]
						#resolve arguments
						setattr(inst, cacheName, serviceFunction(**service.resolveArguments(signatureMap.bind(inst))))
						session.commit()
				return getattr(inst, cacheName)
			
			def __set__(self, instance, value):
				raise Exception("Setting an immutable value")
			
			def __delete__(self, instance):
				raise Exception("Cannot delete immutable value")
		
		return ServiceDescriptor()
	
	@staticmethod
	def hostService(service, callback):
		""" This is used to register a service call with the Registry.  A potential host calls this method to register itself
		as a callback. """
		#if service in  Registry.registeredHosts:
		#	raise Exception("Registering two functions on one service.")
		#TODO: inside website.google is an ugly little thing inside SECData or _addAttribute or something.  it re-registers methods
		#EACH TIME the thing is instantiated.  this should work for now, but i need to basically relook at yahoo and google given
		#this new framework for 'google' and 'bloomberg' and what not.
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
			self.classBinding = getattr(__import__(self.modulename), self.classname)
			self.instance = self.classBinding()
		return self.unboundMethod(self.instance, *args, **kwargs)
	
	def __repr__(self):
		return str(self)
	
	def __str__(self):
		return "<Bound Method %s on class %s in module %s with instance %s>" % (self.unboundMethod, self.classname, self.modulename, self.instance)

def Register(service, moduleName, className):
	def decorator(func):
#		callerFrame = GetCallerFrame()
#		classname = GetClassName(callerFrame)
#		modulename = GetModuleName(callerFrame) 
		Registry.hostService(service, BoundMethod(moduleName, className, func))
		return func
	return decorator
		
#def GetModuleName(stackFrame):
#	qualifiedName = stackFrame[1]
#	moduleName = path.basename(qualifiedName)
#	return moduleName.strip(".py")

#def GetClassName(stackFrame):
#	return stackFrame[3]

#def GetCallerFrame():
#	return inspect.stack()[2]