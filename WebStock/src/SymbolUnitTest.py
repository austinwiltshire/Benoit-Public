import Symbol
import Website
import Yahoo
import datetime
import doctest
import contract
import unittest

contract.checkmod(Symbol)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Symbol))

class SymbolTestCase(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass