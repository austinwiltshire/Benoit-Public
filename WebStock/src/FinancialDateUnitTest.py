""" Tests the FinancialDate package. """

import doctest
import contract
import unittest
import FinancialDate

contract.checkmod(FinancialDate)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(FinancialDate))
		
if __name__ == "__main__": #for coverage tests
	unittest.main()
                 