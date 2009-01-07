""" Module defines a 'safe float', similar to the Maybe monad, such that float operations are defined when something is None/Null.  All ops on a None/Null return
None/Null themselves, but they do not throw exceptions. """

class SafeFloat(float):
	def __new__(cls, val):
		if val is not None:
			toret = float.__new__(cls, val)
			toret.just = True
			return toret
		else:
			toret = float.__new__(cls, 0.0)
			toret.just = False
			return toret
		
	def __mul__(self, other):
		return self._safe_op(other, "__mul__")

	def __add__(self, other):
		return self._safe_op(other, "__add__")
	
	def __sub__(self, other):
		return self._safe_op(other, "__sub__")
	
	def __div__(self, other):
		return self._safe_op(other, "__div__")
	
	def __eq__(self, arg):
		if not self.just:
			if not arg:
				return True
			if arg:
				if isinstance(arg,SafeFloat):
					if not arg.just:
						return True
					else:
						return False
				else:
					return False
		else:
			if not arg:
				return False
			if isinstance(arg,SafeFloat):
				if not arg.just:
					return False
				else:
					return float.__eq__(self,arg)
			else:
				return float.__eq__(self, arg)
			
	def __nonzero__(self):
		return self.just and float.__nonzero__(self)
		
	def _safe_op(self, arg, op):
		if not self.just:
			return SafeFloat(None)
		elif arg is None:
			return SafeFloat(None)
		elif isinstance(arg,SafeFloat) and not arg.just:
				return SafeFloat(None)
		else:
			return SafeFloat(getattr(float,op)(self, arg))
		
		
	def __repr__(self):
		if not self.just:
			return None.__repr__()
		else:
			return float.__repr__(self)
			