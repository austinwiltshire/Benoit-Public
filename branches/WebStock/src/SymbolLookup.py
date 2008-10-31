""" Module handles converting from Yahoo type symbols to Google type symbols.  Functionality may eventually be moved
to the respective modules.  Symbol resolution is a cross cutting concern, though, so this class may actually be incorporated
into Google and Yahoo classes as an aspect/policy style "dependency injection" 

examples:

>>> resolver = SymbolLookup()
>>> resolver.isYahoo("BRK-A")
True

>>> resolver.isGoogle("BRK-A")
False

>>> resolver.isGoogle("BRK.A")
True

>>> resolver.getGoogle("BRK-A")
u'BRK.A'

>>> resolver.isYahoo("BRK.A")
True

>>> resolver.getYahoo("BRK.A")
u'BRK-A'

>>> resolver.getYahoo("OTC:NTDOY")
u'NTDOY.PK'

>>> resolver.getGoogle("NTDOY.PK")
u'OTC:NTDOY'

>>> resolver.getGoogle("OTC:NTDOY")
u'OTC:NTDOY'

>>> resolver.getYahoo("NTDOY.PK")
u'NTDOY.PK'

"""

import re

class SymbolAmbiguous(Exception):
	""" Raised when a symbol cannot be resolved between yahoo and google, usually because of exchange information appended to
	a yahoo symbol being converted to a google symbol.
	
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
			isinstance(self.message, basestring)
		"""
		
		self.symbol = symbol
		super(SymbolAmbiguous,self).__init__(*args, **kwargs)
		
		self.myMessage = "Symbol lookup is ambiguous : \"%s\".  (Could and extension be interpreted as an exchange?) " % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message

class ExchangeInvalid(Exception):
	""" Raised when an exchange in a symbol resolution has no mapping(has no lookup in Google or Yahoo)"
	
	inv:
		#typechecking
		self.exchange != None
		isinstance(self.exchange,basestring)
	"""
	def __init__(self, exchange, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isinstance(exchange,basestring)
		
		post:
			#typechecking
			isinstance(self.message, basestring)
		"""
		
		self.exchange = exchange
		super(ExchangeInvalid,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not resolve exchange code : \"%s\".  Either invalid or ambiguous." % self.exchange
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message
	
class SymbolInvalid(Exception):
	""" Raised when a symbol has no resolution(has no lookup in Google or Yahoo)"
	
	inv:
		#typechecking
		self.symbol != None
		isinstance(self.symbol,str)
	"""
	def __init__(self, symbol, *args, **kwargs):
		"""
		
		pre:
			#typechecking
			isinstance(symbol,basestring)
		
		post:
			#typechecking
			isinstance(self.message, basestring)
		"""
		
		self.symbol = symbol
		super(SymbolInvalid,self).__init__(*args, **kwargs)
		
		self.myMessage = "Could not resolve symbol : \"%s\"" % self.symbol
		
		if not self.message:
			self.message = self.myMessage
		else:
			self.message = "\n".join([self.myMessage,self.message])
		
	def __str__(self):
		return self.message
	
class SymbolLookup(object):
	""" A utility class for symbol resolution.  
	
	inv:
	  isinstance(self.exchangeMapping, dict)
	  all([value in self.exchangeMapping.keys() for value in self.exchangeMapping.values()]) 
	  #ensure that this is a two way dict
	  self.exchangeMapping == SymbolLookup.exchangeMapping
	  isinstance(self.yahooSymbol, type(re.compile("")))
	  isinstance(self.googleSymbol, type(re.compile("")))
	  self.yahooSymbol == SymbolLookup.yahooSymbol
	  self.googleSymbol == SymbolLookup.googleSymbol
	  self.yahooSymbol.match("BRK-A.PK") is not None
	  self.googleSymbol.match("OTC:BRK.A") is not None
	"""
	
	#all of this might be better defined in XML

	#these two regular expressions match yahoo style lookups and google style look ups respectively
	yahooSymbol = re.compile("(?P<name>[A-z1-9]+)(-(?P<extension>[A-z]+))?([.](?P<exchange>[A-z]+))?\Z")
	googleSymbol = re.compile("((?P<exchange>[A-z]+):)?(?P<name>[A-z1-9]+)([.](?P<extension>[A-z]+))?\Z")
	simpleSymbol = re.compile("(?P<name>[A-z1-9]+)\Z")

	#this is a mapping from yahoo style exchanges to google style exchanges, and back again.  
	#TODO: this is a first pass... what might make more sense is an automatic look up.  I can get exhange information off of each(well,
	#right now just google).  Then a simple look up of the exchange on the other side, and an updating of this table(in XML) so that the
	#relationship is better known.  Right now, I just am trying to to KISS (keep it simple stupid)

	exchangeMapping = {"PK":"OTC"}

	for key,value in exchangeMapping.items():
		if value in exchangeMapping.keys():
			raise Exception("Ambiguous exchange data in SymbolLookup.py, key %s ambiguous with value %s" % (key,value))
		exchangeMapping[value] = key

	def __init__(self):
		"""
		pre:
		  all([value in self.exchangeMapping.keys() for value in self.exchangeMapping.values()])

		"""
		#go the other way with regards to my exchanges, making my exchangeMap a two way dict.  Can this be done at the class level?
		#TODO: can this be done at the class level?
		pass

	
	def getGoogle(self, potentialSymbol):
		""" Takes in a potential symbol and returns the Google version of it, if it exists.  If the symbol is invalid, 
		raises an invalid symbol exception.
		
		>>> resolver = SymbolLookup()
		>>> resolver.getGoogle("BRK-A.PK")
		u'OTC:BRK.A'
		
		>>> resolver.getGoogle("BRK.PK")
		u'OTC:BRK'
		
		>>> resolver.getGoogle("BRK-A")
		u'BRK.A'
		
		>>> resolver.getGoogle("OTC:BRK.A")
		u'OTC:BRK.A'
		
		>>> resolver.getGoogle("OTC:BRK")
		u'OTC:BRK'
		
		>>> resolver.getGoogle("BRK.A")
		u'BRK.A'
		
		>>> resolver.getGoogle("IRBT")
		u'IRBT'
		
		>>> resolver.getGoogle("OTC:BRK-A")
		Traceback (most recent call last):
			...
		SymbolInvalid: Could not resolve symbol : \"OTC:BRK-A\"
		
		>>> resolver.getGoogle("BRK-A.FART")
		Traceback (most recent call last):
			...
		ExchangeInvalid: Could not resolve exchange code : \"FART\".  Either invalid or ambiguous.
		
		pre:
		  isinstance(potentialSymbol, basestring)
		  
		post[]:
		  isinstance(__return__, basestring)
		"""
		if self.isSimple(potentialSymbol):
			return unicode(potentialSymbol)
		 
		elif self.isGoogle(potentialSymbol):
			if self.isYahoo(potentialSymbol): #ambiguous, try my best to resolve whether i'm looking at an exchange or an extension
				return self._convertAmbiguousToGoogle(potentialSymbol)
			else:
				return unicode(potentialSymbol)
		
		elif self.isYahoo(potentialSymbol):
			return  self._convertYahooToGoogle(potentialSymbol)
		
		else:
			raise SymbolInvalid(potentialSymbol)
 
 	def _convertAmbiguousToGoogle(self, potentialSymbol):
 		""" Used when I'm trying to convert an ambiguous symbol(could be either yahoo or google) into a Google symbol.
 		Assumes the symbol is a valid google and yahoo symbol.
 		
 		pre:
 			self.isYahoo(potentialSymbol)
 			self.isGoogle(potentialSymbol)
 			isinstance(potentialSymbol,basestring)
 		post[]:
 			isinstance(__return__,basestring)
 			self.isGoogle(potentialSymbol)
 		"""
 		parsedSymbol = self.yahooSymbol.match(potentialSymbol).groupdict()
		#this bit of functionality should ONLY be called in the case of a name.extension(google) or name.exchange(yahoo)
		check = re.compile("[A-z1-9]+[.][A-z]")
		if not check.match(potentialSymbol):
			#I have no idea why this would fail, but just in case, i should throw here rather than let some weird condition
			#go thru
			raise SymbolAmbiguous(potentialSymbol)
		if parsedSymbol["exchange"] in self.exchangeMapping.keys(): #guessing that this is yahoo style exchange info
			exchange = "%s:" % self.exchangeMapping[parsedSymbol["exchange"]]
			name = parsedSymbol["name"]
			return unicode("".join([exchange,name]))
		else: #guessing that this is google style extension info. possibly just bad exchange info!!!!
			return unicode(potentialSymbol)
 		
 	def _convertYahooToGoogle(self, potentialSymbol):
 		""" Used when I'm trying to convert a Yahoo symbol into a Google symbol.  Assumes the symbol is a valid yahoo symbol. 
 		
 		pre:
 			self.isYahoo(potentialSymbol)
 			isinstance(potentialSymbol,basestring)
 		post[]:
 			isinstance(__return__,basestring)
 			self.isGoogle(__return__)
 		"""
 		googleVersion = ""
		parsedSymbol = self.yahooSymbol.match(potentialSymbol).groupdict()
		
		exchange = parsedSymbol["exchange"]
		if exchange:
			if parsedSymbol["exchange"] in self.exchangeMapping.keys():
				exchange = "%s:" % self.exchangeMapping[parsedSymbol["exchange"]]
			else:
				raise ExchangeInvalid(parsedSymbol["exchange"])
		else:
			exchange = "" #no exchange data 
		
		extension = ".%(extension)s" % parsedSymbol if parsedSymbol["extension"] else ""
		name = parsedSymbol["name"]
		
		return unicode("".join([exchange,name,extension]))

 
	def getYahoo(self, potentialSymbol):
		""" Takes in a potential symbol and returns the Yahoo version of it, if it exists.  If the symbol is invalid, 
		raises an invalid symbol exception. 
		
		>>> resolver = SymbolLookup()
		>>> resolver.getYahoo("OTC:BRK.A")
		u'BRK-A.PK'
		
		>>> resolver.getYahoo("OTC:BRK")
		u'BRK.PK'
		
		>>> resolver.getYahoo("BRK.A")
		u'BRK-A'
		
		>>> resolver.getYahoo("BRK-A.PK")
		u'BRK-A.PK'
		
		>>> resolver.getYahoo("BRK.PK")
		u'BRK.PK'
		
		>>> resolver.getYahoo("BRK-A")
		u'BRK-A'
		
		>>> resolver.getYahoo("IRBT")
		u'IRBT'
		
		>>> resolver.getYahoo("OTC:BRK-A")
		Traceback (most recent call last):
			...
		SymbolInvalid: Could not resolve symbol : \"OTC:BRK-A\"
		
		>>> resolver.getYahoo("FART:BRK.A")
		Traceback (most recent call last):
			...
		ExchangeInvalid: Could not resolve exchange code : \"FART\".  Either invalid or ambiguous.
		
		pre:
		  isinstance(potentialSymbol, basestring)
		post[]:
		  isinstance(__return__, basestring)
		"""
		if self.isSimple(potentialSymbol):
			return unicode(potentialSymbol)
		 
		elif self.isYahoo(potentialSymbol):
			if self.isGoogle(potentialSymbol): #ambiguous, try my best to resolve whether i'm looking at an exchange or an extension
				return self._convertAmbiguousToYahoo(potentialSymbol)
			else:
				return unicode(potentialSymbol)
		
		elif self.isGoogle(potentialSymbol):
			return  self._convertGoogleToYahoo(potentialSymbol)
		
		else:
			raise SymbolInvalid(potentialSymbol)
	
	def _convertAmbiguousToYahoo(self, potentialSymbol):
		""" Assumes that the incoming symbol resolves as both a google and yahoo symbol(which only happens in the case of
		name.extension(for google) or name.exchange(yahoo).  Returns a pure yahoo interpretation.
		
		pre:
			isinstance(potentialSymbol,basestring)
			self.isGoogle(potentialSymbol)
			self.isYahoo(potentialSymbol)
		post[]:
			self.isYahoo(__return__)
			isinstance(__return__,basestring)
		"""
#		print potentialSymbol, "AMBIGUOUS ***"
		parsedSymbol = self.googleSymbol.match(potentialSymbol).groupdict()
		#this bit of functionality should ONLY be called in the case of a name.extension(google) or name.exchange(yahoo)
		check = re.compile("[A-z1-9]+[.][A-z]")
		if not check.match(potentialSymbol):
			#I have no idea why this would fail, but just in case, i should throw here rather than let some weird condition
			#go thru
			raise SymbolAmbiguous(potentialSymbol)
#		print "actual exchange %s" % parsedSymbol["extension"]
		if parsedSymbol["extension"] in self.exchangeMapping.keys(): #guessing that this is yahoo style exchange info
			exchange = ".%s" % parsedSymbol["extension"]
			name = parsedSymbol["name"]
			return unicode("".join([name,exchange]))
		else: #guessing that this is google style extension info. possibly just bad exchange info!!!!
			extension = "-%s" % parsedSymbol["extension"]
			name = parsedSymbol["name"]
			return unicode("".join([name,extension]))
	
	def _convertGoogleToYahoo(self, potentialSymbol):
		""" Assumes that the incoming symbol resolves as a Google symbol and converts it to a Yahoo symbol 
		pre:
			isinstance(potentialSymbol,basestring)
			self.isGoogle(potentialSymbol)
		post[]:
			self.isYahoo(__return__)
			isinstance(__return__,basestring)
		"""
		yahooVersion = ""
		parsedSymbol = self.googleSymbol.match(potentialSymbol).groupdict()
		
		exchange = parsedSymbol["exchange"]
		if exchange:
			if parsedSymbol["exchange"] in self.exchangeMapping.keys():
				exchange = ".%s" % self.exchangeMapping[parsedSymbol["exchange"]]
			else:
				raise ExchangeInvalid(parsedSymbol["exchange"])
		else:
			exchange = "" #no exchange data 
		
		extension = "-%(extension)s" % parsedSymbol if parsedSymbol["extension"] else ""
		name = parsedSymbol["name"]
		
		return unicode("".join([name,extension,exchange]))	

	def isSimple(self, potentialSymbol):
		""" A predicate that returns whether or not this symbol is simple enough to be on either exchange.  Namely, if it only 
		consists of a stock name, with no exchange or extension data. 
		
		pre:
			isinstance(potentialSymbol, basestring)
		post[]:
			isinstance(__return__, bool)
		"""
		print potentialSymbol, type(potentialSymbol)
		if self.simpleSymbol.match(potentialSymbol):
			return True
		return False
	
	def isGoogle(self, potentialSymbol):
		""" Predicate that takes in a symbol and returns whether or not its a valid Google symbol.  This does not guarantee 
		at all that the webpage actually exists, only that the symbol is in the proper format 
		
		>>> resolver = SymbolLookup()
		>>> resolver.isGoogle("IRBT")
		True
		
		>>> resolver.isGoogle("IRBT.B")
		True
		
		>>> resolver.isGoogle("NYSE:IRBT")
		True
		
		>>> resolver.isGoogle("AMEX:DD.C")
		True
		
		>>> resolver.isGoogle("DD-C")
		False
		
		>>> resolver.isGoogle("DD-C.AMEX")
		False
		
		>>> resolver.isGoogle("AMEX:.C")
		False
		
		pre:
		  isinstance(potentialSymbol, basestring)
		post[]:
		  isinstance(__return__, bool)
		"""
		if self.googleSymbol.match(potentialSymbol):
			return True
		return False
			
		
	
	def isYahoo(self, potentialSymbol):
		""" Predicate that takes in a symbol and returns whether or not its a valid Yahoo symbol.  This does not guarantee
		at all that the webpage actually exists, only that the symbol is in the proper format 
		
		>>> resolver = SymbolLookup()
		>>> resolver.isYahoo("BRK")
		True
		
		>>> resolver.isYahoo("BRK-A")
		True
		
		>>> resolver.isYahoo("BRK.PK")
		True
		
		>>> resolver.isYahoo("BRK-A.PK")
		True
		
		>>> resolver.isYahoo("BRK.PK-A")
		False
		
		>>> resolver.isYahoo(".PK-A")
		False
		
		>>> resolver.isYahoo("OTC:BRK")
		False
		
		pre:
		  isinstance(potentialSymbol, basestring)
		  
		post[]:
		  isinstance(__return__, bool)
		"""
		if self.yahooSymbol.match(potentialSymbol):
			return True
		return False
		



