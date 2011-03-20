""" Defines a Flyweight base class that will allow anyone who inherits from it to be a flyweight based on it's constructor arguments.  This requires that the
user have no state independent of the constructor arguments, though! """

import weakref
import itertools

class Flyweight(object):
	""" Inherit from this to have your class act like a Flyweight, basing itself completely off its constructor arguments. """
	
	#TODO: use an LRU cache instead?
	_Pool = weakref.WeakValueDictionary()

	def __new__(cls, *args, **kwargs):
		
		#TODO: the below line is also used in cacheing.  May be useful to abstract it out into its own base function like - 'HashArgs(*args, **kwargs)'
		key = "".join(str(x) for x in itertools.chain(args, kwargs.iteritems()))
		
		#TODO: use setdefault instead?
		obj = Flyweight._Pool.get(key, None)

		if not obj:
			obj = super(Flyweight, cls).__new__(cls)
			Flyweight._Pool[key] = obj

		return obj
