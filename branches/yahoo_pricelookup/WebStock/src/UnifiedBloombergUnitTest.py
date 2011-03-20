""" Obsolete unit tests of UnifiedBloomberg. """

import UnifiedBloomberg
import Website
import Yahoo
from datetime import date
import doctest
import contract
import unittest

contract.checkmod(UnifiedBloomberg)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(UnifiedBloomberg))

class UnifiedBloombergTestCase(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass
       
    def testDuplicateMethod(self):
    	class mock(Website.Bloomberg):
    		def getHigh(self):
    			pass
    	self.assertRaises(UnifiedBloomberg.DuplicateMethod, UnifiedBloomberg.UnifiedBloomberg, mock,Yahoo.Yahoo)
    	