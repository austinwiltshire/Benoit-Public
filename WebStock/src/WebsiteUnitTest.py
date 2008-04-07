import Website
#making a change.
from TestTools import assertClose, compareDicts
from datetime import date
import doctest
import contract
import unittest

contract.checkmod(Website)

#val = doctest.testmod(Website)
#print val, "VALuE"
#assert val == (0, 40)

def suite():
    return unittest.TestSuite((unittest.makeSuite(WebsiteTestCase_IncomeStatement, "test"), \
							   unittest.makeSuite(WebsiteTestCase_BalanceSheet, 'test'), \
							   unittest.makeSuite(WebsiteTestCase_CashFlowStatement, 'test'), \
							   doctest.DocTestSuite(Website)))

class WebsiteTestCase(unittest.TestCase):
    def setUp(self):
        self.google = Website.Google()
        
    def tearDown(self):
        del self.google
        self.google = None
        
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
        """ Test that I find Annual DepreciationAmortization"""
        self.assertEquals(self.google.getAnnualDepreciationAmortization("DD"), {date(2007, 12, 31):213.00, \
                                                 date(2006, 12, 31):227.00, \
                                                 date(2005, 12, 31):230.00, \
                                                 date(2004, 12, 31):223.00, \
                                                 date(2003, 12, 31):229.00, \
                                                 date(2002, 12, 31):218.00})        
        
    def testAnnualInterestNetOperating(self):
        """ Test that I find Annual InterestNetOperating"""
        self.assertEquals(self.google.getAnnualInterestNetOperating("DD"), {date(2007, 12, 31):430.00, \
                                             date(2006, 12, 31):460.00, \
                                             date(2005, 12, 31):518.00, \
                                             date(2004, 12, 31):362.00, \
                                             date(2003, 12, 31):347.00, \
                                             date(2002, 12, 31):359.00})
        
    def testAnnualUnusualExpense(self):
        """ Test that I find Annual UnusualExpense"""
        self.assertEquals(self.google.getAnnualUnusualExpense("DD"), {date(2007, 12, 31):0.00, \
                                       date(2006, 12, 31):0.00, \
                                       date(2005, 12, 31):-62.00, \
                                       date(2004, 12, 31):667.00, \
                                       date(2003, 12, 31):1898.00, \
                                       date(2002, 12, 31):290.00})
        
    def testAnnualOtherOperatingExpenses(self):
        """ Test that I find Annual OtherOperatingExpenses"""
        self.assertEquals(self.google.getAnnualOtherOperatingExpenses("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):-62.00, \
                                               date(2002, 12, 31):-25.00})
        
    def testAnnualTotalOperatingExpense(self):
        """ Test that I find Annual TotalOperatingExpense"""
        self.assertEquals(self.google.getAnnualTotalOperatingExpense("DD"), {date(2007, 12, 31):26910.00, \
                                              date(2006, 12, 31):25653.00, \
                                              date(2005, 12, 31):24928.00, \
                                              date(2004, 12, 31):26553.00, \
                                              date(2003, 12, 31):27587.00, \
                                              date(2002, 12, 31):22398.00})
        
    def testAnnualOperatingIncome(self):
        """ Test that I find Annual OperatingIncome"""
        self.assertEquals(self.google.getAnnualOperatingIncome("DD"), {date(2007, 12, 31):3743.00, \
                                        date(2006, 12, 31):3329.00, \
                                        date(2005, 12, 31):3563.00, \
                                        date(2004, 12, 31):1442.00, \
                                        date(2003, 12, 31):143.00, \
                                        date(2002, 12, 31):2124.00})
        
    def testAnnualInterestIncome(self):
        """ Test that I find Annual InterestIncome"""
        self.assertEquals(self.google.getAnnualInterestIncome("DD"), {date(2007, 12, 31):'-', \
                                       date(2006, 12, 31):'-', \
                                       date(2005, 12, 31):'-', \
                                       date(2004, 12, 31):'-', \
                                       date(2003, 12, 31):'-', \
                                       date(2002, 12, 31):'-'})
        
    def testAnnualGainOnSaleOfAssets(self):
        """ Test that I find Annual GainOnSaleOfAssets"""
        self.assertEquals(self.google.getAnnualGainOnSaleOfAssets("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'})
        
    def testAnnualOtherNet(self):
        """ Test that I find Annual OtherNet"""
        self.assertEquals(self.google.getAnnualOtherNet("DD"), {date(2007, 12, 31):'-', \
                                 date(2006, 12, 31):'-', \
                                 date(2005, 12, 31):'-', \
                                 date(2004, 12, 31):'-', \
                                 date(2003, 12, 31):'-', \
                                 date(2002, 12, 31):'-'})
        
    def testAnnualIncomeBeforeTax(self):
        """ Test that I find Annual IncomeBeforeTax"""
        self.assertEquals(self.google.getAnnualIncomeBeforeTax("DD"), {date(2007, 12, 31):3743.00, \
                                        date(2006, 12, 31):3329.00, \
                                        date(2005, 12, 31):3563.00, \
                                        date(2004, 12, 31):1442.00, \
                                        date(2003, 12, 31):143.00, \
                                        date(2002, 12, 31):2124.00})
        
    def testAnnualIncomeAfterTax(self):
        """ Test that I find Annual IncomeAfterTax"""
        self.assertEquals(self.google.getAnnualIncomeAfterTax("DD"), {date(2007, 12, 31):2995.0, \
                                       date(2006, 12, 31):3133.00, \
                                       date(2005, 12, 31):2093.00, \
                                       date(2004, 12, 31):1771.00, \
                                       date(2003, 12, 31):1073.00, \
                                       date(2002, 12, 31):1939.00})
        
    def testAnnualMinorityInterest_Inc(self):
        """ Test that I find Annual MinorityInterest_Inc"""
        self.assertEquals(self.google.getAnnualMinorityInterest_Inc("DD"), {date(2007, 12, 31):-7.00, \
                                         date(2006, 12, 31):15.00, \
                                         date(2005, 12, 31):-37.00, \
                                         date(2004, 12, 31):9.00, \
                                         date(2003, 12, 31):-71.00, \
                                         date(2002, 12, 31):-98.00})
        
    def testAnnualEquityInAffiliates(self):
        """ Test that I find Annual EquityInAffiliates"""
        self.assertEquals(self.google.getAnnualEquityInAffiliates("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'})
        
    def testAnnualNetIncomeBeforeExtraItems(self):
        """ Test that I find Annual NetIncomeBeforeExtraItems"""
        self.assertEquals(self.google.getAnnualNetIncomeBeforeExtraItems("DD"), {date(2007, 12, 31):2988.00, \
                                                  date(2006, 12, 31):3148.00, \
                                                  date(2005, 12, 31):2056.00, \
                                                  date(2004, 12, 31):1780.00, \
                                                  date(2003, 12, 31):1002.00, \
                                                  date(2002, 12, 31):1841.00})
        
    def testAnnualAccountingChange(self):
        """ Test that I find Annual AccountingChange"""
        self.assertEquals(self.google.getAnnualAccountingChange("DD"), {date(2007, 12, 31):'-', \
                                         date(2006, 12, 31):'-', \
                                         date(2005, 12, 31):'-', \
                                         date(2004, 12, 31):'-', \
                                         date(2003, 12, 31):'-', \
                                         date(2002, 12, 31):'-'})
        
    def testAnnualDiscontinuedOperations(self):
        """ Test that I find Annual DiscontinuedOperations"""
        self.assertEquals(self.google.getAnnualDiscontinuedOperations("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'})                                                                
        
    def testAnnualExtraordinaryItem(self):
        """ Test that I find Annual ExtraordinaryItem"""
        self.assertEquals(self.google.getAnnualExtraordinaryItem("DD"), {date(2007, 12, 31):'-', \
                                          date(2006, 12, 31):'-', \
                                          date(2005, 12, 31):'-', \
                                          date(2004, 12, 31):'-', \
                                          date(2003, 12, 31):'-', \
                                          date(2002, 12, 31):'-'})
        
    def testAnnualNetIncome(self):
        """ Test that I find Annual NetIncome"""
        self.assertEquals(self.google.getAnnualNetIncome("DD"), {date(2007, 12, 31):2988.00, \
                                  date(2006, 12, 31):3148.00, \
                                  date(2005, 12, 31):2056.00, \
                                  date(2004, 12, 31):1780.00, \
                                  date(2003, 12, 31):973.00, \
                                  date(2002, 12, 31):-1103.00})
        
    def testAnnualPreferredDividends(self):
        """ Test that I find Annual PreferredDividends"""
        self.assertEquals(self.google.getAnnualPreferredDividends("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'})
        
    def testAnnualIncomeAvailToCommonExclExtraItems(self):
        """ Test that I find Annual IncomeAvailToCommonExclExtraItems"""
        self.assertEquals(self.google.getAnnualIncomeAvailToCommonExclExtraItems("DD"), {date(2007, 12, 31):2978.00, \
                                                          date(2006, 12, 31):3138.00, \
                                                          date(2005, 12, 31):2046.00, \
                                                          date(2004, 12, 31):1770.00, \
                                                          date(2003, 12, 31):992.00, \
                                                          date(2002, 12, 31):1831.00})
        
    def testAnnualIncomeAvailToCommonInclExtraItems(self):
        """ Test that I find Annual IncomeAvailToCommonInclExtraItems"""
        self.assertEquals(self.google.getAnnualIncomeAvailToCommonInclExtraItems("DD"), {date(2007, 12, 31):2978.00, \
                                                          date(2006, 12, 31):3138.00, \
                                                          date(2005, 12, 31):2046.00, \
                                                          date(2004, 12, 31):1770.00, \
                                                          date(2003, 12, 31):963.00, \
                                                          date(2002, 12, 31):-1113.00})                                
        
    def testAnnualBasicWeightedAverageShares(self):
        """ Test that I find Annual BasicWeightedAverageShares"""
        self.assertEquals(self.google.getAnnualBasicWeightedAverageShares("DD"), {date(2007, 12, 31):'-', \
                                                   date(2006, 12, 31):'-', \
                                                   date(2005, 12, 31):'-', \
                                                   date(2004, 12, 31):'-', \
                                                   date(2003, 12, 31):'-', \
                                                   date(2002, 12, 31):'-'})
        
    def testAnnualBasicEPSExclExtraItems(self):
        """ Test that I find Annual BasicEPSExclExtraItems"""
        self.assertEquals(self.google.getAnnualBasicEPSExclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'})
        
    def testAnnualBasicEPSInclExtraItems(self):
        """ Test that I find Annual BasicEPSInclExtraItems"""
        self.assertEquals(self.google.getAnnualBasicEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'})
        
    def testAnnualDilutionAdjustment(self):
        """ Test that I find Annual DilutionAdjustment"""
        self.assertEquals(self.google.getAnnualDilutionAdjustment("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):0.00, \
                                           date(2002, 12, 31):0.00})
        
    def testAnnualDilutedWeightedAverageShares(self):
        """ Test that I find Annual DilutedWeightedAverageShares"""
        self.assertEquals(self.google.getAnnualDilutedWeightedAverageShares("DD"), {date(2007, 12, 31):925.40, \
                                                     date(2006, 12, 31):928.60, \
                                                     date(2005, 12, 31):988.95, \
                                                     date(2004, 12, 31):1003.39, \
                                                     date(2003, 12, 31):1000.01, \
                                                     date(2002, 12, 31):998.74})                                        
        
    def testAnnualDilutedEPSExclExtraItems(self):
        """ Test that I find Annual DilutedEPSExclExtraItems"""
        self.assertEquals(self.google.getAnnualDilutedEPSExclExtraItems("DD"), {date(2007, 12, 31):3.22, \
                                                 date(2006, 12, 31):3.38, \
                                                 date(2005, 12, 31):2.07, \
                                                 date(2004, 12, 31):1.76, \
                                                 date(2003, 12, 31):0.99, \
                                                 date(2002, 12, 31):1.83})
        
    def testAnnualDilutedEPSInclExtraItems(self):
        """ Test that I find Annual DilutedEPSInclExtraItems"""
        self.assertEquals(self.google.getAnnualDilutedEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                                 date(2006, 12, 31):'-', \
                                                 date(2005, 12, 31):'-', \
                                                 date(2004, 12, 31):'-', \
                                                 date(2003, 12, 31):'-', \
                                                 date(2002, 12, 31):'-'})
        
    def testAnnualDividendsPerShare(self):
        """ Test that I find Annual DividendsPerShare"""
        self.assertEquals(self.google.getAnnualDividendsPerShare("DD"), {date(2007, 12, 31):1.52, \
                                          date(2006, 12, 31):1.48, \
                                          date(2005, 12, 31):1.46, \
                                          date(2004, 12, 31):1.40, \
                                          date(2003, 12, 31):1.40, \
                                          date(2002, 12, 31):1.40})
        
    def testAnnualGrossDividends(self):
        """ Test that I find Annual GrossDividends"""
        self.assertEquals(self.google.getAnnualGrossDividends("DD"), {date(2007, 12, 31):'-', \
                                       date(2006, 12, 31):'-', \
                                       date(2005, 12, 31):'-', \
                                       date(2004, 12, 31):'-', \
                                       date(2003, 12, 31):'-', \
                                       date(2002, 12, 31):'-'})
        
    def testAnnualNetIncomeAfterCompExp(self):
        """ Test that I find Annual NetIncomeAfterCompExp"""
        self.assertEquals(self.google.getAnnualNetIncomeAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                              date(2006, 12, 31):'-', \
                                              date(2005, 12, 31):'-', \
                                              date(2004, 12, 31):'-', \
                                              date(2003, 12, 31):'-', \
                                              date(2002, 12, 31):'-'})
        
    def testAnnualBasicEPSAfterCompExp(self):
        """ Test that I find Annual BasicEPSAfterCompExp"""
        self.assertEquals(self.google.getAnnualBasicEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                             date(2006, 12, 31):'-', \
                                             date(2005, 12, 31):'-', \
                                             date(2004, 12, 31):'-', \
                                             date(2003, 12, 31):'-', \
                                             date(2002, 12, 31):'-'})
        
    def testAnnualDilutedEPSAfterCompExp(self):
        """ Test that I find Annual DilutedEPSAfterCompExp"""
        self.assertEquals(self.google.getAnnualDilutedEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'})
        
    def testAnnualDepreciationSupplemental(self):
        """ Test that I find Annual DepreciationSupplemental"""
        self.assertEquals(self.google.getAnnualDepreciationSupplemental("DD"), {date(2007, 12, 31):'-', \
                                                 date(2006, 12, 31):'-', \
                                                 date(2005, 12, 31):'-', \
                                                 date(2004, 12, 31):'-', \
                                                 date(2003, 12, 31):'-', \
                                                 date(2002, 12, 31):'-'})
        
    def testAnnualTotalSpecialItems(self):
        """ Test that I find Annual TotalSpecialItems"""
        self.assertEquals(self.google.getAnnualTotalSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                          date(2006, 12, 31):'-', \
                                          date(2005, 12, 31):'-', \
                                          date(2004, 12, 31):'-', \
                                          date(2003, 12, 31):'-', \
                                          date(2002, 12, 31):'-'})
        
    def testAnnualNormalizedIncomeBeforeTaxes(self):
        """ Test that I find Annual NormalizedIncomeBeforeTaxes"""
        self.assertEquals(self.google.getAnnualNormalizedIncomeBeforeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                    date(2006, 12, 31):'-', \
                                                    date(2005, 12, 31):'-', \
                                                    date(2004, 12, 31):'-', \
                                                    date(2003, 12, 31):'-', \
                                                    date(2002, 12, 31):'-'})                                                                                
        
    def testAnnualEffectsOfSpecialItemsOnIncomeTaxes(self):
        """ Test that I find Annual EffectsOfSpecialItemsOnIncomeTaxes"""
        self.assertEquals(self.google.getAnnualEffectsOfSpecialItemsOnIncomeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                           date(2006, 12, 31):'-', \
                                                           date(2005, 12, 31):'-', \
                                                           date(2004, 12, 31):'-', \
                                                           date(2003, 12, 31):'-', \
                                                           date(2002, 12, 31):'-'})
        
    def testAnnualIncomeTaxesExSpecialItems(self):
        """ Test that I find Annual IncomeTaxesExSpecialItems"""
        self.assertEquals(self.google.getAnnualIncomeTaxesExSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                                  date(2006, 12, 31):'-', \
                                                  date(2005, 12, 31):'-', \
                                                  date(2004, 12, 31):'-', \
                                                  date(2003, 12, 31):'-', \
                                                  date(2002, 12, 31):'-'})
        
    def testAnnualNormalizedIncomeAfterTaxes(self):
        """ Test that I find Annual NormalizedIncomeAfterTaxes"""
        self.assertEquals(self.google.getAnnualNormalizedIncomeAfterTaxes("DD"), {date(2007, 12, 31):'-', \
                                                   date(2006, 12, 31):'-', \
                                                   date(2005, 12, 31):'-', \
                                                   date(2004, 12, 31):'-', \
                                                   date(2003, 12, 31):'-', \
                                                   date(2002, 12, 31):'-'})
        
    def testAnnualNormalizedIncomeAvailableCommon(self):
        """ Test that I find Annual NormalizedIncomeAvailableCommon"""
        self.assertEquals(self.google.getAnnualNormalizedIncomeAvailableCommon("DD"), {date(2007, 12, 31):'-', \
                                                        date(2006, 12, 31):'-', \
                                                        date(2005, 12, 31):'-', \
                                                        date(2004, 12, 31):'-', \
                                                        date(2003, 12, 31):'-', \
                                                        date(2002, 12, 31):'-'})                                
        
    def testAnnualBasicNormalizedEPS(self):
        """ Test that I find Annual BasicNormalizedEPS"""
        self.assertEquals(self.google.getAnnualBasicNormalizedEPS("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'})
        
    def testAnnualDilutedNormalizedEPS(self):
        """ Test that I find Annual DilutedNormalizedEPS"""
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
                                             date(2006, 12, 31):6276.00})
                                             
    def testQuarterlyOtherRevenue(self):
        """ Test that I find Quarterly OtherRevenue""" 
        self.assertEquals(self.google.getQuarterlyOtherRevenue("DD"), {date(2007, 12, 31):230.00, \
                                     date(2007, 9, 30):365.00, \
                                     date(2007, 6, 30):364.00, \
                                     date(2007, 3, 31):316.00, \
                                     date(2006, 12, 31):559.00})
                                        
    def testQuarterlyTotalRevenue(self):
        """ Test that I find Quarterly TotalRevenue"""                                          
        self.assertEquals(self.google.getQuarterlyTotalRevenue("DD"), {date(2007, 12, 31):7213.00, \
                                     date(2007, 9, 30):7040.00, \
                                     date(2007, 6, 30):8239.00, \
                                     date(2007, 3, 31):8161.00, \
                                     date(2006, 12, 31):6835.00})
                                      
    def testQuarterlyCostOfRevenue(self):
        """ Test that I find Quarterly CostOfRevenue"""
        self.assertEquals(self.google.getQuarterlyCostOfRevenue("DD"), {date(2007, 12, 31):5349.00, \
                                      date(2007, 9, 30):5115.00, \
                                      date(2007, 6, 30):5555.00, \
                                      date(2007, 3, 31):5546.00, \
                                      date(2006, 12, 31):5114.00})
                                       
    def testQuarterlyGrossProfit(self):
        """ Test that I find Quarterly GrossProfit"""
        self.assertEquals(self.google.getQuarterlyGrossProfit("DD"), {date(2007, 12, 31):1634.00, \
                                    date(2007, 9, 30):1560.00, \
                                    date(2007, 6, 30):2320.00, \
                                    date(2007, 3, 31):2299.00, \
                                    date(2006, 12, 31):1162.00})
                                    
    def testQuarterlySGAExpenses(self):
        """ Test that I find Quarterly SGAExpenses"""
        self.assertEquals(self.google.getQuarterlySGAExpenses("DD"), {date(2007, 12, 31):852.00, \
                                    date(2007, 9, 30):797.00, \
                                    date(2007, 6, 30):877.00, \
                                    date(2007, 3, 31):838.00, \
                                    date(2006, 12, 31):824.00})
                                    
    def testQuarterlyResearchAndDevelopment(self):
        """ Test that I find Quarterly ResearchAndDevelopment"""
        self.assertEquals(self.google.getQuarterlyResearchAndDevelopment("DD"), {date(2007, 12, 31):359.00, \
                                               date(2007, 9, 30):332.00, \
                                               date(2007, 6, 30):337.00, \
                                               date(2007, 3, 31):310.00, \
                                               date(2006, 12, 31):341.00})
                                                
    def testQuarterlyDepreciationAmortization(self):
        """ Test that I find Quarterly DepreciationAmortization"""
        self.assertEquals(self.google.getQuarterlyDepreciationAmortization("DD"), {date(2007, 12, 31):50.00, \
                                                 date(2007, 9, 30):53.00, \
                                                 date(2007, 6, 30):54.00, \
                                                 date(2007, 3, 31):56.00, \
                                                 date(2006, 12, 31):55.00})
                                                  
    def testQuarterlyInterestNetOperating(self):
        """ Test that I find Quarterly InterestNetOperating"""
        self.assertEquals(self.google.getQuarterlyInterestNetOperating("DD"), {date(2007, 12, 31):110.00, \
                                             date(2007, 9, 30):113.00, \
                                             date(2007, 6, 30):108.00, \
                                             date(2007, 3, 31):99.00, \
                                             date(2006, 12, 31):113.00})
                                             
    def testQuarterlyUnusualExpense(self):
        """ Test that I find Quarterly UnusualExpense""" 
        self.assertEquals(self.google.getQuarterlyUnusualExpense("DD"), {date(2007, 12, 31):'-', \
                                       date(2007, 9, 30):'-', \
                                       date(2007, 6, 30):'-', \
                                       date(2007, 3, 31):'-', \
                                       date(2006, 12, 31):0.00})
                                       
    def testQuarterlyOtherOperatingExpenses(self):
        """ Test that I find Quarterly OtherOperatingExpenses"""
        self.assertEquals(self.google.getQuarterlyOtherOperatingExpenses("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                               
    def testQuarterlyTotalOperatingExpense(self):
        """ Test that I find Quarterly TotalOperatingExpense"""
        self.assertEquals(self.google.getQuarterlyTotalOperatingExpense("DD"), {date(2007, 12, 31):6720.00, \
                                              date(2007, 9, 30):6410.00, \
                                              date(2007, 6, 30):6931.00, \
                                              date(2007, 3, 31):6849.00, \
                                              date(2006, 12, 31):6447.00})
                                               
    def testQuarterlyOperatingIncome(self):
        """ Test that I find Quarterly OperatingIncome"""
        self.assertEquals(self.google.getQuarterlyOperatingIncome("DD"), {date(2007, 12, 31):493.00, \
                                        date(2007, 9, 30):630.00, \
                                        date(2007, 6, 30):1308.00, \
                                        date(2007, 3, 31):1312.00, \
                                        date(2006, 12, 31):388.00})
                                         
    def testQuarterlyInterestIncome(self):
        """ Test that I find Quarterly InterestIncome"""
        self.assertEquals(self.google.getQuarterlyInterestIncome("DD"), {date(2007, 12, 31):'-', \
                                       date(2007, 9, 30):'-', \
                                       date(2007, 6, 30):'-', \
                                       date(2007, 3, 31):'-', \
                                       date(2006, 12, 31):'-'})
                                        
    def testQuarterlyGainOnSaleOfAssets(self):
        """ Test that I find Quarterly GainOnSaleOfAssets"""
        self.assertEquals(self.google.getQuarterlyGainOnSaleOfAssets("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
    def testQuarterlyOtherNet(self):
        """ Test that I find Quarterly OtherNet"""
        self.assertEquals(self.google.getQuarterlyOtherNet("DD"), {date(2007, 12, 31):'-', \
                                 date(2007, 9, 30):'-', \
                                 date(2007, 6, 30):'-', \
                                 date(2007, 3, 31):'-', \
                                 date(2006, 12, 31):'-'})
                                  
    def testQuarterlyIncomeBeforeTax(self):
        """ Test that I find Quarterly IncomeBeforeTax"""
        self.assertEquals(self.google.getQuarterlyIncomeBeforeTax("DD"), {date(2007, 12, 31):493.00, \
                                        date(2007, 9, 30):630.00, \
                                        date(2007, 6, 30):1308.00, \
                                        date(2007, 3, 31):1312.00, \
                                        date(2006, 12, 31):388.00})
                                         
    def testQuarterlyIncomeAfterTax(self):
        """ Test that I find Quarterly IncomeAfterTax"""
        self.assertEquals(self.google.getQuarterlyIncomeAfterTax("DD"), {date(2007, 12, 31):547.00, \
                                       date(2007, 9, 30):528.00, \
                                       date(2007, 6, 30):973.00, \
                                       date(2007, 3, 31):947.00, \
                                       date(2006, 12, 31):853.00})
                                        
    def testQuarterlyMinorityInterest_Inc(self):
        """ Test that I find Quarterly MinorityInterest_Inc"""
        self.assertEquals(self.google.getQuarterlyMinorityInterest_Inc("DD"), {date(2007, 12, 31):-2.00, \
                                         date(2007, 9, 30):-2.00, \
                                         date(2007, 6, 30):-1.00, \
                                         date(2007, 3, 31):-2.00, \
                                         date(2006, 12, 31):18.00})
                                          
    def testQuarterlyEquityInAffiliates(self):
        """ Test that I find Quarterly EquityInAffiliates"""
        self.assertEquals(self.google.getQuarterlyEquityInAffiliates("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
    def testQuarterlyNetIncomeBeforeExtraItems(self):
        """ Test that I find Quarterly NetIncomeBeforeExtraItems"""
        self.assertEquals(self.google.getQuarterlyNetIncomeBeforeExtraItems("DD"), {date(2007, 12, 31):545.00, \
                                                  date(2007, 9, 30):526.00, \
                                                  date(2007, 6, 30):972.00, \
                                                  date(2007, 3, 31):945.00, \
                                                  date(2006, 12, 31):871.00})
                                                   
    def testQuarterlyAccountingChange(self):
        """ Test that I find Quarterly AccountingChange"""
        self.assertEquals(self.google.getQuarterlyAccountingChange("DD"), {date(2007, 12, 31):'-', \
                                         date(2007, 9, 30):'-', \
                                         date(2007, 6, 30):'-', \
                                         date(2007, 3, 31):'-', \
                                         date(2006, 12, 31):'-'})
                                          
    def testQuarterlyDiscontinuedOperations(self):
        """ Test that I find Quarterly DiscontinuedOperations"""
        self.assertEquals(self.google.getQuarterlyDiscontinuedOperations("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                                
    def testQuarterlyExtraordinaryItem(self):
        """ Test that I find Quarterly ExtraordinaryItem"""
        self.assertEquals(self.google.getQuarterlyExtraordinaryItem("DD"), {date(2007, 12, 31):'-', \
                                          date(2007, 9, 30):'-', \
                                          date(2007, 6, 30):'-', \
                                          date(2007, 3, 31):'-', \
                                          date(2006, 12, 31):'-'})
                                           
    def testQuarterlyNetIncome(self):
        """ Test that I find Quarterly NetIncome"""
        self.assertEquals(self.google.getQuarterlyNetIncome("DD"), {date(2007, 12, 31):545.00, \
                                  date(2007, 9, 30):526.00, \
                                  date(2007, 6, 30):972.00, \
                                  date(2007, 3, 31):945.00, \
                                  date(2006, 12, 31):871.00})
                                   
    def testQuarterlyPreferredDividends(self):
        """ Test that I find Quarterly PreferredDividends"""
        self.assertEquals(self.google.getQuarterlyPreferredDividends("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
    def testQuarterlyIncomeAvailToCommonExclExtraItems(self):
        """ Test that I find Quarterly IncomeAvailToCommonExclExtraItems""" 
        self.assertEquals(self.google.getQuarterlyIncomeAvailToCommonExclExtraItems("DD"), {date(2007, 12, 31):543.00, \
                                                          date(2007, 9, 30):524.00, \
                                                          date(2007, 6, 30):969.00, \
                                                          date(2007, 3, 31):942.00, \
                                                          date(2006, 12, 31):869.00})
                                                           
    def testQuarterlyIncomeAvailToCommonInclExtraItems(self):
        """ Test that I find Quarterly IncomeAvailToCommonInclExtraItems""" 
        self.assertEquals(self.google.getQuarterlyIncomeAvailToCommonInclExtraItems("DD"), {date(2007, 12, 31):543.00, \
                                                          date(2007, 9, 30):524.00, \
                                                          date(2007, 6, 30):969.00, \
                                                          date(2007, 3, 31):942.00, \
                                                          date(2006, 12, 31):869.00})
                                                           
    def testQuarterlyBasicWeightedAverageShares(self):
        """ Test that I find Quarterly BasicWeightedAverageShares""" 
        self.assertEquals(self.google.getQuarterlyBasicWeightedAverageShares("DD"), {date(2007, 12, 31):'-', \
                                                   date(2007, 9, 30):'-', \
                                                   date(2007, 6, 30):'-', \
                                                   date(2007, 3, 31):'-', \
                                                   date(2006, 12, 31):'-'})
                                                    
    def testQuarterlyBasicEPSExclExtraItems(self):
        """ Test that I find Quarterly BasicEPSExclExtraItems""" 
        self.assertEquals(self.google.getQuarterlyBasicEPSExclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                                
    def testQuarterlyBasicEPSInclExtraItems(self):
        """ Test that I find Quarterly BasicEPSInclExtraItems""" 
        self.assertEquals(self.google.getQuarterlyBasicEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                                
    def testQuarterlyDilutionAdjustment(self):
        """ Test that I find Quarterly DilutionAdjustment"""
        self.assertEquals(self.google.getQuarterlyDilutionAdjustment("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
    def testQuarterlyDilutedWeightedAverageShares(self):
        """ Test that I find Quarterly DilutedWeightedAverageShares"""
        self.assertEquals(self.google.getQuarterlyDilutedWeightedAverageShares("DD"), {date(2007, 12, 31):906.48, \
                                                     date(2007, 9, 30):929.32, \
                                                     date(2007, 6, 30):932.81, \
                                                     date(2007, 3, 31):933.27, \
                                                     date(2006, 12, 31):941.43})
                                                      
    def testQuarterlyDilutedEPSExclExtraItems(self):
        """ Test that I find Quarterly DilutedEPSExclExtraItems""" 
        self.assertEquals(self.google.getQuarterlyDilutedEPSExclExtraItems("DD"), {date(2007, 12, 31):0.60, \
                                                 date(2007, 9, 30):0.56, \
                                                 date(2007, 6, 30):1.04, \
                                                 date(2007, 3, 31):1.01, \
                                                 date(2006, 12, 31):0.92})
                                                  
    def testQuarterlyDilutedEPSInclExtraItems(self):
        """ Test that I find Quarterly DilutedEPSInclExtraItems""" 
        self.assertEquals(self.google.getQuarterlyDilutedEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                                 date(2007, 9, 30):'-', \
                                                 date(2007, 6, 30):'-', \
                                                 date(2007, 3, 31):'-', \
                                                 date(2006, 12, 31):'-'})
                                                  
    def testQuarterlyDividendsPerShare(self):
        """ Test that I find Quarterly DividendsPerShare""" 
        self.assertEquals(self.google.getQuarterlyDividendsPerShare("DD"), {date(2007, 12, 31):0.41, \
                                          date(2007, 9, 30):0.37, \
                                          date(2007, 6, 30):0.37, \
                                          date(2007, 3, 31):0.37, \
                                          date(2006, 12, 31):0.37})
                                           
    def testQuarterlyGrossDividends(self):
        """ Test that I find Quarterly GrossDividends""" 
        self.assertEquals(self.google.getQuarterlyGrossDividends("DD"), {date(2007, 12, 31):'-', \
                                       date(2007, 9, 30):'-', \
                                       date(2007, 6, 30):'-', \
                                       date(2007, 3, 31):'-', \
                                       date(2006, 12, 31):'-'})
                                        
    def testQuarterlyNetIncomeAfterCompExp(self):
        """ Test that I find Quarterly NetIncomeAfterCompExp"""
        self.assertEquals(self.google.getQuarterlyNetIncomeAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                              date(2007, 9, 30):'-', \
                                              date(2007, 6, 30):'-', \
                                              date(2007, 3, 31):'-', \
                                              date(2006, 12, 31):'-'})
                                               
    def testQuarterlyBasicEPSAfterCompExp(self):
        """ Test that I find Quarterly BasicEPSAfterCompExp"""
        self.assertEquals(self.google.getQuarterlyBasicEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                             date(2007, 9, 30):'-', \
                                             date(2007, 6, 30):'-', \
                                             date(2007, 3, 31):'-', \
                                             date(2006, 12, 31):'-'})
                                              
    def testQuarterlyDilutedEPSAfterCompExp(self):
        """ Test that I find Quarterly DilutedEPSAfterCompExp"""
        self.assertEquals(self.google.getQuarterlyDilutedEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                                
    def testQuarterlyDepreciationSupplemental(self):
        """ Test that I find Quarterly DepreciationSupplemental""" 
        self.assertEquals(self.google.getQuarterlyDepreciationSupplemental("DD"), {date(2007, 12, 31):'-', \
                                                 date(2007, 9, 30):'-', \
                                                 date(2007, 6, 30):'-', \
                                                 date(2007, 3, 31):'-', \
                                                 date(2006, 12, 31):'-'})
                                                  
    def testQuarterlyTotalSpecialItems(self):
        """ Test that I find Quarterly TotalSpecialItems""" 
        self.assertEquals(self.google.getQuarterlyTotalSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                          date(2007, 9, 30):'-', \
                                          date(2007, 6, 30):'-', \
                                          date(2007, 3, 31):'-', \
                                          date(2006, 12, 31):'-'})
                                           
    def testQuarterlyNormalizedIncomeBeforeTaxes(self):
        """ Test that I find Quarterly NormalizedIncomeBeforeTaxes""" 
        self.assertEquals(self.google.getQuarterlyNormalizedIncomeBeforeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                    date(2007, 9, 30):'-', \
                                                    date(2007, 6, 30):'-', \
                                                    date(2007, 3, 31):'-', \
                                                    date(2006, 12, 31):'-'})
                                                     
    def testQuarterlyEffectsOfSpecialItemsOnIncomeTaxes(self):
        """ Test that I find Quarterly EffectsOfSpecialItemsOnIncomeTaxes"""
        self.assertEquals(self.google.getQuarterlyEffectsOfSpecialItemsOnIncomeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                           date(2007, 9, 30):'-', \
                                                           date(2007, 6, 30):'-', \
                                                           date(2007, 3, 31):'-', \
                                                           date(2006, 12, 31):'-'})
                                                            
    def testQuarterlyIncomeTaxesExSpecialItems(self):
        """ Test that I find Quarterly IncomeTaxesExSpecialItems""" 
        self.assertEquals(self.google.getQuarterlyIncomeTaxesExSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                                  date(2007, 9, 30):'-', \
                                                  date(2007, 6, 30):'-', \
                                                  date(2007, 3, 31):'-', \
                                                  date(2006, 12, 31):'-'})
                                                   
    def testQuarterlyNormalizedIncomeAfterTaxes(self):
        """ Test that I find Quarterly NormalizedIncomeAfterTaxes"""
        self.assertEquals(self.google.getQuarterlyNormalizedIncomeAfterTaxes("DD"), {date(2007, 12, 31):'-', \
                                                   date(2007, 9, 30):'-', \
                                                   date(2007, 6, 30):'-', \
                                                   date(2007, 3, 31):'-', \
                                                   date(2006, 12, 31):'-'})
                                                    
    def testQuarterlyNormalizedIncomeAvailableCommon(self):
        """ Test that I find Quarterly NormalizedIncomeAvailableCommon"""
        self.assertEquals(self.google.getQuarterlyNormalizedIncomeAvailableCommon("DD"), {date(2007, 12, 31):'-', \
                                                        date(2007, 9, 30):'-', \
                                                        date(2007, 6, 30):'-', \
                                                        date(2007, 3, 31):'-', \
                                                        date(2006, 12, 31):'-'})
                                                         
    def testQuarterlyBasicNormalizedEPS(self):
        """ Test that I find Quarterly BasicNormalizedEPS"""
        self.assertEquals(self.google.getQuarterlyBasicNormalizedEPS("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
    def testQuarterlyDilutedNormalizedEPS(self):
        """ Test that I find Quarterly DilutedNormalizedEPS""" 
        self.assertEquals(self.google.getQuarterlyDilutedNormalizedEPS("DD"), {date(2007, 12, 31):0.60, \
                                             date(2007, 9, 30):0.56, \
                                             date(2007, 6, 30):1.04, \
                                             date(2007, 3, 31):1.01, \
                                             date(2006, 12, 31):0.92})

        
class WebsiteTestCase_BalanceSheet(WebsiteTestCase):    
    """ Test all the information that comes from an SEC Balance Sheet """
    
    def testAnnualCashAndEquivalents(self):
        """ Test that I find Annual CashAndEquivalents"""
        self.assertEquals(self.google.getAnnualCashAndEquivalents("DD"), {date(2007, 12, 31):1305.00, \
                                           date(2006, 12, 31):1814.00, \
                                           date(2005, 12, 31):1736.00, \
                                           date(2004, 12, 31):3369.00, \
                                           date(2003, 12, 31):3273.00, \
                                           date(2002, 12, 31):3678.00})
        
    def testAnnualShortTermInvestments(self):
        """ Test that I find Annual ShortTermInvestments"""
        self.assertEquals(self.google.getAnnualShortTermInvestments("DD"), {date(2007, 12, 31):131.00, \
                                             date(2006, 12, 31):79.00, \
                                             date(2005, 12, 31):115.00, \
                                             date(2004, 12, 31):167.00, \
                                             date(2003, 12, 31):25.00, \
                                             date(2002, 12, 31):465.00})
        
    def testAnnualCashAndShortTermInvestments(self):
        """ Test that I find Annual CashAndShortTermInvestments"""
        self.assertEquals(self.google.getAnnualCashAndShortTermInvestments("DD"), {date(2007, 12, 31):1436.00, \
                                                    date(2006, 12, 31):1893.00, \
                                                    date(2005, 12, 31):1851.00, \
                                                    date(2004, 12, 31):3536.00, \
                                                    date(2003, 12, 31):3298.00, \
                                                    date(2002, 12, 31):4143.00})
        
    def testAnnualAccountsReceivableTrade(self):
        """ Test that I find Annual AccountsReceivableTrade"""
        self.assertEquals(self.google.getAnnualAccountsReceivableTrade("DD"), {date(2007, 12, 31):4649.00, \
                                                date(2006, 12, 31):4335.00, \
                                                date(2005, 12, 31):3907.00, \
                                                date(2004, 12, 31):3860.00, \
                                                date(2003, 12, 31):3427.00, \
                                                date(2002, 12, 31):2913.00})
        
    def testAnnualReceivablesOther(self):
        """ Test that I find Annual ReceivablesOther"""
        self.assertEquals(self.google.getAnnualReceivablesOther("DD"), {date(2007, 12, 31):'-', \
                                         date(2006, 12, 31):'-', \
                                         date(2005, 12, 31):'-', \
                                         date(2004, 12, 31):'-', \
                                         date(2003, 12, 31):'-', \
                                         date(2002, 12, 31):'-'})
        
    def testAnnualTotalReceivablesNet(self):
        """ Test that I find Annual TotalReceivablesNet"""
        self.assertEquals(self.google.getAnnualTotalReceivablesNet("DD"), {date(2007, 12, 31):5683.00, \
                                            date(2006, 12, 31):5198.00, \
                                            date(2005, 12, 31):4801.00, \
                                            date(2004, 12, 31):4889.00, \
                                            date(2003, 12, 31):4218.00, \
                                            date(2002, 12, 31):3884.00})                                                        
        
    def testAnnualTotalInventory(self):
        """ Test that I find Annual TotalInventory"""
        self.assertEquals(self.google.getAnnualTotalInventory("DD"), {date(2007, 12, 31):5278.00, \
                                       date(2006, 12, 31):4941.00, \
                                       date(2005, 12, 31):4743.00, \
                                       date(2004, 12, 31):4489.00, \
                                       date(2003, 12, 31):4107.00, \
                                       date(2002, 12, 31):4409.00})
        
    def testAnnualPrepaidExpenses(self):
        """ Test that I find Annual PrepaidExpenses"""
        self.assertEquals(self.google.getAnnualPrepaidExpenses("DD"), {date(2007, 12, 31):199.00, \
                                        date(2006, 12, 31):182.00, \
                                        date(2005, 12, 31):199.00, \
                                        date(2004, 12, 31):209.00, \
                                        date(2003, 12, 31):208.00, \
                                        date(2002, 12, 31):175.00})
        
    def testAnnualOtherCurrentAssetsTotal(self):
        """ Test that I find Annual OtherCurrentAssetsTotal"""
        self.assertEquals(self.google.getAnnualOtherCurrentAssetsTotal("DD"), {date(2007, 12, 31):564.00, \
                                                date(2006, 12, 31):656.00, \
                                                date(2005, 12, 31):828.00, \
                                                date(2004, 12, 31):2088.00, \
                                                date(2003, 12, 31):6631.00, \
                                                date(2002, 12, 31):848.00})
        
    def testAnnualTotalCurrentAssets(self):
        """ Test that I find Annual TotalCurrentAssets"""
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
        """ Test that I find Annual LongTermInvestments"""
        self.assertEquals(self.google.getAnnualLongTermInvestments("DD"), {date(2007, 12, 31):908.00, \
                                            date(2006, 12, 31):897.00, \
                                            date(2005, 12, 31):937.00, \
                                            date(2004, 12, 31):1140.00, \
                                            date(2003, 12, 31):1445.00, \
                                            date(2002, 12, 31):2190.00})
        
    def testAnnualOtherLongTermAssets(self):
        """ Test that I find Annual OtherLongTermAssets"""
        self.assertEquals(self.google.getAnnualOtherLongTermAssets("DD"), {date(2007, 12, 31):4273.00, \
                                            date(2006, 12, 31):2925.00, \
                                            date(2005, 12, 31):4824.00, \
                                            date(2004, 12, 31):4092.00, \
                                            date(2003, 12, 31):2023.00, \
                                            date(2002, 12, 31):1005.00})
        
    def testAnnualTotalAssets(self):
        """ Test that I find Annual TotalAssets"""
        self.assertEquals(self.google.getAnnualTotalAssets("DD"), {date(2007, 12, 31):34131.00, \
                                    date(2006, 12, 31):31777.00, \
                                    date(2005, 12, 31):33291.00, \
                                    date(2004, 12, 31):35632.00, \
                                    date(2003, 12, 31):37039.00, \
                                    date(2002, 12, 31):34621.00})
        
    def testAnnualAccountsPayable(self):
        """ Test that I find Annual AccountsPayable"""
        self.assertEquals(self.google.getAnnualAccountsPayable("DD"), {date(2007, 12, 31):3172.00, \
                                        date(2006, 12, 31):2711.00, \
                                        date(2005, 12, 31):2670.00, \
                                        date(2004, 12, 31):2661.00, \
                                        date(2003, 12, 31):2412.00, \
                                        date(2002, 12, 31):2727.00})
        
    def testAnnualAccruedExpenses(self):
        """ Test that I find Annual AccruedExpenses"""
        self.assertEquals(self.google.getAnnualAccruedExpenses("DD"), {date(2007, 12, 31):3823.00, \
                                        date(2006, 12, 31):3534.00, \
                                        date(2005, 12, 31):3075.00, \
                                        date(2004, 12, 31):4054.00, \
                                        date(2003, 12, 31):2963.00, \
                                        date(2002, 12, 31):3137.00})
        
    def testAnnualNotesPayable(self):
        """ Test that I find Annual NotesPayable"""
        self.assertEquals(self.google.getAnnualNotesPayable("DD"), {date(2007, 12, 31):1349.00, \
                                     date(2006, 12, 31):354.00, \
                                     date(2005, 12, 31):0.00, \
                                     date(2004, 12, 31):0.00, \
                                     date(2003, 12, 31):0.00, \
                                     date(2002, 12, 31):0.00})
        
    def testAnnualCurrentPortLTDebtToCapital(self):
        """ Test that I find Annual CurrentPortLTDebtToCapital"""
        self.assertEquals(self.google.getAnnualCurrentPortLTDebtToCapital("DD"), {date(2007, 12, 31):21.00, \
                                                   date(2006, 12, 31):1163.00, \
                                                   date(2005, 12, 31):1397.00, \
                                                   date(2004, 12, 31):936.00, \
                                                   date(2003, 12, 31):5914.00, \
                                                   date(2002, 12, 31):1185.00})                                        
        
    def testAnnualOtherCurrentLiabilities(self):
        """ Test that I find Annual OtherCurrentLiabilities"""
        self.assertEquals(self.google.getAnnualOtherCurrentLiabilities("DD"), {date(2007, 12, 31):176.00, \
                                                date(2006, 12, 31):178.00, \
                                                date(2005, 12, 31):294.00, \
                                                date(2004, 12, 31):288.00, \
                                                date(2003, 12, 31):1754.00, \
                                                date(2002, 12, 31):47.00}) 
    def testAnnualTotalCurrentLiabilities(self):
        """ Test that I find Annual TotalCurrentLiabilities""" 
        self.assertEquals(self.google.getAnnualTotalCurrentLiabilities("DD"), {date(2007, 12, 31):8541.00, \
                                                date(2006, 12, 31):7940.00, \
                                                date(2005, 12, 31):7436.00, \
                                                date(2004, 12, 31):7939.00, \
                                                date(2003, 12, 31):13043.00, \
                                                date(2002, 12, 31):7096.00}) 
    def testAnnualLongTermDebt(self):
        """ Test that I find Annual LongTermDebt""" 
        self.assertEquals(self.google.getAnnualLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                     date(2006, 12, 31):6013.00, \
                                     date(2005, 12, 31):6783.00, \
                                     date(2004, 12, 31):5548.00, \
                                     date(2003, 12, 31):4301.00, \
                                     date(2002, 12, 31):5647.00}) 
    def testAnnualCapitalLeaseObligations(self):
        """ Test that I find Annual CapitalLeaseObligations""" 
        self.assertEquals(self.google.getAnnualCapitalLeaseObligations("DD"), {date(2007, 12, 31):'-', \
                                                date(2006, 12, 31):'-', \
                                                date(2005, 12, 31):'-', \
                                                date(2004, 12, 31):'-', \
                                                date(2003, 12, 31):'-', \
                                                date(2002, 12, 31):'-'}) 
    def testAnnualTotalLongTermDebt(self):
        """ Test that I find Annual TotalLongTermDebt""" 
        self.assertEquals(self.google.getAnnualTotalLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                          date(2006, 12, 31):6013.00, \
                                          date(2005, 12, 31):6783.00, \
                                          date(2004, 12, 31):5548.00, \
                                          date(2003, 12, 31):4301.00, \
                                          date(2002, 12, 31):5647.00}) 
    def testAnnualTotalDebt(self):
        """ Test that I find Annual TotalDebt""" 
        self.assertEquals(self.google.getAnnualTotalDebt("DD"), {date(2007, 12, 31):7325.00, \
                                  date(2006, 12, 31):7530.00, \
                                  date(2005, 12, 31):8180.00, \
                                  date(2004, 12, 31):6484.00, \
                                  date(2003, 12, 31):10215.00, \
                                  date(2002, 12, 31):6832.00}) 
    def testAnnualDeferredIncomeTax(self):
        """ Test that I find Annual DeferredIncomeTax""" 
        self.assertEquals(self.google.getAnnualDeferredIncomeTax("DD"), {date(2007, 12, 31):802.00, \
                                          date(2006, 12, 31):269.00, \
                                          date(2005, 12, 31):1179.00, \
                                          date(2004, 12, 31):966.00, \
                                          date(2003, 12, 31):508.00, \
                                          date(2002, 12, 31):563.00}) 
    def testAnnualMinorityInterest_Bal(self):
        """ Test that I find Annual MinorityInterest_Bal""" 
        self.assertEquals(self.google.getAnnualMinorityInterest_Bal("DD"), {date(2007, 12, 31):442.00, \
                                         date(2006, 12, 31):441.00, \
                                         date(2005, 12, 31):490.00, \
                                         date(2004, 12, 31):1110.00, \
                                         date(2003, 12, 31):497.00, \
                                         date(2002, 12, 31):2423.00}) 
    def testAnnualOtherLiabilities(self):
        """ Test that I find Annual OtherLiabilities""" 
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
        """ Test that I find Annual RedeemablePreferredStock""" 
        self.assertEquals(self.google.getAnnualRedeemablePreferredStock("DD"), {date(2007, 12, 31):'-', \
                                                 date(2006, 12, 31):'-', \
                                                 date(2005, 12, 31):'-', \
                                                 date(2004, 12, 31):'-', \
                                                 date(2003, 12, 31):'-', \
                                                 date(2002, 12, 31):'-'}) 
    def testAnnualPreferredStockNonRedeemable(self):
        """ Test that I find Annual PreferredStockNonRedeemable""" 
        self.assertEquals(self.google.getAnnualPreferredStockNonRedeemable("DD"), {date(2007, 12, 31):237.00, \
                                                    date(2006, 12, 31):237.00, \
                                                    date(2005, 12, 31):237.00, \
                                                    date(2004, 12, 31):237.00, \
                                                    date(2003, 12, 31):237.00, \
                                                    date(2002, 12, 31):237.00}) 
    def testAnnualCommonStock(self):
        """ Test that I find Annual CommonStock""" 
        self.assertEquals(self.google.getAnnualCommonStock("DD"), {date(2007, 12, 31):296.00, \
                                    date(2006, 12, 31):303.00, \
                                    date(2005, 12, 31):302.00, \
                                    date(2004, 12, 31):324.00, \
                                    date(2003, 12, 31):325.00, \
                                    date(2002, 12, 31):324.00}) 
    def testAnnualAdditionalPaidInCapital(self):
        """ Test that I find Annual AdditionalPaidInCapital""" 
        self.assertEquals(self.google.getAnnualAdditionalPaidInCapital("DD"), {date(2007, 12, 31):8179.00, \
                                                date(2006, 12, 31):7797.00, \
                                                date(2005, 12, 31):7679.00, \
                                                date(2004, 12, 31):7784.00, \
                                                date(2003, 12, 31):7522.00, \
                                                date(2002, 12, 31):7377.00}) 
    def testAnnualRetainedEarnings(self):
        """ Test that I find Annual RetainedEarnings""" 
        self.assertEquals(self.google.getAnnualRetainedEarnings("DD"), {date(2007, 12, 31):9945.00, \
                                         date(2006, 12, 31):9679.00, \
                                         date(2005, 12, 31):7990.00, \
                                         date(2004, 12, 31):10182.00, \
                                         date(2003, 12, 31):10185.00, \
                                         date(2002, 12, 31):10619.00}) 
    def testAnnualTreasuryStock(self):
        """ Test that I find Annual TreasuryStock"""
        self.assertEquals(self.google.getAnnualTreasuryStock("DD"), {date(2007, 12, 31):-6727.00, \
                                      date(2006, 12, 31):-6727.00, \
                                      date(2005, 12, 31):-6727.00, \
                                      date(2004, 12, 31):-6727.00, \
                                      date(2003, 12, 31):-6727.00, \
                                      date(2002, 12, 31):-6727.00}) 
    def testAnnualOtherEquity(self):
        """ Test that I find Annual OtherEquity""" 
        self.assertEquals(self.google.getAnnualOtherEquity("DD"), {date(2007, 12, 31):-794.00, \
                                    date(2006, 12, 31):-1867.00, \
                                    date(2005, 12, 31):-518.00, \
                                    date(2004, 12, 31):-423.00, \
                                    date(2003, 12, 31):-1761.00, \
                                    date(2002, 12, 31):-2767.00}) 
    def testAnnualTotalEquity(self):
        """ Test that I find Annual TotalEquity"""
        self.assertEquals(self.google.getAnnualTotalEquity("DD"), {date(2007, 12, 31):11136.00, \
                                    date(2006, 12, 31):9422.00, \
                                    date(2005, 12, 31):8963.00, \
                                    date(2004, 12, 31):11377.00, \
                                    date(2003, 12, 31):9781.00, \
                                    date(2002, 12, 31):9063.00}) 
    def testAnnualTotalLiabilitiesAndShareholdersEquity(self):
        """ Test that I find Annual TotalLiabilitiesAndShareholdersEquity""" 
        self.assertEquals(self.google.getAnnualTotalLiabilitiesAndShareholdersEquity("DD"), {date(2007, 12, 31):34131.00, \
                                                              date(2006, 12, 31):31777.00, \
                                                              date(2005, 12, 31):33292.00, \
                                                              date(2004, 12, 31):35632.00, \
                                                              date(2003, 12, 31):37039.00, \
                                                              date(2002, 12, 31):34621.00}) 
    def testAnnualSharesOuts(self):
        """ Test that I find Annual SharesOuts""" 
        self.assertEquals(self.google.getAnnualSharesOuts("DD"), {date(2007, 12, 31):'-', \
                                   date(2006, 12, 31):'-', \
                                   date(2005, 12, 31):'-', \
                                   date(2004, 12, 31):'-', \
                                   date(2003, 12, 31):'-', \
                                   date(2002, 12, 31):'-'}) 
    def testAnnualTotalCommonSharesOutstanding(self):
        """ Test that I find Annual TotalCommonSharesOutstanding""" 
        self.assertEquals(self.google.getAnnualTotalCommonSharesOutstanding("DD"), {date(2007, 12, 31):899.29, \
                                                     date(2006, 12, 31):922.07, \
                                                     date(2005, 12, 31):919.61, \
                                                     date(2004, 12, 31):994.34, \
                                                     date(2003, 12, 31):997.28, \
                                                     date(2002, 12, 31):993.94}) 
 
    def testQuarterlyCashAndEquivalents(self):
        """ Test that I find Quarterly CashAndEquivalents"""
        self.assertEquals(self.google.getQuarterlyCashAndEquivalents("DD"), {date(2007, 12, 31):1305.00, \
                                           date(2007, 9, 30):1209.00, \
                                           date(2007, 6, 30):987.00, \
                                           date(2007, 3, 31):883.00, \
                                           date(2006, 12, 31):1814.00})
                                            
    def testQuarterlyShortTermInvestments(self):
        """ Test that I find Quarterly ShortTermInvestments""" 
        self.assertEquals(self.google.getQuarterlyShortTermInvestments("DD"), {date(2007, 12, 31):131.00, \
                                             date(2007, 9, 30):109.00, \
                                             date(2007, 6, 30):102.00, \
                                             date(2007, 3, 31):71.00, \
                                             date(2006, 12, 31):79.00})
                                              
    def testQuarterlyCashAndShortTermInvestments(self):
        """ Test that I find Quarterly CashAndShortTermInvestments""" 
        self.assertEquals(self.google.getQuarterlyCashAndShortTermInvestments("DD"), {date(2007, 12, 31):1436.00, \
                                                    date(2007, 9, 30):1318.00, \
                                                    date(2007, 6, 30):1089.00, \
                                                    date(2007, 3, 31):954.00, \
                                                    date(2006, 12, 31):1893.00})
                                                     
    def testQuarterlyAccountsReceivableTrade(self):
        """ Test that I find Quarterly AccountsReceivableTrade"""
        self.assertEquals(self.google.getQuarterlyAccountsReceivableTrade("DD"), {date(2007, 12, 31):5683.00, \
                                                date(2007, 9, 30):6990.00, \
                                                date(2007, 6, 30):7370.00, \
                                                date(2007, 3, 31):6813.00, \
                                                date(2006, 12, 31):5198.00})
                                                
    def testQuarterlyReceivablesOther(self):
        """ Test that I find Quarterly ReceivablesOther"""
        self.assertEquals(self.google.getQuarterlyReceivablesOther("DD"), {date(2007, 12, 31):'-', \
                                         date(2007, 9, 30):'-', \
                                         date(2007, 6, 30):'-', \
                                         date(2007, 3, 31):'-', \
                                         date(2006, 12, 31):'-'})
                                          
    def testQuarterlyTotalReceivablesNet(self):
        """ Test that I find Quarterly TotalReceivablesNet""" 
        self.assertEquals(self.google.getQuarterlyTotalReceivablesNet("DD"), {date(2007, 12, 31):5683.00, \
                                            date(2007, 9, 30):6990.00, \
                                            date(2007, 6, 30):7370.00, \
                                            date(2007, 3, 31):6813.00, \
                                            date(2006, 12, 31):5198.00})
                                             
    def testQuarterlyTotalInventory(self):
        """ Test that I find Quarterly TotalInventory"""
        self.assertEquals(self.google.getQuarterlyTotalInventory("DD"), {date(2007, 12, 31):5278.00, \
                                       date(2007, 9, 30):4963.00, \
                                       date(2007, 6, 30):4481.00, \
                                       date(2007, 3, 31):4855.00, \
                                       date(2006, 12, 31):4941.00})
                                        
    def testQuarterlyPrepaidExpenses(self):
        """ Test that I find Quarterly PrepaidExpenses""" 
        self.assertEquals(self.google.getQuarterlyPrepaidExpenses("DD"), {date(2007, 12, 31):199.00, \
                                        date(2007, 9, 30):195.00, \
                                        date(2007, 6, 30):199.00, \
                                        date(2007, 3, 31):213.00, \
                                        date(2006, 12, 31):182.00})
                                         
    def testQuarterlyOtherCurrentAssetsTotal(self):
        """ Test that I find Quarterly OtherCurrentAssetsTotal"""
        self.assertEquals(self.google.getQuarterlyOtherCurrentAssetsTotal("DD"), {date(2007, 12, 31):564.00, \
                                                date(2007, 9, 30):665.00, \
                                                date(2007, 6, 30):675.00, \
                                                date(2007, 3, 31):697.00, \
                                                date(2006, 12, 31):656.00})
                                                 
    def testQuarterlyTotalCurrentAssets(self):
        """ Test that I find Quarterly TotalCurrentAssets"""
        self.assertEquals(self.google.getQuarterlyTotalCurrentAssets("DD"), {date(2007, 12, 31):13160.00, \
                                           date(2007, 9, 30):14131.00, \
                                           date(2007, 6, 30):13814.00, \
                                           date(2007, 3, 31):13532.00, \
                                           date(2006, 12, 31):12870.00})
                                            
    def testQuarterlyPPE(self):
        """ Test that I find Quarterly PPE"""
        self.assertEquals(self.google.getQuarterlyPPE("DD"), {date(2007, 12, 31):26593.00, \
                            date(2007, 9, 30):26302.00, \
                            date(2007, 6, 30):26053.00, \
                            date(2007, 3, 31):25876.00, \
                            date(2006, 12, 31):25719.00})
                             
    def testQuarterlyGoodwill(self):
        """ Test that I find Quarterly Goodwill"""
        self.assertEquals(self.google.getQuarterlyGoodwill("DD"), {date(2007, 12, 31):2074.00, \
                                 date(2007, 9, 30):2110.00, \
                                 date(2007, 6, 30):2108.00, \
                                 date(2007, 3, 31):2108.00, \
                                 date(2006, 12, 31):2108.00})
                                  
    def testQuarterlyIntangibles(self):
        """ Test that I find Quarterly Intangibles"""
        self.assertEquals(self.google.getQuarterlyIntangibles("DD"), {date(2007, 12, 31):2856.00, \
                                    date(2007, 9, 30):2904.00, \
                                    date(2007, 6, 30):2381.00, \
                                    date(2007, 3, 31):2436.00, \
                                    date(2006, 12, 31):2479.00})
                                     
    def testQuarterlyLongTermInvestments(self):
        """ Test that I find Quarterly LongTermInvestments"""
        self.assertEquals(self.google.getQuarterlyLongTermInvestments("DD"), {date(2007, 12, 31):818.00, \
                                            date(2007, 9, 30):791.00, \
                                            date(2007, 6, 30):802.00, \
                                            date(2007, 3, 31):790.00, \
                                            date(2006, 12, 31):803.00})
                                             
    def testQuarterlyOtherLongTermAssets(self):
        """ Test that I find Quarterly OtherLongTermAssets"""
        self.assertEquals(self.google.getQuarterlyOtherLongTermAssets("DD"), {date(2007, 12, 31):4363.00, \
                                            date(2007, 9, 30):3411.00, \
                                            date(2007, 6, 30):3267.00, \
                                            date(2007, 3, 31):3182.00, \
                                            date(2006, 12, 31):3019.00})
                                            
    def testQuarterlyTotalAssets(self):
        """ Test that I find Quarterly """
        self.assertEquals(self.google.getQuarterlyTotalAssets("DD"), {date(2007, 12, 31):34131.00, \
                                    date(2007, 9, 30):33915.00, \
                                    date(2007, 6, 30):32850.00, \
                                    date(2007, 3, 31):32473.00, \
                                    date(2006, 12, 31):31777.00})
                                     
    def testQuarterlyAccountsPayable(self):
        """ Test that I find Quarterly AccountsPayable""" 
        self.assertEquals(self.google.getQuarterlyAccountsPayable("DD"), {date(2007, 12, 31):3172.00, \
                                        date(2007, 9, 30):2873.00, \
                                        date(2007, 6, 30):2539.00, \
                                        date(2007, 3, 31):2782.00, \
                                        date(2006, 12, 31):2711.00})
                                         
    def testQuarterlyAccruedExpenses(self):
        """ Test that I find Quarterly AccruedExpenses"""
        self.assertEquals(self.google.getQuarterlyAccruedExpenses("DD"), {date(2007, 12, 31):3823.00, \
                                        date(2007, 9, 30):2972.00, \
                                        date(2007, 6, 30):2921.00, \
                                        date(2007, 3, 31):3020.00, \
                                        date(2006, 12, 31):3534.00})
                                         
    def testQuarterlyNotesPayable(self):
        """ Test that I find Quarterly NotesPayable"""
        self.assertEquals(self.google.getQuarterlyNotesPayable("DD"), {date(2007, 12, 31):1349.00, \
                                     date(2007, 9, 30):3618.00, \
                                     date(2007, 6, 30):1226.00, \
                                     date(2007, 3, 31):429.00, \
                                     date(2006, 12, 31):354.00})
                                      
    def testQuarterlyCurrentPortLTDebtToCapital(self):
        """ Test that I find Quarterly CurrentPortLTDebtToCapital"""
        self.assertEquals(self.google.getQuarterlyCurrentPortLTDebtToCapital("DD"), {date(2007, 12, 31):21.00, \
                                                   date(2007, 9, 30):'-', \
                                                   date(2007, 6, 30):1149.00, \
                                                   date(2007, 3, 31):1161.00, \
                                                   date(2006, 12, 31):1163.00})
                                                    
    def testQuarterlyOtherCurrentLiabilities(self):
        """ Test that I find Quarterly OtherCurrentLiabilities"""
        self.assertEquals(self.google.getQuarterlyOtherCurrentLiabilities("DD"), {date(2007, 12, 31):176.00, \
                                                date(2007, 9, 30):334.00, \
                                                date(2007, 6, 30):369.00, \
                                                date(2007, 3, 31):422.00, \
                                                date(2006, 12, 31):178.00})
                                                 
    def testQuarterlyTotalCurrentLiabilities(self):
        """ Test that I find Quarterly TotalCurrentLiabilities"""
        self.assertEquals(self.google.getQuarterlyTotalCurrentLiabilities("DD"), {date(2007, 12, 31):8541.00, \
                                                date(2007, 9, 30):9797.00, \
                                                date(2007, 6, 30):8204.00, \
                                                date(2007, 3, 31):7814.00, \
                                                date(2006, 12, 31):7940.00})
                                                 
    def testQuarterlyLongTermDebt(self):
        """ Test that I find Quarterly LongTermDebt"""
        self.assertEquals(self.google.getQuarterlyLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                     date(2007, 9, 30):5367.00, \
                                     date(2007, 6, 30):5664.00, \
                                     date(2007, 3, 31):6010.00, \
                                     date(2006, 12, 31):6013.00})
                                      
    def testQuarterlyCapitalLeaseObligations(self):
        """ Test that I find Quarterly CapitalLeaseObligations"""
        self.assertEquals(self.google.getQuarterlyCapitalLeaseObligations("DD"), {date(2007, 12, 31):'-', \
                                                date(2007, 9, 30):'-', \
                                                date(2007, 6, 30):'-', \
                                                date(2007, 3, 31):'-', \
                                                date(2006, 12, 31):'-'})
                                                 
    def testQuarterlyTotalLongTermDebt(self):
        """ Test that I find Quarterly TotalLongTermDebt"""
        self.assertEquals(self.google.getQuarterlyTotalLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                          date(2007, 9, 30):5367.00, \
                                          date(2007, 6, 30):5664.00, \
                                          date(2007, 3, 31):6010.00, \
                                          date(2006, 12, 31):6013.00})
                                           
    def testQuarterlyTotalDebt(self):
        """ Test that I find Quarterly TotalDebt"""
        self.assertEquals(self.google.getQuarterlyTotalDebt("DD"), {date(2007, 12, 31):7325.00, \
                                  date(2007, 9, 30):8985.00, \
                                  date(2007, 6, 30):8039.00, \
                                  date(2007, 3, 31):7600.00, \
                                  date(2006, 12, 31):7530.00})
                                   
    def testQuarterlyDeferredIncomeTax(self):
        """ Test that I find Quarterly DeferredIncomeTax"""
        self.assertEquals(self.google.getQuarterlyDeferredIncomeTax("DD"), {date(2007, 12, 31):802.00, \
                                          date(2007, 9, 30):404.00, \
                                          date(2007, 6, 30):395.00, \
                                          date(2007, 3, 31):402.00, \
                                          date(2006, 12, 31):269.00})
                                           
    def testQuarterlyMinorityInterest_Bal(self):
        """ Test that I find Quarterly MinorityInterest_Bal"""
        self.assertEquals(self.google.getQuarterlyMinorityInterest_Bal("DD"), {date(2007, 12, 31):442.00, \
                                         date(2007, 9, 30):445.00, \
                                         date(2007, 6, 30):442.00, \
                                         date(2007, 3, 31):442.00, \
                                         date(2006, 12, 31):441.00})
                                          
    def testQuarterlyOtherLiabilities(self):
        """ Test that I find Quarterly OtherLiabilities"""
        self.assertEquals(self.google.getQuarterlyOtherLiabilities("DD"), {date(2007, 12, 31):7255.00, \
                                         date(2007, 9, 30):7984.00, \
                                         date(2007, 6, 30):7455.00, \
                                         date(2007, 3, 31):7629.00, \
                                         date(2006, 12, 31):7692.00})
                                          
    def testQuarterlyTotalLiabilities(self):
        """ Test that I find Quarterly TotalLiabilities"""
        self.assertEquals(self.google.getQuarterlyTotalLiabilities("DD"), {date(2007, 12, 31):22995.00, \
                                         date(2007, 9, 30):23997.00, \
                                         date(2007, 6, 30):22160.00, \
                                         date(2007, 3, 31):22297.00, \
                                         date(2006, 12, 31):22355.00})
                                          
    def testQuarterlyRedeemablePreferredStock(self):
        """ Test that I find Quarterly RedeemablePreferredStock"""
        self.assertEquals(self.google.getQuarterlyRedeemablePreferredStock("DD"), {date(2007, 12, 31):'-', \
                                                 date(2007, 9, 30):'-', \
                                                 date(2007, 6, 30):'-', \
                                                 date(2007, 3, 31):'-', \
                                                 date(2006, 12, 31):'-'})
                                                  
    def testQuarterlyPreferredStockNonRedeemable(self):
        """ Test that I find Quarterly PreferredStockNonRedeemable"""
        self.assertEquals(self.google.getQuarterlyPreferredStockNonRedeemable("DD"), {date(2007, 12, 31):237.00, \
                                                    date(2007, 9, 30):237.00, \
                                                    date(2007, 6, 30):237.00, \
                                                    date(2007, 3, 31):237.00, \
                                                    date(2006, 12, 31):237.00})
                                                     
    def testQuarterlyCommonStock(self):
        """ Test that I find Quarterly CommonStock"""
        self.assertEquals(self.google.getQuarterlyCommonStock("DD"), {date(2007, 12, 31):296.00, \
                                    date(2007, 9, 30):296.00, \
                                    date(2007, 6, 30):302.00, \
                                    date(2007, 3, 31):303.00, \
                                    date(2006, 12, 31):303.00})
                                     
    def testQuarterlyAdditionalPaidInCapital(self):
        """ Test that I find Quarterly AdditionalPaidInCapital"""
        self.assertEquals(self.google.getQuarterlyAdditionalPaidInCapital("DD"), {date(2007, 12, 31):8179.00, \
                                                date(2007, 9, 30):8121.00, \
                                                date(2007, 6, 30):8187.00, \
                                                date(2007, 3, 31):8072.00, \
                                                date(2006, 12, 31):7797.00})
                                                 
    def testQuarterlyRetainedEarnings(self):
        """ Test that I find Quarterly RetainedEarnings"""
        self.assertEquals(self.google.getQuarterlyRetainedEarnings("DD"), {date(2007, 12, 31):9945.00, \
                                         date(2007, 9, 30):9772.00, \
                                         date(2007, 6, 30):10516.00, \
                                         date(2007, 3, 31):10142.00, \
                                         date(2006, 12, 31):9679.00})
                                          
    def testQuarterlyTreasuryStock(self):
        """ Test that I find Quarterly TreasuryStock"""
        self.assertEquals(self.google.getQuarterlyTreasuryStock("DD"), {date(2007, 12, 31):-6727.00, \
                                      date(2007, 9, 30):-6727.00, \
                                      date(2007, 6, 30):-6727.00, \
                                      date(2007, 3, 31):-6727.00, \
                                      date(2006, 12, 31):-6727.00})
                                       
    def testQuarterlyOtherEquity(self):
        """ Test that I find Quarterly OtherEquity"""
        self.assertEquals(self.google.getQuarterlyOtherEquity("DD"), {date(2007, 12, 31):-794.00, \
                                    date(2007, 9, 30):-1781.00, \
                                    date(2007, 6, 30):-1825.00, \
                                    date(2007, 3, 31):-1851.00, \
                                    date(2006, 12, 31):-1867.00})
                                     
    def testQuarterlyTotalEquity(self):
        """ Test that I find Quarterly TotalEquity"""
        self.assertEquals(self.google.getQuarterlyTotalEquity("DD"), {date(2007, 12, 31):11136.00, \
                                    date(2007, 9, 30):9918.00, \
                                    date(2007, 6, 30):10690.00, \
                                    date(2007, 3, 31):10176.00, \
                                    date(2006, 12, 31):9422.00})
                                     
    def testQuarterlyTotalLiabilitiesAndShareholdersEquity(self):
        """ Test that I find Quarterly TotalLiabilitiesAndShareholdersEquity"""
        self.assertEquals(self.google.getQuarterlyTotalLiabilitiesAndShareholdersEquity("DD"), {date(2007, 12, 31):34131.00, \
                                                              date(2007, 9, 30):33915.00, \
                                                              date(2007, 6, 30):32850.00, \
                                                              date(2007, 3, 31):32473.00, \
                                                              date(2006, 12, 31):31777.00})
                                                               
    def testQuarterlySharesOuts(self):
        """ Test that I find Quarterly SharesOuts"""
        self.assertEquals(self.google.getQuarterlySharesOuts("DD"), {date(2007, 12, 31):'-', \
                                   date(2007, 9, 30):'-', \
                                   date(2007, 6, 30):'-', \
                                   date(2007, 3, 31):'-', \
                                   date(2006, 12, 31):'-'})
                                    
    def testQuarterlyTotalCommonSharesOutstanding(self):
        """ Test that I find Quarterly TotalCommonSharesOutstanding"""
        self.assertEquals(self.google.getQuarterlyTotalCommonSharesOutstanding("DD"), {date(2007, 12, 31):899.29, \
                                                     date(2007, 9, 30):898.93, \
                                                     date(2007, 6, 30):920.27, \
                                                     date(2007, 3, 31):923.60, \
                                                     date(2006, 12, 31):922.07})

class WebsiteTestCase_CashFlow(WebsiteTestCase):    
    """ Test all the information that comes from an SEC Cash Flow Statement """
    def testAnnualNetIncomeStartingLine(self):
        """ Test that I find Annual NetIncomeStartingLine"""
        self.assertEquals(self.google.getAnnualNetIncomeStartingLine("DD"), {date(2007, 12, 31):2988.00, \
                                              date(2006, 12, 31):3148.00, \
                                              date(2005, 12, 31):2056.00, \
                                              date(2004, 12, 31):1780.00, \
                                              date(2003, 12, 31):973.00, \
                                              date(2002, 12, 31):-1103.00})
    def testAnnualDepreciationDepletion(self):
        """ Test that I find Annual DepreciationDepletion"""  
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
        """ Test that I find Annual DeferredTaxes"""
        self.assertEquals(self.google.getAnnualDeferredTaxes("DD"), {date(2007, 12, 31):-1.00, \
                                      date(2006, 12, 31):-615.00, \
                                      date(2005, 12, 31):109.00, \
                                      date(2004, 12, 31):'-', \
                                      date(2003, 12, 31):'-', \
                                      date(2002, 12, 31):'-'}) 
    def testAnnualNonCashItems(self):
        """ Test that I find Annual NonCashItems"""
        self.assertEquals(self.google.getAnnualNonCashItems("DD"), {date(2007, 12, 31):88.00, \
                                     date(2006, 12, 31):-93.00, \
                                     date(2005, 12, 31):-1703.00, \
                                     date(2004, 12, 31):732.00, \
                                     date(2003, 12, 31):2278.00, \
                                     date(2002, 12, 31):3752.00}) 
    def testAnnualChangesInWorkingCapital(self):
        """ Test that I find Annual ChangesInWorkingCapital"""
        self.assertEquals(self.google.getAnnualChangesInWorkingCapital("DD"), {date(2007, 12, 31):-156.00, \
                                                date(2006, 12, 31):-88.00, \
                                                date(2005, 12, 31):722.00, \
                                                date(2004, 12, 31):-628.00, \
                                                date(2003, 12, 31):-2246.00, \
                                                date(2002, 12, 31):-1725.00}) 
    def testAnnualCashFromOperatingActivities(self):
        """ Test that I find Annual CashFromOperatingActivities"""
        self.assertEquals(self.google.getAnnualCashFromOperatingActivities("DD"), {date(2007, 12, 31):4290.00, \
                                                    date(2006, 12, 31):3736.00, \
                                                    date(2005, 12, 31):2542.00, \
                                                    date(2004, 12, 31):3231.00, \
                                                    date(2003, 12, 31):2589.00, \
                                                    date(2002, 12, 31):2439.00})
    def testAnnualCapitalExpenditures(self):
        """ Test that I find Annual CapitalExpenditures"""
        self.assertEquals(self.google.getAnnualCapitalExpenditures("DD"), {date(2007, 12, 31):-1585.00, \
                                            date(2006, 12, 31):-1532.00, \
                                            date(2005, 12, 31):-1340.00, \
                                            date(2004, 12, 31):-1232.00, \
                                            date(2003, 12, 31):-1713.00, \
                                            date(2002, 12, 31):-1280.00}) 
    def testAnnualOtherInvestingCashFlow(self):
        """ Test that I find Annual OtherInvestingCashFlow"""
        self.assertEquals(self.google.getAnnualOtherInvestingCashFlow("DD"), {date(2007, 12, 31):-165.00, \
                                               date(2006, 12, 31):187.00, \
                                               date(2005, 12, 31):738.00, \
                                               date(2004, 12, 31):3168.00, \
                                               date(2003, 12, 31):-1662.00, \
                                               date(2002, 12, 31):-1312.00}) 
    def testAnnualCashFromInvestingActivities(self):
        """ Test that I find Annual CashFromInvestingActivities"""
        self.assertEquals(self.google.getAnnualCashFromInvestingActivities("DD"), {date(2007, 12, 31):-1750.00, \
                                                    date(2006, 12, 31):-1345.00, \
                                                    date(2005, 12, 31):-602.00, \
                                                    date(2004, 12, 31):1936.00, \
                                                    date(2003, 12, 31):-3375.00, \
                                                    date(2002, 12, 31):-2592.00}) 
    def testAnnualFinancingCashFlowItems(self):
        """ Test that I find Annual FinancingCashFlowItems"""
        self.assertEquals(self.google.getAnnualFinancingCashFlowItems("DD"), {date(2007, 12, 31):-67.00, \
                                               date(2006, 12, 31):-22.00, \
                                               date(2005, 12, 31):-13.00, \
                                               date(2004, 12, 31):-79.00, \
                                               date(2003, 12, 31):-2005.00, \
                                               date(2002, 12, 31):0.00}) 
    def testAnnualTotalCashDividendsPaid(self):
        """ Test that I find Annual TotalCashDividendsPaid"""
        self.assertEquals(self.google.getAnnualTotalCashDividendsPaid("DD"), {date(2007, 12, 31):-1409.00, \
                                               date(2006, 12, 31):-1378.00, \
                                               date(2005, 12, 31):-1439.00, \
                                               date(2004, 12, 31):-1404.00, \
                                               date(2003, 12, 31):-1407.00, \
                                               date(2002, 12, 31):-1401.00}) 
    def testAnnualIssuanceOfStock(self):
        """ Test that I find Annual IssuanceOfStock"""
        self.assertEquals(self.google.getAnnualIssuanceOfStock("DD"), {date(2007, 12, 31):-1250.00, \
                                        date(2006, 12, 31):-132.00, \
                                        date(2005, 12, 31):-3171.00, \
                                        date(2004, 12, 31):-260.00, \
                                        date(2003, 12, 31):52.00, \
                                        date(2002, 12, 31):-436.00}) 
    def testAnnualIssuanceOfDebt(self):
        """ Test that I find Annual IssuanceOfDebt"""
        self.assertEquals(self.google.getAnnualIssuanceOfDebt("DD"), {date(2007, 12, 31):-343.00, \
                                       date(2006, 12, 31):-791.00, \
                                       date(2005, 12, 31):1772.00, \
                                       date(2004, 12, 31):-3807.00, \
                                       date(2003, 12, 31):3391.00, \
                                       date(2002, 12, 31):-281.00}) 
    def testAnnualCashFromFinancingActivities(self):
        """ Test that I find Annual CashFromFinancingActivities"""
        self.assertEquals(self.google.getAnnualCashFromFinancingActivities("DD"), {date(2007, 12, 31):-3069.00, \
                                                    date(2006, 12, 31):-2323.00, \
                                                    date(2005, 12, 31):-2851.00, \
                                                    date(2004, 12, 31):-5550.00, \
                                                    date(2003, 12, 31):31.00, \
                                                    date(2002, 12, 31):-2118.00}) 
    def testAnnualForeignExchangeEffects(self):
        """ Test that I find Annual ForeignExchangeEffects"""
        self.assertEquals(self.google.getAnnualForeignExchangeEffects("DD"), {date(2007, 12, 31):20.00, \
                                               date(2006, 12, 31):10.00, \
                                               date(2005, 12, 31):-722.00, \
                                               date(2004, 12, 31):404.00, \
                                               date(2003, 12, 31):425.00, \
                                               date(2002, 12, 31):186.00}) 
    def testAnnualNetChangeInCash(self):
        """ Test that I find Annual NetChangeInCash"""
        self.assertEquals(self.google.getAnnualNetChangeInCash("DD"), {date(2007, 12, 31):-509.00, \
                                        date(2006, 12, 31):78.00, \
                                        date(2005, 12, 31):-1633.00, \
                                        date(2004, 12, 31):21.00, \
                                        date(2003, 12, 31):-330.00, \
                                        date(2002, 12, 31):-2085.00}) 
    def testAnnualCashInterestPaid(self):
        """ Test that I find Annual CashInterestPaid"""
        self.assertEquals(self.google.getAnnualCashInterestPaid("DD"), {date(2007, 12, 31):527.00, \
                                         date(2006, 12, 31):295.00, \
                                         date(2005, 12, 31):479.00, \
                                         date(2004, 12, 31):366.00, \
                                         date(2003, 12, 31):357.00, \
                                         date(2002, 12, 31):402.00}) 
    def testAnnualCashTaxesPaid(self):
        """ Test that I find Annual CashTaxesPaid"""
        self.assertEquals(self.google.getAnnualCashTaxesPaid("DD"), {date(2007, 12, 31):795.00, \
                                      date(2006, 12, 31):899.00, \
                                      date(2005, 12, 31):355.00, \
                                      date(2004, 12, 31):521.00, \
                                      date(2003, 12, 31):278.00, \
                                      date(2002, 12, 31):1691.00}) 
 
        #quarterly
        
    def testQuarterlyNetIncomeStartingLine(self):
        """ Test that I find Quarterly """
        self.assertEquals(self.google.getQuarterlyNetIncomeStartingLine("DD"), {date(2007, 12, 31):545.00, \
                                              date(2007, 9, 30):526.00, \
                                              date(2007, 6, 30):972.00, \
                                              date(2007, 3, 31):945.00})
                                              
                                              
    def testQuarterlyDepreciationDepletion(self):
        """ Test that I find Quarterly DepreciationDepletion"""
        self.assertEquals(self.google.getQuarterlyDepreciationDepletion("DD"), {date(2007, 12, 31):292.00, \
                                              date(2007, 9, 30):287.00, \
                                              date(2007, 6, 30):289.00, \
                                              date(2007, 3, 31):290.00})
                                              
                                              
    def testQuarterlyAmortization(self):
        """ Test that I find Quarterly Amortization""" 
        self.assertEquals(self.google.getQuarterlyAmortization("DD"), {date(2007, 12, 31):50.00, \
                                     date(2007, 9, 30):53.00, \
                                     date(2007, 6, 30):54.00, \
                                     date(2007, 3, 31):56.00})
                                     
                                      
    def testQuarterlyDeferredTaxes(self):
        """ Test that I find Quarterly DeferredTaxes"""
        self.assertEquals(self.google.getQuarterlyDeferredTaxes("DD"), {date(2007, 12, 31):'-', \
                                      date(2007, 9, 30):'-', \
                                      date(2007, 6, 30):'-', \
                                      date(2007, 3, 31):'-'})
                                      
                                       
    def testQuarterlyNonCashItems(self):
        """ Test that I find Quarterly NonCashItems"""
        self.assertEquals(self.google.getQuarterlyNonCashItems("DD"), {date(2007, 12, 31):164.00, \
                                     date(2007, 9, 30):-32.00, \
                                     date(2007, 6, 30):-33.00, \
                                     date(2007, 3, 31):-11.00})
                                     
                                      
    def testQuarterlyChangesInWorkingCapital(self):
        """ Test that I find Quarterly ChangesInWorkingCapital"""
        self.assertEquals(self.google.getQuarterlyChangesInWorkingCapital("DD"), {date(2007, 12, 31):1814.00, \
                                                date(2007, 9, 30):209.00, \
                                                date(2007, 6, 30):-659.00, \
                                                date(2007, 3, 31):-1520.00})
                                                
                                                 
    def testQuarterlyCashFromOperatingActivities(self):
        """ Test that I find Quarterly CashFromOperatingActivities"""
        self.assertEquals(self.google.getQuarterlyCashFromOperatingActivities("DD"), {date(2007, 12, 31):2864.00, \
                                                    date(2007, 9, 30):1043.00, \
                                                    date(2007, 6, 30):623.00, \
                                                    date(2007, 3, 31):-240.00})
                                                    
                                                    
    def testQuarterlyCapitalExpenditures(self):
        """ Test that I find Quarterly CapitalExpenditures"""
        self.assertEquals(self.google.getQuarterlyCapitalExpenditures("DD"), {date(2007, 12, 31):-566.00, \
                                            date(2007, 9, 30):-398.00, \
                                            date(2007, 6, 30):-348.00, \
                                            date(2007, 3, 31):-273.00})
                                            
                                             
    def testQuarterlyOtherInvestingCashFlow(self):
        """ Test that I find Quarterly OtherInvestingCashFlow"""
        self.assertEquals(self.google.getQuarterlyOtherInvestingCashFlow("DD"), {date(2007, 12, 31):-164.00, \
                                               date(2007, 9, 30):50.00, \
                                               date(2007, 6, 30):-55.00, \
                                               date(2007, 3, 31):4.00})
                                               
                                                
    def testQuarterlyCashFromInvestingActivities(self):
        """ Test that I find Quarterly CashFromInvestingActivities"""
        self.assertEquals(self.google.getQuarterlyCashFromInvestingActivities("DD"), {date(2007, 12, 31):-730.00, \
                                                    date(2007, 9, 30):-348.00, \
                                                    date(2007, 6, 30):-403.00, \
                                                    date(2007, 3, 31):-269.00})
                                                    
                                                     
    def testQuarterlyFinancingCashFlowItems(self):
        """ Test that I find Quarterly FinancingCashFlowItems"""
        self.assertEquals(self.google.getQuarterlyFinancingCashFlowItems("DD"), {date(2007, 12, 31):5.00, \
                                               date(2007, 9, 30):8.00, \
                                               date(2007, 6, 30):-11.00, \
                                               date(2007, 3, 31):-69.00})
                                               
                                                
    def testQuarterlyTotalCashDividendsPaid(self):
        """ Test that I find Quarterly TotalCashDividendsPaid"""
        self.assertEquals(self.google.getQuarterlyTotalCashDividendsPaid("DD"), {date(2007, 12, 31):-372.00, \
                                               date(2007, 9, 30):-345.00, \
                                               date(2007, 6, 30):-345.00, \
                                               date(2007, 3, 31):-347.00})
                                               
                                                
    def testQuarterlyIssuanceOfStock(self):
        """ Test that I find Quarterly IssuanceOfStock"""
        self.assertEquals(self.google.getQuarterlyIssuanceOfStock("DD"), {date(2007, 12, 31):14.00, \
                                        date(2007, 9, 30):-1029.00, \
                                        date(2007, 6, 30):-185.00, \
                                        date(2007, 3, 31):-50.00})
                                        
                                         
    def testQuarterlyIssuanceOfDebt(self):
        """ Test that I find Quarterly IssuanceOfDebt"""
        self.assertEquals(self.google.getQuarterlyIssuanceOfDebt("DD"), {date(2007, 12, 31):-1673.00, \
                                       date(2007, 9, 30):858.00, \
                                       date(2007, 6, 30):431.00, \
                                       date(2007, 3, 31):41.00})
                                       
                                        
    def testQuarterlyCashFromFinancingActivities(self):
        """ Test that I find Quarterly CashFromFinancingActivities"""
        self.assertEquals(self.google.getQuarterlyCashFromFinancingActivities("DD"), {date(2007, 12, 31):-2026.00, \
                                                    date(2007, 9, 30):-508.00, \
                                                    date(2007, 6, 30):-110.00, \
                                                    date(2007, 3, 31):-425.00})
                                                    
                                                     
    def testQuarterlyForeignExchangeEffects(self):
        """ Test that I find Quarterly ForeignExchangeEffects"""
        self.assertEquals(self.google.getQuarterlyForeignExchangeEffects("DD"), {date(2007, 12, 31):-12.00, \
                                               date(2007, 9, 30):35.00, \
                                               date(2007, 6, 30):-6.00, \
                                               date(2007, 3, 31):3.00})
                                               
                                                
    def testQuarterlyNetChangeInCash(self):
        """ Test that I find Quarterly NetChangeInCash"""
        self.assertEquals(self.google.getQuarterlyNetChangeInCash("DD"), {date(2007, 12, 31):96.00, \
                                        date(2007, 9, 30):222.00, \
                                        date(2007, 6, 30):104.00, \
                                        date(2007, 3, 31):-931.00})
                                        
                                         
    def testQuarterlyCashInterestPaid(self):
        """ Test that I find Quarterly CashInterestPaid"""
        self.assertEquals(self.google.getQuarterlyCashInterestPaid("DD"), {date(2007, 12, 31):'-', \
                                         date(2007, 9, 30):'-', \
                                         date(2007, 6, 30):'-', \
                                         date(2007, 3, 31):'-'})
                                         
                                          
    def testQuarterlyCashTaxesPaid(self):
        """ Test that I find Quarterly CashTaxesPaid"""
        self.assertEquals(self.google.getQuarterlyCashTaxesPaid("DD"), {date(2007, 12, 31):'-', \
                                      date(2007, 9, 30):'-', \
                                      date(2007, 6, 30):'-', \
                                      date(2007, 3, 31):'-'})

#quarterly
#incomestatement

                                              
 

#testing balance sheet

                                                      
 
#cash flow


                                      
                                       
