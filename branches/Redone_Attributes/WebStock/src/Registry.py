""" This module is a core component of the generic functions used to drive the bloomberg framework.  It provides a central repository of generic functions saved
by UID. """

from Service import Service
from inspect import ismethod
from elixir import session, Boolean
from os import path
from peak.rules import abstract, when
from Adapt import Adaptable, Adapt
from datetime import date, datetime

_Registry_ = {}

def Add(func):
	""" Add a function to the registry, using it's name as the UID.  This should not be used by users. """
	_Registry_[func.__name__] = func
	
def Get(funcName):
	""" Return a function from the registry, via it's UID. """
#	if funcName not in Registry.keys():
#		print Registry.keys()
	return dashesToNull(_Registry_[funcName])

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
	""" This helper class converts unbound methods into functions, using a cacheing scheme.  Assumes the underlying object is a singleton/flyweight and has no
	important state. """
	
	storedObjects = {}
	
	@classmethod
	def MethodToFunction(cls, method):
		cls.storedObjects[method.im_class] = method.im_class()
		
		def _(*args, **kwargs):
			return method(cls.storedObjects[method.im_class], *args, **kwargs)
		return _

def isboundmethod(func):
	""" Returns true if this method is bound, false otherwise.  Assumes that this is a method being passed in. """
	return isinstance(func.im_self, func.im_class)

def Register(name, func):
	""" Adds a function to the registry given a specific name. This is to be used by users, not add. Wraps the function in a generic wrapper to abstract
	away whether or not the arguments are unicode, strings, dates, datetimes, or Stocks themselves. """
	
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