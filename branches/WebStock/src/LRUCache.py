from collections import deque

class LRUCache(object):
	def __init__(self, maxsize):
		self.maxsize = maxsize
		self.cache = {}
		self.queue = deque()
		self.refcount = {}
		
	def _update_(self, key):
		self.queue.append(key)
		self.refcount[key] = self.refcount.get(key,0) + 1
		
		while len(self.cache) > self.maxsize:
			k = self.queue.popleft()
			self.refcount[k] -= 1
			if not self.refcount[k]:
				del self.cache[k]
				del self.refcount[k]
				
		if len(self.queue) > self.maxsize * 4:
			for i in [None] * _len(queue):
				k = queue_popleft()
				if self.refcount[k] == 1:
					self.queue.append(k)
				else:
					self.refcount[k] -= 1
			assert len(self.queue) == len(self.cache) == len(self.refcount) == sum(refcount.itervalues()) 
				
	def __getitem__(self, key):
		self._update_(key)
		return self.cache[key]
		
	def __setitem__(self, key, value):
		self._update_(key)
		self.cache[key] = value
		
	def __contains__(self, key):
		return key in self.cache
