import re

def publicInterface(anObject):
	return [x for x in dir(anObject) if  callable(getattr(anObject,x)) and x[0] != '_']

def isString(aPossibleString):
	return isinstance(aPossibleString, str) or isinstance(aPossibleString, unicode)

def isRegex(aPossibleRegex):
	return isinstance(aPossibleRegex, type(re.compile("")))