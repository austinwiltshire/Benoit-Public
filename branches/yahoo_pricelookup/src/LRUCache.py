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
			for i in [None] * len(self.queue):
				k = self.queue.popleft()
				if self.refcount[k] == 1:
					self.queue.append(k)
				else:
					self.refcount[k] -= 1
			#TODO: this would be good to log.  i dont know why it's getting out of sync but there's an easy way to fix it!
			#TODO: switch to an exception handling format and also log the error in addition to fixing it.
			#TODO: consider a global 'exception policy', with values like "bailout", "recover" and "ignore"
			if not len(self.queue) == len(self.cache) == len(self.refcount) == sum(self.refcount.itervalues()):
				print len(self.queue), len(self.cache), len(self.refcount), sum(self.refcount.itervalues())
				self.cache = {}
				self.queue = deque()
				self.refcount = {}
				self._update_(key) #attempt to re-add the key
				
	def __getitem__(self, key):
		self._update_(key)
		return self.cache[key]
		
	def __setitem__(self, key, value):
		self.cache[key] = value
		self._update_(key)
		
	def __contains__(self, key):
		return key in self.cache
