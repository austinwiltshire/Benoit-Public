import datetime
import doctest
import contract
import unittest
#import Market

import Module2

#contract.checkmod(Market)

#class DoctestWrapper(unittest.TestSuite):
#	def __init__(self):
#		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Market))

class MarketTestCase(unittest.TestCase):
	def setUp(self):
		self.symbol = Module2.Symbol("IRBT")
	
#	def testQuarterlyCashAndEquivalents(self):
#		self.assertAlmostEqual(self.symbol.Date(6,28,2008).Financials.Quarter.BalanceSheet.CashAndEquivalents, 14.76)
		
#	def testAnnualRevenue(self):
#		self.assertAlmostEquals(self.symbol.Date(12, 29, 2007).Financials.Annual.IncomeStatement.Revenue, 249.08)
	
#	def testQuarterlyRevenue(self):
#		self.assertAlmostEquals(self.symbol.Date(6,28,2008).Financials.Quarter.IncomeStatement.Revenue, 67.2)
		
#	def testAnnualCashAndEquivalents(self):
#		self.assertAlmostEqual(self.symbol.Date(12,29,2007).Financials.Annual.BalanceSheet.CashAndEquivalents, 26.73)
		
#	def testAnnualNetIncomeStartingLine(self):
#		self.assertAlmostEquals(self.symbol.Date(6,28,2008).Financials.Quarter.CashFlowStatement.NetIncomeStartingLine, -4.51)
		
#	def testQuarterlyNetIncomeStartingLine(self):
#		self.assertAlmostEqual(self.symbol.Date(12,29,2007).Financials.Annual.CashFlowStatement.NetIncomeStartingLine, 9.06)
		
#	def testDailyHigh(self):
#		self.assertAlmostEqual(self.symbol.Date(4,21,2008).Prices.High, 17.78)
		
	def testIndustry(self):
		self.assertEqual(self.symbol.Meta.Industry, u"Appliance & Tool")
		
#	def testPE(self):
#		self.assertAlmostEqual(self.symbol.Date(4,21,2008).Fundamentals.PriceToEarnings, 47.13, places = 2)
		
#	def testUnusualIncome(self):
#		self.assertAlmostEqual(self.symbol.Date(12,29,2007).Financials.Quarter.IncomeStatement.UnusualExpense, 1.68)
		
#	def testNoneType(self):
#		self.assertEqual(self.symbol.Date(3,29,2008).Financials.Quarter.IncomeStatement.UnusualExpense, None)