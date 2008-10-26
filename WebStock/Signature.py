#TODO: document how this works

import itertools

class Signature(object):
	class Argument(object):
		def __init__(self, argType, keyword):
			self.argType = argType
			self.keyword = keyword
			
		def __hash__(self):
			return hash("".join([str(self.keyword),str(self.argType)]))
								
		def __eq__(self, other):
			return self.keyword == other.keyword and self.argType == other.argType
		
		def __cmp__(self, other):
			return hash(self) < hash(other)
		
		def __str__(self):
			return " ".join([str(self.keyword),str(self.argType)])
		
		def __repr__(self):
			return str(self)
		
	def __init__(self, *arguments):
		self.arguments = [] 
		
		for (keyword,argType) in arguments:
			self.arguments.append(Signature.Argument(keyword,argType))
		
	def __hash__(self):
		return hash("".join([str(x) for x in self.arguments]))
	
	def __eq__(self, other):
		return all(x==y for (x,y) in zip(self.arguments,other.arguments))
	
	def __cmp__(self, other):
		return hash(self) < hash(other)
	
	def __str__(self):
		return ",".join(["".join(["(",str(argument),")"]) for argument in self.arguments])
	
	def __repr__(self):
		return str(self)
	
	def getArguments(self):
		return self.arguments
	
class SignatureMap(object):
	def __init__(self, map):
		self.map = map
		
	def bind(self, bindingInstance):
		return BoundSignatureMap(self.map, bindingInstance)

					
class BoundSignatureMap(object):
	def __init__(self, map, bindingInstance):
		self.map = map
		self.bindingInstance = bindingInstance
		
	def resolveArguments(self, arguments):
		kwargs = {}
		for argument in arguments:
			kwargs[argument.keyword] = getattr(self.bindingInstance, self.map[argument.keyword])
		return kwargs