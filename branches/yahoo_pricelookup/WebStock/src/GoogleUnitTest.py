import Google
from TestTools import assertClose, compareDicts
from datetime import date
import datetime
import doctest
import contract
import unittest
#import FinancialDate

contract.checkmod(Google)
#contract.checkmod(FinancialDate)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Google))

class GoogleTestCase(unittest.TestCase):
	#date tests
	
	def testDates(self):
		""" Basic tests for date functionality on google.  Tests each 'standard' function """
		
		self.assertEqual(Google.getAnnualIncomeStatementDates("ATVI")[-1], date(2007, 12, 31))
		self.assertEqual(Google.getQuarterlyIncomeStatementDates("ATVI")[-1], date(2008, 9, 30))
		self.assertEqual(Google.getAnnualBalanceSheetDates("ATVI")[-1], date(2007, 12, 31))
		self.assertEqual(Google.getQuarterlyBalanceSheetDates("ATVI")[-1], date(2008, 9, 30))
		self.assertEqual(Google.getAnnualCashFlowStatementDates("ATVI")[-1], date(2007, 12, 31))
		self.assertEqual(Google.getQuarterlyCashFlowStatementDates("ATVI")[-1], date(2008, 9, 30))
		
	def testDatesFails(self):
		""" Ensures date checks raise proper errors """
		
		self.assertRaises(Google.SymbolNotFound, lambda: Google.getAnnualIncomeStatementDates("CHEESE"))
		self.assertRaises(Google.SymbolHasNoFinancials, lambda: Google.getAnnualIncomeStatementDates("NTDOY"))
	
	
	#failure tests
	def testNonNegativeNumbers(self):
		""" Make sure I'm not mixing up negatives, this should fail """
		#TODO: BRK.B routes to BRK.A on the webiste itself, but now that i don't route through the website...
		# this works in the old one due to routing but... really, should it be supported?
		self.assertNotEqual(Google.getAnnualCashFromInvestingActivities("BRK.A",date(2006, 12, 31)), 14077.0)
	
	def testBigNumbers(self):
		""" Make sure I don't loose precision with big numbers, this should fail """
		self.assertNotEqual(Google.getAnnualTotalAssets("IBN",date(2006, 3, 31)), 2772295.1)
	
	def testZeroes(self):
		""" Make sure numbers that shouldn't be zero fail """
		self.assertNotEqual(Google.getQuarterlyDividendsPerShare("IRBT", date(2007, 12, 29)) ,-0.06)
		
	def testTinyNumbers(self):
		""" Make sure numbers near zero that are wrong fail """
		self.assertNotEqual(Google.getQuarterlyDilutedNormalizedEPS('S', date(2008, 9, 30)), -0.11) 
     
	def testDashesMixedWithNumbers(self): 
		""" Make sure that a wrong answer with dashes and numbers fails """
		self.assertNotEqual(Google.getQuarterlyIntangibles(('BOOM'), date(2007, 9, 30)), 0.0)
		
	def testRandomLookups(self):
		""" Make sure to not screw up a random search and make sure it fails if its wrong """
		self.assertNotAlmostEqual(Google.getAnnualIssuanceOfStock("CSCO", date(2005, 07, 30)), 9148.00)
		
	#redundency tests
	def testAnnualAndQuarterlyAccess(self):
		""" Test random quarterly and annual output """
		#randomly testing other symbols and dates that I've already checked is more robust and ensures that there's no single point of failure
		#in other words, ensures that one test isn't 'accidently' passing.
		
		#annuals
		self.assertAlmostEqual(Google.getAnnualRevenue("CICI", date(2006, 12, 31)), 2.34)
		self.assertAlmostEqual(Google.getAnnualCashAndEquivalents("CICI", date(2006, 12, 31)), 0.73)
		self.assertAlmostEqual(Google.getAnnualNetIncomeStartingLine("CICI", date(2006, 12, 31)), -3.29)
		
		#quarterlys
		self.assertAlmostEqual(Google.getQuarterlyRevenue("CICI", date(2007, 12, 31)), 0.8) 
		self.assertAlmostEqual(Google.getQuarterlyCashAndEquivalents("CICI", date(2007, 12, 31)), 1.14) 
		self.assertAlmostEqual(Google.getQuarterlyNetIncomeStartingLine("CICI", date(2007, 12, 31)), -0.64)
	
	
	#format tests
	def testMixedBoldedSpanned(self):
		""" Test results that have mixed bold and span tags in them """
		self.assertEqual(Google.getQuarterlyOperatingIncome('S', date(2007, 12, 31)),-29625.0)
	
	def testMixedSpanned(self):
		""" Test results that have mixed span tags in them """
		self.assertEqual(Google.getQuarterlyOtherNet('S', date(2008, 3, 31)),None)
		
	def testAllSpannedBolded(self):
		""" Tests results that are all spanned and bolded """
		self.assertEqual(Google.getQuarterlyIncomeAfterTax('S', date(2008, 3, 31)),-505.00)
 
	def testBoldedKeyword(self):
		""" Tests results that rely on a bolded keyword """
		self.assertEqual(Google.getQuarterlyTotalRevenue("IRBT", date(2008, 3, 29)), 57.30)
 
	def testSpannedKeyword(self):
		""" Tests results that rely on a spanned keyword """
		self.assertEqual(Google.getQuarterlyCashAndEquivalents("IRBT", date(2008, 3, 29)), 22.86)
    
	def testMixedDashesAndNotZeros(self):
		""" Tests that dashes can be mixed with non-zero numbers """
		self.assertEqual(Google.getAnnualLongTermInvestments("WHR", date(2007, 12, 31)), None)
	
	#income statement annuals
	def testAnnualRevenue(self):
		""" Test that I find Annual Revenue """
		self.assertEquals(Google.getAnnualRevenue("DD", date(2007, 12, 31)),29378.00)
		
	def testAnnualOtherRevenue(self):
		""" Test that I find Annual Other Revenue """
		self.assertEquals(Google.getAnnualOtherRevenue("DD", date(2007, 12, 31)),1275.00)
 
	def testAnnualTotalRevenue(self):
		""" Test that I find Annual Total Revenue """
		self.assertEquals(Google.getAnnualTotalRevenue("DD", date(2007, 12, 31)),30653.00)
		
	def testAnnualCostOfRevenue(self):
		""" Test that I find Annual Cost of Revenue """
		self.assertEquals(Google.getAnnualCostOfRevenue("DD", date(2007, 12, 31)),21746.00)
		
	def testAnnualGrossProfit(self):
		""" Test that I find Annual Gross Profit"""
		self.assertEquals(Google.getAnnualGrossProfit("DD", date(2007, 12, 31)),7632.00)
		
	def testAnnualSGAExpenses(self):
		""" Test that I find Annual SGA Expenses"""
		self.assertEquals(Google.getAnnualSGAExpenses("DD", date(2007, 12, 31)),3396.00)
		
	def testAnnualResarchAndDevelopment(self):
		""" Test that I find Annual Resarch And Development """
		self.assertEquals(Google.getAnnualResearchAndDevelopment("DD", date(2007, 12, 31)),1338.00)
		
	def testAnnualDepreciationAmortization(self):
		""" Test that I find Annual Depreciation and Amortization"""
		self.assertEquals(Google.getAnnualDepreciationAmortization("DD", date(2007, 12, 31)),None)		
		
	def testAnnualInterestNetOperating(self):
		""" Test that I find Annual Interest Net Operating"""
		self.assertEquals(Google.getAnnualInterestNetOperating("DD", date(2007, 12, 31)),430.00)
		
	def testAnnualUnusualExpense(self):
		""" Test that I find Annual Unusual Expense"""
		self.assertEquals(Google.getAnnualUnusualExpense("DD", date(2007, 12, 31)),None)
		
	def testAnnualOtherOperatingExpenses(self):
		""" Test that I find Annual Other Operating Expenses"""
		self.assertEquals(Google.getAnnualOtherOperatingExpenses("DD", date(2007, 12, 31)),None)
		
	def testAnnualTotalOperatingExpense(self):
		""" Test that I find Annual Total Operating Expense"""
		self.assertEquals(Google.getAnnualTotalOperatingExpense("DD", date(2007, 12, 31)),26910.00)
		
	def testAnnualOperatingIncome(self):
		""" Test that I find Annual Operating Income"""
		self.assertEquals(Google.getAnnualOperatingIncome("DD", date(2007, 12, 31)),3743.00)
		
	def testAnnualInterestIncome(self):
		""" Test that I find Annual Interest Income"""
		self.assertEquals(Google.getAnnualInterestIncome("DD", date(2007, 12, 31)),None)
		
	def testAnnualGainOnSaleOfAssets(self):
		""" Test that I find Annual Gain On Sale Of Assets"""
		self.assertEquals(Google.getAnnualGainOnSaleOfAssets("DD", date(2007, 12, 31)),None)
		
	def testAnnualOtherNet(self):
		""" Test that I find Annual Other Net"""
		self.assertEquals(Google.getAnnualOtherNet("DD", date(2007, 12, 31)),None)
		
	def testAnnualIncomeBeforeTax(self):
		""" Test that I find Annual Income Before Tax"""
		self.assertEquals(Google.getAnnualIncomeBeforeTax("DD", date(2007, 12, 31)),3743.00)
		
	def testAnnualIncomeAfterTax(self):
		""" Test that I find Annual Income After Tax"""
		self.assertEquals(Google.getAnnualIncomeAfterTax("DD", date(2007, 12, 31)),2995.0)
		
	def testAnnualMinorityInterest_Inc(self):
		""" Test that I find Annual Minority Interest(Income Statement) """
		self.assertEquals(Google.getAnnualMinorityInterest_Inc("DD", date(2007, 12, 31)),-7.00)
		
	def testAnnualEquityInAffiliates(self):
		""" Test that I find Annual Equity In Affiliates"""
		self.assertEquals(Google.getAnnualEquityInAffiliates("DD", date(2007, 12, 31)),None)
		
	def testAnnualNetIncomeBeforeExtraItems(self):
		""" Test that I find Annual Net Income Before Extra Items"""
		self.assertEquals(Google.getAnnualNetIncomeBeforeExtraItems("DD", date(2007, 12, 31)),2988.00)
		
	def testAnnualAccountingChange(self):
		""" Test that I find Annual Accounting Change"""
		self.assertEquals(Google.getAnnualAccountingChange("DD", date(2007, 12, 31)),None)
		
	def testAnnualDiscontinuedOperations(self):
		""" Test that I find Annual Discontinued Operations"""
		self.assertEquals(Google.getAnnualDiscontinuedOperations("DD", date(2007, 12, 31)),None)																
		
	def testAnnualExtraordinaryItem(self):
		""" Test that I find Annual Extraordinary Item"""
		self.assertEquals(Google.getAnnualExtraordinaryItem("DD", date(2007, 12, 31)),None)
		
	def testAnnualNetIncome(self):
		""" Test that I find Annual Net Income"""
		self.assertEquals(Google.getAnnualNetIncome("DD", date(2007, 12, 31)),2988.00)
		
	def testAnnualPreferredDividends(self):
		""" Test that I find Annual Preferred Dividends"""
		self.assertEquals(Google.getAnnualPreferredDividends("DD", date(2007, 12, 31)),None)
		
	def testAnnualIncomeAvailToCommonExclExtraItems(self):
		""" Test that I find Annual Income Avail T oCommon Excl Extra Items"""
		self.assertEquals(Google.getAnnualIncomeAvailToCommonExclExtraItems("DD", date(2007, 12, 31)),2978.00)
		
	def testAnnualIncomeAvailToCommonInclExtraItems(self):
		""" Test that I find Annual Income Avail To Common Incl Extra Items"""
		self.assertEquals(Google.getAnnualIncomeAvailToCommonInclExtraItems("DD", date(2007, 12, 31)),2978.00)								
		
	def testAnnualBasicWeightedAverageShares(self):
		""" Test that I find Annual Basic Weighted Average Shares"""
		self.assertEquals(Google.getAnnualBasicWeightedAverageShares("DD", date(2007, 12, 31)),None)
		
	def testAnnualBasicEPSExclExtraItems(self):
		""" Test that I find Annual Basic EPS Excl Extra Items"""
		self.assertEquals(Google.getAnnualBasicEPSExclExtraItems("DD", date(2007, 12, 31)),None)
		
	def testAnnualBasicEPSInclExtraItems(self):
		""" Test that I find Annual Basic EPS Incl Extra Items"""
		self.assertEquals(Google.getAnnualBasicEPSInclExtraItems("DD", date(2007, 12, 31)),None)
		
	def testAnnualDilutionAdjustment(self):
		""" Test that I find Annual Dilution Adjustment"""
		self.assertEquals(Google.getAnnualDilutionAdjustment("DD", date(2007, 12, 31)),None)
		
	def testAnnualDilutedWeightedAverageShares(self):
		""" Test that I find Annual Diluted Weighted Average Shares"""
		self.assertEquals(Google.getAnnualDilutedWeightedAverageShares("DD", date(2007, 12, 31)),925.40)										
		
	def testAnnualDilutedEPSExclExtraItems(self):
		""" Test that I find Annual Diluted EPS Excl Extra Items"""
		self.assertEquals(Google.getAnnualDilutedEPSExclExtraItems("DD", date(2007, 12, 31)),3.22)
		
	def testAnnualDilutedEPSInclExtraItems(self):
		""" Test that I find Annual Diluted EPS Incl Extra Items"""
		self.assertEquals(Google.getAnnualDilutedEPSInclExtraItems("DD", date(2007, 12, 31)),None)
		
	def testAnnualDividendsPerShare(self):
		""" Test that I find Annual Dividends Per Share"""
		self.assertEquals(Google.getAnnualDividendsPerShare("DD", date(2007, 12, 31)),1.52)
		
	def testAnnualGrossDividends(self):
		""" Test that I find Annual Gross Dividends"""
		self.assertEquals(Google.getAnnualGrossDividends("DD", date(2007, 12, 31)),None)
		
	def testAnnualNetIncomeAfterCompExp(self):
		""" Test that I find Annual Net Income After Comp Exp"""
		self.assertEquals(Google.getAnnualNetIncomeAfterCompExp("DD", date(2007, 12, 31)),None)
		
	def testAnnualBasicEPSAfterCompExp(self):
		""" Test that I find Annual Basic EPS After Comp Exp"""
		self.assertEquals(Google.getAnnualBasicEPSAfterCompExp("DD", date(2007, 12, 31)),None)
		
	def testAnnualDilutedEPSAfterCompExp(self):
		""" Test that I find Annual Diluted EPS After Comp Exp"""
		self.assertEquals(Google.getAnnualDilutedEPSAfterCompExp("DD", date(2007, 12, 31)),None)
		
	def testAnnualDepreciationSupplemental(self):
		""" Test that I find Annual Depreciation Supplemental"""
		self.assertEquals(Google.getAnnualDepreciationSupplemental("DD", date(2007, 12, 31)),None)
		
	def testAnnualTotalSpecialItems(self):
		""" Test that I find Annual Total Special Items"""
		self.assertEquals(Google.getAnnualTotalSpecialItems("DD", date(2007, 12, 31)),None)
		
	def testAnnualNormalizedIncomeBeforeTaxes(self):
		""" Test that I find Annual Normalized Income Before Taxes"""
		self.assertEquals(Google.getAnnualNormalizedIncomeBeforeTaxes("DD", date(2007, 12, 31)),None)																				
		
	def testAnnualEffectsOfSpecialItemsOnIncomeTaxes(self):
		""" Test that I find Annual Effects Of Special Items On Income Taxes"""
		self.assertEquals(Google.getAnnualEffectsOfSpecialItemsOnIncomeTaxes("DD", date(2007, 12, 31)),None)
		
	def testAnnualIncomeTaxesExSpecialItems(self):
		""" Test that I find Annual Income Taxes Ex Special Items"""
		self.assertEquals(Google.getAnnualIncomeTaxesExSpecialItems("DD", date(2007, 12, 31)),None)
		
	def testAnnualNormalizedIncomeAfterTaxes(self):
		""" Test that I find Annual Normalized Income After Taxes"""
		self.assertEquals(Google.getAnnualNormalizedIncomeAfterTaxes("DD", date(2007, 12, 31)),None)
		
	def testAnnualNormalizedIncomeAvailableCommon(self):
		""" Test that I find Annual Normalized Income Available Common"""
		self.assertEquals(Google.getAnnualNormalizedIncomeAvailableCommon("DD", date(2007, 12, 31)),None)								
		
	def testAnnualBasicNormalizedEPS(self):
		""" Test that I find Annual Basic Normalized EPS"""
		self.assertEquals(Google.getAnnualBasicNormalizedEPS("DD", date(2007, 12, 31)),None)
		
	def testAnnualDilutedNormalizedEPS(self):
		""" Test that I find Annual Diluted Normalized EPS"""
		self.assertEquals(Google.getAnnualDilutedNormalizedEPS("DD", date(2007, 12, 31)),3.22)
		
	#income statement quarterly
	def testQuarterlyRevenue(self):
		""" Test that I find Quarterly Revenue"""
		self.assertEquals(Google.getQuarterlyRevenue("DD", date(2008, 3, 31)),8575.00)
											 
	def testQuarterlyOtherRevenue(self):
		""" Test that I find Quarterly Other Revenue""" 
		self.assertEquals(Google.getQuarterlyOtherRevenue("DD", date(2008, 3, 31)),195.00)
										
	def testQuarterlyTotalRevenue(self):
		""" Test that I find Quarterly Total Revenue"""										  
		self.assertEquals(Google.getQuarterlyTotalRevenue("DD", date(2008, 3, 31)),8770.00)
									  
	def testQuarterlyCostOfRevenue(self):
		""" Test that I find Quarterly Cost Of Revenue"""
		self.assertEquals(Google.getQuarterlyCostOfRevenue("DD", date(2008, 3, 31)),5956.00)
									   
	def testQuarterlyGrossProfit(self):
		""" Test that I find Quarterly Gross Profit"""
		self.assertEquals(Google.getQuarterlyGrossProfit("DD", date(2008, 3, 31)),2619.00)
									
	def testQuarterlySGAExpenses(self):
		""" Test that I find Quarterly SGA Expenses"""
		self.assertEquals(Google.getQuarterlySGAExpenses("DD", date(2008, 3, 31)),934.00)
									
	def testQuarterlyResearchAndDevelopment(self):
		""" Test that I find Quarterly Research And Development"""
		self.assertEquals(Google.getQuarterlyResearchAndDevelopment("DD", date(2008, 3, 31)),330.00)
												
	def testQuarterlyDepreciationAmortization(self):
		""" Test that I find Quarterly Depreciation Amortization"""
		self.assertEquals(Google.getQuarterlyDepreciationAmortization("DD", date(2008, 3, 31)),None)
												  
	def testQuarterlyInterestNetOperating(self):
		""" Test that I find Quarterly Interest Net Operating"""
		self.assertEquals(Google.getQuarterlyInterestNetOperating("DD", date(2008, 3, 31)),80.00)
											 
	def testQuarterlyUnusualExpense(self):
		""" Test that I find Quarterly Unusual Expense""" 
		self.assertEquals(Google.getQuarterlyUnusualExpense("DD", date(2008, 3, 31)),0.00)
									   
	def testQuarterlyOtherOperatingExpenses(self):
		""" Test that I find Quarterly Other Operating Expenses"""
		self.assertEquals(Google.getQuarterlyOtherOperatingExpenses("DD", date(2008, 3, 31)),None)
											   
	def testQuarterlyTotalOperatingExpense(self):
		""" Test that I find Quarterly Total Operating Expense"""
		self.assertEquals(Google.getQuarterlyTotalOperatingExpense("DD", date(2008, 3, 31)),7300.00)
											   
	def testQuarterlyOperatingIncome(self):
		""" Test that I find Quarterly Operating Income"""
		self.assertEquals(Google.getQuarterlyOperatingIncome("DD", date(2008, 3, 31)),1470.00)
										 
	def testQuarterlyInterestIncome(self):
		""" Test that I find Quarterly Interest Income"""
		self.assertEquals(Google.getQuarterlyInterestIncome("DD", date(2008, 3, 31)),None)
										
	def testQuarterlyGainOnSaleOfAssets(self):
		""" Test that I find Quarterly Gain On Sale Of Assets"""
		self.assertEquals(Google.getQuarterlyGainOnSaleOfAssets("DD", date(2008, 3, 31)),None)
											
	def testQuarterlyOtherNet(self):
		""" Test that I find Quarterly Other Net"""
		self.assertEquals(Google.getQuarterlyOtherNet("DD", date(2008, 3, 31)),None)
								  
	def testQuarterlyIncomeBeforeTax(self):
		""" Test that I find Quarterly Income Before Tax"""
		self.assertEquals(Google.getQuarterlyIncomeBeforeTax("DD", date(2008, 3, 31)),1470.00)
										 
	def testQuarterlyIncomeAfterTax(self):
		""" Test that I find Quarterly Income After Tax"""
		self.assertEquals(Google.getQuarterlyIncomeAfterTax("DD", date(2008, 3, 31)),1197.00)
										
	def testQuarterlyMinorityInterest_Inc(self):
		""" Test that I find Quarterly Minority Interest(Income Statement)"""
		self.assertEquals(Google.getQuarterlyMinorityInterest_Inc("DD", date(2008, 3, 31)),-6.00)
										  
	def testQuarterlyEquityInAffiliates(self):
		""" Test that I find Quarterly Equity In Affiliates"""
		self.assertEquals(Google.getQuarterlyEquityInAffiliates("DD", date(2008, 3, 31)),None)
											
	def testQuarterlyNetIncomeBeforeExtraItems(self):
		""" Test that I find Quarterly Net Income Before Extra Items"""
		self.assertEquals(Google.getQuarterlyNetIncomeBeforeExtraItems("DD", date(2008, 3, 31)),1191.00)
												   
	def testQuarterlyAccountingChange(self):
		""" Test that I find Quarterly Accounting Change"""
		self.assertEquals(Google.getQuarterlyAccountingChange("DD", date(2008, 3, 31)),None)
										  
	def testQuarterlyDiscontinuedOperations(self):
		""" Test that I find Quarterly Discontinued Operations"""
		self.assertEquals(Google.getQuarterlyDiscontinuedOperations("DD", date(2008, 3, 31)),None)
												
	def testQuarterlyExtraordinaryItem(self):
		""" Test that I find Quarterly Extraordinary Item"""
		self.assertEquals(Google.getQuarterlyExtraordinaryItem("DD", date(2008, 3, 31)),None)
										   
	def testQuarterlyNetIncome(self):
		""" Test that I find Quarterly Net Income"""
		self.assertEquals(Google.getQuarterlyNetIncome("DD", date(2008, 3, 31)),1191.00)
								   
	def testQuarterlyPreferredDividends(self):
		""" Test that I find Quarterly Preferred Dividends"""
		self.assertEquals(Google.getQuarterlyPreferredDividends("DD", date(2008, 3, 31)),None)
											
	def testQuarterlyIncomeAvailToCommonExclExtraItems(self):
		""" Test that I find Quarterly Income Avail To Common Excl Extra Items""" 
		self.assertEquals(Google.getQuarterlyIncomeAvailToCommonExclExtraItems("DD", date(2008, 3, 31)),1188.00)
														   
	def testQuarterlyIncomeAvailToCommonInclExtraItems(self):
		""" Test that I find Quarterly Income Avail To Common Incl Extra Items""" 
		self.assertEquals(Google.getQuarterlyIncomeAvailToCommonInclExtraItems("DD", date(2008, 3, 31)),1188.00)
														   
	def testQuarterlyBasicWeightedAverageShares(self):
		""" Test that I find Quarterly Basic Weighted Average Shares""" 
		self.assertEquals(Google.getQuarterlyBasicWeightedAverageShares("DD", date(2008, 3, 31)),None)
													
	def testQuarterlyBasicEPSExclExtraItems(self):
		""" Test that I find Quarterly Basic EPS Excl Extra Items""" 
		self.assertEquals(Google.getQuarterlyBasicEPSExclExtraItems("DD", date(2008, 3, 31)),None)
												
	def testQuarterlyBasicEPSInclExtraItems(self):
		""" Test that I find Quarterly Basic EPS Incl Extra Items""" 
		self.assertEquals(Google.getQuarterlyBasicEPSInclExtraItems("DD", date(2008, 3, 31)),None)
												
	def testQuarterlyDilutionAdjustment(self):
		""" Test that I find Quarterly Dilution Adjustment"""
		self.assertEquals(Google.getQuarterlyDilutionAdjustment("DD", date(2008, 3, 31)),None)
											
	def testQuarterlyDilutedWeightedAverageShares(self):
		""" Test that I find Quarterly Diluted Weighted Average Shares"""
		self.assertEquals(Google.getQuarterlyDilutedWeightedAverageShares("DD", date(2008, 3, 31)),906.19)
													  
	def testQuarterlyDilutedEPSExclExtraItems(self):
		""" Test that I find Quarterly Diluted EPS Excl Extra Items""" 
		self.assertEquals(Google.getQuarterlyDilutedEPSExclExtraItems("DD", date(2008, 3, 31)),1.31)
												  
	def testQuarterlyDilutedEPSInclExtraItems(self):
		""" Test that I find Quarterly Diluted EPS Incl Extra Items""" 
		self.assertEquals(Google.getQuarterlyDilutedEPSInclExtraItems("DD", date(2008, 3, 31)),None)
												  
	def testQuarterlyDividendsPerShare(self):
		""" Test that I find Quarterly Dividends Per Share""" 
		self.assertEquals(Google.getQuarterlyDividendsPerShare("DD", date(2008, 3, 31)),0.41)
										   
	def testQuarterlyGrossDividends(self):
		""" Test that I find Quarterly Gross Dividends""" 
		self.assertEquals(Google.getQuarterlyGrossDividends("DD", date(2008, 3, 31)),None)
										
	def testQuarterlyNetIncomeAfterCompExp(self):
		""" Test that I find Quarterly Net Income After Comp Exp"""
		self.assertEquals(Google.getQuarterlyNetIncomeAfterCompExp("DD", date(2008, 3, 31)),None)
											   
	def testQuarterlyBasicEPSAfterCompExp(self):
		""" Test that I find Quarterly Basic EPS After Comp Exp"""
		self.assertEquals(Google.getQuarterlyBasicEPSAfterCompExp("DD", date(2008, 3, 31)),None)
											  
	def testQuarterlyDilutedEPSAfterCompExp(self):
		""" Test that I find Quarterly Diluted EPS After Comp Exp"""
		self.assertEquals(Google.getQuarterlyDilutedEPSAfterCompExp("DD", date(2008, 3, 31)),None)
												
	def testQuarterlyDepreciationSupplemental(self):
		""" Test that I find Quarterly Depreciation Supplemental""" 
		self.assertEquals(Google.getQuarterlyDepreciationSupplemental("DD", date(2008, 3, 31)),None)
												  
	def testQuarterlyTotalSpecialItems(self):
		""" Test that I find Quarterly Total Special Items""" 
		self.assertEquals(Google.getQuarterlyTotalSpecialItems("DD", date(2008, 3, 31)),None)
										   
	def testQuarterlyNormalizedIncomeBeforeTaxes(self):
		""" Test that I find Quarterly Normalized Income Before Taxes""" 
		self.assertEquals(Google.getQuarterlyNormalizedIncomeBeforeTaxes("DD", date(2008, 3, 31)),None)
													 
	def testQuarterlyEffectsOfSpecialItemsOnIncomeTaxes(self):
		""" Test that I find Quarterly EffectsOf Special Items On Income Taxes"""
		self.assertEquals(Google.getQuarterlyEffectsOfSpecialItemsOnIncomeTaxes("DD", date(2008, 3, 31)),None)
															
	def testQuarterlyIncomeTaxesExSpecialItems(self):
		""" Test that I find Quarterly Income Taxes Ex Special Items""" 
		self.assertEquals(Google.getQuarterlyIncomeTaxesExSpecialItems("DD", date(2008, 3, 31)),None)
												   
	def testQuarterlyNormalizedIncomeAfterTaxes(self):
		""" Test that I find Quarterly Normalized Income After Taxes"""
		self.assertEquals(Google.getQuarterlyNormalizedIncomeAfterTaxes("DD", date(2008, 3, 31)),None)
													
	def testQuarterlyNormalizedIncomeAvailableCommon(self):
		""" Test that I find Quarterly Normalized Income Available Common"""
		self.assertEquals(Google.getQuarterlyNormalizedIncomeAvailableCommon("DD", date(2008, 3, 31)),None)
														 
	def testQuarterlyBasicNormalizedEPS(self):
		""" Test that I find Quarterly Basic Normalized EPS"""
		self.assertEquals(Google.getQuarterlyBasicNormalizedEPS("DD", date(2008, 3, 31)),None)
											
	def testQuarterlyDilutedNormalizedEPS(self):
		""" Test that I find Quarterly Diluted Normalized EPS""" 
		self.assertEquals(Google.getQuarterlyDilutedNormalizedEPS("DD", date(2008, 3, 31)),1.31)
		
		
	#test balance sheet information
	def testAnnualCashAndEquivalents(self):
		""" Test that I find Annual Cash And Equivalents"""
		self.assertEquals(Google.getAnnualCashAndEquivalents("DD", date(2007, 12, 31)),1305.00)
		
	def testAnnualShortTermInvestments(self):
		""" Test that I find Annual Short Term Investments"""
		self.assertEquals(Google.getAnnualShortTermInvestments("DD", date(2007, 12, 31)),131.00)
		
	def testAnnualCashAndShortTermInvestments(self):
		""" Test that I find Annual Cash And Short Term Investments"""
		self.assertEquals(Google.getAnnualCashAndShortTermInvestments("DD", date(2007, 12, 31)),1436.00)
		
	def testAnnualAccountsReceivableTrade(self):
		""" Test that I find Annual Accounts Receivable Trade"""
		self.assertEquals(Google.getAnnualAccountsReceivableTrade("DD", date(2007, 12, 31)),4649.00)
		
	def testAnnualReceivablesOther(self):
		""" Test that I find Annual Receivables Other"""
		self.assertEquals(Google.getAnnualReceivablesOther("DD", date(2007, 12, 31)),None)
		
	def testAnnualTotalReceivablesNet(self):
		""" Test that I find Annual Total Receivables Net"""
		self.assertEquals(Google.getAnnualTotalReceivablesNet("DD", date(2007, 12, 31)),5683.00)														
		
	def testAnnualTotalInventory(self):
		""" Test that I find Annual Total Inventory"""
		self.assertEquals(Google.getAnnualTotalInventory("DD", date(2007, 12, 31)),5278.00)
		
	def testAnnualPrepaidExpenses(self):
		""" Test that I find Annual Prepaid Expenses"""
		self.assertEquals(Google.getAnnualPrepaidExpenses("DD", date(2007, 12, 31)),199.00)
		
	def testAnnualOtherCurrentAssetsTotal(self):
		""" Test that I find Annual OtherCurrent Assets Total"""
		self.assertEquals(Google.getAnnualOtherCurrentAssetsTotal("DD", date(2007, 12, 31)),564.00)
		
	def testAnnualTotalCurrentAssets(self):
		""" Test that I find Annual Total Current Assets"""
		self.assertEquals(Google.getAnnualTotalCurrentAssets("DD", date(2007, 12, 31)),13160.00)
		
	def testAnnualPPE(self):
		""" Test that I find Annual PPE"""
		self.assertEquals(Google.getAnnualPPE("DD", date(2007, 12, 31)),26593.00)										
		
	def testAnnualGoodwill(self):
		""" Test that I find Annual Goodwill"""
		self.assertEquals(Google.getAnnualGoodwill("DD", date(2007, 12, 31)),2074.00)
		
	def testAnnualIntangibles(self):
		""" Test that I find Annual Intangibles"""
		self.assertEquals(Google.getAnnualIntangibles("DD", date(2007, 12, 31)),2856.00)
		
	def testAnnualLongTermInvestments(self):
		""" Test that I find Annual Long Term Investments"""
		self.assertEquals(Google.getAnnualLongTermInvestments("DD", date(2007, 12, 31)),908.00)
		
	def testAnnualOtherLongTermAssets(self):
		""" Test that I find Annual Other Long Term Assets"""
		self.assertEquals(Google.getAnnualOtherLongTermAssets("DD", date(2007, 12, 31)),4273.00)
		
	def testAnnualTotalAssets(self):
		""" Test that I find Annual Total Assets"""
		self.assertEquals(Google.getAnnualTotalAssets("DD", date(2007, 12, 31)),34131.00)
		
	def testAnnualAccountsPayable(self):
		""" Test that I find Annual Accounts Payable"""
		self.assertEquals(Google.getAnnualAccountsPayable("DD", date(2007, 12, 31)),3172.00)
		
	def testAnnualAccruedExpenses(self):
		""" Test that I find Annual Accrued Expenses"""
		self.assertEquals(Google.getAnnualAccruedExpenses("DD", date(2007, 12, 31)),2842.00)
		
	def testAnnualNotesPayable(self):
		""" Test that I find Annual Notes Payable"""
		self.assertEquals(Google.getAnnualNotesPayable("DD", date(2007, 12, 31)),1349.00)
		
	def testAnnualCurrentPortLTDebtToCapital(self):
		""" Test that I find Annual Current Port LT Debt To Capital"""
		self.assertEquals(Google.getAnnualCurrentPortLTDebtToCapital("DD", date(2007, 12, 31)),21.00)										
		
	def testAnnualOtherCurrentLiabilities(self):
		""" Test that I find Annual Other Current Liabilities"""
		self.assertEquals(Google.getAnnualOtherCurrentLiabilities("DD", date(2007, 12, 31)),1157.00)
		 
	def testAnnualTotalCurrentLiabilities(self):
		""" Test that I find Annual Total Current Liabilities""" 
		self.assertEquals(Google.getAnnualTotalCurrentLiabilities("DD", date(2007, 12, 31)),8541.00)
		 
	def testAnnualLongTermDebt(self):
		""" Test that I find Annual Long Term Debt""" 
		self.assertEquals(Google.getAnnualLongTermDebt("DD", date(2007, 12, 31)),5945.00)
		 
	def testAnnualCapitalLeaseObligations(self):
		""" Test that I find Annual Capital Lease Obligations""" 
		self.assertEquals(Google.getAnnualCapitalLeaseObligations("DD", date(2007, 12, 31)),10.0)
		 
	def testAnnualTotalLongTermDebt(self):
		""" Test that I find Annual Total Long Term Debt""" 
		self.assertEquals(Google.getAnnualTotalLongTermDebt("DD", date(2007, 12, 31)),5955.00)
		 
	def testAnnualTotalDebt(self):
		""" Test that I find Annual Total Debt""" 
		self.assertEquals(Google.getAnnualTotalDebt("DD", date(2007, 12, 31)),7325.00)
		 
	def testAnnualDeferredIncomeTax(self):
		""" Test that I find Annual Deferred Income Tax""" 
		self.assertEquals(Google.getAnnualDeferredIncomeTax("DD", date(2007, 12, 31)),802.00)
		 
	def testAnnualMinorityInterest_Bal(self):
		""" Test that I find Annual Minority Interes(Balance Sheet)""" 
		self.assertEquals(Google.getAnnualMinorityInterest_Bal("DD", date(2007, 12, 31)),442.00)
		 
	def testAnnualOtherLiabilities(self):
		""" Test that I find Annual Other Liabilities""" 
		self.assertEquals(Google.getAnnualOtherLiabilities("DD", date(2007, 12, 31)),7255.00)
		 
	def testAnnualTotalLiabilities(self):
		""" Test that I find Annual TotalLiabilities""" 
		self.assertEquals(Google.getAnnualTotalLiabilities("DD", date(2007, 12, 31)),22995.00)
		 
	def testAnnualRedeemablePreferredStock(self):
		""" Test that I find Annual Redeemable Preferred Stock""" 
		self.assertEquals(Google.getAnnualRedeemablePreferredStock("DD", date(2007, 12, 31)),None)
		 
	def testAnnualPreferredStockNonRedeemable(self):
		""" Test that I find Annual Preferred Stock Non Redeemable""" 
		self.assertEquals(Google.getAnnualPreferredStockNonRedeemable("DD", date(2007, 12, 31)),237.00)
		 
	def testAnnualCommonStock(self):
		""" Test that I find Annual Common Stock""" 
		self.assertEquals(Google.getAnnualCommonStock("DD", date(2007, 12, 31)),296.00)
		 
	def testAnnualAdditionalPaidInCapital(self):
		""" Test that I find Annual Additional Paid In Capital""" 
		self.assertEquals(Google.getAnnualAdditionalPaidInCapital("DD", date(2007, 12, 31)),8179.00)
		 
	def testAnnualRetainedEarnings(self):
		""" Test that I find Annual Retained Earnings""" 
		self.assertEquals(Google.getAnnualRetainedEarnings("DD", date(2007, 12, 31)),9945.00)
		 
	def testAnnualTreasuryStock(self):
		""" Test that I find Annual Treasury Stock"""
		self.assertEquals(Google.getAnnualTreasuryStock("DD", date(2007, 12, 31)),-6727.00)
		 
	def testAnnualOtherEquity(self):
		""" Test that I find Annual Other Equity""" 
		self.assertEquals(Google.getAnnualOtherEquity("DD", date(2007, 12, 31)),-794.00)
		 
	def testAnnualTotalEquity(self):
		""" Test that I find Annual Total Equity"""
		self.assertEquals(Google.getAnnualTotalEquity("DD", date(2007, 12, 31)),11136.00)
		 
	def testAnnualTotalLiabilitiesAndShareholdersEquity(self):
		""" Test that I find Annual Total Liabilities And Shareholders Equity""" 
		self.assertEquals(Google.getAnnualTotalLiabilitiesAndShareholdersEquity("DD", date(2007, 12, 31)),34131.00)
		 
	def testAnnualSharesOuts(self):
		""" Test that I find Annual Shares Outs""" 
		self.assertEquals(Google.getAnnualSharesOuts("DD", date(2007, 12, 31)),None) 
		
	def testAnnualTotalCommonSharesOutstanding(self):
		""" Test that I find Annual Total Common Shares Outstanding""" 
		self.assertEquals(Google.getAnnualTotalCommonSharesOutstanding("DD", date(2007, 12, 31)),899.29)
 
 
 
		#quarterly balance sheet
 	def testQuarterlyCashAndEquivalents(self):
		""" Test that I find Quarterly Cash And Equivalents"""
		self.assertEquals(Google.getQuarterlyCashAndEquivalents("DD", date(2008, 3, 31)),1094.00)
											
	def testQuarterlyShortTermInvestments(self):
		""" Test that I find Quarterly Short Term Investments""" 
		self.assertEquals(Google.getQuarterlyShortTermInvestments("DD", date(2008, 3, 31)),33.00)
											  
	def testQuarterlyCashAndShortTermInvestments(self):
		""" Test that I find Quarterly Cash And Short Term Investments""" 
		self.assertEquals(Google.getQuarterlyCashAndShortTermInvestments("DD", date(2008, 3, 31)),1127.00)
													 
	def testQuarterlyAccountsReceivableTrade(self):
		""" Test that I find Quarterly Accounts Receivable Trade"""
		self.assertEquals(Google.getQuarterlyAccountsReceivableTrade("DD", date(2008, 3, 31)),7645.00)
												
	def testQuarterlyReceivablesOther(self):
		""" Test that I find Quarterly Receivables Other"""
		self.assertEquals(Google.getQuarterlyReceivablesOther("DD", date(2008, 3, 31)),None)
										  
	def testQuarterlyTotalReceivablesNet(self):
		""" Test that I find Quarterly Total Receivables Net""" 
		self.assertEquals(Google.getQuarterlyTotalReceivablesNet("DD", date(2008, 3, 31)),7645.00)
											 
	def testQuarterlyTotalInventory(self):
		""" Test that I find Quarterly Total Inventory"""
		self.assertEquals(Google.getQuarterlyTotalInventory("DD", date(2008, 3, 31)),5310.00)
										
	def testQuarterlyPrepaidExpenses(self):
		""" Test that I find Quarterly Prepaid Expenses""" 
		self.assertEquals(Google.getQuarterlyPrepaidExpenses("DD", date(2008, 3, 31)),212.00)
										 
	def testQuarterlyOtherCurrentAssetsTotal(self):
		""" Test that I find Quarterly Other Current Assets Total"""
		self.assertEquals(Google.getQuarterlyOtherCurrentAssetsTotal("DD", date(2008, 3, 31)),567.00)
												 
	def testQuarterlyTotalCurrentAssets(self):
		""" Test that I find Quarterly Total Current Assets"""
		self.assertEquals(Google.getQuarterlyTotalCurrentAssets("DD", date(2008, 3, 31)),14861.00)
											
	def testQuarterlyPPE(self):
		""" Test that I find Quarterly PPE"""
		self.assertEquals(Google.getQuarterlyPPE("DD", date(2008, 3, 31)),26941.00)
							 
	def testQuarterlyGoodwill(self):
		""" Test that I find Quarterly Goodwill"""
		self.assertEquals(Google.getQuarterlyGoodwill("DD", date(2008, 3, 31)),2074.00)
								  
	def testQuarterlyIntangibles(self):
		""" Test that I find Quarterly Intangibles"""
		self.assertEquals(Google.getQuarterlyIntangibles("DD", date(2008, 3, 31)),2781.00)
									 
	def testQuarterlyLongTermInvestments(self):
		""" Test that I find Quarterly Long Term Investments"""
		self.assertEquals(Google.getQuarterlyLongTermInvestments("DD", date(2008, 3, 31)),818.00)
											 
	def testQuarterlyOtherLongTermAssets(self):
		""" Test that I find Quarterly Other Long Term Assets"""
		self.assertEquals(Google.getQuarterlyOtherLongTermAssets("DD", date(2008, 3, 31)),4789.00)
											
	def testQuarterlyTotalAssets(self):
		""" Test that I find Quarterly Total Assets"""
		self.assertEquals(Google.getQuarterlyTotalAssets("DD", date(2008, 3, 31)),36228.00)
									 
	def testQuarterlyAccountsPayable(self):
		""" Test that I find Quarterly Accounts Payable""" 
		self.assertEquals(Google.getQuarterlyAccountsPayable("DD", date(2008, 3, 31)),3061.00)
										 
	def testQuarterlyAccruedExpenses(self):
		""" Test that I find Quarterly Accrued Expenses"""
		self.assertEquals(Google.getQuarterlyAccruedExpenses("DD", date(2008, 3, 31)),3360.00)
										 
	def testQuarterlyNotesPayable(self):
		""" Test that I find Quarterly Notes Payable"""
		self.assertEquals(Google.getQuarterlyNotesPayable("DD", date(2008, 3, 31)),3196.00)
									  
	def testQuarterlyCurrentPortLTDebtToCapital(self):
		""" Test that I find Quarterly Current Port LT Debt To Capital"""
		self.assertEquals(Google.getQuarterlyCurrentPortLTDebtToCapital("DD", date(2008, 3, 31)),None)
													
	def testQuarterlyOtherCurrentLiabilities(self):
		""" Test that I find Quarterly Other Current Liabilities"""
		self.assertEquals(Google.getQuarterlyOtherCurrentLiabilities("DD", date(2008, 3, 31)),177.00)
												 
	def testQuarterlyTotalCurrentLiabilities(self):
		""" Test that I find Quarterly Total Current Liabilities"""
		self.assertEquals(Google.getQuarterlyTotalCurrentLiabilities("DD", date(2008, 3, 31)),9794.00)
												 
	def testQuarterlyLongTermDebt(self):
		""" Test that I find Quarterly Long Term Debt"""
		self.assertEquals(Google.getQuarterlyLongTermDebt("DD", date(2008, 3, 31)),5784.00)
									  
	def testQuarterlyCapitalLeaseObligations(self):
		""" Test that I find Quarterly Capital Lease Obligations"""
		self.assertEquals(Google.getQuarterlyCapitalLeaseObligations("DD", date(2008, 3, 31)),None)
												 
	def testQuarterlyTotalLongTermDebt(self):
		""" Test that I find Quarterly Total Long Term Debt"""
		self.assertEquals(Google.getQuarterlyTotalLongTermDebt("DD", date(2008, 3, 31)),5784.00)
										   
	def testQuarterlyTotalDebt(self):
		""" Test that I find Quarterly Total Debt"""
		self.assertEquals(Google.getQuarterlyTotalDebt("DD", date(2008, 3, 31)),8980.00)
								   
	def testQuarterlyDeferredIncomeTax(self):
		""" Test that I find Quarterly Deferred Income Tax"""
		self.assertEquals(Google.getQuarterlyDeferredIncomeTax("DD", date(2008, 3, 31)),894.00)
										   
	def testQuarterlyMinorityInterest_Bal(self):
		""" Test that I find Quarterly Minority Interest(Balance Sheet)"""
		self.assertEquals(Google.getQuarterlyMinorityInterest_Bal("DD", date(2008, 3, 31)),443.00)
										  
	def testQuarterlyOtherLiabilities(self):
		""" Test that I find Quarterly Other Liabilities"""
		self.assertEquals(Google.getQuarterlyOtherLiabilities("DD", date(2008, 3, 31)),7191.00)
										  
	def testQuarterlyTotalLiabilities(self):
		""" Test that I find Quarterly Total Liabilities"""
		self.assertEquals(Google.getQuarterlyTotalLiabilities("DD", date(2008, 3, 31)),24106.00)
										  
	def testQuarterlyRedeemablePreferredStock(self):
		""" Test that I find Quarterly Redeemable Preferred Stock"""
		self.assertEquals(Google.getQuarterlyRedeemablePreferredStock("DD", date(2008, 3, 31)),None)
												  
	def testQuarterlyPreferredStockNonRedeemable(self):
		""" Test that I find Quarterly Preferred Stock Non Redeemable"""
		self.assertEquals(Google.getQuarterlyPreferredStockNonRedeemable("DD", date(2008, 3, 31)),237.00)
													 
	def testQuarterlyCommonStock(self):
		""" Test that I find Quarterly Common Stock"""
		self.assertEquals(Google.getQuarterlyCommonStock("DD", date(2008, 3, 31)),296.00)
									 
	def testQuarterlyAdditionalPaidInCapital(self):
		""" Test that I find Quarterly Additional Paid In Capital"""
		self.assertEquals(Google.getQuarterlyAdditionalPaidInCapital("DD", date(2008, 3, 31)),8220.00)
												 
	def testQuarterlyRetainedEarnings(self):
		""" Test that I find Quarterly Retained Earnings"""
		self.assertEquals(Google.getQuarterlyRetainedEarnings("DD", date(2008, 3, 31)),10764.00)
										  
	def testQuarterlyTreasuryStock(self):
		""" Test that I find Quarterly Treasury Stock"""
		self.assertEquals(Google.getQuarterlyTreasuryStock("DD", date(2008, 3, 31)),-6727.00)
									   
	def testQuarterlyOtherEquity(self):
		""" Test that I find Quarterly Other Equity"""
		self.assertEquals(Google.getQuarterlyOtherEquity("DD", date(2008, 3, 31)),-668.00)
									 
	def testQuarterlyTotalEquity(self):
		""" Test that I find Quarterly Total Equity"""
		self.assertEquals(Google.getQuarterlyTotalEquity("DD", date(2008, 3, 31)),12122.00)
									 
	def testQuarterlyTotalLiabilitiesAndShareholdersEquity(self):
		""" Test that I find Quarterly Total Liabilities And Shareholders Equity"""
		self.assertEquals(Google.getQuarterlyTotalLiabilitiesAndShareholdersEquity("DD", date(2008, 3, 31)),36228.00)
															   
	def testQuarterlySharesOuts(self):
		""" Test that I find Quarterly Shares Outs"""
		self.assertEquals(Google.getQuarterlySharesOuts("DD", date(2008, 3, 31)),None)
									
	def testQuarterlyTotalCommonSharesOutstanding(self):
		""" Test that I find Quarterly Total Common Shares Outstanding"""
		self.assertEquals(Google.getQuarterlyTotalCommonSharesOutstanding("DD", date(2008, 3, 31)),900.52)
		
	#test annual cash flows information
	def testAnnualNetIncomeStartingLine(self):
		""" Test that I find Annual Net Income or Starting Line"""
		self.assertEquals(Google.getAnnualNetIncomeStartingLine("DD", date(2007, 12, 31)),2988.00)
		
	def testAnnualDepreciationDepletion(self):
		""" Test that I find Annual Depreciation Depletion"""  
		self.assertEquals(Google.getAnnualDepreciationDepletion("DD", date(2007, 12, 31)),1158.00)
		
	def testAnnualAmortization(self):
		""" Test that I find Annual Amortization"""  
		self.assertEquals(Google.getAnnualAmortization("DD", date(2007, 12, 31)),213.00)
		 
	def testAnnualDeferredTaxes(self):
		""" Test that I find Annual Deferred Taxes"""
		self.assertEquals(Google.getAnnualDeferredTaxes("DD", date(2007, 12, 31)),-1.00)
		 
	def testAnnualNonCashItems(self):
		""" Test that I find Annual Non Cash Items"""
		self.assertEquals(Google.getAnnualNonCashItems("DD", date(2007, 12, 31)),88.00)
		 
	def testAnnualChangesInWorkingCapital(self):
		""" Test that I find Annual Changes In Working Capital"""
		self.assertEquals(Google.getAnnualChangesInWorkingCapital("DD", date(2007, 12, 31)),-156.00)
		 
	def testAnnualCashFromOperatingActivities(self):
		""" Test that I find Annual Cash From Operating Activities"""
		self.assertEquals(Google.getAnnualCashFromOperatingActivities("DD", date(2007, 12, 31)),4290.00)
		
	def testAnnualCapitalExpenditures(self):
		""" Test that I find Annual Capital Expenditures"""
		self.assertEquals(Google.getAnnualCapitalExpenditures("DD", date(2007, 12, 31)),-1585.00)
		 
	def testAnnualOtherInvestingCashFlow(self):
		""" Test that I find Annual Other Investing Cash Flow"""
		self.assertEquals(Google.getAnnualOtherInvestingCashFlow("DD", date(2007, 12, 31)),-165.00)
		 
	def testAnnualCashFromInvestingActivities(self):
		""" Test that I find Annual Cash From Investing Activities"""
		self.assertEquals(Google.getAnnualCashFromInvestingActivities("DD", date(2007, 12, 31)),-1750.00)
		 
	def testAnnualFinancingCashFlowItems(self):
		""" Test that I find Annual Financing Cash Flow Items"""
		self.assertEquals(Google.getAnnualFinancingCashFlowItems("DD", date(2007, 12, 31)),-67.00)
		 
	def testAnnualTotalCashDividendsPaid(self):
		""" Test that I find Annual Total Cash Dividends Paid"""
		self.assertEquals(Google.getAnnualTotalCashDividendsPaid("DD", date(2007, 12, 31)),-1409.00)
		 
	def testAnnualIssuanceOfStock(self):
		""" Test that I find Annual Issuance Of Stock"""
		self.assertEquals(Google.getAnnualIssuanceOfStock("DD", date(2007, 12, 31)),-1250.00)
		 
	def testAnnualIssuanceOfDebt(self):
		""" Test that I find Annual Issuance Of Debt"""
		self.assertEquals(Google.getAnnualIssuanceOfDebt("DD", date(2007, 12, 31)),-343.00)
		 
	def testAnnualCashFromFinancingActivities(self):
		""" Test that I find Annual Cash From Financing Activities"""
		self.assertEquals(Google.getAnnualCashFromFinancingActivities("DD", date(2007, 12, 31)),-3069.00)
		 
	def testAnnualForeignExchangeEffects(self):
		""" Test that I find Annual Foreign Exchange Effects"""
		self.assertEquals(Google.getAnnualForeignExchangeEffects("DD", date(2007, 12, 31)),20.00)
		 
	def testAnnualNetChangeInCash(self):
		""" Test that I find Annual Net Change In Cash"""
		self.assertEquals(Google.getAnnualNetChangeInCash("DD", date(2007, 12, 31)),-509.00)
		 
	def testAnnualCashInterestPaid(self):
		""" Test that I find Annual Cash Interest Paid"""
		self.assertEquals(Google.getAnnualCashInterestPaid("DD", date(2007, 12, 31)),527.00)
		 
	def testAnnualCashTaxesPaid(self):
		""" Test that I find Annual Cash Taxes Paid"""
		self.assertEquals(Google.getAnnualCashTaxesPaid("DD", date(2007, 12, 31)),795.00)

		#quarterly cash flow
		
	def testQuarterlyNetIncomeStartingLine(self):
		""" Test that I find Quarterly Net Income or Starting Line"""
		self.assertEquals(Google.getQuarterlyNetIncomeStartingLine("DD", date(2008, 3, 31)),1191.00)
											  
											  
	def testQuarterlyDepreciationDepletion(self):
		""" Test that I find Quarterly Depreciation Depletion"""
		self.assertEquals(Google.getQuarterlyDepreciationDepletion("DD", date(2008, 3, 31)),287.0)
											  
											  
	def testQuarterlyAmortization(self):
		""" Test that I find Quarterly Amortization""" 
		self.assertEquals(Google.getQuarterlyAmortization("DD", date(2008, 3, 31)),93.00)
									 
									  
	def testQuarterlyDeferredTaxes(self):
		""" Test that I find Quarterly Deferred Taxes"""
		self.assertEquals(Google.getQuarterlyDeferredTaxes("DD", date(2008, 3, 31)),None)
									  
									   
	def testQuarterlyNonCashItems(self):
		""" Test that I find Quarterly Non Cash Items"""
		self.assertEquals(Google.getQuarterlyNonCashItems("DD", date(2008, 3, 31)),-9.00)
									 
									  
	def testQuarterlyChangesInWorkingCapital(self):
		""" Test that I find Quarterly Changes In Working Capital"""
		self.assertEquals(Google.getQuarterlyChangesInWorkingCapital("DD", date(2008, 3, 31)),-2513.00)
												
												 
	def testQuarterlyCashFromOperatingActivities(self):
		""" Test that I find Quarterly Cash From Operating Activities"""
		self.assertEquals(Google.getQuarterlyCashFromOperatingActivities("DD", date(2008, 3, 31)),-951.00)
													
													
	def testQuarterlyCapitalExpenditures(self):
		""" Test that I find Quarterly Capital Expenditures"""
		self.assertEquals(Google.getQuarterlyCapitalExpenditures("DD", date(2008, 3, 31)),-410.00)
											
											 
	def testQuarterlyOtherInvestingCashFlow(self):
		""" Test that I find Quarterly Other Investing Cash Flow"""
		self.assertEquals(Google.getQuarterlyOtherInvestingCashFlow("DD", date(2008, 3, 31)),-110.00)
											   
												
	def testQuarterlyCashFromInvestingActivities(self):
		""" Test that I find Quarterly Cash From Investing Activities"""
		self.assertEquals(Google.getQuarterlyCashFromInvestingActivities("DD", date(2008, 3, 31)),-520.00)
													
													 
	def testQuarterlyFinancingCashFlowItems(self):
		""" Test that I find Quarterly Financing Cash Flow Items"""
		self.assertEquals(Google.getQuarterlyFinancingCashFlowItems("DD", date(2008, 3, 31)),4.00)
											   
												
	def testQuarterlyTotalCashDividendsPaid(self):
		""" Test that I find Quarterly Total Cash Dividends Paid"""
		self.assertEquals(Google.getQuarterlyTotalCashDividendsPaid("DD", date(2008, 3, 31)),-372.00)
											   
												
	def testQuarterlyIssuanceOfStock(self):
		""" Test that I find Quarterly Issuance Of Stock"""
		self.assertEquals(Google.getQuarterlyIssuanceOfStock("DD", date(2008, 3, 31)),19.00)
										
										 
	def testQuarterlyIssuanceOfDebt(self):
		""" Test that I find Quarterly Issuance Of Debt"""
		self.assertEquals(Google.getQuarterlyIssuanceOfDebt("DD", date(2008, 3, 31)),1611.00)
									   
										
	def testQuarterlyCashFromFinancingActivities(self):
		""" Test that I find Quarterly Cash From Financing Activities"""
		self.assertEquals(Google.getQuarterlyCashFromFinancingActivities("DD", date(2008, 3, 31)),1262.00)
													
													 
	def testQuarterlyForeignExchangeEffects(self):
		""" Test that I find Quarterly Foreign Exchange Effects"""
		self.assertEquals(Google.getQuarterlyForeignExchangeEffects("DD", date(2008, 3, 31)),-2.00)
											   
												
	def testQuarterlyNetChangeInCash(self):
		""" Test that I find Quarterly Net Change In Cash"""
		self.assertEquals(Google.getQuarterlyNetChangeInCash("DD", date(2008, 3, 31)),-211.00)
										
										 
	def testQuarterlyCashInterestPaid(self):
		""" Test that I find Quarterly Cash Interest Paid"""
		self.assertEquals(Google.getQuarterlyCashInterestPaid("DD", date(2008, 3, 31)),None)
										 
										  
	def testQuarterlyCashTaxesPaid(self):
		""" Test that I find Quarterly Cash Taxes Paid"""
		self.assertEquals(Google.getQuarterlyCashTaxesPaid("DD", date(2008, 3, 31)),None)
 
 
if __name__ == "__main__": #for coverage tests
	unittest.main()
	unittest.TestLoader
									   
