def Handles(exception,returns=None,constraints=lambda e: True):
	def _(func):
		def __(*args, **kwargs):
			try:
				return func(*args, **kwargs)
			except exception, e:
				if constraints(e):
					return returns
				else:
					raise
		__.__name__ = func.__name__
		__.__doc__ = func.__doc__
		return __
	return _

IsOperandErrorPlus = lambda e: "unsupported operand type(s) for +:" in e
IsOperandErrorMinus = lambda e: "unsupported operand type(s) for -:" in e
IsOperandErrorDivides = lambda e: "unsupported operand type(s) for /:" in e
IsOperandErrorMultiplies = lambda e: "unsupported operand type(s) for *:" in e  
		