import re
import datetime
import copy
import inspect
from itertools import chain

def getBy(iterable, n=1):
	iterable = iter(iterable)
	for x in iterable:
		args = [x]
		for addition in xrange(n-1):
			args.append(iterable.next())
		yield tuple(args)
		

def publicInterface(anObject):
	""" Returns all functions on this objects public interface that are not appended with a _.
	
	>>> class x:
	...		def public(self):
	...			pass
	...		class innerClass:
	...			pass
	...		def _private(self):
	...			pass
	...		def __impl__(self):
	...			pass
	...
	>>> publicInterface(x)
	['public'] 

	"""
	
	
	return [x for x in dir(anObject) if  callable(getattr(anObject,x)) and x[0] != '_' and not isinstance(getattr(anObject,x),type)]

def delegateInterface(cls, interface, wrapper):
	""" Helper private function that implements my own little delegated interface idiom.
	Pushes the interface's methods on to this object, and sets all of the calls equal to 
	'wrapper' which gets passed in the method name and arguments.
	
	pre:
		#typechecking
		isinstance(dir(interface), list)
		all(isinstance(x, str) for x in dir(interface))
		callable(wrapper)
		
		#make sure i don't already have the attribute
		all(not hasattr(cls,x) for x in publicInterface(interface))
		
	post[self]:
		#ensure that i've added the attributes
		all(hasattr(cls,x) for x in publicInterface(interface))
		all(callable(getattr(cls,x)) for x in publicInterface(interface))
		
		#has documentation string
		all(hasattr(getattr(cls,x),'__doc__') for x in publicInterface(interface))
	
	"""
	
	def functionWrapper(func, methodName):
		""" I can't use a lambda for this because lambda's don't bind to their arguments until they
		are called.  Meaning if i call lambda x: y(x), it call's whatever y is THEN, and if y has
		changed via a reference or something, then the lambda has completely changed! 
	
		pre:
			isinstance(methodName, str) or isinstance(methodName, unicode)
			callable(func)
		
		post[]:
			callable(__return__)
	
		"""
		def _(self, *args, **kwargs):
			return func(self, methodName, *args, **kwargs)
		return _
	
   	for method in publicInterface(interface):
   		funcToSet = functionWrapper(wrapper,method)
   		funcToSet.__doc__ = " This method is delegated to %s, check documentation there. " % interface
   	   	setattr(cls,method, funcToSet)

def isString(aPossibleString):
	return isinstance(aPossibleString, basestring) 

def isRegex(aPossibleRegex):
	return isinstance(aPossibleRegex, type(re.compile("")))

def dateFromString(stringifiedDate):
	""" Assumes a YEAR-MO-DA layout.  """
	#TODO: bound to already be in the standard library.  dont want to find it right now
	#TODO: look into pipes.  would make more since to just take3 things, turn them into ints
	#then you have your year month day unpacking
	return datetime.datetime.strptime(stringifiedDate,"%Y-%m-%d").date()

class Cache(dict):
	def __init__(self, method):
		super(Cache,self).__init__(self)
		self._missingmethod = method
	
	def __missing__(self, key):
		self[key] = self._missingmethod(key)
		return self[key]
	
def checkCache(new, old, key):
	""" Used as a convienience function for contracts.  Ensures that cache's grow when they should and don't when they shouldnt. """
	return (len(new.keys()) - len(old.keys()) == 1) if (key not in old.keys()) else (len(new.keys()) - len(old.keys()) == 0)

class Lazy(object):
	def __init__(self, func):
		self._func = func
		self.__name__ = func.__name__
		self.__doc__ = func.__doc__
		
	def __get__(self, inst, cls=None):
		if inst is None:
			return None
		result = inst.__dict__[self.__name__] = self._func(inst)
		return result
	
def isClassMethod(cls, func=None):
	if not func:
		#syntax here is to just assume they passed us the method itself
		return inspect.ismethod(cls) and cls.im_class is type
	elif func and isString(func):
		#passed in a string function to check against cls
		return hasattr(cls, func) and inspect.ismethod(getattr(cls,func)) and issubclass(getattr(cls,func).im_class, type)
	
class ClassAccess(object):
	""" This is a pretty nasty hack to wrap a class, allowing access to it's class methods only, closed over any args you pass in in it's init """
	def __init__(self, cls, *args, **kwargs):
		self.cls = cls
		self.args = args
		self.kwargs = kwargs
		
	def __getattr__(self, name):
		if isClassMethod(self.cls, name):
			return lambda *args, **kwargs : getattr(self.cls, name)(*(self.args + args), **dict((key, value) for key,value in chain(self.kwargs.iteritems(), kwargs.iteritems())))
		else:
			raise AttributeError, name

#def const(function):
#	def constantFunc(*args, **kwargs):
#		selfdict = copy.deepcopy(args[0].__dict__)
#		toReturn = function(*args, **kwargs)
#		assert args[0].__dict__ == selfdict, "Violated const-ness"
#		return toReturn
#	constantFunc.__doc__ = function.__doc__ + "\n\t\t\t pre:\n\t\t\t\t 1 == 0\n"
#	return constantFunc

#class a(object):
#	def __init__(self):
#		self.val = 0
#		
#	@const
#	def aconstfunc(self, x):
#		""" a constant function
#		pre:
#			1 == 1
#		pre:
#			1 == 1
#		"""
#		self.val = x 
	