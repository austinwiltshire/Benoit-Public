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
       
#TODO: test that repeats don't occur in the date iterators 
#TODO: test that all dates on a specific stock are in the iterator and visaversa, use an old stock like DD