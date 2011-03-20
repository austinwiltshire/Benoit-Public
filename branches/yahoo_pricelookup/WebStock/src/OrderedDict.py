""" A dumb ordered dict. """

class OrderedDict(object):
	def __init__(self, *args):
		
		self._keys = []
		self._values = []
		self._map = {}
		
		for key,value in args:
			self._keys.append(key)
			self._values.append(value)
			self._map[key] = value
			
	def __getitem__(self, key):
		return self._map[key]
	
#	def __setitem__(self, key, value):
#	implement this later... or just loko up a real ordered dict
#		self._map[key] = value
#		self.keys.append

	def keys(self):
		for key in self._keys:
			yield key
	
	def values(self):
		for value in self._values:
			yield value
			
	def items(self):
		for key,value in zip(self._keys,self._values):
			yield (key,value)
	
	