import doctest
import contract
import unittest
import FinancialXML

contract.checkmod(FinancialXML)

doctest.testmod(FinancialXML)

class DoctestWrapper(unittest.TestSuite):
    def __init__(self):
        unittest.TestSuite.__init__(self, doctest.DocTestSuite(FinancialXML))