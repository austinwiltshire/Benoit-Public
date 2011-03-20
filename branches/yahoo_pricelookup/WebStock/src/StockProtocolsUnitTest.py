""" Verification test for Stock Protocols, which was a prototype for the new generic function implementation of registry. """

import doctest
import contract
import unittest
import StockProtocols

from datetime import datetime, date

#contract.checkmod(Market)

#class DoctestWrapper(unittest.TestSuite):
#	def __init__(self):
#		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Market))

class StockProtocolsTestCase(unittest.TestCase):
	def setUp(self):
		pass
	
	def testBasic(self):
		
		@StockProtocols.resolver
		def what_what_in_the_butt(symbol):
			""" i'm delicate like a flower """
			
			return symbol
				
		self.assertTrue(what_what_in_the_butt.__name__ == "what_what_in_the_butt")
		self.assertTrue(what_what_in_the_butt.__doc__ == " i'm delicate like a flower ")
		self.assertTrue(what_what_in_the_butt(u"irbt") == u"irbt")
		
		class x(object):
			def __init__(self, a):
				self.Symbol = a
		
		b = x("irbt")
		self.assertTrue(what_what_in_the_butt(b) == u"irbt")
		
		@StockProtocols.resolver
		def symbol_date(symbol, date):
			return (symbol, date)
		
		class y(object):
			def __init__(self, s, d):
				self.Symbol = s
				self.Date = d
		
		c = y(u"irbt",date(2008,7,12))
		
		self.assertTrue(symbol_date(c) == (u"irbt",date(2008,7,12)))
		self.assertTrue(symbol_date("irbt",datetime(2008,7,12)) == (u"irbt",date(2008,7,12)))
		self.assertTrue(what_what_in_the_butt(stock=b) == (u"irbt"))
		self.assertTrue(symbol_date(stock=c) == (u"irbt",date(2008,7,12)))
		self.assertTrue(what_what_in_the_butt(symbol="irbt") == (u"irbt"))
		self.assertTrue(what_what_in_the_butt(symbol=u"irbt") == (u"irbt"))
		self.assertTrue(symbol_date(symbol="irbt",date=datetime(2008,7,12)) == (u"irbt",date(2008,7,12)))
		self.assertTrue(symbol_date(date(2008,7,12), symbol="irbt") == (u"irbt",date(2008,7,12)))
			
		self.assertTrue(StockProtocols.Registry.symbol_date("irbt", date=datetime(2008,7,12)) == (u"irbt",date(2008,7,12)))
		self.assertTrue(StockProtocols.Registry.what_what_in_the_butt(symbol="irbt") == (u"irbt"))
		