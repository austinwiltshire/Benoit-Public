import weakref
import itertools

class Flyweight(object):
    _Pool = weakref.WeakValueDictionary()

    def __new__(cls, *args, **kwargs):
    	key = "".join(str(x) for x in itertools.chain(args, kwargs.iteritems()))
        obj = Flyweight._Pool.get(key, None)

        if not obj:
            obj = super(Flyweight,cls).__new__(cls)
            Flyweight._Pool[key] = obj

        return obj
