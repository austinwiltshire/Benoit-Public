import doctest
import contract
import unittest
import SymbolLookup

contract.checkmod(SymbolLookup)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(SymbolLookup))
		
if __name__ == "__main__": #for coverage tests
	unittest.main()
                 