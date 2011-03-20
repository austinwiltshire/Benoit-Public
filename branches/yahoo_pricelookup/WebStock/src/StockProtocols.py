""" OBSOLETE.  Pulled apart into Registry, Adapt """

from peak.rules import abstract, when, after
from datetime import datetime, date
from FinancialDate import toDate

class _Registry(object):
	def add(self, func):
		setattr(self,func.__name__,func)
		
	def get(self, func_name):
		return getattr(self,func_name)
	
Registry = _Registry()

def Adaptable_Match(objtype,typetype):
	def _(objinst, typeinst):
		return isinstance(objinst,objtype) and (typeinst is typetype or issubclass(typeinst, typetype))
	return _

def Strict_Match(objtype,typetype):
	def _(objinst, typeinst):
		return type(objinst) is objtype and (typeinst is typetype)
	return _

@abstract()
def Adapt(lhs, rhs):
	""" Converts the lhs to the rhs and returns it """
	
#base case
@when(Adapt, "type(lhs) is rhs")
def Adapt(lhs, rhs):
	return lhs

def Adaptable(lhs, rhs):
	return False

@when(Adapt, "Adaptable_Match(str,unicode)(lhs,rhs)")
def Adapt(lhs, rhs):
	return rhs(lhs)

@when(Adapt, "Adaptable_Match(unicode,str)(lhs,rhs)")
def Adapt(lhs, rhs):
	return rhs(lhs)

@when(Adapt, "Strict_Match(date,datetime)(lhs,rhs)")
def Adapt(lhs, rhs):
	return rhs(lhs.year, lhs.month, lhs.day)

@when(Adapt, "Strict_Match(datetime,date)(lhs,rhs)")
def Adapt(lhs, rhs):
	return rhs(lhs.year, lhs.month, lhs.day)

@when(Adaptable, "isinstance(lhs,rhs)")
def Adaptable(lhs, rhs):
	return True	

@when(Adaptable, "Adaptable_Match(str,unicode)(lhs,rhs)")
def Adaptable(lhs, rhs):
	return True

@when(Adaptable, "Adaptable_Match(unicode,str)(lhs,rhs)")
def Adaptable(lhs, rhs):
	return True

#datetime subclasses date, so if we pass in a datetime we should trigger the default case which is isinstance
@when(Adaptable, "Strict_Match(date,datetime)(lhs,rhs)")
def Adaptable(lhs, rhs):
	return True

def resolver(func):
	
	@abstract()
	def work(*args, **kwargs):
		pass
	
	work.__name__ = func.__name__
	work.__doc__ = func.__doc__
	
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
	
	Registry.add(work)
	return work
#	
#	@when(work, "len(args) == 1 and len(kwargs) == 1 and 'date' in kwargs and isinstance(kwargs['date'],date) and isinstance(args[0],unicode)")
#	def work(*args, **kwargs):
#		symbol = args[0]
#		date = kwargs['date']
#		return func(symbol, date)
	
	
	