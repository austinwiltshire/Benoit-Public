import Website
from TestTools import assertClose, compareDicts
from datetime import date
import doctest
import contract
import unittest

contract.checkmod(Website)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Website))

class WebsiteTestCase(unittest.TestCase):
    def setUp(self):
        self.google = Website.Google()
        
    def tearDown(self):
        del self.google
        self.google = None
        
class SoupFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = Website.Google.SoupFactory()
        self.meta = Website.Google.Metadata
        self.sec = Website.Google.SECData
        
    def tearDown(self):
        del self.factory
        del self.meta
        del self.sec
        self.factory = None
        self.meta = None
        self.sec = None
        
    def testBasicSoup(self):
    	""" Test that I can build/see stuff from a basicSoup """
    	metasoup = self.meta(self.factory.buildBasicSoup("MMM"), self.factory)
    	self.assertEqual(metasoup.getIndustry(), u"Conglomerates")
    	self.assertEqual(metasoup.getCurrencyReported(), u"USD")
    	self.assertEqual(metasoup.getExchange(), u"NYSE")
    	
    def testMetaSoup(self):
    	""" Test that I can build and see stuff from a MetaSoup """
    	metasoup = self.meta(self.factory.buildMetaSoup("XRAY"), self.factory)
    	competitors = set(metasoup.getCompetitors())
    	self.assertEqual(competitors, set([u"YDNT",u"ALGN",u"BLTI",u"MLSS",u"PDEX",u"NADX",u"SIRO",u"BSML",u"IART",u"MMM"]))
    	self.assertEqual(metasoup.getSector(), u"Healthcare")
    	self.assertEqual(metasoup.getProperName(), u"DENTSPLY International Inc.")
    	
    def testSECSoup(self):
    	""" Test that I can build and see things from an SEC soup """
    	secsoup = self.sec(self.factory.buildSECSoup("YDNT"))
    	self.assertEqual(secsoup.getQuarterlyRevenue()[date(2007,12,31)], 25.04)
    	self.assertEqual(secsoup.getQuarterlyTotalCurrentAssets()[date(2007,12,31)], 32.86)
    	self.assertEqual(secsoup.getQuarterlyCashFromOperatingActivities()[date(2007,12,31)], 3.77)
    	
    def testIsSECSoupTrue(self):
    	""" Test that I can detect an SEC soup """
    	secsoup = self.factory.buildBasicSoup("YDNT")
    	self.assertTrue(self.factory._isSECSoup(secsoup))
    
    def testIsSECSoupFalse(self):
    	""" Test that I can detect an SEC soup when I don't have one """
    	secsoup = self.factory.buildBasicSoup("NTDOY")
    	self.assertFalse(self.factory._isSECSoup(secsoup))
    	
    def testIsBasicSoupTrue(self):
    	""" Test that I can detect a Basic Soup """
    	basicsoup = self.factory.buildBasicSoup("IRBT")
    	self.assertTrue(self.factory._isBasicSoup(basicsoup))
        
	def testIsBasicSoupFalse(self):
		""" Test that I can detect a basic soup when I don't have one """
		basicsoup = self.factory.buildBasicSoup("FARX")
		self.assertFalse(self.factory._isBasicSoup(basicsoup))
    
    def testIsMetaSoupTrue(self):
    	""" Test that I can detect a meta soup """
    	metasoup = self.factory.buildBasicSoup("GOOG")
    	self.assertTrue(self.factory._isMetaSoup(metasoup))
    	
    def testIsMetaSoupFalse(self):
    	""" Test that I can detect a meta soup when I don't have one """
    	metasoup = self.factory.buildBasicSoup("CSCA")
    	self.assertFalse(self.factory._isMetaSoup(metasoup))        
        
class WebsiteTestCase_FailureTests(WebsiteTestCase):
	""" None of these should pass! """
	def testNonNegativeNumbers(self):
		""" Make sure I'm not mixing up negatives, this should fail """
		self.assertNotEqual(self.google.getAnnualCashFromInvestingActivities("BRK.B"), {date(2007,12,31):-13428.0,\
                                                                    date(2006,12,31):14077.0,\
                                                                    date(2005,12,31):-13841.0,\
                                                                    date(2004,12,31):315.0,\
                                                                    date(2003,12,31):16029.0,\
                                                                    date(2002,12,31):-1311.0})
	
	def testBigNumbers(self):
		""" Make sure I don't loose precision with big numbers, this should fail """
		self.assertNotEqual(self.google.getAnnualTotalAssets("IBN"), {date(2007,3,31):3943347.0,\
                                                   date(2006,3,31):2772295.1,\
                                                   date(2005,3,31):1784337.0,\
                                                   date(2004,3,31):1409131.0,\
                                                   date(2003,3,31):1180263.0,\
                                                   date(2002,3,31):743362.0})
	
	def testZeroes(self):
		""" Make sure numbers that shouldn't be zero fail """
		self.assertNotEqual(self.google.getQuarterlyDividendsPerShare("IRBT"), {date(2007,12,29):-0.06,\
                                                     date(2007,9,29):0.0,\
                                                     date(2007,6,30):0.0,\
                                                     date(2007,3,31):0.0,\
                                                     date(2006,12,30):0.0})
		
	def testTinyNumbers(self):
		""" Make sure numbers near zero that are wrong fail """
		self.assertNotEqual(self.google.getQuarterlyDilutedNormalizedEPS('S'), {date(2007,12,31):-3.55,\
                                                     date(2007,9,30):0.5,\
                                                     date(2007,6,30):0.0,\
                                                     date(2007,3,31):-0.03,\
                                                     date(2006,12,31):0.11}) 
     
	def testDashesMixedWithNumbers(self): 
		""" Make sure that a wrong answer with dashes and numbers fails """
		self.assertNotEqual(self.google.getQuarterlyDilutionAdjustment('S'), {date(2007,12,31):0.00,\
                                                     date(2007,9,30):'-',\
                                                     date(2007,6,30):0.00,\
                                                     date(2007,3,31):0.00,\
                                                     date(2006,12,31):0.00})
	def testRandomLookups(self):
		""" Make sure to not screw up a random search and make sure it fails if its wrong """
		self.assertNotAlmostEqual(self.google.getAnnualIssuanceOfStock("CSCO", date(2005,07,30)),9148.00)
		
		#failed key
		self.assertNotEqual(self.google.getQuarterlyAmortization("GOOG"), {date(2007,12,31):48.03,\
                                                         date(2007,9,30):41.96,\
                                                         date(2007,6,30):35.22,\
                                                         date(2007,3,30):34.70})
		#failed value
		self.assertNotEqual(self.google.getQuarterlyAmortization("GOOG"), {date(2007,12,31):48.03,\
                                                         date(2007,9,30):41.96,\
                                                         date(2007,6,30):35.22,\
                                                         date(2007,3,31):35.70})
		
		#missing values/keys
		self.assertNotEqual(self.google.getAnnualDeferredTaxes("RDS.A"), {date(2006,12,31):1833.0,\
                                                       date(2004,12,31):-1007.0})
        
class WebsiteTestCase_RandomAccess(WebsiteTestCase):
	""" These tests randomly check different output to ensure that it is not just DD that works """
	def testAnnualAndQuarterlyAccess(self):
		""" Test random quarterly and annual output """
		#randomly testing other symbols and dates that I've already checked is more robust and ensures that there's no single point of failure
		#in other words, ensures that one test isn't 'accidently' passing.
		
		#annuals
		self.assertAlmostEqual(self.google.getAnnualRevenue("CICI", date(2006,12,31)), 2.34)
		self.assertAlmostEqual(self.google.getAnnualCashAndEquivalents("CICI", date(2006,12,31)), 0.73)
		self.assertAlmostEqual(self.google.getAnnualNetIncomeStartingLine("CICI", date(2006,12,31)), -3.29)
		
		#quarterlys
		self.assertAlmostEqual(self.google.getQuarterlyRevenue("CICI", date(2007,9,30)), .46) 
		self.assertAlmostEqual(self.google.getQuarterlyCashAndEquivalents("CICI", date(2007,9,30)), 3.24) 
		self.assertAlmostEqual(self.google.getQuarterlyNetIncomeStartingLine("CICI", date(2007,9,30)), -1.10)
		
	def testWeirdName(self):
		""" Tests a weird symbol name to make sure I'm finding it right """
		self.assertEqual(self.google.getAnnualCashFromInvestingActivities("BRK.B"), {date(2007,12,31):-13428.0,\
                                                                    date(2006,12,31):-14077.0,\
                                                                    date(2005,12,31):-13841.0,\
                                                                    date(2004,12,31):315.0,\
                                                                    date(2003,12,31):16029.0,\
                                                                    date(2002,12,31):-1311.0})
	
	#Tests included as doctests:
	#Checking for ADR's
	#Checking for out of the ordinary dates
	#Checking foreign stocks
	#
		
	
class WebsiteTestCase_WebpageFormat(WebsiteTestCase):
	""" Test suite that checks for problems that tend to deal with formatting of the webpage """
	def testMixedBoldedSpanned(self):
		""" Test results that have mixed bold and span tags in them """
		self.assertEqual(self.google.getQuarterlyOperatingIncome('S'), {date(2007,12,31):-29625.0,\
                                                     date(2007,9,30):398.0,\
                                                     date(2007,6,30):317.0,\
                                                     date(2007,3,31):1.0,\
                                                     date(2006,12,31):569.0})
	
	def testMixedSpanned(self):
		""" Test results that have mixed span tags in them """
		self.assertEqual(self.google.getQuarterlyOtherNet('S'), {date(2007,12,31):234.0,\
                                                     date(2007,9,30):0.0,\
                                                     date(2007,6,30):13.0,\
                                                     date(2007,3,31):-4.0,\
                                                     date(2006,12,31):142.0})
		
	def testAllSpannedBolded(self):
		""" Tests results that are all spanned and bolded """
		self.assertEqual(self.google.getQuarterlyIncomeAfterTax('S'), {date(2007,12,31):-29452.00,\
                                                     date(2007,9,30):64.0,\
                                                     date(2007,6,30):-192.0,\
                                                     date(2007,3,31):-211.0,\
                                                     date(2006,12,31):261.0})
 
	def testBoldedKeyword(self):
		""" Tests results that rely on a bolded keyword """
		self.assertEqual(self.google.getQuarterlyTotalRevenue("IRBT"), {date(2007,12,29):98.74,\
                                                     date(2007,9,29):110.85,\
                                                     date(2007,6,30):47.01,\
                                                     date(2007,3,31):39.49,\
                                                     date(2008,3,29):57.30})
 
	def testSpannedKeyword(self):
		""" Tests results that rely on a spanned keyword """
		self.assertEqual(self.google.getQuarterlyCashAndEquivalents("IRBT"), {date(2007,12,29):26.73,\
                                                     date(2007,9,29):23.20,\
                                                     date(2007,6,30):10.26,\
                                                     date(2007,3,31):9.40,\
                                                     date(2008,3,29):22.86})
    
	def testMixedDashesAndNotZeros(self):
		""" Tests that dashes can be mixed with non-zero numbers """
		self.assertEqual(self.google.getAnnualLongTermInvestments("WHR"), {date(2007,12,31):'-',\
                                                     date(2006,12,31):'-',\
                                                     date(2005,12,31):28.00,\
                                                     date(2004,12,31):16.00,\
                                                     date(2003,12,31):11.00,\
                                                     date(2002,12,31):7.00})
		
	#tests included as doctests:
	#all zeros
	#numbers close to zero
	#mixing zeros and dashes
	#plain bold embedded
	#plain spanned embedded
	#all negatives
        
class WebsiteTestCase_IncomeStatement(WebsiteTestCase):
    def testAnnualRevenue(self):
        """ Test that I find Annual Revenue """
        self.assertEquals(self.google.getAnnualRevenue("DD"), {date(2007, 12, 31):29378.00, \
                                                                    date(2006, 12, 31):27421.00, \
                                                                                date(2005, 12, 31):26639.00, \
                                                                                date(2004, 12, 31):27340.00, \
                                                                                date(2003, 12, 31):26996.00, \
                                                                                date(2002, 12, 31):24006})
        
    def testAnnualOtherRevenue(self):
        """ Test that I find Annual Other Revenue """
        self.assertEquals(self.google.getAnnualOtherRevenue("DD"), {date(2007, 12, 31):1275.00, \
                                                                        date(2006, 12, 31):1561.00, \
                                                                        date(2005, 12, 31):1852.00, \
                                                                        date(2004, 12, 31):655.00, \
                                                                        date(2003, 12, 31):734.00, \
                                                                        date(2002, 12, 31):516.00})
 
    def testAnnualTotalRevenue(self):
        """ Test that I find Annual Total Revenue """
        self.assertEquals(self.google.getAnnualTotalRevenue("DD"), {date(2007, 12, 31):30653.00, \
                                                       date(2006, 12, 31):28982.00, \
                                                       date(2005, 12, 31):28491.00, \
                                                       date(2004, 12, 31):27995.00, \
                                                       date(2003, 12, 31):27730.00, \
                                                       date(2002, 12, 31):24522.00})
        
    def testAnnualCostOfRevenue(self):
        """ Test that I find Annual Cost of Revenue """
        self.assertEquals(self.google.getAnnualCostOfRevenue("DD"), {date(2007, 12, 31):21565.00, \
                                                                          date(2006, 12, 31):20440.00, \
                                                                          date(2005, 12, 31):19683.00, \
                                                                          date(2004, 12, 31):20827.00, \
                                                                          date(2003, 12, 31):20759.00, \
                                                                          date(2002, 12, 31):17529.00})
        
    def testAnnualGrossProfit(self):
        """ Test that I find Annual Gross Profit"""
        self.assertEquals(self.google.getAnnualGrossProfit("DD"), {date(2007, 12, 31):7813.00, \
                                    date(2006, 12, 31):6981.00, \
                                    date(2005, 12, 31):6956.00, \
                                    date(2004, 12, 31):6513.00, \
                                    date(2003, 12, 31):6237.00, \
                                    date(2002, 12, 31):6477.00})
        
    def testAnnualSGAExpenses(self):
        """ Test that I find Annual SGA Expenses"""
        self.assertEquals(self.google.getAnnualSGAExpenses("DD"), {date(2007, 12, 31):3364.00, \
                                    date(2006, 12, 31):3224.00, \
                                    date(2005, 12, 31):3223.00, \
                                    date(2004, 12, 31):3141.00, \
                                    date(2003, 12, 31):3067.00, \
                                    date(2002, 12, 31):2763.00})
        
    def testAnnualResarchAndDevelopment(self):
        """ Test that I find Annual Resarch And Development """
        self.assertEquals(self.google.getAnnualResearchAndDevelopment("DD"), {date(2007, 12, 31):1338.00, \
                                               date(2006, 12, 31):1302.00, \
                                               date(2005, 12, 31):1336.00, \
                                               date(2004, 12, 31):1333.00, \
                                               date(2003, 12, 31):1349.00, \
                                               date(2002, 12, 31):1264.00})
        
    def testAnnualDepreciationAmortization(self):
        """ Test that I find Annual Depreciation and Amortization"""
        self.assertEquals(self.google.getAnnualDepreciationAmortization("DD"), {date(2007, 12, 31):213.00, \
                                                 date(2006, 12, 31):227.00, \
                                                 date(2005, 12, 31):230.00, \
                                                 date(2004, 12, 31):223.00, \
                                                 date(2003, 12, 31):229.00, \
                                                 date(2002, 12, 31):218.00})        
        
    def testAnnualInterestNetOperating(self):
        """ Test that I find Annual Interest Net Operating"""
        self.assertEquals(self.google.getAnnualInterestNetOperating("DD"), {date(2007, 12, 31):430.00, \
                                             date(2006, 12, 31):460.00, \
                                             date(2005, 12, 31):518.00, \
                                             date(2004, 12, 31):362.00, \
                                             date(2003, 12, 31):347.00, \
                                             date(2002, 12, 31):359.00})
        
    def testAnnualUnusualExpense(self):
        """ Test that I find Annual Unusual Expense"""
        self.assertEquals(self.google.getAnnualUnusualExpense("DD"), {date(2007, 12, 31):0.00, \
                                       date(2006, 12, 31):0.00, \
                                       date(2005, 12, 31):-62.00, \
                                       date(2004, 12, 31):667.00, \
                                       date(2003, 12, 31):1898.00, \
                                       date(2002, 12, 31):290.00})
        
    def testAnnualOtherOperatingExpenses(self):
        """ Test that I find Annual Other Operating Expenses"""
        self.assertEquals(self.google.getAnnualOtherOperatingExpenses("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):-62.00, \
                                               date(2002, 12, 31):-25.00})
        
    def testAnnualTotalOperatingExpense(self):
        """ Test that I find Annual Total Operating Expense"""
        self.assertEquals(self.google.getAnnualTotalOperatingExpense("DD"), {date(2007, 12, 31):26910.00, \
                                              date(2006, 12, 31):25653.00, \
                                              date(2005, 12, 31):24928.00, \
                                              date(2004, 12, 31):26553.00, \
                                              date(2003, 12, 31):27587.00, \
                                              date(2002, 12, 31):22398.00})
        
    def testAnnualOperatingIncome(self):
        """ Test that I find Annual Operating Income"""
        self.assertEquals(self.google.getAnnualOperatingIncome("DD"), {date(2007, 12, 31):3743.00, \
                                        date(2006, 12, 31):3329.00, \
                                        date(2005, 12, 31):3563.00, \
                                        date(2004, 12, 31):1442.00, \
                                        date(2003, 12, 31):143.00, \
                                        date(2002, 12, 31):2124.00})
        
    def testAnnualInterestIncome(self):
        """ Test that I find Annual Interest Income"""
        self.assertEquals(self.google.getAnnualInterestIncome("DD"), {date(2007, 12, 31):'-', \
                                       date(2006, 12, 31):'-', \
                                       date(2005, 12, 31):'-', \
                                       date(2004, 12, 31):'-', \
                                       date(2003, 12, 31):'-', \
                                       date(2002, 12, 31):'-'})
        
    def testAnnualGainOnSaleOfAssets(self):
        """ Test that I find Annual Gain On Sale Of Assets"""
        self.assertEquals(self.google.getAnnualGainOnSaleOfAssets("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'})
        
    def testAnnualOtherNet(self):
        """ Test that I find Annual Other Net"""
        self.assertEquals(self.google.getAnnualOtherNet("DD"), {date(2007, 12, 31):'-', \
                                 date(2006, 12, 31):'-', \
                                 date(2005, 12, 31):'-', \
                                 date(2004, 12, 31):'-', \
                                 date(2003, 12, 31):'-', \
                                 date(2002, 12, 31):'-'})
        
    def testAnnualIncomeBeforeTax(self):
        """ Test that I find Annual Income Before Tax"""
        self.assertEquals(self.google.getAnnualIncomeBeforeTax("DD"), {date(2007, 12, 31):3743.00, \
                                        date(2006, 12, 31):3329.00, \
                                        date(2005, 12, 31):3563.00, \
                                        date(2004, 12, 31):1442.00, \
                                        date(2003, 12, 31):143.00, \
                                        date(2002, 12, 31):2124.00})
        
    def testAnnualIncomeAfterTax(self):
        """ Test that I find Annual Income After Tax"""
        self.assertEquals(self.google.getAnnualIncomeAfterTax("DD"), {date(2007, 12, 31):2995.0, \
                                       date(2006, 12, 31):3133.00, \
                                       date(2005, 12, 31):2093.00, \
                                       date(2004, 12, 31):1771.00, \
                                       date(2003, 12, 31):1073.00, \
                                       date(2002, 12, 31):1939.00})
        
    def testAnnualMinorityInterest_Inc(self):
        """ Test that I find Annual Minority Interest(Income Statement) """
        self.assertEquals(self.google.getAnnualMinorityInterest_Inc("DD"), {date(2007, 12, 31):-7.00, \
                                         date(2006, 12, 31):15.00, \
                                         date(2005, 12, 31):-37.00, \
                                         date(2004, 12, 31):9.00, \
                                         date(2003, 12, 31):-71.00, \
                                         date(2002, 12, 31):-98.00})
        
    def testAnnualEquityInAffiliates(self):
        """ Test that I find Annual Equity In Affiliates"""
        self.assertEquals(self.google.getAnnualEquityInAffiliates("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'})
        
    def testAnnualNetIncomeBeforeExtraItems(self):
        """ Test that I find Annual Net Income Before Extra Items"""
        self.assertEquals(self.google.getAnnualNetIncomeBeforeExtraItems("DD"), {date(2007, 12, 31):2988.00, \
                                                  date(2006, 12, 31):3148.00, \
                                                  date(2005, 12, 31):2056.00, \
                                                  date(2004, 12, 31):1780.00, \
                                                  date(2003, 12, 31):1002.00, \
                                                  date(2002, 12, 31):1841.00})
        
    def testAnnualAccountingChange(self):
        """ Test that I find Annual Accounting Change"""
        self.assertEquals(self.google.getAnnualAccountingChange("DD"), {date(2007, 12, 31):'-', \
                                         date(2006, 12, 31):'-', \
                                         date(2005, 12, 31):'-', \
                                         date(2004, 12, 31):'-', \
                                         date(2003, 12, 31):'-', \
                                         date(2002, 12, 31):'-'})
        
    def testAnnualDiscontinuedOperations(self):
        """ Test that I find Annual Discontinued Operations"""
        self.assertEquals(self.google.getAnnualDiscontinuedOperations("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'})                                                                
        
    def testAnnualExtraordinaryItem(self):
        """ Test that I find Annual Extraordinary Item"""
        self.assertEquals(self.google.getAnnualExtraordinaryItem("DD"), {date(2007, 12, 31):'-', \
                                          date(2006, 12, 31):'-', \
                                          date(2005, 12, 31):'-', \
                                          date(2004, 12, 31):'-', \
                                          date(2003, 12, 31):'-', \
                                          date(2002, 12, 31):'-'})
        
    def testAnnualNetIncome(self):
        """ Test that I find Annual Net Income"""
        self.assertEquals(self.google.getAnnualNetIncome("DD"), {date(2007, 12, 31):2988.00, \
                                  date(2006, 12, 31):3148.00, \
                                  date(2005, 12, 31):2056.00, \
                                  date(2004, 12, 31):1780.00, \
                                  date(2003, 12, 31):973.00, \
                                  date(2002, 12, 31):-1103.00})
        
    def testAnnualPreferredDividends(self):
        """ Test that I find Annual Preferred Dividends"""
        self.assertEquals(self.google.getAnnualPreferredDividends("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'})
        
    def testAnnualIncomeAvailToCommonExclExtraItems(self):
        """ Test that I find Annual Income Avail T oCommon Excl Extra Items"""
        self.assertEquals(self.google.getAnnualIncomeAvailToCommonExclExtraItems("DD"), {date(2007, 12, 31):2978.00, \
                                                          date(2006, 12, 31):3138.00, \
                                                          date(2005, 12, 31):2046.00, \
                                                          date(2004, 12, 31):1770.00, \
                                                          date(2003, 12, 31):992.00, \
                                                          date(2002, 12, 31):1831.00})
        
    def testAnnualIncomeAvailToCommonInclExtraItems(self):
        """ Test that I find Annual Income Avail To Common Incl Extra Items"""
        self.assertEquals(self.google.getAnnualIncomeAvailToCommonInclExtraItems("DD"), {date(2007, 12, 31):2978.00, \
                                                          date(2006, 12, 31):3138.00, \
                                                          date(2005, 12, 31):2046.00, \
                                                          date(2004, 12, 31):1770.00, \
                                                          date(2003, 12, 31):963.00, \
                                                          date(2002, 12, 31):-1113.00})                                
        
    def testAnnualBasicWeightedAverageShares(self):
        """ Test that I find Annual Basic Weighted Average Shares"""
        self.assertEquals(self.google.getAnnualBasicWeightedAverageShares("DD"), {date(2007, 12, 31):'-', \
                                                   date(2006, 12, 31):'-', \
                                                   date(2005, 12, 31):'-', \
                                                   date(2004, 12, 31):'-', \
                                                   date(2003, 12, 31):'-', \
                                                   date(2002, 12, 31):'-'})
        
    def testAnnualBasicEPSExclExtraItems(self):
        """ Test that I find Annual Basic EPS Excl Extra Items"""
        self.assertEquals(self.google.getAnnualBasicEPSExclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'})
        
    def testAnnualBasicEPSInclExtraItems(self):
        """ Test that I find Annual Basic EPS Incl Extra Items"""
        self.assertEquals(self.google.getAnnualBasicEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'})
        
    def testAnnualDilutionAdjustment(self):
        """ Test that I find Annual Dilution Adjustment"""
        self.assertEquals(self.google.getAnnualDilutionAdjustment("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):0.00, \
                                           date(2002, 12, 31):0.00})
        
    def testAnnualDilutedWeightedAverageShares(self):
        """ Test that I find Annual Diluted Weighted Average Shares"""
        self.assertEquals(self.google.getAnnualDilutedWeightedAverageShares("DD"), {date(2007, 12, 31):925.40, \
                                                     date(2006, 12, 31):928.60, \
                                                     date(2005, 12, 31):988.95, \
                                                     date(2004, 12, 31):1003.39, \
                                                     date(2003, 12, 31):1000.01, \
                                                     date(2002, 12, 31):998.74})                                        
        
    def testAnnualDilutedEPSExclExtraItems(self):
        """ Test that I find Annual Diluted EPS Excl Extra Items"""
        self.assertEquals(self.google.getAnnualDilutedEPSExclExtraItems("DD"), {date(2007, 12, 31):3.22, \
                                                 date(2006, 12, 31):3.38, \
                                                 date(2005, 12, 31):2.07, \
                                                 date(2004, 12, 31):1.76, \
                                                 date(2003, 12, 31):0.99, \
                                                 date(2002, 12, 31):1.83})
        
    def testAnnualDilutedEPSInclExtraItems(self):
        """ Test that I find Annual Diluted EPS Incl Extra Items"""
        self.assertEquals(self.google.getAnnualDilutedEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                                 date(2006, 12, 31):'-', \
                                                 date(2005, 12, 31):'-', \
                                                 date(2004, 12, 31):'-', \
                                                 date(2003, 12, 31):'-', \
                                                 date(2002, 12, 31):'-'})
        
    def testAnnualDividendsPerShare(self):
        """ Test that I find Annual Dividends Per Share"""
        self.assertEquals(self.google.getAnnualDividendsPerShare("DD"), {date(2007, 12, 31):1.52, \
                                          date(2006, 12, 31):1.48, \
                                          date(2005, 12, 31):1.46, \
                                          date(2004, 12, 31):1.40, \
                                          date(2003, 12, 31):1.40, \
                                          date(2002, 12, 31):1.40})
        
    def testAnnualGrossDividends(self):
        """ Test that I find Annual Gross Dividends"""
        self.assertEquals(self.google.getAnnualGrossDividends("DD"), {date(2007, 12, 31):'-', \
                                       date(2006, 12, 31):'-', \
                                       date(2005, 12, 31):'-', \
                                       date(2004, 12, 31):'-', \
                                       date(2003, 12, 31):'-', \
                                       date(2002, 12, 31):'-'})
        
    def testAnnualNetIncomeAfterCompExp(self):
        """ Test that I find Annual Net Income After Comp Exp"""
        self.assertEquals(self.google.getAnnualNetIncomeAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                              date(2006, 12, 31):'-', \
                                              date(2005, 12, 31):'-', \
                                              date(2004, 12, 31):'-', \
                                              date(2003, 12, 31):'-', \
                                              date(2002, 12, 31):'-'})
        
    def testAnnualBasicEPSAfterCompExp(self):
        """ Test that I find Annual Basic EPS After Comp Exp"""
        self.assertEquals(self.google.getAnnualBasicEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                             date(2006, 12, 31):'-', \
                                             date(2005, 12, 31):'-', \
                                             date(2004, 12, 31):'-', \
                                             date(2003, 12, 31):'-', \
                                             date(2002, 12, 31):'-'})
        
    def testAnnualDilutedEPSAfterCompExp(self):
        """ Test that I find Annual Diluted EPS After Comp Exp"""
        self.assertEquals(self.google.getAnnualDilutedEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'})
        
    def testAnnualDepreciationSupplemental(self):
        """ Test that I find Annual Depreciation Supplemental"""
        self.assertEquals(self.google.getAnnualDepreciationSupplemental("DD"), {date(2007, 12, 31):'-', \
                                                 date(2006, 12, 31):'-', \
                                                 date(2005, 12, 31):'-', \
                                                 date(2004, 12, 31):'-', \
                                                 date(2003, 12, 31):'-', \
                                                 date(2002, 12, 31):'-'})
        
    def testAnnualTotalSpecialItems(self):
        """ Test that I find Annual Total Special Items"""
        self.assertEquals(self.google.getAnnualTotalSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                          date(2006, 12, 31):'-', \
                                          date(2005, 12, 31):'-', \
                                          date(2004, 12, 31):'-', \
                                          date(2003, 12, 31):'-', \
                                          date(2002, 12, 31):'-'})
        
    def testAnnualNormalizedIncomeBeforeTaxes(self):
        """ Test that I find Annual Normalized Income Before Taxes"""
        self.assertEquals(self.google.getAnnualNormalizedIncomeBeforeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                    date(2006, 12, 31):'-', \
                                                    date(2005, 12, 31):'-', \
                                                    date(2004, 12, 31):'-', \
                                                    date(2003, 12, 31):'-', \
                                                    date(2002, 12, 31):'-'})                                                                                
        
    def testAnnualEffectsOfSpecialItemsOnIncomeTaxes(self):
        """ Test that I find Annual Effects Of Special Items On Income Taxes"""
        self.assertEquals(self.google.getAnnualEffectsOfSpecialItemsOnIncomeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                           date(2006, 12, 31):'-', \
                                                           date(2005, 12, 31):'-', \
                                                           date(2004, 12, 31):'-', \
                                                           date(2003, 12, 31):'-', \
                                                           date(2002, 12, 31):'-'})
        
    def testAnnualIncomeTaxesExSpecialItems(self):
        """ Test that I find Annual Income Taxes Ex Special Items"""
        self.assertEquals(self.google.getAnnualIncomeTaxesExSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                                  date(2006, 12, 31):'-', \
                                                  date(2005, 12, 31):'-', \
                                                  date(2004, 12, 31):'-', \
                                                  date(2003, 12, 31):'-', \
                                                  date(2002, 12, 31):'-'})
        
    def testAnnualNormalizedIncomeAfterTaxes(self):
        """ Test that I find Annual Normalized Income After Taxes"""
        self.assertEquals(self.google.getAnnualNormalizedIncomeAfterTaxes("DD"), {date(2007, 12, 31):'-', \
                                                   date(2006, 12, 31):'-', \
                                                   date(2005, 12, 31):'-', \
                                                   date(2004, 12, 31):'-', \
                                                   date(2003, 12, 31):'-', \
                                                   date(2002, 12, 31):'-'})
        
    def testAnnualNormalizedIncomeAvailableCommon(self):
        """ Test that I find Annual Normalized Income Available Common"""
        self.assertEquals(self.google.getAnnualNormalizedIncomeAvailableCommon("DD"), {date(2007, 12, 31):'-', \
                                                        date(2006, 12, 31):'-', \
                                                        date(2005, 12, 31):'-', \
                                                        date(2004, 12, 31):'-', \
                                                        date(2003, 12, 31):'-', \
                                                        date(2002, 12, 31):'-'})                                
        
    def testAnnualBasicNormalizedEPS(self):
        """ Test that I find Annual Basic Normalized EPS"""
        self.assertEquals(self.google.getAnnualBasicNormalizedEPS("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'})
        
    def testAnnualDilutedNormalizedEPS(self):
        """ Test that I find Annual Diluted Normalized EPS"""
        self.assertEquals(self.google.getAnnualDilutedNormalizedEPS("DD"), {date(2007, 12, 31):3.22, \
                                             date(2006, 12, 31):3.38, \
                                             date(2005, 12, 31):2.03, \
                                             date(2004, 12, 31):2.20, \
                                             date(2003, 12, 31):2.19, \
                                             date(2002, 12, 31):1.90})
        
    #quarterly stuff
    
    def testQuarterlyRevenue(self):
        """ Test that I find Quarterly Revenue"""
        self.assertEquals(self.google.getQuarterlyRevenue("DD"), {date(2007, 12, 31):6983.00, \
                                             date(2007, 9, 30):6675.00, \
                                             date(2007, 6, 30):7875.00, \
                                             date(2007, 3, 31):7845.00, \
                                             date(2008, 3, 31):8575.00})
                                             
    def testQuarterlyOtherRevenue(self):
        """ Test that I find Quarterly Other Revenue""" 
        self.assertEquals(self.google.getQuarterlyOtherRevenue("DD"), {date(2007, 12, 31):230.00, \
                                     date(2007, 9, 30):365.00, \
                                     date(2007, 6, 30):364.00, \
                                     date(2007, 3, 31):316.00, \
                                     date(2008, 3, 31):195.00})
                                        
    def testQuarterlyTotalRevenue(self):
        """ Test that I find Quarterly Total Revenue"""                                          
        self.assertEquals(self.google.getQuarterlyTotalRevenue("DD"), {date(2007, 12, 31):7213.00, \
                                     date(2007, 9, 30):7040.00, \
                                     date(2007, 6, 30):8239.00, \
                                     date(2007, 3, 31):8161.00, \
                                     date(2008, 3, 31):8770.00})
                                      
    def testQuarterlyCostOfRevenue(self):
        """ Test that I find Quarterly Cost Of Revenue"""
        self.assertEquals(self.google.getQuarterlyCostOfRevenue("DD"), {date(2007, 12, 31):5349.00, \
                                      date(2007, 9, 30):5115.00, \
                                      date(2007, 6, 30):5555.00, \
                                      date(2007, 3, 31):5594.00, \
                                      date(2008, 3, 31):5956.00})
                                       
    def testQuarterlyGrossProfit(self):
        """ Test that I find Quarterly Gross Profit"""
        self.assertEquals(self.google.getQuarterlyGrossProfit("DD"), {date(2007, 12, 31):1634.00, \
                                    date(2007, 9, 30):1560.00, \
                                    date(2007, 6, 30):2320.00, \
                                    date(2007, 3, 31):2251.00, \
                                    date(2008, 3, 31):2619.00})
                                    
    def testQuarterlySGAExpenses(self):
        """ Test that I find Quarterly SGA Expenses"""
        self.assertEquals(self.google.getQuarterlySGAExpenses("DD"), {date(2007, 12, 31):852.00, \
                                    date(2007, 9, 30):797.00, \
                                    date(2007, 6, 30):877.00, \
                                    date(2007, 3, 31):846.00, \
                                    date(2008, 3, 31):934.00})
                                    
    def testQuarterlyResearchAndDevelopment(self):
        """ Test that I find Quarterly Research And Development"""
        self.assertEquals(self.google.getQuarterlyResearchAndDevelopment("DD"), {date(2007, 12, 31):359.00, \
                                               date(2007, 9, 30):332.00, \
                                               date(2007, 6, 30):337.00, \
                                               date(2007, 3, 31):310.00, \
                                               date(2008, 3, 31):330.00})
                                                
    def testQuarterlyDepreciationAmortization(self):
        """ Test that I find Quarterly Depreciation Amortization"""
        self.assertEquals(self.google.getQuarterlyDepreciationAmortization("DD"), {date(2007, 12, 31):50.00, \
                                                 date(2007, 9, 30):53.00, \
                                                 date(2007, 6, 30):54.00, \
                                                 date(2007, 3, 31):'-', \
                                                 date(2008, 3, 31):'-'})
                                                  
    def testQuarterlyInterestNetOperating(self):
        """ Test that I find Quarterly Interest Net Operating"""
        self.assertEquals(self.google.getQuarterlyInterestNetOperating("DD"), {date(2007, 12, 31):110.00, \
                                             date(2007, 9, 30):113.00, \
                                             date(2007, 6, 30):108.00, \
                                             date(2007, 3, 31):99.00, \
                                             date(2008, 3, 31):80.00})
                                             
    def testQuarterlyUnusualExpense(self):
        """ Test that I find Quarterly Unusual Expense""" 
        self.assertEquals(self.google.getQuarterlyUnusualExpense("DD"), {date(2007, 12, 31):'-', \
                                       date(2007, 9, 30):'-', \
                                       date(2007, 6, 30):'-', \
                                       date(2007, 3, 31):'-', \
                                       date(2008, 3, 31):0.00})
                                       
    def testQuarterlyOtherOperatingExpenses(self):
        """ Test that I find Quarterly Other Operating Expenses"""
        self.assertEquals(self.google.getQuarterlyOtherOperatingExpenses("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2008, 3, 31):'-'})
                                               
    def testQuarterlyTotalOperatingExpense(self):
        """ Test that I find Quarterly Total Operating Expense"""
        self.assertEquals(self.google.getQuarterlyTotalOperatingExpense("DD"), {date(2007, 12, 31):6720.00, \
                                              date(2007, 9, 30):6410.00, \
                                              date(2007, 6, 30):6931.00, \
                                              date(2007, 3, 31):6849.00, \
                                              date(2008, 3, 31):7300.00})
                                               
    def testQuarterlyOperatingIncome(self):
        """ Test that I find Quarterly Operating Income"""
        self.assertEquals(self.google.getQuarterlyOperatingIncome("DD"), {date(2007, 12, 31):493.00, \
                                        date(2007, 9, 30):630.00, \
                                        date(2007, 6, 30):1308.00, \
                                        date(2007, 3, 31):1312.00, \
                                        date(2008, 3, 31):1470.00})
                                         
    def testQuarterlyInterestIncome(self):
        """ Test that I find Quarterly Interest Income"""
        self.assertEquals(self.google.getQuarterlyInterestIncome("DD"), {date(2007, 12, 31):'-', \
                                       date(2007, 9, 30):'-', \
                                       date(2007, 6, 30):'-', \
                                       date(2007, 3, 31):'-', \
                                       date(2008, 3, 31):'-'})
                                        
    def testQuarterlyGainOnSaleOfAssets(self):
        """ Test that I find Quarterly Gain On Sale Of Assets"""
        self.assertEquals(self.google.getQuarterlyGainOnSaleOfAssets("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2008, 3, 31):'-'})
                                            
    def testQuarterlyOtherNet(self):
        """ Test that I find Quarterly Other Net"""
        self.assertEquals(self.google.getQuarterlyOtherNet("DD"), {date(2007, 12, 31):'-', \
                                 date(2007, 9, 30):'-', \
                                 date(2007, 6, 30):'-', \
                                 date(2007, 3, 31):'-', \
                                 date(2008, 3, 31):'-'})
                                  
    def testQuarterlyIncomeBeforeTax(self):
        """ Test that I find Quarterly Income Before Tax"""
        self.assertEquals(self.google.getQuarterlyIncomeBeforeTax("DD"), {date(2007, 12, 31):493.00, \
                                        date(2007, 9, 30):630.00, \
                                        date(2007, 6, 30):1308.00, \
                                        date(2007, 3, 31):1312.00, \
                                        date(2008, 3, 31):1470.00})
                                         
    def testQuarterlyIncomeAfterTax(self):
        """ Test that I find Quarterly Income After Tax"""
        self.assertEquals(self.google.getQuarterlyIncomeAfterTax("DD"), {date(2007, 12, 31):547.00, \
                                       date(2007, 9, 30):528.00, \
                                       date(2007, 6, 30):973.00, \
                                       date(2007, 3, 31):947.00, \
                                       date(2008, 3, 31):1197.00})
                                        
    def testQuarterlyMinorityInterest_Inc(self):
        """ Test that I find Quarterly Minority Interest(Income Statement)"""
        self.assertEquals(self.google.getQuarterlyMinorityInterest_Inc("DD"), {date(2007, 12, 31):-2.00, \
                                         date(2007, 9, 30):-2.00, \
                                         date(2007, 6, 30):-1.00, \
                                         date(2007, 3, 31):-2.00, \
                                         date(2008, 3, 31):-6.00})
                                          
    def testQuarterlyEquityInAffiliates(self):
        """ Test that I find Quarterly Equity In Affiliates"""
        self.assertEquals(self.google.getQuarterlyEquityInAffiliates("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2008, 3, 31):'-'})
                                            
    def testQuarterlyNetIncomeBeforeExtraItems(self):
        """ Test that I find Quarterly Net Income Before Extra Items"""
        self.assertEquals(self.google.getQuarterlyNetIncomeBeforeExtraItems("DD"), {date(2007, 12, 31):545.00, \
                                                  date(2007, 9, 30):526.00, \
                                                  date(2007, 6, 30):972.00, \
                                                  date(2007, 3, 31):945.00, \
                                                  date(2008, 3, 31):1191.00})
                                                   
    def testQuarterlyAccountingChange(self):
        """ Test that I find Quarterly Accounting Change"""
        self.assertEquals(self.google.getQuarterlyAccountingChange("DD"), {date(2007, 12, 31):'-', \
                                         date(2007, 9, 30):'-', \
                                         date(2007, 6, 30):'-', \
                                         date(2007, 3, 31):'-', \
                                         date(2008, 3, 31):'-'})
                                          
    def testQuarterlyDiscontinuedOperations(self):
        """ Test that I find Quarterly Discontinued Operations"""
        self.assertEquals(self.google.getQuarterlyDiscontinuedOperations("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2008, 3, 31):'-'})
                                                
    def testQuarterlyExtraordinaryItem(self):
        """ Test that I find Quarterly Extraordinary Item"""
        self.assertEquals(self.google.getQuarterlyExtraordinaryItem("DD"), {date(2007, 12, 31):'-', \
                                          date(2007, 9, 30):'-', \
                                          date(2007, 6, 30):'-', \
                                          date(2007, 3, 31):'-', \
                                          date(2008, 3, 31):'-'})
                                           
    def testQuarterlyNetIncome(self):
        """ Test that I find Quarterly Net Income"""
        self.assertEquals(self.google.getQuarterlyNetIncome("DD"), {date(2007, 12, 31):545.00, \
                                  date(2007, 9, 30):526.00, \
                                  date(2007, 6, 30):972.00, \
                                  date(2007, 3, 31):945.00, \
                                  date(2008, 3, 31):1191.00})
                                   
    def testQuarterlyPreferredDividends(self):
        """ Test that I find Quarterly Preferred Dividends"""
        self.assertEquals(self.google.getQuarterlyPreferredDividends("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2008, 3, 31):'-'})
                                            
    def testQuarterlyIncomeAvailToCommonExclExtraItems(self):
        """ Test that I find Quarterly Income Avail To Common Excl Extra Items""" 
        self.assertEquals(self.google.getQuarterlyIncomeAvailToCommonExclExtraItems("DD"), {date(2007, 12, 31):543.00, \
                                                          date(2007, 9, 30):524.00, \
                                                          date(2007, 6, 30):969.00, \
                                                          date(2007, 3, 31):942.00, \
                                                          date(2008, 3, 31):1188.00})
                                                           
    def testQuarterlyIncomeAvailToCommonInclExtraItems(self):
        """ Test that I find Quarterly Income Avail To Common Incl Extra Items""" 
        self.assertEquals(self.google.getQuarterlyIncomeAvailToCommonInclExtraItems("DD"), {date(2007, 12, 31):543.00, \
                                                          date(2007, 9, 30):524.00, \
                                                          date(2007, 6, 30):969.00, \
                                                          date(2007, 3, 31):942.00, \
                                                          date(2008, 3, 31):1188.00})
                                                           
    def testQuarterlyBasicWeightedAverageShares(self):
        """ Test that I find Quarterly Basic Weighted Average Shares""" 
        self.assertEquals(self.google.getQuarterlyBasicWeightedAverageShares("DD"), {date(2007, 12, 31):'-', \
                                                   date(2007, 9, 30):'-', \
                                                   date(2007, 6, 30):'-', \
                                                   date(2007, 3, 31):'-', \
                                                   date(2008, 3, 31):'-'})
                                                    
    def testQuarterlyBasicEPSExclExtraItems(self):
        """ Test that I find Quarterly Basic EPS Excl Extra Items""" 
        self.assertEquals(self.google.getQuarterlyBasicEPSExclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2008, 3, 31):'-'})
                                                
    def testQuarterlyBasicEPSInclExtraItems(self):
        """ Test that I find Quarterly Basic EPS Incl Extra Items""" 
        self.assertEquals(self.google.getQuarterlyBasicEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2008, 3, 31):'-'})
                                                
    def testQuarterlyDilutionAdjustment(self):
        """ Test that I find Quarterly Dilution Adjustment"""
        self.assertEquals(self.google.getQuarterlyDilutionAdjustment("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2008, 3, 31):'-'})
                                            
    def testQuarterlyDilutedWeightedAverageShares(self):
        """ Test that I find Quarterly Diluted Weighted Average Shares"""
        self.assertEquals(self.google.getQuarterlyDilutedWeightedAverageShares("DD"), {date(2007, 12, 31):906.48, \
                                                     date(2007, 9, 30):929.32, \
                                                     date(2007, 6, 30):932.81, \
                                                     date(2007, 3, 31):933.27, \
                                                     date(2008, 3, 31):906.19})
                                                      
    def testQuarterlyDilutedEPSExclExtraItems(self):
        """ Test that I find Quarterly Diluted EPS Excl Extra Items""" 
        self.assertEquals(self.google.getQuarterlyDilutedEPSExclExtraItems("DD"), {date(2007, 12, 31):0.60, \
                                                 date(2007, 9, 30):0.56, \
                                                 date(2007, 6, 30):1.04, \
                                                 date(2007, 3, 31):1.01, \
                                                 date(2008, 3, 31):1.31})
                                                  
    def testQuarterlyDilutedEPSInclExtraItems(self):
        """ Test that I find Quarterly Diluted EPS Incl Extra Items""" 
        self.assertEquals(self.google.getQuarterlyDilutedEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                                 date(2007, 9, 30):'-', \
                                                 date(2007, 6, 30):'-', \
                                                 date(2007, 3, 31):'-', \
                                                 date(2008, 3, 31):'-'})
                                                  
    def testQuarterlyDividendsPerShare(self):
        """ Test that I find Quarterly Dividends Per Share""" 
        self.assertEquals(self.google.getQuarterlyDividendsPerShare("DD"), {date(2007, 12, 31):0.41, \
                                          date(2007, 9, 30):0.37, \
                                          date(2007, 6, 30):0.37, \
                                          date(2007, 3, 31):0.37, \
                                          date(2008, 3, 31):0.41})
                                           
    def testQuarterlyGrossDividends(self):
        """ Test that I find Quarterly Gross Dividends""" 
        self.assertEquals(self.google.getQuarterlyGrossDividends("DD"), {date(2007, 12, 31):'-', \
                                       date(2007, 9, 30):'-', \
                                       date(2007, 6, 30):'-', \
                                       date(2007, 3, 31):'-', \
                                       date(2008, 3, 31):'-'})
                                        
    def testQuarterlyNetIncomeAfterCompExp(self):
        """ Test that I find Quarterly Net Income After Comp Exp"""
        self.assertEquals(self.google.getQuarterlyNetIncomeAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                              date(2007, 9, 30):'-', \
                                              date(2007, 6, 30):'-', \
                                              date(2007, 3, 31):'-', \
                                              date(2008, 3, 31):'-'})
                                               
    def testQuarterlyBasicEPSAfterCompExp(self):
        """ Test that I find Quarterly Basic EPS After Comp Exp"""
        self.assertEquals(self.google.getQuarterlyBasicEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                             date(2007, 9, 30):'-', \
                                             date(2007, 6, 30):'-', \
                                             date(2007, 3, 31):'-', \
                                             date(2008, 3, 31):'-'})
                                              
    def testQuarterlyDilutedEPSAfterCompExp(self):
        """ Test that I find Quarterly Diluted EPS After Comp Exp"""
        self.assertEquals(self.google.getQuarterlyDilutedEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2008, 3, 31):'-'})
                                                
    def testQuarterlyDepreciationSupplemental(self):
        """ Test that I find Quarterly Depreciation Supplemental""" 
        self.assertEquals(self.google.getQuarterlyDepreciationSupplemental("DD"), {date(2007, 12, 31):'-', \
                                                 date(2007, 9, 30):'-', \
                                                 date(2007, 6, 30):'-', \
                                                 date(2007, 3, 31):'-', \
                                                 date(2008, 3, 31):'-'})
                                                  
    def testQuarterlyTotalSpecialItems(self):
        """ Test that I find Quarterly Total Special Items""" 
        self.assertEquals(self.google.getQuarterlyTotalSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                          date(2007, 9, 30):'-', \
                                          date(2007, 6, 30):'-', \
                                          date(2007, 3, 31):'-', \
                                          date(2008, 3, 31):'-'})
                                           
    def testQuarterlyNormalizedIncomeBeforeTaxes(self):
        """ Test that I find Quarterly Normalized Income Before Taxes""" 
        self.assertEquals(self.google.getQuarterlyNormalizedIncomeBeforeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                    date(2007, 9, 30):'-', \
                                                    date(2007, 6, 30):'-', \
                                                    date(2007, 3, 31):'-', \
                                                    date(2008, 3, 31):'-'})
                                                     
    def testQuarterlyEffectsOfSpecialItemsOnIncomeTaxes(self):
        """ Test that I find Quarterly EffectsOf Special Items On Income Taxes"""
        self.assertEquals(self.google.getQuarterlyEffectsOfSpecialItemsOnIncomeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                           date(2007, 9, 30):'-', \
                                                            date(2007, 6, 30):'-', \
                                                           date(2007, 3, 31):'-', \
                                                           date(2008, 3, 31):'-'})
                                                            
    def testQuarterlyIncomeTaxesExSpecialItems(self):
        """ Test that I find Quarterly Income Taxes Ex Special Items""" 
        self.assertEquals(self.google.getQuarterlyIncomeTaxesExSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                                  date(2007, 9, 30):'-', \
                                                  date(2007, 6, 30):'-', \
                                                  date(2007, 3, 31):'-', \
                                                  date(2008, 3, 31):'-'})
                                                   
    def testQuarterlyNormalizedIncomeAfterTaxes(self):
        """ Test that I find Quarterly Normalized Income After Taxes"""
        self.assertEquals(self.google.getQuarterlyNormalizedIncomeAfterTaxes("DD"), {date(2007, 12, 31):'-', \
                                                   date(2007, 9, 30):'-', \
                                                   date(2007, 6, 30):'-', \
                                                   date(2007, 3, 31):'-', \
                                                   date(2008, 3, 31):'-'})
                                                    
    def testQuarterlyNormalizedIncomeAvailableCommon(self):
        """ Test that I find Quarterly Normalized Income Available Common"""
        self.assertEquals(self.google.getQuarterlyNormalizedIncomeAvailableCommon("DD"), {date(2007, 12, 31):'-', \
                                                        date(2007, 9, 30):'-', \
                                                        date(2007, 6, 30):'-', \
                                                        date(2007, 3, 31):'-', \
                                                        date(2008, 3, 31):'-'})
                                                         
    def testQuarterlyBasicNormalizedEPS(self):
        """ Test that I find Quarterly Basic Normalized EPS"""
        self.assertEquals(self.google.getQuarterlyBasicNormalizedEPS("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2008, 3, 31):'-'})
                                            
    def testQuarterlyDilutedNormalizedEPS(self):
        """ Test that I find Quarterly Diluted Normalized EPS""" 
        self.assertEquals(self.google.getQuarterlyDilutedNormalizedEPS("DD"), {date(2007, 12, 31):0.60, \
                                             date(2007, 9, 30):0.56, \
                                             date(2007, 6, 30):1.04, \
                                             date(2007, 3, 31):1.01, \
                                             date(2008, 3, 31):1.31})
 
        
class WebsiteTestCase_BalanceSheet(WebsiteTestCase):    
    """ Test all the information that comes from an SEC Balance Sheet """
    
    def testAnnualCashAndEquivalents(self):
        """ Test that I find Annual Cash And Equivalents"""
        self.assertEquals(self.google.getAnnualCashAndEquivalents("DD"), {date(2007, 12, 31):1305.00, \
                                           date(2006, 12, 31):1814.00, \
                                           date(2005, 12, 31):1736.00, \
                                           date(2004, 12, 31):3369.00, \
                                           date(2003, 12, 31):3273.00, \
                                           date(2002, 12, 31):3678.00})
        
    def testAnnualShortTermInvestments(self):
        """ Test that I find Annual Short Term Investments"""
        self.assertEquals(self.google.getAnnualShortTermInvestments("DD"), {date(2007, 12, 31):131.00, \
                                             date(2006, 12, 31):79.00, \
                                             date(2005, 12, 31):115.00, \
                                             date(2004, 12, 31):167.00, \
                                             date(2003, 12, 31):25.00, \
                                             date(2002, 12, 31):465.00})
        
    def testAnnualCashAndShortTermInvestments(self):
        """ Test that I find Annual Cash And Short Term Investments"""
        self.assertEquals(self.google.getAnnualCashAndShortTermInvestments("DD"), {date(2007, 12, 31):1436.00, \
                                                    date(2006, 12, 31):1893.00, \
                                                    date(2005, 12, 31):1851.00, \
                                                    date(2004, 12, 31):3536.00, \
                                                    date(2003, 12, 31):3298.00, \
                                                    date(2002, 12, 31):4143.00})
        
    def testAnnualAccountsReceivableTrade(self):
        """ Test that I find Annual Accounts Receivable Trade"""
        self.assertEquals(self.google.getAnnualAccountsReceivableTrade("DD"), {date(2007, 12, 31):4649.00, \
                                                date(2006, 12, 31):4335.00, \
                                                date(2005, 12, 31):3907.00, \
                                                date(2004, 12, 31):3860.00, \
                                                date(2003, 12, 31):3427.00, \
                                                date(2002, 12, 31):2913.00})
        
    def testAnnualReceivablesOther(self):
        """ Test that I find Annual Receivables Other"""
        self.assertEquals(self.google.getAnnualReceivablesOther("DD"), {date(2007, 12, 31):'-', \
                                         date(2006, 12, 31):'-', \
                                         date(2005, 12, 31):'-', \
                                         date(2004, 12, 31):'-', \
                                         date(2003, 12, 31):'-', \
                                         date(2002, 12, 31):'-'})
        
    def testAnnualTotalReceivablesNet(self):
        """ Test that I find Annual Total Receivables Net"""
        self.assertEquals(self.google.getAnnualTotalReceivablesNet("DD"), {date(2007, 12, 31):5683.00, \
                                            date(2006, 12, 31):5198.00, \
                                            date(2005, 12, 31):4801.00, \
                                            date(2004, 12, 31):4889.00, \
                                            date(2003, 12, 31):4218.00, \
                                            date(2002, 12, 31):3884.00})                                                        
        
    def testAnnualTotalInventory(self):
        """ Test that I find Annual Total Inventory"""
        self.assertEquals(self.google.getAnnualTotalInventory("DD"), {date(2007, 12, 31):5278.00, \
                                       date(2006, 12, 31):4941.00, \
                                       date(2005, 12, 31):4743.00, \
                                       date(2004, 12, 31):4489.00, \
                                       date(2003, 12, 31):4107.00, \
                                       date(2002, 12, 31):4409.00})
        
    def testAnnualPrepaidExpenses(self):
        """ Test that I find Annual Prepaid Expenses"""
        self.assertEquals(self.google.getAnnualPrepaidExpenses("DD"), {date(2007, 12, 31):199.00, \
                                        date(2006, 12, 31):182.00, \
                                        date(2005, 12, 31):199.00, \
                                        date(2004, 12, 31):209.00, \
                                        date(2003, 12, 31):208.00, \
                                        date(2002, 12, 31):175.00})
        
    def testAnnualOtherCurrentAssetsTotal(self):
        """ Test that I find Annual OtherCurrent Assets Total"""
        self.assertEquals(self.google.getAnnualOtherCurrentAssetsTotal("DD"), {date(2007, 12, 31):564.00, \
                                                date(2006, 12, 31):656.00, \
                                                date(2005, 12, 31):828.00, \
                                                date(2004, 12, 31):2088.00, \
                                                date(2003, 12, 31):6631.00, \
                                                date(2002, 12, 31):848.00})
        
    def testAnnualTotalCurrentAssets(self):
        """ Test that I find Annual Total Current Assets"""
        self.assertEquals(self.google.getAnnualTotalCurrentAssets("DD"), {date(2007, 12, 31):13160.00, \
                                           date(2006, 12, 31):12870.00, \
                                           date(2005, 12, 31):12422.00, \
                                           date(2004, 12, 31):15211.00, \
                                           date(2003, 12, 31):18462.00, \
                                           date(2002, 12, 31):13459.00})
        
    def testAnnualPPE(self):
        """ Test that I find Annual PPE"""
        self.assertEquals(self.google.getAnnualPPE("DD"), {date(2007, 12, 31):26593.00, \
                            date(2006, 12, 31):25719.00, \
                            date(2005, 12, 31):24963.00, \
                            date(2004, 12, 31):23978.00, \
                            date(2003, 12, 31):24149.00, \
                            date(2002, 12, 31):33732.00})                                        
        
    def testAnnualGoodwill(self):
        """ Test that I find Annual Goodwill"""
        self.assertEquals(self.google.getAnnualGoodwill("DD"), {date(2007, 12, 31):2074.00, \
                                 date(2006, 12, 31):2108.00, \
                                 date(2005, 12, 31):2087.00, \
                                 date(2004, 12, 31):2082.00, \
                                 date(2003, 12, 31):1939.00, \
                                 date(2002, 12, 31):1167.00})
        
    def testAnnualIntangibles(self):
        """ Test that I find Annual Intangibles"""
        self.assertEquals(self.google.getAnnualIntangibles("DD"), {date(2007, 12, 31):2856.00, \
                                    date(2006, 12, 31):2479.00, \
                                    date(2005, 12, 31):2712.00, \
                                    date(2004, 12, 31):2883.00, \
                                    date(2003, 12, 31):3278.00, \
                                    date(2002, 12, 31):3514.00})
        
    def testAnnualLongTermInvestments(self):
        """ Test that I find Annual Long Term Investments"""
        self.assertEquals(self.google.getAnnualLongTermInvestments("DD"), {date(2007, 12, 31):908.00, \
                                            date(2006, 12, 31):897.00, \
                                            date(2005, 12, 31):937.00, \
                                            date(2004, 12, 31):1140.00, \
                                            date(2003, 12, 31):1445.00, \
                                            date(2002, 12, 31):2190.00})
        
    def testAnnualOtherLongTermAssets(self):
        """ Test that I find Annual Other Long Term Assets"""
        self.assertEquals(self.google.getAnnualOtherLongTermAssets("DD"), {date(2007, 12, 31):4273.00, \
                                            date(2006, 12, 31):2925.00, \
                                            date(2005, 12, 31):4824.00, \
                                            date(2004, 12, 31):4092.00, \
                                            date(2003, 12, 31):2023.00, \
                                            date(2002, 12, 31):1005.00})
        
    def testAnnualTotalAssets(self):
        """ Test that I find Annual Total Assets"""
        self.assertEquals(self.google.getAnnualTotalAssets("DD"), {date(2007, 12, 31):34131.00, \
                                    date(2006, 12, 31):31777.00, \
                                    date(2005, 12, 31):33291.00, \
                                    date(2004, 12, 31):35632.00, \
                                    date(2003, 12, 31):37039.00, \
                                    date(2002, 12, 31):34621.00})
        
    def testAnnualAccountsPayable(self):
        """ Test that I find Annual Accounts Payable"""
        self.assertEquals(self.google.getAnnualAccountsPayable("DD"), {date(2007, 12, 31):3172.00, \
                                        date(2006, 12, 31):2711.00, \
                                        date(2005, 12, 31):2670.00, \
                                        date(2004, 12, 31):2661.00, \
                                        date(2003, 12, 31):2412.00, \
                                        date(2002, 12, 31):2727.00})
        
    def testAnnualAccruedExpenses(self):
        """ Test that I find Annual Accrued Expenses"""
        self.assertEquals(self.google.getAnnualAccruedExpenses("DD"), {date(2007, 12, 31):3823.00, \
                                        date(2006, 12, 31):3534.00, \
                                        date(2005, 12, 31):3075.00, \
                                        date(2004, 12, 31):4054.00, \
                                        date(2003, 12, 31):2963.00, \
                                        date(2002, 12, 31):3137.00})
        
    def testAnnualNotesPayable(self):
        """ Test that I find Annual Notes Payable"""
        self.assertEquals(self.google.getAnnualNotesPayable("DD"), {date(2007, 12, 31):1349.00, \
                                     date(2006, 12, 31):354.00, \
                                     date(2005, 12, 31):0.00, \
                                     date(2004, 12, 31):0.00, \
                                     date(2003, 12, 31):0.00, \
                                     date(2002, 12, 31):0.00})
        
    def testAnnualCurrentPortLTDebtToCapital(self):
        """ Test that I find Annual Current Port LT Debt To Capital"""
        self.assertEquals(self.google.getAnnualCurrentPortLTDebtToCapital("DD"), {date(2007, 12, 31):21.00, \
                                                   date(2006, 12, 31):1163.00, \
                                                   date(2005, 12, 31):1397.00, \
                                                   date(2004, 12, 31):936.00, \
                                                   date(2003, 12, 31):5914.00, \
                                                   date(2002, 12, 31):1185.00})                                        
        
    def testAnnualOtherCurrentLiabilities(self):
        """ Test that I find Annual Other Current Liabilities"""
        self.assertEquals(self.google.getAnnualOtherCurrentLiabilities("DD"), {date(2007, 12, 31):176.00, \
                                                date(2006, 12, 31):178.00, \
                                                date(2005, 12, 31):294.00, \
                                                date(2004, 12, 31):288.00, \
                                                date(2003, 12, 31):1754.00, \
                                                date(2002, 12, 31):47.00}) 
    def testAnnualTotalCurrentLiabilities(self):
        """ Test that I find Annual Total Current Liabilities""" 
        self.assertEquals(self.google.getAnnualTotalCurrentLiabilities("DD"), {date(2007, 12, 31):8541.00, \
                                                date(2006, 12, 31):7940.00, \
                                                date(2005, 12, 31):7436.00, \
                                                date(2004, 12, 31):7939.00, \
                                                date(2003, 12, 31):13043.00, \
                                                date(2002, 12, 31):7096.00}) 
    def testAnnualLongTermDebt(self):
        """ Test that I find Annual Long Term Debt""" 
        self.assertEquals(self.google.getAnnualLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                     date(2006, 12, 31):6013.00, \
                                     date(2005, 12, 31):6783.00, \
                                     date(2004, 12, 31):5548.00, \
                                     date(2003, 12, 31):4301.00, \
                                     date(2002, 12, 31):5647.00}) 
    def testAnnualCapitalLeaseObligations(self):
        """ Test that I find Annual Capital Lease Obligations""" 
        self.assertEquals(self.google.getAnnualCapitalLeaseObligations("DD"), {date(2007, 12, 31):'-', \
                                                date(2006, 12, 31):'-', \
                                                date(2005, 12, 31):'-', \
                                                date(2004, 12, 31):'-', \
                                                date(2003, 12, 31):'-', \
                                                date(2002, 12, 31):'-'}) 
    def testAnnualTotalLongTermDebt(self):
        """ Test that I find Annual Total Long Term Debt""" 
        self.assertEquals(self.google.getAnnualTotalLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                          date(2006, 12, 31):6013.00, \
                                          date(2005, 12, 31):6783.00, \
                                          date(2004, 12, 31):5548.00, \
                                          date(2003, 12, 31):4301.00, \
                                          date(2002, 12, 31):5647.00}) 
    def testAnnualTotalDebt(self):
        """ Test that I find Annual Total Debt""" 
        self.assertEquals(self.google.getAnnualTotalDebt("DD"), {date(2007, 12, 31):7325.00, \
                                  date(2006, 12, 31):7530.00, \
                                  date(2005, 12, 31):8180.00, \
                                  date(2004, 12, 31):6484.00, \
                                  date(2003, 12, 31):10215.00, \
                                  date(2002, 12, 31):6832.00}) 
    def testAnnualDeferredIncomeTax(self):
        """ Test that I find Annual Deferred Income Tax""" 
        self.assertEquals(self.google.getAnnualDeferredIncomeTax("DD"), {date(2007, 12, 31):802.00, \
                                          date(2006, 12, 31):269.00, \
                                          date(2005, 12, 31):1179.00, \
                                          date(2004, 12, 31):966.00, \
                                          date(2003, 12, 31):508.00, \
                                          date(2002, 12, 31):563.00}) 
    def testAnnualMinorityInterest_Bal(self):
        """ Test that I find Annual Minority Interes(Balance Sheet)""" 
        self.assertEquals(self.google.getAnnualMinorityInterest_Bal("DD"), {date(2007, 12, 31):442.00, \
                                         date(2006, 12, 31):441.00, \
                                         date(2005, 12, 31):490.00, \
                                         date(2004, 12, 31):1110.00, \
                                         date(2003, 12, 31):497.00, \
                                         date(2002, 12, 31):2423.00}) 
    def testAnnualOtherLiabilities(self):
        """ Test that I find Annual Other Liabilities""" 
        self.assertEquals(self.google.getAnnualOtherLiabilities("DD"), {date(2007, 12, 31):7255.00, \
                                         date(2006, 12, 31):7692.00, \
                                         date(2005, 12, 31):8441.00, \
                                         date(2004, 12, 31):8692.00, \
                                         date(2003, 12, 31):8909.00, \
                                         date(2002, 12, 31):9829.00}) 
    def testAnnualTotalLiabilities(self):
        """ Test that I find Annual TotalLiabilities""" 
        self.assertEquals(self.google.getAnnualTotalLiabilities("DD"), {date(2007, 12, 31):22995.00, \
                                         date(2006, 12, 31):22355.00, \
                                          date(2005, 12, 31):24329.00, \
                                         date(2004, 12, 31):24255.00, \
                                         date(2003, 12, 31):27258.00, \
                                         date(2002, 12, 31):25558.00}) 
    def testAnnualRedeemablePreferredStock(self):
        """ Test that I find Annual Redeemable Preferred Stock""" 
        self.assertEquals(self.google.getAnnualRedeemablePreferredStock("DD"), {date(2007, 12, 31):'-', \
                                                 date(2006, 12, 31):'-', \
                                                 date(2005, 12, 31):'-', \
                                                 date(2004, 12, 31):'-', \
                                                 date(2003, 12, 31):'-', \
                                                 date(2002, 12, 31):'-'}) 
    def testAnnualPreferredStockNonRedeemable(self):
        """ Test that I find Annual Preferred Stock Non Redeemable""" 
        self.assertEquals(self.google.getAnnualPreferredStockNonRedeemable("DD"), {date(2007, 12, 31):237.00, \
                                                    date(2006, 12, 31):237.00, \
                                                    date(2005, 12, 31):237.00, \
                                                    date(2004, 12, 31):237.00, \
                                                    date(2003, 12, 31):237.00, \
                                                    date(2002, 12, 31):237.00}) 
    def testAnnualCommonStock(self):
        """ Test that I find Annual Common Stock""" 
        self.assertEquals(self.google.getAnnualCommonStock("DD"), {date(2007, 12, 31):296.00, \
                                    date(2006, 12, 31):303.00, \
                                    date(2005, 12, 31):302.00, \
                                    date(2004, 12, 31):324.00, \
                                    date(2003, 12, 31):325.00, \
                                    date(2002, 12, 31):324.00}) 
    def testAnnualAdditionalPaidInCapital(self):
        """ Test that I find Annual Additional Paid In Capital""" 
        self.assertEquals(self.google.getAnnualAdditionalPaidInCapital("DD"), {date(2007, 12, 31):8179.00, \
                                                date(2006, 12, 31):7797.00, \
                                                date(2005, 12, 31):7679.00, \
                                                date(2004, 12, 31):7784.00, \
                                                date(2003, 12, 31):7522.00, \
                                                date(2002, 12, 31):7377.00}) 
    def testAnnualRetainedEarnings(self):
        """ Test that I find Annual Retained Earnings""" 
        self.assertEquals(self.google.getAnnualRetainedEarnings("DD"), {date(2007, 12, 31):9945.00, \
                                         date(2006, 12, 31):9679.00, \
                                         date(2005, 12, 31):7990.00, \
                                         date(2004, 12, 31):10182.00, \
                                         date(2003, 12, 31):10185.00, \
                                         date(2002, 12, 31):10619.00}) 
    def testAnnualTreasuryStock(self):
        """ Test that I find Annual Treasury Stock"""
        self.assertEquals(self.google.getAnnualTreasuryStock("DD"), {date(2007, 12, 31):-6727.00, \
                                      date(2006, 12, 31):-6727.00, \
                                      date(2005, 12, 31):-6727.00, \
                                      date(2004, 12, 31):-6727.00, \
                                      date(2003, 12, 31):-6727.00, \
                                      date(2002, 12, 31):-6727.00}) 
    def testAnnualOtherEquity(self):
        """ Test that I find Annual Other Equity""" 
        self.assertEquals(self.google.getAnnualOtherEquity("DD"), {date(2007, 12, 31):-794.00, \
                                    date(2006, 12, 31):-1867.00, \
                                    date(2005, 12, 31):-518.00, \
                                    date(2004, 12, 31):-423.00, \
                                    date(2003, 12, 31):-1761.00, \
                                    date(2002, 12, 31):-2767.00}) 
    def testAnnualTotalEquity(self):
        """ Test that I find Annual Total Equity"""
        self.assertEquals(self.google.getAnnualTotalEquity("DD"), {date(2007, 12, 31):11136.00, \
                                    date(2006, 12, 31):9422.00, \
                                    date(2005, 12, 31):8963.00, \
                                    date(2004, 12, 31):11377.00, \
                                    date(2003, 12, 31):9781.00, \
                                    date(2002, 12, 31):9063.00}) 
    def testAnnualTotalLiabilitiesAndShareholdersEquity(self):
        """ Test that I find Annual Total Liabilities And Shareholders Equity""" 
        self.assertEquals(self.google.getAnnualTotalLiabilitiesAndShareholdersEquity("DD"), {date(2007, 12, 31):34131.00, \
                                                              date(2006, 12, 31):31777.00, \
                                                              date(2005, 12, 31):33292.00, \
                                                              date(2004, 12, 31):35632.00, \
                                                              date(2003, 12, 31):37039.00, \
                                                              date(2002, 12, 31):34621.00}) 
    def testAnnualSharesOuts(self):
        """ Test that I find Annual Shares Outs""" 
        self.assertEquals(self.google.getAnnualSharesOuts("DD"), {date(2007, 12, 31):'-', \
                                   date(2006, 12, 31):'-', \
                                   date(2005, 12, 31):'-', \
                                   date(2004, 12, 31):'-', \
                                   date(2003, 12, 31):'-', \
                                   date(2002, 12, 31):'-'}) 
    def testAnnualTotalCommonSharesOutstanding(self):
        """ Test that I find Annual Total Common Shares Outstanding""" 
        self.assertEquals(self.google.getAnnualTotalCommonSharesOutstanding("DD"), {date(2007, 12, 31):899.29, \
                                                     date(2006, 12, 31):922.07, \
                                                     date(2005, 12, 31):919.61, \
                                                     date(2004, 12, 31):994.34, \
                                                     date(2003, 12, 31):997.28, \
                                                     date(2002, 12, 31):993.94})
         
 #Quarterly
 
    def testQuarterlyCashAndEquivalents(self):
        """ Test that I find Quarterly Cash And Equivalents"""
        self.assertEquals(self.google.getQuarterlyCashAndEquivalents("DD"), {date(2007, 12, 31):1305.00, \
                                           date(2007, 9, 30):1209.00, \
                                           date(2007, 6, 30):987.00, \
                                           date(2007, 3, 31):883.00, \
                                           date(2008, 3, 31):1094.00})
                                            
    def testQuarterlyShortTermInvestments(self):
        """ Test that I find Quarterly Short Term Investments""" 
        self.assertEquals(self.google.getQuarterlyShortTermInvestments("DD"), {date(2007, 12, 31):131.00, \
                                             date(2007, 9, 30):109.00, \
                                             date(2007, 6, 30):102.00, \
                                             date(2007, 3, 31):71.00, \
                                             date(2008, 3, 31):33.00})
                                              
    def testQuarterlyCashAndShortTermInvestments(self):
        """ Test that I find Quarterly Cash And Short Term Investments""" 
        self.assertEquals(self.google.getQuarterlyCashAndShortTermInvestments("DD"), {date(2007, 12, 31):1436.00, \
                                                    date(2007, 9, 30):1318.00, \
                                                    date(2007, 6, 30):1089.00, \
                                                    date(2007, 3, 31):954.00, \
                                                    date(2008, 3, 31):1127.00})
                                                     
    def testQuarterlyAccountsReceivableTrade(self):
        """ Test that I find Quarterly Accounts Receivable Trade"""
        self.assertEquals(self.google.getQuarterlyAccountsReceivableTrade("DD"), {date(2007, 12, 31):5683.00, \
                                                date(2007, 9, 30):6990.00, \
                                                date(2007, 6, 30):7370.00, \
                                                date(2007, 3, 31):6813.00, \
                                                date(2008, 3, 31):7645.00})
                                                
    def testQuarterlyReceivablesOther(self):
        """ Test that I find Quarterly Receivables Other"""
        self.assertEquals(self.google.getQuarterlyReceivablesOther("DD"), {date(2007, 12, 31):'-', \
                                         date(2007, 9, 30):'-', \
                                         date(2007, 6, 30):'-', \
                                         date(2007, 3, 31):'-', \
                                         date(2008, 3, 31):'-'})
                                          
    def testQuarterlyTotalReceivablesNet(self):
        """ Test that I find Quarterly Total Receivables Net""" 
        self.assertEquals(self.google.getQuarterlyTotalReceivablesNet("DD"), {date(2007, 12, 31):5683.00, \
                                            date(2007, 9, 30):6990.00, \
                                            date(2007, 6, 30):7370.00, \
                                            date(2007, 3, 31):6813.00, \
                                            date(2008, 3, 31):7645.00})
                                             
    def testQuarterlyTotalInventory(self):
        """ Test that I find Quarterly Total Inventory"""
        self.assertEquals(self.google.getQuarterlyTotalInventory("DD"), {date(2007, 12, 31):5278.00, \
                                       date(2007, 9, 30):4963.00, \
                                       date(2007, 6, 30):4481.00, \
                                       date(2007, 3, 31):4855.00, \
                                       date(2008, 3, 31):5310.00})
                                        
    def testQuarterlyPrepaidExpenses(self):
        """ Test that I find Quarterly Prepaid Expenses""" 
        self.assertEquals(self.google.getQuarterlyPrepaidExpenses("DD"), {date(2007, 12, 31):199.00, \
                                        date(2007, 9, 30):195.00, \
                                        date(2007, 6, 30):199.00, \
                                        date(2007, 3, 31):213.00, \
                                        date(2008, 3, 31):212.00})
                                         
    def testQuarterlyOtherCurrentAssetsTotal(self):
        """ Test that I find Quarterly Other Current Assets Total"""
        self.assertEquals(self.google.getQuarterlyOtherCurrentAssetsTotal("DD"), {date(2007, 12, 31):564.00, \
                                                date(2007, 9, 30):665.00, \
                                                date(2007, 6, 30):675.00, \
                                                date(2007, 3, 31):697.00, \
                                                date(2008, 3, 31):567.00})
                                                 
    def testQuarterlyTotalCurrentAssets(self):
        """ Test that I find Quarterly Total Current Assets"""
        self.assertEquals(self.google.getQuarterlyTotalCurrentAssets("DD"), {date(2007, 12, 31):13160.00, \
                                           date(2007, 9, 30):14131.00, \
                                           date(2007, 6, 30):13814.00, \
                                           date(2007, 3, 31):13532.00, \
                                           date(2008, 3, 31):14861.00})
                                            
    def testQuarterlyPPE(self):
        """ Test that I find Quarterly PPE"""
        self.assertEquals(self.google.getQuarterlyPPE("DD"), {date(2007, 12, 31):26593.00, \
                            date(2007, 9, 30):26302.00, \
                            date(2007, 6, 30):26053.00, \
                            date(2007, 3, 31):25876.00, \
                            date(2008, 3, 31):26941.00})
                             
    def testQuarterlyGoodwill(self):
        """ Test that I find Quarterly Goodwill"""
        self.assertEquals(self.google.getQuarterlyGoodwill("DD"), {date(2007, 12, 31):2074.00, \
                                 date(2007, 9, 30):2110.00, \
                                 date(2007, 6, 30):2108.00, \
                                 date(2007, 3, 31):2108.00, \
                                 date(2008, 3, 31):2074.00})
                                  
    def testQuarterlyIntangibles(self):
        """ Test that I find Quarterly Intangibles"""
        self.assertEquals(self.google.getQuarterlyIntangibles("DD"), {date(2007, 12, 31):2856.00, \
                                    date(2007, 9, 30):2904.00, \
                                    date(2007, 6, 30):2381.00, \
                                    date(2007, 3, 31):2436.00, \
                                    date(2008, 3, 31):2781.00})
                                     
    def testQuarterlyLongTermInvestments(self):
        """ Test that I find Quarterly Long Term Investments"""
        self.assertEquals(self.google.getQuarterlyLongTermInvestments("DD"), {date(2007, 12, 31):818.00, \
                                            date(2007, 9, 30):791.00, \
                                            date(2007, 6, 30):802.00, \
                                            date(2007, 3, 31):790.00, \
                                            date(2008, 3, 31):818.00})
                                             
    def testQuarterlyOtherLongTermAssets(self):
        """ Test that I find Quarterly Other Long Term Assets"""
        self.assertEquals(self.google.getQuarterlyOtherLongTermAssets("DD"), {date(2007, 12, 31):4363.00, \
                                            date(2007, 9, 30):3411.00, \
                                            date(2007, 6, 30):3267.00, \
                                            date(2007, 3, 31):3182.00, \
                                            date(2008, 3, 31):4789.00})
                                            
    def testQuarterlyTotalAssets(self):
        """ Test that I find Quarterly Total Assets"""
        self.assertEquals(self.google.getQuarterlyTotalAssets("DD"), {date(2007, 12, 31):34131.00, \
                                    date(2007, 9, 30):33915.00, \
                                    date(2007, 6, 30):32850.00, \
                                    date(2007, 3, 31):32473.00, \
                                    date(2008, 3, 31):36228.00})
                                     
    def testQuarterlyAccountsPayable(self):
        """ Test that I find Quarterly Accounts Payable""" 
        self.assertEquals(self.google.getQuarterlyAccountsPayable("DD"), {date(2007, 12, 31):3172.00, \
                                        date(2007, 9, 30):2873.00, \
                                        date(2007, 6, 30):2539.00, \
                                        date(2007, 3, 31):2782.00, \
                                        date(2008, 3, 31):3061.00})
                                         
    def testQuarterlyAccruedExpenses(self):
        """ Test that I find Quarterly Accrued Expenses"""
        self.assertEquals(self.google.getQuarterlyAccruedExpenses("DD"), {date(2007, 12, 31):3823.00, \
                                        date(2007, 9, 30):2972.00, \
                                        date(2007, 6, 30):2921.00, \
                                        date(2007, 3, 31):3020.00, \
                                        date(2008, 3, 31):3360.00})
                                         
    def testQuarterlyNotesPayable(self):
        """ Test that I find Quarterly Notes Payable"""
        self.assertEquals(self.google.getQuarterlyNotesPayable("DD"), {date(2007, 12, 31):1349.00, \
                                     date(2007, 9, 30):3618.00, \
                                     date(2007, 6, 30):1226.00, \
                                     date(2007, 3, 31):429.00, \
                                     date(2008, 3, 31):3196.00})
                                      
    def testQuarterlyCurrentPortLTDebtToCapital(self):
        """ Test that I find Quarterly Current Port LT Debt To Capital"""
        self.assertEquals(self.google.getQuarterlyCurrentPortLTDebtToCapital("DD"), {date(2007, 12, 31):21.00, \
                                                   date(2007, 9, 30):'-', \
                                                   date(2007, 6, 30):1149.00, \
                                                   date(2007, 3, 31):1161.00, \
                                                   date(2008, 3, 31):'-'})
                                                    
    def testQuarterlyOtherCurrentLiabilities(self):
        """ Test that I find Quarterly Other Current Liabilities"""
        self.assertEquals(self.google.getQuarterlyOtherCurrentLiabilities("DD"), {date(2007, 12, 31):176.00, \
                                                date(2007, 9, 30):334.00, \
                                                date(2007, 6, 30):369.00, \
                                                date(2007, 3, 31):422.00, \
                                                date(2008, 3, 31):177.00})
                                                 
    def testQuarterlyTotalCurrentLiabilities(self):
        """ Test that I find Quarterly Total Current Liabilities"""
        self.assertEquals(self.google.getQuarterlyTotalCurrentLiabilities("DD"), {date(2007, 12, 31):8541.00, \
                                                date(2007, 9, 30):9797.00, \
                                                date(2007, 6, 30):8204.00, \
                                                date(2007, 3, 31):7814.00, \
                                                date(2008, 3, 31):9794.00})
                                                 
    def testQuarterlyLongTermDebt(self):
        """ Test that I find Quarterly Long Term Debt"""
        self.assertEquals(self.google.getQuarterlyLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                     date(2007, 9, 30):5367.00, \
                                     date(2007, 6, 30):5664.00, \
                                     date(2007, 3, 31):6010.00, \
                                     date(2008, 3, 31):5784.00})
                                      
    def testQuarterlyCapitalLeaseObligations(self):
        """ Test that I find Quarterly Capital Lease Obligations"""
        self.assertEquals(self.google.getQuarterlyCapitalLeaseObligations("DD"), {date(2007, 12, 31):'-', \
                                                date(2007, 9, 30):'-', \
                                                date(2007, 6, 30):'-', \
                                                date(2007, 3, 31):'-', \
                                                date(2008, 3, 31):'-'})
                                                 
    def testQuarterlyTotalLongTermDebt(self):
        """ Test that I find Quarterly Total Long Term Debt"""
        self.assertEquals(self.google.getQuarterlyTotalLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                          date(2007, 9, 30):5367.00, \
                                          date(2007, 6, 30):5664.00, \
                                          date(2007, 3, 31):6010.00, \
                                          date(2008, 3, 31):5784.00})
                                           
    def testQuarterlyTotalDebt(self):
        """ Test that I find Quarterly Total Debt"""
        self.assertEquals(self.google.getQuarterlyTotalDebt("DD"), {date(2007, 12, 31):7325.00, \
                                  date(2007, 9, 30):8985.00, \
                                  date(2007, 6, 30):8039.00, \
                                  date(2007, 3, 31):7600.00, \
                                  date(2008, 3, 31):8980.00})
                                   
    def testQuarterlyDeferredIncomeTax(self):
        """ Test that I find Quarterly Deferred Income Tax"""
        self.assertEquals(self.google.getQuarterlyDeferredIncomeTax("DD"), {date(2007, 12, 31):802.00, \
                                          date(2007, 9, 30):404.00, \
                                          date(2007, 6, 30):395.00, \
                                          date(2007, 3, 31):402.00, \
                                          date(2008, 3, 31):894.00})
                                           
    def testQuarterlyMinorityInterest_Bal(self):
        """ Test that I find Quarterly Minority Interest(Balance Sheet)"""
        self.assertEquals(self.google.getQuarterlyMinorityInterest_Bal("DD"), {date(2007, 12, 31):442.00, \
                                         date(2007, 9, 30):445.00, \
                                         date(2007, 6, 30):442.00, \
                                         date(2007, 3, 31):442.00, \
                                         date(2008, 3, 31):443.00})
                                          
    def testQuarterlyOtherLiabilities(self):
        """ Test that I find Quarterly Other Liabilities"""
        self.assertEquals(self.google.getQuarterlyOtherLiabilities("DD"), {date(2007, 12, 31):7255.00, \
                                         date(2007, 9, 30):7984.00, \
                                         date(2007, 6, 30):7455.00, \
                                         date(2007, 3, 31):7629.00, \
                                         date(2008, 3, 31):7191.00})
                                          
    def testQuarterlyTotalLiabilities(self):
        """ Test that I find Quarterly Total Liabilities"""
        self.assertEquals(self.google.getQuarterlyTotalLiabilities("DD"), {date(2007, 12, 31):22995.00, \
                                         date(2007, 9, 30):23997.00, \
                                         date(2007, 6, 30):22160.00, \
                                         date(2007, 3, 31):22297.00, \
                                         date(2008, 3, 31):24106.00})
                                          
    def testQuarterlyRedeemablePreferredStock(self):
        """ Test that I find Quarterly Redeemable Preferred Stock"""
        self.assertEquals(self.google.getQuarterlyRedeemablePreferredStock("DD"), {date(2007, 12, 31):'-', \
                                                 date(2007, 9, 30):'-', \
                                                 date(2007, 6, 30):'-', \
                                                 date(2007, 3, 31):'-', \
                                                 date(2008, 3, 31):'-'})
                                                  
    def testQuarterlyPreferredStockNonRedeemable(self):
        """ Test that I find Quarterly Preferred Stock Non Redeemable"""
        self.assertEquals(self.google.getQuarterlyPreferredStockNonRedeemable("DD"), {date(2007, 12, 31):237.00, \
                                                    date(2007, 9, 30):237.00, \
                                                    date(2007, 6, 30):237.00, \
                                                    date(2007, 3, 31):237.00, \
                                                    date(2008, 3, 31):237.00})
                                                     
    def testQuarterlyCommonStock(self):
        """ Test that I find Quarterly Common Stock"""
        self.assertEquals(self.google.getQuarterlyCommonStock("DD"), {date(2007, 12, 31):296.00, \
                                    date(2007, 9, 30):296.00, \
                                    date(2007, 6, 30):302.00, \
                                    date(2007, 3, 31):303.00, \
                                    date(2008, 3, 31):296.00})
                                     
    def testQuarterlyAdditionalPaidInCapital(self):
        """ Test that I find Quarterly Additional Paid In Capital"""
        self.assertEquals(self.google.getQuarterlyAdditionalPaidInCapital("DD"), {date(2007, 12, 31):8179.00, \
                                                date(2007, 9, 30):8121.00, \
                                                date(2007, 6, 30):8187.00, \
                                                date(2007, 3, 31):8072.00, \
                                                date(2008, 3, 31):8220.00})
                                                 
    def testQuarterlyRetainedEarnings(self):
        """ Test that I find Quarterly Retained Earnings"""
        self.assertEquals(self.google.getQuarterlyRetainedEarnings("DD"), {date(2007, 12, 31):9945.00, \
                                         date(2007, 9, 30):9772.00, \
                                         date(2007, 6, 30):10516.00, \
                                         date(2007, 3, 31):10142.00, \
                                         date(2008, 3, 31):10764.00})
                                          
    def testQuarterlyTreasuryStock(self):
        """ Test that I find Quarterly Treasury Stock"""
        self.assertEquals(self.google.getQuarterlyTreasuryStock("DD"), {date(2007, 12, 31):-6727.00, \
                                      date(2007, 9, 30):-6727.00, \
                                      date(2007, 6, 30):-6727.00, \
                                      date(2007, 3, 31):-6727.00, \
                                      date(2008, 3, 31):-6727.00})
                                       
    def testQuarterlyOtherEquity(self):
        """ Test that I find Quarterly Other Equity"""
        self.assertEquals(self.google.getQuarterlyOtherEquity("DD"), {date(2007, 12, 31):-794.00, \
                                    date(2007, 9, 30):-1781.00, \
                                    date(2007, 6, 30):-1825.00, \
                                    date(2007, 3, 31):-1851.00, \
                                    date(2008, 3, 31):-668.00})
                                     
    def testQuarterlyTotalEquity(self):
        """ Test that I find Quarterly Total Equity"""
        self.assertEquals(self.google.getQuarterlyTotalEquity("DD"), {date(2007, 12, 31):11136.00, \
                                    date(2007, 9, 30):9918.00, \
                                    date(2007, 6, 30):10690.00, \
                                    date(2007, 3, 31):10176.00, \
                                    date(2008, 3, 31):12122.00})
                                     
    def testQuarterlyTotalLiabilitiesAndShareholdersEquity(self):
        """ Test that I find Quarterly Total Liabilities And Shareholders Equity"""
        self.assertEquals(self.google.getQuarterlyTotalLiabilitiesAndShareholdersEquity("DD"), {date(2007, 12, 31):34131.00, \
                                                              date(2007, 9, 30):33915.00, \
                                                              date(2007, 6, 30):32850.00, \
                                                              date(2007, 3, 31):32473.00, \
                                                              date(2008, 3, 31):36228.00})
                                                               
    def testQuarterlySharesOuts(self):
        """ Test that I find Quarterly Shares Outs"""
        self.assertEquals(self.google.getQuarterlySharesOuts("DD"), {date(2007, 12, 31):'-', \
                                   date(2007, 9, 30):'-', \
                                   date(2007, 6, 30):'-', \
                                   date(2007, 3, 31):'-', \
                                   date(2008, 3, 31):'-'})
                                    
    def testQuarterlyTotalCommonSharesOutstanding(self):
        """ Test that I find Quarterly Total Common Shares Outstanding"""
        self.assertEquals(self.google.getQuarterlyTotalCommonSharesOutstanding("DD"), {date(2007, 12, 31):899.29, \
                                                     date(2007, 9, 30):898.93, \
                                                     date(2007, 6, 30):920.27, \
                                                     date(2007, 3, 31):923.60, \
                                                     date(2008, 3, 31):900.52})
 
class WebsiteTestCase_CashFlow(WebsiteTestCase):    
    """ Test all the information that comes from an SEC Cash Flow Statement """
    def testAnnualNetIncomeStartingLine(self):
        """ Test that I find Annual Net Income or Starting Line"""
        self.assertEquals(self.google.getAnnualNetIncomeStartingLine("DD"), {date(2007, 12, 31):2988.00, \
                                              date(2006, 12, 31):3148.00, \
                                              date(2005, 12, 31):2056.00, \
                                              date(2004, 12, 31):1780.00, \
                                              date(2003, 12, 31):973.00, \
                                              date(2002, 12, 31):-1103.00})
    def testAnnualDepreciationDepletion(self):
        """ Test that I find Annual Depreciation Depletion"""  
        self.assertEquals(self.google.getAnnualDepreciationDepletion("DD"), {date(2007, 12, 31):1158.00, \
                                              date(2006, 12, 31):1157.00, \
                                              date(2005, 12, 31):1128.00, \
                                              date(2004, 12, 31):1124.00, \
                                              date(2003, 12, 31):1355.00, \
                                              date(2002, 12, 31):1297.00})
    def testAnnualAmortization(self):
        """ Test that I find Annual Amortization"""  
        self.assertEquals(self.google.getAnnualAmortization("DD"), {date(2007, 12, 31):213.00, \
                                     date(2006, 12, 31):227.00, \
                                     date(2005, 12, 31):230.00, \
                                     date(2004, 12, 31):223.00, \
                                     date(2003, 12, 31):229.00, \
                                     date(2002, 12, 31):218.00}) 
    def testAnnualDeferredTaxes(self):
        """ Test that I find Annual Deferred Taxes"""
        self.assertEquals(self.google.getAnnualDeferredTaxes("DD"), {date(2007, 12, 31):-1.00, \
                                      date(2006, 12, 31):-615.00, \
                                      date(2005, 12, 31):109.00, \
                                      date(2004, 12, 31):'-', \
                                      date(2003, 12, 31):'-', \
                                      date(2002, 12, 31):'-'}) 
    def testAnnualNonCashItems(self):
        """ Test that I find Annual Non Cash Items"""
        self.assertEquals(self.google.getAnnualNonCashItems("DD"), {date(2007, 12, 31):88.00, \
                                     date(2006, 12, 31):-93.00, \
                                     date(2005, 12, 31):-1703.00, \
                                     date(2004, 12, 31):732.00, \
                                     date(2003, 12, 31):2278.00, \
                                     date(2002, 12, 31):3752.00}) 
    def testAnnualChangesInWorkingCapital(self):
        """ Test that I find Annual Changes In Working Capital"""
        self.assertEquals(self.google.getAnnualChangesInWorkingCapital("DD"), {date(2007, 12, 31):-156.00, \
                                                date(2006, 12, 31):-88.00, \
                                                date(2005, 12, 31):722.00, \
                                                date(2004, 12, 31):-628.00, \
                                                date(2003, 12, 31):-2246.00, \
                                                date(2002, 12, 31):-1725.00}) 
    def testAnnualCashFromOperatingActivities(self):
        """ Test that I find Annual Cash From Operating Activities"""
        self.assertEquals(self.google.getAnnualCashFromOperatingActivities("DD"), {date(2007, 12, 31):4290.00, \
                                                    date(2006, 12, 31):3736.00, \
                                                    date(2005, 12, 31):2542.00, \
                                                    date(2004, 12, 31):3231.00, \
                                                    date(2003, 12, 31):2589.00, \
                                                    date(2002, 12, 31):2439.00})
    def testAnnualCapitalExpenditures(self):
        """ Test that I find Annual Capital Expenditures"""
        self.assertEquals(self.google.getAnnualCapitalExpenditures("DD"), {date(2007, 12, 31):-1585.00, \
                                            date(2006, 12, 31):-1532.00, \
                                            date(2005, 12, 31):-1340.00, \
                                            date(2004, 12, 31):-1232.00, \
                                            date(2003, 12, 31):-1713.00, \
                                            date(2002, 12, 31):-1280.00}) 
    def testAnnualOtherInvestingCashFlow(self):
        """ Test that I find Annual Other Investing Cash Flow"""
        self.assertEquals(self.google.getAnnualOtherInvestingCashFlow("DD"), {date(2007, 12, 31):-165.00, \
                                               date(2006, 12, 31):187.00, \
                                               date(2005, 12, 31):738.00, \
                                               date(2004, 12, 31):3168.00, \
                                               date(2003, 12, 31):-1662.00, \
                                               date(2002, 12, 31):-1312.00}) 
    def testAnnualCashFromInvestingActivities(self):
        """ Test that I find Annual Cash From Investing Activities"""
        self.assertEquals(self.google.getAnnualCashFromInvestingActivities("DD"), {date(2007, 12, 31):-1750.00, \
                                                    date(2006, 12, 31):-1345.00, \
                                                    date(2005, 12, 31):-602.00, \
                                                    date(2004, 12, 31):1936.00, \
                                                    date(2003, 12, 31):-3375.00, \
                                                    date(2002, 12, 31):-2592.00}) 
    def testAnnualFinancingCashFlowItems(self):
        """ Test that I find Annual Financing Cash Flow Items"""
        self.assertEquals(self.google.getAnnualFinancingCashFlowItems("DD"), {date(2007, 12, 31):-67.00, \
                                               date(2006, 12, 31):-22.00, \
                                               date(2005, 12, 31):-13.00, \
                                               date(2004, 12, 31):-79.00, \
                                               date(2003, 12, 31):-2005.00, \
                                               date(2002, 12, 31):0.00}) 
    def testAnnualTotalCashDividendsPaid(self):
        """ Test that I find Annual Total Cash Dividends Paid"""
        self.assertEquals(self.google.getAnnualTotalCashDividendsPaid("DD"), {date(2007, 12, 31):-1409.00, \
                                               date(2006, 12, 31):-1378.00, \
                                               date(2005, 12, 31):-1439.00, \
                                               date(2004, 12, 31):-1404.00, \
                                               date(2003, 12, 31):-1407.00, \
                                               date(2002, 12, 31):-1401.00}) 
    def testAnnualIssuanceOfStock(self):
        """ Test that I find Annual Issuance Of Stock"""
        self.assertEquals(self.google.getAnnualIssuanceOfStock("DD"), {date(2007, 12, 31):-1250.00, \
                                        date(2006, 12, 31):-132.00, \
                                        date(2005, 12, 31):-3171.00, \
                                        date(2004, 12, 31):-260.00, \
                                        date(2003, 12, 31):52.00, \
                                        date(2002, 12, 31):-436.00}) 
    def testAnnualIssuanceOfDebt(self):
        """ Test that I find Annual Issuance Of Debt"""
        self.assertEquals(self.google.getAnnualIssuanceOfDebt("DD"), {date(2007, 12, 31):-343.00, \
                                       date(2006, 12, 31):-791.00, \
                                       date(2005, 12, 31):1772.00, \
                                       date(2004, 12, 31):-3807.00, \
                                       date(2003, 12, 31):3391.00, \
                                       date(2002, 12, 31):-281.00}) 
    def testAnnualCashFromFinancingActivities(self):
        """ Test that I find Annual Cash From Financing Activities"""
        self.assertEquals(self.google.getAnnualCashFromFinancingActivities("DD"), {date(2007, 12, 31):-3069.00, \
                                                    date(2006, 12, 31):-2323.00, \
                                                    date(2005, 12, 31):-2851.00, \
                                                    date(2004, 12, 31):-5550.00, \
                                                    date(2003, 12, 31):31.00, \
                                                    date(2002, 12, 31):-2118.00}) 
    def testAnnualForeignExchangeEffects(self):
        """ Test that I find Annual Foreign Exchange Effects"""
        self.assertEquals(self.google.getAnnualForeignExchangeEffects("DD"), {date(2007, 12, 31):20.00, \
                                               date(2006, 12, 31):10.00, \
                                               date(2005, 12, 31):-722.00, \
                                               date(2004, 12, 31):404.00, \
                                               date(2003, 12, 31):425.00, \
                                               date(2002, 12, 31):186.00}) 
    def testAnnualNetChangeInCash(self):
        """ Test that I find Annual Net Change In Cash"""
        self.assertEquals(self.google.getAnnualNetChangeInCash("DD"), {date(2007, 12, 31):-509.00, \
                                        date(2006, 12, 31):78.00, \
                                        date(2005, 12, 31):-1633.00, \
                                        date(2004, 12, 31):21.00, \
                                        date(2003, 12, 31):-330.00, \
                                        date(2002, 12, 31):-2085.00}) 
    def testAnnualCashInterestPaid(self):
        """ Test that I find Annual Cash Interest Paid"""
        self.assertEquals(self.google.getAnnualCashInterestPaid("DD"), {date(2007, 12, 31):527.00, \
                                         date(2006, 12, 31):295.00, \
                                         date(2005, 12, 31):479.00, \
                                         date(2004, 12, 31):366.00, \
                                         date(2003, 12, 31):357.00, \
                                         date(2002, 12, 31):402.00}) 
    def testAnnualCashTaxesPaid(self):
        """ Test that I find Annual Cash Taxes Paid"""
        self.assertEquals(self.google.getAnnualCashTaxesPaid("DD"), {date(2007, 12, 31):795.00, \
                                      date(2006, 12, 31):899.00, \
                                      date(2005, 12, 31):355.00, \
                                      date(2004, 12, 31):521.00, \
                                      date(2003, 12, 31):278.00, \
                                      date(2002, 12, 31):1691.00}) 
 
        #quarterly
        
    def testQuarterlyNetIncomeStartingLine(self):
        """ Test that I find Quarterly Net Income or Starting Line"""
        self.assertEquals(self.google.getQuarterlyNetIncomeStartingLine("DD"), {date(2008, 3, 31): 1191.00,\
																			    date(2007, 12, 31):545.00, \
                                              date(2007, 9, 30):526.00, \
                                              date(2007, 6, 30):972.00, \
                                              date(2007, 3, 31):945.00})
                                              
                                              
    def testQuarterlyDepreciationDepletion(self):
        """ Test that I find Quarterly Depreciation Depletion"""
        self.assertEquals(self.google.getQuarterlyDepreciationDepletion("DD"), {date(2008, 3, 31): 287.0,\
																			    date(2007, 12, 31):292.00, \
                                              date(2007, 9, 30):287.00, \
                                              date(2007, 6, 30):289.00, \
                                              date(2007, 3, 31):290.00})
                                              
                                              
    def testQuarterlyAmortization(self):
        """ Test that I find Quarterly Amortization""" 
        self.assertEquals(self.google.getQuarterlyAmortization("DD"), {date(2008, 3, 31): 93.00,\
																	   date(2007, 12, 31):50.00, \
                                     date(2007, 9, 30):53.00, \
                                     date(2007, 6, 30):54.00, \
                                     date(2007, 3, 31):56.00})
                                     
                                      
    def testQuarterlyDeferredTaxes(self):
        """ Test that I find Quarterly Deferred Taxes"""
        self.assertEquals(self.google.getQuarterlyDeferredTaxes("DD"), {date(2008, 3, 31): '-',\
																	    date(2007, 12, 31):'-', \
                                      date(2007, 9, 30):'-', \
                                      date(2007, 6, 30):'-', \
                                      date(2007, 3, 31):'-'})
                                      
                                       
    def testQuarterlyNonCashItems(self):
        """ Test that I find Quarterly Non Cash Items"""
        self.assertEquals(self.google.getQuarterlyNonCashItems("DD"), {date(2008, 3, 31): -9.00,\
																	   date(2007, 12, 31):164.00, \
                                     date(2007, 9, 30):-32.00, \
                                     date(2007, 6, 30):-33.00, \
                                     date(2007, 3, 31):-11.00})
                                     
                                      
    def testQuarterlyChangesInWorkingCapital(self):
        """ Test that I find Quarterly Changes In Working Capital"""
        self.assertEquals(self.google.getQuarterlyChangesInWorkingCapital("DD"), {date(2008, 3, 31): -2513.00,\
																				  date(2007, 12, 31):1814.00, \
                                                date(2007, 9, 30):209.00, \
                                                date(2007, 6, 30):-659.00, \
                                                date(2007, 3, 31):-1520.00})
                                                
                                                 
    def testQuarterlyCashFromOperatingActivities(self):
        """ Test that I find Quarterly Cash From Operating Activities"""
        self.assertEquals(self.google.getQuarterlyCashFromOperatingActivities("DD"), {date(2008, 3, 31): -951.00,\
																					  date(2007, 12, 31):2864.00, \
                                                    date(2007, 9, 30):1043.00, \
                                                    date(2007, 6, 30):623.00, \
                                                    date(2007, 3, 31):-240.00})
                                                    
                                                    
    def testQuarterlyCapitalExpenditures(self):
        """ Test that I find Quarterly Capital Expenditures"""
        self.assertEquals(self.google.getQuarterlyCapitalExpenditures("DD"), {date(2008, 3, 31): -410.00,\
																			  date(2007, 12, 31):-566.00, \
                                            date(2007, 9, 30):-398.00, \
                                            date(2007, 6, 30):-348.00, \
                                            date(2007, 3, 31):-273.00})
                                            
                                             
    def testQuarterlyOtherInvestingCashFlow(self):
        """ Test that I find Quarterly Other Investing Cash Flow"""
        self.assertEquals(self.google.getQuarterlyOtherInvestingCashFlow("DD"), {date(2008, 3, 31): -110.00,\
																				 date(2007, 12, 31):-164.00, \
                                               date(2007, 9, 30):50.00, \
                                               date(2007, 6, 30):-55.00, \
                                               date(2007, 3, 31):4.00})
                                               
                                                
    def testQuarterlyCashFromInvestingActivities(self):
        """ Test that I find Quarterly Cash From Investing Activities"""
        self.assertEquals(self.google.getQuarterlyCashFromInvestingActivities("DD"), {date(2008, 3, 31): -520.00,\
																					  date(2007, 12, 31):-730.00, \
                                                    date(2007, 9, 30):-348.00, \
                                                    date(2007, 6, 30):-403.00, \
                                                    date(2007, 3, 31):-269.00})
                                                    
                                                     
    def testQuarterlyFinancingCashFlowItems(self):
        """ Test that I find Quarterly Financing Cash Flow Items"""
        self.assertEquals(self.google.getQuarterlyFinancingCashFlowItems("DD"), {date(2008, 3, 31): 4.00,\
																				 date(2007, 12, 31):5.00, \
                                               date(2007, 9, 30):8.00, \
                                               date(2007, 6, 30):-11.00, \
                                               date(2007, 3, 31):-69.00})
                                               
                                                
    def testQuarterlyTotalCashDividendsPaid(self):
        """ Test that I find Quarterly Total Cash Dividends Paid"""
        self.assertEquals(self.google.getQuarterlyTotalCashDividendsPaid("DD"), {date(2008, 3, 31): -372.00,\
																				 date(2007, 12, 31):-372.00, \
                                               date(2007, 9, 30):-345.00, \
                                               date(2007, 6, 30):-345.00, \
                                               date(2007, 3, 31):-347.00})
                                               
                                                
    def testQuarterlyIssuanceOfStock(self):
        """ Test that I find Quarterly Issuance Of Stock"""
        self.assertEquals(self.google.getQuarterlyIssuanceOfStock("DD"), {date(2008, 3, 31): 19.00,\
																		  date(2007, 12, 31):14.00, \
                                        date(2007, 9, 30):-1029.00, \
                                        date(2007, 6, 30):-185.00, \
                                        date(2007, 3, 31):-50.00})
                                        
                                         
    def testQuarterlyIssuanceOfDebt(self):
        """ Test that I find Quarterly Issuance Of Debt"""
        self.assertEquals(self.google.getQuarterlyIssuanceOfDebt("DD"), {date(2008, 3, 31): 1611.00,\
																		 date(2007, 12, 31):-1673.00, \
                                       date(2007, 9, 30):858.00, \
                                       date(2007, 6, 30):431.00, \
                                       date(2007, 3, 31):41.00})
                                       
                                        
    def testQuarterlyCashFromFinancingActivities(self):
        """ Test that I find Quarterly Cash From Financing Activities"""
        self.assertEquals(self.google.getQuarterlyCashFromFinancingActivities("DD"), {date(2008, 3, 31): 1262.00,\
																					  date(2007, 12, 31):-2026.00, \
                                                    date(2007, 9, 30):-508.00, \
                                                    date(2007, 6, 30):-110.00, \
                                                    date(2007, 3, 31):-425.00})
                                                    
                                                     
    def testQuarterlyForeignExchangeEffects(self):
        """ Test that I find Quarterly Foreign Exchange Effects"""
        self.assertEquals(self.google.getQuarterlyForeignExchangeEffects("DD"), {date(2008, 3, 31): -2.00,\
																				 date(2007, 12, 31):-12.00, \
                                               date(2007, 9, 30):35.00, \
                                               date(2007, 6, 30):-6.00, \
                                               date(2007, 3, 31):3.00})
                                               
                                                
    def testQuarterlyNetChangeInCash(self):
        """ Test that I find Quarterly Net Change In Cash"""
        self.assertEquals(self.google.getQuarterlyNetChangeInCash("DD"), {date(2008, 3, 31): -211.00,\
																		  date(2007, 12, 31):96.00, \
                                        date(2007, 9, 30):222.00, \
                                        date(2007, 6, 30):104.00, \
                                        date(2007, 3, 31):-931.00})
                                        
                                         
    def testQuarterlyCashInterestPaid(self):
        """ Test that I find Quarterly Cash Interest Paid"""
        self.assertEquals(self.google.getQuarterlyCashInterestPaid("DD"), {date(2008, 3, 31): '-',\
																		   date(2007, 12, 31):'-', \
                                         date(2007, 9, 30):'-', \
                                         date(2007, 6, 30):'-', \
                                         date(2007, 3, 31):'-'})
                                         
                                          
    def testQuarterlyCashTaxesPaid(self):
        """ Test that I find Quarterly Cash Taxes Paid"""
        self.assertEquals(self.google.getQuarterlyCashTaxesPaid("DD"), {date(2008, 3, 31): '-',\
																	    date(2007, 12, 31):'-', \
                                      date(2007, 9, 30):'-', \
                                      date(2007, 6, 30):'-', \
                                      date(2007, 3, 31):'-'})
 
 
if __name__ == "__main__": #for coverage tests
	unittest.main()
                                       
