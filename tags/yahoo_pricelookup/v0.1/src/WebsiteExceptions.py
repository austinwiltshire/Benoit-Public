
#NOTE: added
#translates key errors into date errors on Google Financial Functions
def ThrowsDateError(func):
    def _(symbol, date):
        try:
            return func(symbol, date)
        except KeyError, e:
            raise DateNotFound(symbol, date)
    return _

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
	
class SymbolHasNoFinancials(Exception):
	""" Raised when a symbol is a tracked company, but the company has no SEC documents
	available.
	
	inv:
		#typechecking
		self.symbol != None
		isinstance(self.symbol,basestring)
	
	"""
	
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isinstance(symbol,str) or isinstance(symbol,unicode)
		
		post:
			#typechecking
			isinstance(self.message, str) or isinstance(self.message, unicode)
		"""
		self.symbol = symbol
		super(SymbolHasNoFinancials,self).__init__(*args, **kwargs)
		
		self.myMessage = "Symbol does not support financials: \"%s\""  % (self.symbol)
		
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
	
class SectorInformationNotFound(Exception):
	""" Raised when a symbol does not support Sector information "
	
	inv:
		#typechecking
		self.symbol != None
		isString(self.symbol)
	"""
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isString(symbol)
		
		post:
			#typechecking
			isString(self.message)
		"""
		
		self.symbol = symbol
		super(SectorInformationNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not find Sector Information for symbol: \"%s\"" % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message

class IndustryInformationNotFound(Exception):
	""" Raised when a symbol does not support Industry Information "
	
	inv:
		#typechecking
		self.symbol != None
		isString(self.symbol)
	"""
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isString(symbol)
		
		post:
			#typechecking
			isString(self.message)
		"""
		
		self.symbol = symbol
		super(IndustryInformationNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not find Industry Information for symbol: \"%s\"" % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message

class CurrencyInformationNotFound(Exception):
	""" Raised when a Currency Information for this symbol is not supported "
	
	inv:
		#typechecking
		self.symbol != None
		isString(self.symbol)
	"""
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isString(symbol)
		
		post:
			#typechecking
			isString(self.message)
		"""
		
		self.symbol = symbol
		super(CurrencyInformationNotFound,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not find Currency Information for symbol: \"%s\"" % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message