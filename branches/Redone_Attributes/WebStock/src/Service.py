""" OBSOLETE. """

from Signature import Signature
from datetime import date

class Service(object):
	def __init__(self, name, signature, configClass=None):
		self.name = name
		self.signature = signature
		self.configClass = configClass
		
	def __hash__(self):
		return hash("".join([self.name,str(self.signature),str(self.configClass)]))
	
	def __eq__(self, other):
		return self.name == other.name and self.signature == other.signature and self.configClass == other.configClass
	
	def __str__(self):
		return ":".join([self.name,str(self.signature),str(self.configClass)])
	
	def __repr__(self):
		return str(self) 
	
	def resolveArguments(self, mapping):
		return mapping.resolveArguments(self.signature.getArguments())
	
	@classmethod
	def Daily(cls, name):
		return cls(name, Signature((unicode,"symbol"),(date,"date")),{"frequency":"daily"})
	
	@classmethod
	def Quarterly(cls, name):
		return cls(name, Signature((unicode,"symbol"),(date,"date")),{"frequency":"quarterly"})
	
	@classmethod
	def Annually(cls, name):
		return cls(name, Signature((unicode,"symbol"),(date,"date")),{"frequency":"annually"})
	
	@classmethod
	def Meta(cls, name):
		return cls(name, Signature((unicode,"symbol")),{"meta":True})