import re
import datetime
import copy


def publicInterface(anObject):
	return [x for x in dir(anObject) if  callable(getattr(anObject,x)) and x[0] != '_']

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
	