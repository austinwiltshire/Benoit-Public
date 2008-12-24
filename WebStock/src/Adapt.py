from datetime import date, datetime
from peak.rules import abstract, when

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