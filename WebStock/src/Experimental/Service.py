from Signature import Signature

class Service(object):
	def __init__(self, name, signature):
		self.name = name
		self.signature = signature
		
	def __hash__(self):
		return (hash(self.name) * 2) + (hash(self.signature) * 3)
	
	def __eq__(self, other):
		return self.name == other.name and self.signature == other.signature
	
	def __cmp__(self, other):
		return hash(self) < hash(other) 
	
	def __str__(self):
		return ":".join([self.name,str(self.signature)])
	
	def __repr__(self):
		return str(self) 
	
	def resolveArguments(self, mapping):
		return mapping.resolveArguments(self.signature.getArguments())
		
		