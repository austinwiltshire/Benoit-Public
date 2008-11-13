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
				print "cache hit on ", key, func.__name__
				val = cache[key]
			else:
				print "cache miss on ", key, func.__name__
				cache[key] = val = func(*args, **kwargs)
			return val
		return _
	
class cached_method(object):
	def __init__(self, size):
		print "init cache"
		self.size = size
	
	def __call__(self, func):
		print "calling cache"
		cache = LRUCache(self.size)
		def _(*args, **kwargs):
			print "calling cache"
			key = "".join(str(x) for x in itertools.chain(args[1:], kwargs.iteritems()))
			if key in cache:
				print "cache hit on ", key, func.__name__
				val = cache[key]
			else:
				print "cache miss on ", key, func.__name__
				cache[key] = val = func(*args, **kwargs)
			return val
		return _