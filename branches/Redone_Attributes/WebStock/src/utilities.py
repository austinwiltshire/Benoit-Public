""" Various utilities and helper functions. """

import re
import datetime
import copy
import inspect
from itertools import chain, ifilter

def getNestedAttr(obj, path):
	
	if "." in path:
		return getNestedAttr(getattr(obj,head(path.split(".",1))), head(tail(path.split(".",1))))
	else:
		return getattr(obj,path)
	

def findFirst(seq,pred):
	try:
		return ifilter(pred, seq).next()
	except StopIteration, e:
		return None
	
def findLast(seq,pred):
	return findFirst(reversed(seq),pred)

def iterModule(module):
	for obj in dir(module):
		yield obj,getattr(module,obj)

def head(lst):
	return lst[0]

def tail(lst):
	return lst[1:]

#TODO: investigate itertools for something like this.
def getBy(iterable, n=1):
	""" Turns an iteratble of N into an iterable of N / X, where the new iterable returns every X'th element in N """
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

#TODO: obsolete.  Gross.  I'm glad I don't do this any more.
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

#TODO: replace with ADAPT
def isString(aPossibleString):
	""" Literate Programming aid to check whether or not the argument is a string. """
	return isinstance(aPossibleString, basestring) 

#TODO: any time this is used probably means my typeing is weak anyway and it should be removed.
def isRegex(aPossibleRegex):
	""" Literate programming aid ot check whether or not the argument is a regex. """
	return isinstance(aPossibleRegex, type(re.compile("")))

#TODO: is this used?
def dateFromString(stringifiedDate):
	""" Assumes a YEAR-MO-DA layout.  """
	#TODO: bound to already be in the standard library.  dont want to find it right now
	#TODO: look into pipes.  would make more since to just take3 things, turn them into ints
	#then you have your year month day unpacking
	return datetime.datetime.strptime(stringifiedDate,"%Y-%m-%d").date()

#TODO: Obsolete.  use cached.py
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
	""" Decorator for lazy initialization of attributes on classes. """
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
	""" Predicate returns whether the function is a class method of cls, as opposed to a staticmethod or function or unbound method or normal method. """
	if not func:
		#syntax here is to just assume they passed us the method itself
		return inspect.ismethod(cls) and cls.im_class is type
	elif func and isString(func):
		#passed in a string function to check against cls
		return hasattr(cls, func) and inspect.ismethod(getattr(cls,func)) and issubclass(getattr(cls,func).im_class, type)

#TODO: gross.  Obsolete.
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
	