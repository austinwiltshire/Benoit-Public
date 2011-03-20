""" Defines a Flyweight base class that will allow anyone who inherits from it to be a flyweight based on it's constructor arguments.  This requires that the
user have no state independent of the constructor arguments, though! """

import weakref
import itertools
import LRUCache

class Flyweight(object):
	""" Inherit from this to have your class act like a Flyweight, basing itself completely off its constructor arguments. """
	
	#TODO: use an LRU cache instead?
#	_Pool = weakref.WeakValueDictionary()
	_Pool = LRUCache.LRUCache(1000)

	def __new__(cls, *args, **kwargs):
		
		#TODO: the below line is also used in cacheing.  May be useful to abstract it out into its own base function like - 'HashArgs(*args, **kwargs)'
		key = "".join(str(x) for x in itertools.chain(args, kwargs.iteritems()))
		
		#TODO: use setdefault instead?
		if not key in Flyweight._Pool:		
		#obj = Flyweight._Pool.get(key, None)
			Flyweight._Pool[key] = super(Flyweight, cls).__new__(cls)
			Flyweight._Pool[key]._flyweight_init_(*args, **kwargs)
			
		return Flyweight._Pool[key]
		#return obj
