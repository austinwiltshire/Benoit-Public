from Service import Service
from inspect import ismethod
from elixir import session, Boolean
from os import path
from peak.rules import abstract, when
from Adapt import Adaptable, Adapt
from datetime import date, datetime

Registry = {}

def Add(func):
	Registry[func.__name__] = func
	
def Get(funcName):
	if funcName not in Registry.keys():
		print Registry.keys()
	return dashesToNull(Registry[funcName])

def dashesToNull(func):
	""" Takes invalid results and turns them into valid ones.  Including dashes for character input from raw web data, or exceptions from attempting to add or
	subtract from bad data in a compound ratio or something. """
	
	def _(*args, **kwargs):
		try:
			result = func(*args, **kwargs)
			if result=='-':
				return None
			else:
				return result
		except TypeError, e:
			#this happened because None was attempted to be minused from.  i.e., if there is invalid input, like information doesnt exist from the web, we get
			#none back.  actually, we get a '-' back, so we return none in this function.  however, if this is wrapping a compound function that aattempts to 
			#put together multiple things from the web, one of them might be none, and then we get a type error.  hopefully.
			if "unsupported operand type(s) for " in e.message:
				return None
			else:
				#this means the type error was not due to a None problem.
				raise
	return _

class FunctionHelper(object):
	
	storedObjects = {}
	
	@classmethod
	def MethodToFunction(cls, method):
		cls.storedObjects[method.im_class] = method.im_class()
		
		def _(*args, **kwargs):
#			print "calling", method, "on", method.im_class()
			return method(cls.storedObjects[method.im_class], *args, **kwargs)
		return _

#class Registry(object):
#	""" Provides functions for mapping "Hosts" to "Interfaces".  Hosts are things that say they can provide a certain service
#	given a certain contract, while Interfaces are items that need that service and also provide a certain contract/signature.
#	Bloomberg does the job of matching up interfaces to hosts """
#	
#	registeredHosts = {}
#	
#	@staticmethod
#	def getServiceFunction(service):
#		print dir(service)
#		return Registry.registeredHosts[service]
#	
#	@staticmethod
#	def getService(service, signatureMap):
#		def _(self, *args, **kwargs):
#			print dir(service)
#			return Registry.registeredHosts[service](**service.resolveArguments(signatureMap.bind(self)))
#		return _
#		
#	#TODO: it'd be nice if i could seperate this database memoization from the 
#	# call to the service function.
##
#	
#	@staticmethod
#	def hostService(service, callback):
#		""" This is used to register a service call with the Registry.  A potential host calls this method to register itself
#		as a callback. """
#		#if service in  Registry.registeredHosts:
#		#	raise Exception("Registering two functions on one service.")
#		#TODO: inside website.google is an ugly little thing inside SECData or _addAttribute or something.  it re-registers methods
#		#EACH TIME the thing is instantiated.  this should work for now, but i need to basically relook at yahoo and google given
#		#this new framework for 'google' and 'bloomberg' and what not.
#		#added dashes to null wrapper to turn dashes found by the webframework into None.
#		Registry.registeredHosts[service] = dashesToNull(callback)
		
#class Callback(object):
#	pass
#
#class BoundMethod(Callback):
#	""" Represents a bound method on a class. """
#	def __init__(self, moduleName, className, unboundMethod):
#		self.modulename = moduleName
#		self.classname = className
#		self.unboundMethod = unboundMethod
#		self.instance = None
#		
#	def __call__(self, *args, **kwargs):
#		if not self.instance:
#			self.classBinding = getattr(__import__(self.modulename), self.classname)
#			self.instance = self.classBinding()
#		return self.unboundMethod(self.instance, *args, **kwargs)
#	
#	def __repr__(self):
#		return str(self)
#	
#	def __str__(self):
#		return "<Bound Method %s on class %s in module %s with instance %s>" % (self.unboundMethod, self.classname, self.modulename, self.instance)

#def Register(service, moduleName, className):
#	def decorator(func):
#		callerFrame = GetCallerFrame()
#		classname = GetClassName(callerFrame)
#		modulename = GetModuleName(callerFrame) 
#		Registry.hostService(service, BoundMethod(moduleName, className, func))
#		return func
#	return decorator

def isboundmethod(func):
	""" Returns true if this method is bound, false otherwise.  Assumes that this is a method being passed in. """
	return isinstance(func.im_self, func.im_class)

#def Register(service):
#	def decorator(func):
#		
#		if ismethod(func):
#			if not isboundmethod(func):
#				cleanFunc = FunctionHelper.MethodToFunction(func)
#		else:
#			cleanFunc = func
#			
#		Registry.hostService(service, cleanFunc)
#		
#		return func
#	return decorator


def Register(name, func):
	
	#print "registering", (func.__name__ if not manualName else manualName)
	@abstract()
	def work(*args, **kwargs):
		pass
	
	work.__name__ = name
	work.__doc__ = func.__doc__
	
	if ismethod(func):
		if not isboundmethod(func):
			func = FunctionHelper.MethodToFunction(func)
	
	#symbol case
	@when(work, "len(args) == 1 and len(kwargs) == 0 and Adaptable(args[0],unicode)")
	def work(*args, **kwargs):
		symbol = Adapt(args[0],unicode)
		return func(symbol)
		
	@when(work, "len(args) == 1 and len(kwargs) == 0 and hasattr(args[0],'Symbol')")
	def work(*args, **kwargs):
		stock = args[0]
		return func(stock.Symbol)

	
	@when(work, "len(args) == 1 and len(kwargs) == 0 and hasattr(args[0],'Symbol') and hasattr(args[0],'Date')")
	def work(*args, **kwargs):
		stock = args[0]
		return func(stock.Symbol, stock.Date)
	
	@when(work, "len(args) == 2 and len(kwargs) == 0 and Adaptable(args[0],unicode) and Adaptable(args[1],date)")
	def work(*args, **kwargs):
		symbol = Adapt(args[0],unicode)
		_date = Adapt(args[1],date)
		return func(symbol, _date)
	
	@when(work, "len(args) == 0 and len(kwargs) == 1 and 'stock' in kwargs and hasattr(kwargs['stock'],'Symbol')")
	def work(*args, **kwargs):
		symbol = kwargs['stock'].Symbol
		return func(symbol)
	
	@when(work, "len(args) == 0 and len(kwargs) == 1 and 'stock' in kwargs and hasattr(kwargs['stock'],'Symbol') and hasattr(kwargs['stock'],'Date')")
	def work(*args, **kwargs):
		symbol = kwargs['stock'].Symbol
		date = kwargs['stock'].Date
		return func(symbol, date)
	
	@when(work, "len(args) == 0 and len(kwargs) == 1 and 'symbol' in kwargs and Adaptable(kwargs['symbol'],unicode)")
	def work(*args, **kwargs):
		symbol = Adapt(kwargs['symbol'],unicode)
		return func(symbol)

	@when(work, "len(args) == 0 and len(kwargs) == 2 and 'symbol' in kwargs and 'date' in kwargs and Adaptable(kwargs['symbol'],unicode) and Adaptable(kwargs['date'],date)")
	def work(*args, **kwargs):
		symbol = Adapt(kwargs['symbol'],unicode)
		_date = Adapt(kwargs['date'],date)
		return func(symbol, _date)
	
	@when(work, "len(args) == 1 and len(kwargs) == 1 and 'symbol' in kwargs and Adaptable(kwargs['symbol'],unicode) and Adaptable(args[0],date)")
	def work(*args, **kwargs):
		symbol = Adapt(kwargs['symbol'],unicode)
		_date = Adapt(args[0],date)
		return func(symbol, _date)
	
	@when(work, "len(args) == 1 and len(kwargs) == 1 and 'date' in kwargs and Adaptable(kwargs['date'],date) and Adaptable(args[0],unicode)")
	def work(*args, **kwargs):
		symbol = Adapt(args[0],unicode)
		_date = Adapt(kwargs['date'],date)
		return func(symbol, _date)
	
	Add(work)
	return work

#def GetModuleName(stackFrame):
#	qualifiedName = stackFrame[1]
#	moduleName = path.basename(qualifiedName)
#	return moduleName.strip(".py")

#def GetClassName(stackFrame):
#	return stackFrame[3]

#def GetCallerFrame():
#	return inspect.stack()[2]