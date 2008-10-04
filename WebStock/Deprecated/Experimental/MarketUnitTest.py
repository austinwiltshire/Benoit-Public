import datetime
import doctest
import contract
import unittest
import Market

contract.checkmod(Market)

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
		self.assertAlmostEqual(self.symbol.Annual(datetime.datetime(2007,12,29)).BalanceSheet.CashAndEquivalents, 26.73)
		
	def testAnnualNetIncomeStartingLine(self):
		self.assertAlmostEquals(self.symbol.Quarter(datetime.datetime(2008,6,28)).CashFlowStatement.NetIncomeStartingLine, -4.51)
		
	def testQuarterlyNetIncomeStartingLine(self):
		self.assertAlmostEqual(self.symbol.Annual(datetime.datetime(2007,12,29)).CashFlowStatement.NetIncomeStartingLine, 9.06)
		
	def testDailyHigh(self):
		self.assertAlmostEqual(self.symbol.Daily(datetime.date(2008,4,21)).TradingDay.High, 17.78)
		
	def testIndustry(self):
		self.assertEqual(self.symbol.Meta.Metadata.Industry, u"Appliance & Tool")