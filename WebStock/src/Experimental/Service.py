from Signature import Signature

class Service(object):
	def __init__(self, name, signature, config=None):
		self.name = name
		self.signature = signature
		self.config = config
		
	def __hash__(self):
		return hash("".join([self.name,str(self.signature),str(self.config)]))
	
	def __eq__(self, other):
		return self.name == other.name and self.signature == other.signature and self.config == other.config
	
	def __cmp__(self, other):
		#this seems evil
		print "Do I ever get called?"
		return hash(self) < hash(other) 
	
	def __str__(self):
		return ":".join([self.name,str(self.signature),str(self.config)])
	
	def __repr__(self):
		return str(self) 
	
	def resolveArguments(self, mapping):
		return mapping.resolveArguments(self.signature.getArguments())