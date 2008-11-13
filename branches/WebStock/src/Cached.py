from LRUCache import LRUCache
import itertools

class cached(object):
	def __init__(self, size):
		print "init cache"
		self.size = size
	
	def __call__(self, func):
		print "calling cache"
		cache = LRUCache(self.size)
		def _(*args, **kwargs):
			print "calling cache"
			key = "".join(str(x) for x in itertools.chain(args, kwargs.iteritems()))
			if key in cache:
				val = cache[key]
			else:
				cache[key] = val = func(*args, **kwargs)
			return val
		return _