class SymbolNotFound(Exception):
	""" Raised when a symbol is not found or information for it cannot be found "
	
	inv:
		#typechecking
		self.symbol != None
		isinstance(self.symbol,basestring)
	"""
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isinstance(symbol,basestring)
		
		post:
			#typechecking
			isinstance(self.message, str) or isinstance(self.message, unicode)
		"""
		
		self.symbol = symbol
		super(SymbolNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not find symbol : \"%s\"" % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message
	
class DateNotFound(Exception):
	""" Raised when a requested date is not available for a peice of information on
	a stock. 
	
	inv:
		#typechecking
		self.symbol != None
		isinstance(self.symbol,basestring)
		self.date != None
		isinstance(self.date,datetime.date)
	"""
	
	def __init__(self, symbol, date, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isinstance(symbol,basestring)
			isinstance(date,datetime.date)
			
		post:
			#typechecking
			isinstance(self.message, str) or isinstance(self.message, unicode)
		"""
		
		self.symbol = symbol
		self.date = date

		super(DateNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Symbol \"%s\" does not support date : %s" % (self.symbol, str(self.date))
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message