""" This module implements a decorator that can cache functions. """

from LRUCache import LRUCache
import itertools

class cached(object):
	""" This decorator uses a Least-Recently-Used scheme for cacheing, with the size set at set up time. """
	
	def __init__(self, size=1):
		""" Size is set at initialization time. """
		self.size = size
	
	def __call__(self, func):
		""" This function is able to cache based on positional and keyword arguments, assuming all arguments can be stringified to be unique. """
		
		cache = LRUCache(self.size)
		def _(*args, **kwargs):
			key = "".join(str(x) for x in itertools.chain(args, kwargs.iteritems()))
			if key in cache:
				val = cache[key]
			else:
				cache[key] = val = func(*args, **kwargs)
			return val
		return _