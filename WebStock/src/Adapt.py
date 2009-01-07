""" Adapt provides two generic functions, adaptable and adapt.  Adaptable takes two arguments, the left hand side is an object and the right hand side is a type.
The function returns true if there exists a function Adapt that defines how to convert the left hand side object into the type of the right hand side.  Adapt, as a 
generic function, actually does the logic needed to turn the left hand side into an instance of the right hand side.  After importing this module, users can add 
new interfaces to adapt and adaptable, as well as expect to be able to use any interfaces other modules have added. 

Implementation Notes:

Adaptable could be reimplemented as a function to be called with two types, and that function automatically registers 'adaptable' as true.  The rest are false.
"""

from datetime import date, datetime
from peak.rules import abstract, when

def Adaptable_Match(objtype,typetype):
	""" This is a helper function that covers many types of adaptation.  It follows a templating pattern where the wrapper function takes in types, and specializes
	the inner function which is returned. """
	def _(objinst, typeinst):
		return isinstance(objinst,objtype) and (typeinst is typetype or issubclass(typeinst, typetype))
	return _

def Strict_Match(objtype,typetype):
	""" Similar to Adaptable_Match, this is a helper function that covers many types of adaptation and available for use in generic dispatch mechanisms.  As opposed
	to Adaptable_Match, strict match only allows instances of the types themselves passed in, rather than any subclassing or other methods.  This is used generally
	in cases of converting an instance of a class to an instance of a superclass, where such conversions are not already handled. """
	def _(objinst, typeinst):
		return type(objinst) is objtype and (typeinst is typetype)
	return _

@abstract()
def Adapt(lhs, rhs):
	""" Converts the lhs to the rhs and returns it """
	
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

@when(Adaptable, "Strict_Match(date,datetime)(lhs,rhs)")
def Adaptable(lhs, rhs):
	return True