import datetime
import doctest
import contract
import unittest
import Market

#contract.checkmod(Market)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Market))

class MarketTestCase(unittest.TestCase):
	def setUp(self):
		self.symbol = Market.Symbol("IRBT")
	
	def testQuarterlyCashAndEquivalents(self):
		self.assertAlmostEqual(self.symbol.Quarter(datetime.datetime(2008,6,28)).BalanceSheet.CashAndEquivalents, 14.76)
		
	def testAnnualRevenue(self):
		self.assertAlmostEquals(self.symbol.Annual(datetime.datetime(2007,12,29)).IncomeStatement.Revenue, 249.08)
	
	def testQuarterlyRevenue(self):
		self.assertAlmostEquals(self.symbol.Quarter(datetime.datetime(2008,6,28)).IncomeStatement.Revenue, 67.2)
		
	def testAnnualCashAndEquivalents(self):
		self.assertAlmostEqual(self.symbol.Quarter(datetime.datetime(2007,12,29)).BalanceSheet.CashAndEquivalents, 26.73)