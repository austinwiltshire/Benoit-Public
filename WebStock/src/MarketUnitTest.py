""" Runs tests on the current Market DSL implementation, currently stored in Module2.py """

import datetime
import doctest
import contract
import unittest

import Module2
from Adapt import Adapt
import Website

#TODO:
# run test that uniqueness is enforced

#contract.checkmod(Market)

#class DoctestWrapper(unittest.TestSuite):
#	def __init__(self):
#		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Market))

class MarketTestCase(unittest.TestCase):
#	def setUp(self):
#		#TODO: Move this out into seperate tests so I can test better over multiple stocks.
#		self.symbol = Module2.Symbol("IRBT")
#	
#	def testQuarterlyCashAndEquivalents(self):
#		self.assertAlmostEqual(self.symbol.Date(6,28,2008).Financials.Quarter.BalanceSheet.CashAndEquivalents, 14.76)
#		
#	def testAnnualRevenue(self):
#		self.assertAlmostEquals(self.symbol.Date(12, 29, 2007).Financials.Annual.IncomeStatement.Revenue, 249.08)
#	
#	def testQuarterlyRevenue(self):
#		self.assertAlmostEquals(self.symbol.Date(6,28,2008).Financials.Quarter.IncomeStatement.Revenue, 67.2)
#		
#	def testAnnualCashAndEquivalents(self):
#		self.assertAlmostEqual(self.symbol.Date(12,29,2007).Financials.Annual.BalanceSheet.CashAndEquivalents, 26.73)
#		
#	def testAnnualNetIncomeStartingLine(self):
#		self.assertAlmostEquals(self.symbol.Date(6,28,2008).Financials.Quarter.CashFlowStatement.NetIncomeStartingLine, -4.51)
#		
#	def testQuarterlyNetIncomeStartingLine(self):
#		self.assertAlmostEqual(self.symbol.Date(12,29,2007).Financials.Annual.CashFlowStatement.NetIncomeStartingLine, 9.06)
#		
#	def testDailyHigh(self):
#		self.assertAlmostEqual(self.symbol.Date(4,21,2008).Prices.High, 17.78)
#		
#	def testIndustry(self):
#		self.assertEqual(self.symbol.Meta.Industry, u"Appliance & Tool")
#		
#	def testPE(self):
#		#make sure my financials are in the DB
#		self.symbol.Date(12,29,2007).Financials.Annual.IncomeStatement.NetIncome
#		self.symbol.Date(12,29,2007).Financials.Annual.BalanceSheet.TotalCommonSharesOutstanding
#		
#		self.assertAlmostEqual(self.symbol.Date(4,21,2008).Fundamentals.PriceToEarnings, 47.13, places = 2)
		
	def testPrefetch(self):
		self.symbol = Module2.Symbol("DD")
		self.symbol.prefetch()
			
		
		self.assertEqual(set(self.symbol.AvailableDates(Module2.Financials.Annual.IncomeStatement)),\
						 set([datetime.date(2007,12,31), datetime.date(2006,12,31), datetime.date(2005,12,31), datetime.date(2004,12,31)]))
		
		self.assertEqual(set(self.symbol.AvailableDates(Module2.Financials.Quarter.IncomeStatement)),\
						  set([datetime.date(2008,9,30), datetime.date(2008,6,30), datetime.date(2008,3,31), datetime.date(2007,12,31), datetime.date(2007,9,30)]))
		
		self.assertEqual(set(self.symbol.AvailableDates(Module2.Financials.Annual.CashFlowStatement)),\
						 set([datetime.date(2007,12,31), datetime.date(2006,12,31), datetime.date(2005,12,31), datetime.date(2004,12,31)]))
		
		self.assertEqual(set(self.symbol.AvailableDates(Module2.Financials.Quarter.CashFlowStatement)),\
						  set([datetime.date(2008,9,30), datetime.date(2008,6,30), datetime.date(2008,3,31), datetime.date(2007,12,31)]))
		
		self.assertEqual(set(self.symbol.AvailableDates(Module2.Financials.Annual.BalanceSheet)),\
						 set([datetime.date(2007,12,31), datetime.date(2006,12,31), datetime.date(2005,12,31), datetime.date(2004,12,31)]))
		
		self.assertEqual(set(self.symbol.AvailableDates(Module2.Financials.Quarter.BalanceSheet)),\
						  set([datetime.date(2008,9,30), datetime.date(2008,6,30), datetime.date(2008,3,31), datetime.date(2007,12,31), datetime.date(2007,9,30)]))
		
		self.assertEqual(self.symbol.AvailableDates(Module2.Prices)[-1], datetime.date(2009,1,2))
		
#	def testUnusualIncome(self):
#		self.assertAlmostEqual(self.symbol.Date(12,29,2007).Financials.Quarter.IncomeStatement.UnusualExpense, 1.68)
#		
#	def testNoneType(self):
#		self.assertEqual(self.symbol.Date(3,29,2008).Financials.Quarter.IncomeStatement.UnusualExpense, None)
#		
#	def testZAvailableDatesFinancials(self):
#		#unit test does these in alphabetical order.  i really shouldn't rely on the ordering anyway but whatever
#		self.assertEqual(self.symbol.AvailableDates(Module2.Financials.Annual.BalanceSheet),[datetime.date(2007,12,29)])
#		
#	def testZAvailableDatesPrices(self):
#		#unit test does these in alphabetical order.  i really shouldn't rely on the ordering anyway but whatever
#		self.assertEqual(self.symbol.AvailableDates(Module2.Prices),[datetime.date(2008,4,21)])
#		
#	def testZAvailableDatesFundamentals(self):
#		#unit test does these in alphabetical order.  i really shouldn't rely on the ordering anyway but whatever
#		self.assertEqual(self.symbol.AvailableDates(Module2.Fundamentals),[datetime.date(2008,4,21)])		
#		
#	def testZMostRecent(self):
#		cashflow = self.symbol.Date(7,20,2008).MostRecent(Module2.Financials.Quarter.CashFlowStatement)
#		self.assertEqual(cashflow.NetIncomeStartingLine, -4.51)
#		self.assertEqual(Adapt(cashflow.Date,datetime.date), datetime.date(2008,6,28))
#	
#	def testRaise(self):
#		testFunctor = lambda cf : cf.NetIncomeStartingLine
#		self.assertRaises(Website.DateNotFound, testFunctor, self.symbol.Date(7,20,2008).Financials.Quarter.CashFlowStatement)
#		self.assertEqual([x.Date for x in Module2.Financials.Quarter.CashFlowStatement.query().all()], [datetime.datetime(2008,6,28)])