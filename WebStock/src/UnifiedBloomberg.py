"""

A bloomberg that unifies any number of other bloombergs behind a single interface.

>>> ub = UnifiedBloomberg(Yahoo.Yahoo,Website.Google)
>>> ub.getHigh("IRBT", datetime.date(2007,4,2)) == 13.37
True

>>> round(ub.getQuarterlyGoodwill("IBM", date(2007,9,30)))
13843.0

Can take in either instantiations of other bloombergs or classes, or a combination thereof.

>>> isinstance(UnifiedBloomberg(Yahoo.Yahoo(), Website.Google()), UnifiedBloomberg)
True

>>> isinstance(UnifiedBloomberg(Website.Google, Yahoo.Yahoo()), UnifiedBloomberg)
True

>>> isinstance(UnifiedBloomberg(Website.Google(), Yahoo.Yahoo), UnifiedBloomberg)
True

Will raise an error if you try and add two bloombergs with the same methods.
	
>>> ub = UnifiedBloomberg(Yahoo.Yahoo,Yahoo.Yahoo)
Traceback (most recent call last):
	...
DuplicateMethod "getHigh", bailing out.

Also can simply be a wrapper around a single Bloomberg

>>> ub = UnifiedBloomberg(Yahoo.Yahoo)
>>> ub.getHigh("IRBT", datetime.date(2007,4,2)) == 13.37
True

"""

import datetime
import Website
from utilities import publicInterface 

class DuplicateMethod(Exception):
	""" Raised when a symbol is not found or information for it cannot be found "
	
	inv:
		#typechecking
		self.symbol != None
		isinstance(self.method,basestring)
	"""
	def __init__(self, method, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isinstance(symbol,basestring)
		"""
		
		self.method = method
		super(DuplicateMethod,self).__init__(*args, **kwargs)
		
	def __str__(self):
		toReturn = "Duplicated Method: \"%s\", bailing out." % self.method
		if hasattr(self,"message"):
			toReturn = "\n".join([toReturn, self.message])
		return toReturn

class UnifiedBloomberg(Website.Bloomberg):
	""" Unifies the interface to a variable number of other bloombergs 
	
	>>> ub = UnifiedBloomberg(Yahoo.Yahoo(),Google.Google)
	>>> ub.getClose("IRBT", datetime.date(2007,5,2)) == 12.00
	True
	
	>>> ub.getAnnualDefferedTaxes("S", datetime.date(2007,12,31)) == 1000.00
	True
	
	Can take either already instantiated bloombergs or bloomberg classes
	
	>>> ub = UnifiedBloomberg(Yahoo.Yahoo, Google.Google())
	>>> ub.getAdjustedClose("DD", datetime.date(2005,1,20)) == 12.00
	True
	
	Will raise an error if you try and add two bloombergs with the same methods.
	
	>>> ub = UnifiedBloomberg(Yahoo.Yahoo,Yahoo.Yahoo)
	Traceback (most recent call last):
		...
	Duplicated Method: "getHigh", bailing out.
	
	inv:
		isinstance(self._delegates, dict)
		all(isinstance(val, key) for key,val in self._delegates.items())
	
	"""
	
	def __init__(self, *args):
		""" Expect to get an array of bloombergs to unify 
		
		pre:
			all(isinstance(x, Bloomberg) or (isinstance(x, type) and isinstance(x(), Bloomberg)) for x in args)
		post[args]:
			isinstance(self._delegates, dict)
			all(x in self._delegates for x in args)
			
		"""
		self._delegates = {}
		
		for bloomberg in args:
			self._delegate(bloomberg)
			
	def _delegate(self, bloomberg):
		""" Takes a bloomberg and sets a dict entry to it, as well as setting up all method calls such that they will forward on 
		to an instantiation of this bloomberg 
		
		pre:
			isinstance(bloomberg, Bloomberg) or (isinstance(bloomberg, type) and isinstance(bloomberg(), Bloomberg))
			bloomberg not in self._delegates.keys()
		post[]:
			all(hasattr(self, method) for method in publicInterface(bloomberg))
			all(callable(getattr(self,method)) for method in publicInterfacE(bloomberg))
			bloomberg in self._delegates.keys()
			isinstance(self._delegates[bloomberg], bloomberg)
		"""
		
		if isinstance(bloomberg, type): #if it's a type, we need to instantiate it
			self._delegateClass(bloomberg)
		else:
			self._delegatePrototype(bloomberg) #if its already instantiated(if it took non default args it needs to be)
		
		for method in publicInterface(bloomberg):
			self._assign(method, bloomberg)
	
	def _delegateClass(self, bloomberg):
		""" Delegates to a bloomberg class, that is, a type of bloomberg that is not instantiated yet. 
		
		pre:
			isinstance(bloomberg, type) and isinstance(bloomberg(), Bloomberg)
			bloomberg not in self._delegates.keys()
			bloomberg() not in self._delegates.values()
			all(not isinstance(x, bloomberg) for x in self._delegates.values())
		post[]:
			bloomberg in self._delegates.keys()
			bloomberg in self._delegates.values()
		"""
		self._delegates[bloomberg] = bloomberg() #assumes default constructable
	
	
	#TODO: do a run time check to make sure that i'm not adding an instantiated version of a class or visa versa - i need to have a test 
	#for this and checking for post/pre condition violations is not a good idea.
	
	def _delegatePrototype(self, bloomberg):
		""" Sets the delegate dictionary for an already instantiated bloomberg 
		
		pre:
			isinstance(bloomberg, Bloomberg)
			type(bloomberg) not in self._delegates.keys()
			bloomberg not in self._delegates.keys()
			bloomberg not in self._delegates.values()
		post[]:
			bloomberg in self._delegates.keys()
			bloomberg in self._delegates.values()
		"""
		self._delegates[bloomberg] = bloomberg #assumes already constructed
	
	def _assign(self, method, bloomberg):
		""" Sets a given method to a delegated function call - will forward this method on to the given bloomberg 
		
		pre:
			isinstance(bloomberg, Bloomberg) or isinstance(bloomberg(), Bloomberg)
			hasattr(bloomberg,method)
			callable(getattr(bloomberg,method))
			not hasattr(self, method)
		post[]:
			hasattr(self,method)
			callable(getattr(self,method))
		"""
		if hasattr(self, method):
			raise DuplicateMethod(method)
		
		setattr(self, method, self._delegateCallWrapper(method, bloomberg))
		
	def _delegateCallWrapper(self, method, bloomberg):
		""" Helper function that returns a bound function such that all method calls are seemlessly forwarded to an instantiation
		of the given bloomberg 
		
		pre:
			callable(getattr(bloomberg,method))
			isinstance(bloomberg, Bloomberg) or isinstance(bloomberg(), Bloomberg)
		post:
			callable(__return__)
		"""
		def _(*args, **kwargs):
			return getattr(self._delegates[bloomberg], method)(*args,**kwargs)
		return _								