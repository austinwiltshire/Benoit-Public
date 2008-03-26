import Website
#making a change.
from TestTools import assertClose, compareDicts
from datetime import date

totest = Website.Google()


#i am making a change!!!

#incomestatement
res =compareDicts(totest.getAnnualRevenue("DD"), {date(2007, 12, 31):29378.00, \
                                             date(2006, 12, 31):27421.00, \
                                             date(2005, 12, 31):26639.00, \
                                             date(2004, 12, 31):27340.00, \
                                             date(2003, 12, 31):26996.00, \
                                             date(2002, 12, 31):24006})
assert res[0], res[1] 
res = compareDictsres = compareDicts(totest.getAnnualOtherRevenue("DD"), {date(2007, 12, 31):1275.00, \
                                     date(2006, 12, 31):1561.00, \
                                     date(2005, 12, 31):1852.00, \
                                     date(2004, 12, 31):655.00, \
                                     date(2003, 12, 31):734.00, \
                                     date(2002, 12, 31):516.00})   
assert res[0], res[1]                                          
res = compareDicts(totest.getAnnualTotalRevenue("DD"), {date(2007, 12, 31):30653.00, \
                                     date(2006, 12, 31):28982.00, \
                                     date(2005, 12, 31):28491.00, \
                                     date(2004, 12, 31):27995.00, \
                                     date(2003, 12, 31):27730.00, \
                                     date(2002, 12, 31):24522.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCostOfRevenue("DD"), {date(2007, 12, 31):21565.00, \
                                      date(2006, 12, 31):20440.00, \
                                      date(2005, 12, 31):19683.00, \
                                      date(2004, 12, 31):20827.00, \
                                      date(2003, 12, 31):20759.00, \
                                      date(2002, 12, 31):17529.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualGrossProfit("DD"), {date(2007, 12, 31):7813.00, \
                                    date(2006, 12, 31):6981.00, \
                                    date(2005, 12, 31):6956.00, \
                                    date(2004, 12, 31):6513.00, \
                                    date(2003, 12, 31):6237.00, \
                                    date(2002, 12, 31):6477.00})
assert res[0], res[1] 
res = compareDicts(totest.getAnnualSGAExpenses("DD"), {date(2007, 12, 31):3364.00, \
                                    date(2006, 12, 31):3224.00, \
                                    date(2005, 12, 31):3223.00, \
                                    date(2004, 12, 31):3141.00, \
                                    date(2003, 12, 31):3067.00, \
                                    date(2002, 12, 31):2763.00})
assert res[0], res[1] 
res = compareDicts(totest.getAnnualResearchAndDevelopment("DD"), {date(2007, 12, 31):1338.00, \
                                               date(2006, 12, 31):1302.00, \
                                               date(2005, 12, 31):1336.00, \
                                               date(2004, 12, 31):1333.00, \
                                               date(2003, 12, 31):1349.00, \
                                               date(2002, 12, 31):1264.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDepreciationAmortization("DD"), {date(2007, 12, 31):213.00, \
                                                 date(2006, 12, 31):227.00, \
                                                 date(2005, 12, 31):230.00, \
                                                 date(2004, 12, 31):223.00, \
                                                 date(2003, 12, 31):229.00, \
                                                 date(2002, 12, 31):218.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualInterestNetOperating("DD"), {date(2007, 12, 31):430.00, \
                                             date(2006, 12, 31):460.00, \
                                             date(2005, 12, 31):518.00, \
                                             date(2004, 12, 31):362.00, \
                                             date(2003, 12, 31):347.00, \
                                             date(2002, 12, 31):359.00})
assert res[0], res[1] 
res = compareDicts(totest.getAnnualUnusualExpense("DD"), {date(2007, 12, 31):0.00, \
                                       date(2006, 12, 31):0.00, \
                                       date(2005, 12, 31):-62.00, \
                                       date(2004, 12, 31):667.00, \
                                       date(2003, 12, 31):1898.00, \
                                       date(2002, 12, 31):290.00})
assert res[0], res[1] 
res = compareDicts(totest.getAnnualOtherOperatingExpenses("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):-62.00, \
                                               date(2002, 12, 31):-25.00})
assert res[0], res[1] 
res = compareDicts(totest.getAnnualTotalOperatingExpense("DD"), {date(2007, 12, 31):26910.00, \
                                              date(2006, 12, 31):25653.00, \
                                              date(2005, 12, 31):24928.00, \
                                              date(2004, 12, 31):26553.00, \
                                              date(2003, 12, 31):27587.00, \
                                              date(2002, 12, 31):22398.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualOperatingIncome("DD"), {date(2007, 12, 31):3743.00, \
                                        date(2006, 12, 31):3329.00, \
                                        date(2005, 12, 31):3563.00, \
                                        date(2004, 12, 31):1442.00, \
                                        date(2003, 12, 31):143.00, \
                                        date(2002, 12, 31):2124.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualInterestIncome("DD"), {date(2007, 12, 31):'-', \
                                       date(2006, 12, 31):'-', \
                                       date(2005, 12, 31):'-', \
                                       date(2004, 12, 31):'-', \
                                       date(2003, 12, 31):'-', \
                                       date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualGainOnSaleOfAssets("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualOtherNet("DD"), {date(2007, 12, 31):'-', \
                                 date(2006, 12, 31):'-', \
                                 date(2005, 12, 31):'-', \
                                 date(2004, 12, 31):'-', \
                                 date(2003, 12, 31):'-', \
                                 date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualIncomeBeforeTax("DD"), {date(2007, 12, 31):3743.00, \
                                        date(2006, 12, 31):3329.00, \
                                        date(2005, 12, 31):3563.00, \
                                        date(2004, 12, 31):1442.00, \
                                        date(2003, 12, 31):143.00, \
                                        date(2002, 12, 31):2124.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualIncomeAfterTax("DD"), {date(2007, 12, 31):2995.0, \
                                       date(2006, 12, 31):3133.00, \
                                       date(2005, 12, 31):2093.00, \
                                       date(2004, 12, 31):1771.00, \
                                       date(2003, 12, 31):1073.00, \
                                       date(2002, 12, 31):1939.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualMinorityInterest_Inc("DD"), {date(2007, 12, 31):-7.00, \
                                         date(2006, 12, 31):15.00, \
                                         date(2005, 12, 31):-37.00, \
                                         date(2004, 12, 31):9.00, \
                                         date(2003, 12, 31):-71.00, \
                                         date(2002, 12, 31):-98.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualEquityInAffiliates("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualNetIncomeBeforeExtraItems("DD"), {date(2007, 12, 31):2988.00, \
                                                  date(2006, 12, 31):3148.00, \
                                                  date(2005, 12, 31):2056.00, \
                                                  date(2004, 12, 31):1780.00, \
                                                  date(2003, 12, 31):1002.00, \
                                                  date(2002, 12, 31):1841.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualAccountingChange("DD"), {date(2007, 12, 31):'-', \
                                         date(2006, 12, 31):'-', \
                                         date(2005, 12, 31):'-', \
                                         date(2004, 12, 31):'-', \
                                         date(2003, 12, 31):'-', \
                                         date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDiscontinuedOperations("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualExtraordinaryItem("DD"), {date(2007, 12, 31):'-', \
                                          date(2006, 12, 31):'-', \
                                          date(2005, 12, 31):'-', \
                                          date(2004, 12, 31):'-', \
                                          date(2003, 12, 31):'-', \
                                          date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualNetIncome("DD"), {date(2007, 12, 31):2988.00, \
                                  date(2006, 12, 31):3148.00, \
                                  date(2005, 12, 31):2056.00, \
                                  date(2004, 12, 31):1780.00, \
                                  date(2003, 12, 31):973.00, \
                                  date(2002, 12, 31):-1103.00},prnt=True) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualPreferredDividends("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualIncomeAvailToCommonExclExtraItems("DD"), {date(2007, 12, 31):2978.00, \
                                                          date(2006, 12, 31):3138.00, \
                                                          date(2005, 12, 31):2046.00, \
                                                          date(2004, 12, 31):1770.00, \
                                                          date(2003, 12, 31):992.00, \
                                                          date(2002, 12, 31):1831.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualIncomeAvailToCommonInclExtraItems("DD"), {date(2007, 12, 31):2978.00, \
                                                          date(2006, 12, 31):3138.00, \
                                                          date(2005, 12, 31):2046.00, \
                                                          date(2004, 12, 31):1770.00, \
                                                          date(2003, 12, 31):963.00, \
                                                          date(2002, 12, 31):-1113.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualBasicWeightedAverageShares("DD"), {date(2007, 12, 31):'-', \
                                                   date(2006, 12, 31):'-', \
                                                   date(2005, 12, 31):'-', \
                                                   date(2004, 12, 31):'-', \
                                                   date(2003, 12, 31):'-', \
                                                   date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualBasicEPSExclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualBasicEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDilutionAdjustment("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):0.00, \
                                           date(2002, 12, 31):0.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDilutedWeightedAverageShares("DD"), {date(2007, 12, 31):925.40, \
                                                     date(2006, 12, 31):928.60, \
                                                     date(2005, 12, 31):988.95, \
                                                     date(2004, 12, 31):1003.39, \
                                                     date(2003, 12, 31):1000.01, \
                                                     date(2002, 12, 31):998.74}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDilutedEPSExclExtraItems("DD"), {date(2007, 12, 31):3.22, \
                                                 date(2006, 12, 31):3.38, \
                                                 date(2005, 12, 31):2.07, \
                                                 date(2004, 12, 31):1.76, \
                                                 date(2003, 12, 31):0.99, \
                                                 date(2002, 12, 31):1.83}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDilutedEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                                 date(2006, 12, 31):'-', \
                                                 date(2005, 12, 31):'-', \
                                                 date(2004, 12, 31):'-', \
                                                 date(2003, 12, 31):'-', \
                                                 date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDividendsPerShare("DD"), {date(2007, 12, 31):1.52, \
                                          date(2006, 12, 31):1.48, \
                                          date(2005, 12, 31):1.46, \
                                          date(2004, 12, 31):1.40, \
                                          date(2003, 12, 31):1.40, \
                                          date(2002, 12, 31):1.40}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualGrossDividends("DD"), {date(2007, 12, 31):'-', \
                                       date(2006, 12, 31):'-', \
                                       date(2005, 12, 31):'-', \
                                       date(2004, 12, 31):'-', \
                                       date(2003, 12, 31):'-', \
                                       date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualNetIncomeAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                              date(2006, 12, 31):'-', \
                                              date(2005, 12, 31):'-', \
                                              date(2004, 12, 31):'-', \
                                              date(2003, 12, 31):'-', \
                                              date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualBasicEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                             date(2006, 12, 31):'-', \
                                             date(2005, 12, 31):'-', \
                                             date(2004, 12, 31):'-', \
                                             date(2003, 12, 31):'-', \
                                             date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDilutedEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                               date(2006, 12, 31):'-', \
                                               date(2005, 12, 31):'-', \
                                               date(2004, 12, 31):'-', \
                                               date(2003, 12, 31):'-', \
                                               date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDepreciationSupplemental("DD"), {date(2007, 12, 31):'-', \
                                                 date(2006, 12, 31):'-', \
                                                 date(2005, 12, 31):'-', \
                                                 date(2004, 12, 31):'-', \
                                                 date(2003, 12, 31):'-', \
                                                 date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                          date(2006, 12, 31):'-', \
                                          date(2005, 12, 31):'-', \
                                          date(2004, 12, 31):'-', \
                                          date(2003, 12, 31):'-', \
                                          date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualNormalizedIncomeBeforeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                    date(2006, 12, 31):'-', \
                                                    date(2005, 12, 31):'-', \
                                                    date(2004, 12, 31):'-', \
                                                    date(2003, 12, 31):'-', \
                                                    date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualEffectsOfSpecialItemsOnIncomeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                           date(2006, 12, 31):'-', \
                                                           date(2005, 12, 31):'-', \
                                                           date(2004, 12, 31):'-', \
                                                           date(2003, 12, 31):'-', \
                                                           date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualIncomeTaxesExSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                                  date(2006, 12, 31):'-', \
                                                  date(2005, 12, 31):'-', \
                                                  date(2004, 12, 31):'-', \
                                                  date(2003, 12, 31):'-', \
                                                  date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualNormalizedIncomeAfterTaxes("DD"), {date(2007, 12, 31):'-', \
                                                   date(2006, 12, 31):'-', \
                                                   date(2005, 12, 31):'-', \
                                                   date(2004, 12, 31):'-', \
                                                   date(2003, 12, 31):'-', \
                                                   date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualNormalizedIncomeAvailableCommon("DD"), {date(2007, 12, 31):'-', \
                                                        date(2006, 12, 31):'-', \
                                                        date(2005, 12, 31):'-', \
                                                        date(2004, 12, 31):'-', \
                                                        date(2003, 12, 31):'-', \
                                                        date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualBasicNormalizedEPS("DD"), {date(2007, 12, 31):'-', \
                                           date(2006, 12, 31):'-', \
                                           date(2005, 12, 31):'-', \
                                           date(2004, 12, 31):'-', \
                                           date(2003, 12, 31):'-', \
                                           date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDilutedNormalizedEPS("DD"), {date(2007, 12, 31):3.22, \
                                             date(2006, 12, 31):3.38, \
                                             date(2005, 12, 31):2.03, \
                                             date(2004, 12, 31):2.20, \
                                             date(2003, 12, 31):2.19, \
                                             date(2002, 12, 31):1.90}) 
assert res[0], res[1]

#testing balance sheet
res = compareDicts(totest.getAnnualCashAndEquivalents("DD"), {date(2007, 12, 31):1305.00, \
                                           date(2006, 12, 31):1814.00, \
                                           date(2005, 12, 31):1736.00, \
                                           date(2004, 12, 31):3369.00, \
                                           date(2003, 12, 31):3273.00, \
                                           date(2002, 12, 31):3678.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualShortTermInvestments("DD"), {date(2007, 12, 31):131.00, \
                                             date(2006, 12, 31):79.00, \
                                             date(2005, 12, 31):115.00, \
                                             date(2004, 12, 31):167.00, \
                                             date(2003, 12, 31):25.00, \
                                             date(2002, 12, 31):465.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCashAndShortTermInvestments("DD"), {date(2007, 12, 31):1436.00, \
                                                    date(2006, 12, 31):1893.00, \
                                                    date(2005, 12, 31):1851.00, \
                                                    date(2004, 12, 31):3536.00, \
                                                    date(2003, 12, 31):3298.00, \
                                                    date(2002, 12, 31):4143.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualAccountsReceivableTrade("DD"), {date(2007, 12, 31):4649.00, \
                                                date(2006, 12, 31):4335.00, \
                                                date(2005, 12, 31):3907.00, \
                                                date(2004, 12, 31):3860.00, \
                                                date(2003, 12, 31):3427.00, \
                                                date(2002, 12, 31):2913.00})
assert res[0], res[1]
res = compareDicts(totest.getAnnualReceivablesOther("DD"), {date(2007, 12, 31):'-', \
                                         date(2006, 12, 31):'-', \
                                         date(2005, 12, 31):'-', \
                                         date(2004, 12, 31):'-', \
                                         date(2003, 12, 31):'-', \
                                         date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalReceivablesNet("DD"), {date(2007, 12, 31):5683.00, \
                                            date(2006, 12, 31):5198.00, \
                                            date(2005, 12, 31):4801.00, \
                                            date(2004, 12, 31):4889.00, \
                                            date(2003, 12, 31):4218.00, \
                                            date(2002, 12, 31):3884.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalInventory("DD"), {date(2007, 12, 31):5278.00, \
                                       date(2006, 12, 31):4941.00, \
                                       date(2005, 12, 31):4743.00, \
                                       date(2004, 12, 31):4489.00, \
                                       date(2003, 12, 31):4107.00, \
                                       date(2002, 12, 31):4409.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualPrepaidExpenses("DD"), {date(2007, 12, 31):199.00, \
                                        date(2006, 12, 31):182.00, \
                                        date(2005, 12, 31):199.00, \
                                        date(2004, 12, 31):209.00, \
                                        date(2003, 12, 31):208.00, \
                                        date(2002, 12, 31):175.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualOtherCurrentAssetsTotal("DD"), {date(2007, 12, 31):564.00, \
                                                date(2006, 12, 31):656.00, \
                                                date(2005, 12, 31):828.00, \
                                                date(2004, 12, 31):2088.00, \
                                                date(2003, 12, 31):6631.00, \
                                                date(2002, 12, 31):848.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalCurrentAssets("DD"), {date(2007, 12, 31):13160.00, \
                                           date(2006, 12, 31):12870.00, \
                                           date(2005, 12, 31):12422.00, \
                                           date(2004, 12, 31):15211.00, \
                                           date(2003, 12, 31):18462.00, \
                                           date(2002, 12, 31):13459.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualPPE("DD"), {date(2007, 12, 31):26593.00, \
                            date(2006, 12, 31):25719.00, \
                            date(2005, 12, 31):24963.00, \
                            date(2004, 12, 31):23978.00, \
                            date(2003, 12, 31):24149.00, \
                            date(2002, 12, 31):33732.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualGoodwill("DD"), {date(2007, 12, 31):2074.00, \
                                 date(2006, 12, 31):2108.00, \
                                 date(2005, 12, 31):2087.00, \
                                 date(2004, 12, 31):2082.00, \
                                 date(2003, 12, 31):1939.00, \
                                 date(2002, 12, 31):1167.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualIntangibles("DD"), {date(2007, 12, 31):2856.00, \
                                    date(2006, 12, 31):2479.00, \
                                    date(2005, 12, 31):2712.00, \
                                    date(2004, 12, 31):2883.00, \
                                    date(2003, 12, 31):3278.00, \
                                    date(2002, 12, 31):3514.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualLongTermInvestments("DD"), {date(2007, 12, 31):908.00, \
                                            date(2006, 12, 31):897.00, \
                                            date(2005, 12, 31):937.00, \
                                            date(2004, 12, 31):1140.00, \
                                            date(2003, 12, 31):1445.00, \
                                            date(2002, 12, 31):2190.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualOtherLongTermAssets("DD"), {date(2007, 12, 31):4273.00, \
                                            date(2006, 12, 31):2925.00, \
                                            date(2005, 12, 31):4824.00, \
                                            date(2004, 12, 31):4092.00, \
                                            date(2003, 12, 31):2023.00, \
                                            date(2002, 12, 31):1005.00})
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalAssets("DD"), {date(2007, 12, 31):34131.00, \
                                    date(2006, 12, 31):31777.00, \
                                    date(2005, 12, 31):33291.00, \
                                    date(2004, 12, 31):35632.00, \
                                    date(2003, 12, 31):37039.00, \
                                    date(2002, 12, 31):34621.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualAccountsPayable("DD"), {date(2007, 12, 31):3172.00, \
                                        date(2006, 12, 31):2711.00, \
                                        date(2005, 12, 31):2670.00, \
                                        date(2004, 12, 31):2661.00, \
                                        date(2003, 12, 31):2412.00, \
                                        date(2002, 12, 31):2727.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualAccruedExpenses("DD"), {date(2007, 12, 31):3823.00, \
                                        date(2006, 12, 31):3534.00, \
                                        date(2005, 12, 31):3075.00, \
                                        date(2004, 12, 31):4054.00, \
                                        date(2003, 12, 31):2963.00, \
                                        date(2002, 12, 31):3137.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualNotesPayable("DD"), {date(2007, 12, 31):1349.00, \
                                     date(2006, 12, 31):354.00, \
                                     date(2005, 12, 31):0.00, \
                                     date(2004, 12, 31):0.00, \
                                     date(2003, 12, 31):0.00, \
                                     date(2002, 12, 31):0.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCurrentPortLTDebtToCapital("DD"), {date(2007, 12, 31):21.00, \
                                                   date(2006, 12, 31):1163.00, \
                                                   date(2005, 12, 31):1397.00, \
                                                   date(2004, 12, 31):936.00, \
                                                   date(2003, 12, 31):5914.00, \
                                                   date(2002, 12, 31):1185.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualOtherCurrentLiabilities("DD"), {date(2007, 12, 31):176.00, \
                                                date(2006, 12, 31):178.00, \
                                                date(2005, 12, 31):294.00, \
                                                date(2004, 12, 31):288.00, \
                                                date(2003, 12, 31):1754.00, \
                                                date(2002, 12, 31):47.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalCurrentLiabilities("DD"), {date(2007, 12, 31):8541.00, \
                                                date(2006, 12, 31):7940.00, \
                                                date(2005, 12, 31):7436.00, \
                                                date(2004, 12, 31):7939.00, \
                                                date(2003, 12, 31):13043.00, \
                                                date(2002, 12, 31):7096.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                     date(2006, 12, 31):6013.00, \
                                     date(2005, 12, 31):6783.00, \
                                     date(2004, 12, 31):5548.00, \
                                     date(2003, 12, 31):4301.00, \
                                     date(2002, 12, 31):5647.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCapitalLeaseObligations("DD"), {date(2007, 12, 31):'-', \
                                                date(2006, 12, 31):'-', \
                                                date(2005, 12, 31):'-', \
                                                date(2004, 12, 31):'-', \
                                                date(2003, 12, 31):'-', \
                                                date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                          date(2006, 12, 31):6013.00, \
                                          date(2005, 12, 31):6783.00, \
                                          date(2004, 12, 31):5548.00, \
                                          date(2003, 12, 31):4301.00, \
                                          date(2002, 12, 31):5647.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalDebt("DD"), {date(2007, 12, 31):7325.00, \
                                  date(2006, 12, 31):7530.00, \
                                  date(2005, 12, 31):8180.00, \
                                  date(2004, 12, 31):6484.00, \
                                  date(2003, 12, 31):10215.00, \
                                  date(2002, 12, 31):6832.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDeferredIncomeTax("DD"), {date(2007, 12, 31):802.00, \
                                          date(2006, 12, 31):269.00, \
                                          date(2005, 12, 31):1179.00, \
                                          date(2004, 12, 31):966.00, \
                                          date(2003, 12, 31):508.00, \
                                          date(2002, 12, 31):563.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualMinorityInterest_Bal("DD"), {date(2007, 12, 31):442.00, \
                                         date(2006, 12, 31):441.00, \
                                         date(2005, 12, 31):490.00, \
                                         date(2004, 12, 31):1110.00, \
                                         date(2003, 12, 31):497.00, \
                                         date(2002, 12, 31):2423.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualOtherLiabilities("DD"), {date(2007, 12, 31):7255.00, \
                                         date(2006, 12, 31):7692.00, \
                                         date(2005, 12, 31):8441.00, \
                                         date(2004, 12, 31):8692.00, \
                                         date(2003, 12, 31):8909.00, \
                                         date(2002, 12, 31):9829.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalLiabilities("DD"), {date(2007, 12, 31):22995.00, \
                                         date(2006, 12, 31):22355.00, \
                                         date(2005, 12, 31):24329.00, \
                                         date(2004, 12, 31):24255.00, \
                                         date(2003, 12, 31):27258.00, \
                                         date(2002, 12, 31):25558.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualRedeemablePreferredStock("DD"), {date(2007, 12, 31):'-', \
                                                 date(2006, 12, 31):'-', \
                                                 date(2005, 12, 31):'-', \
                                                 date(2004, 12, 31):'-', \
                                                 date(2003, 12, 31):'-', \
                                                 date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualPreferredStockNonRedeemable("DD"), {date(2007, 12, 31):237.00, \
                                                    date(2006, 12, 31):237.00, \
                                                    date(2005, 12, 31):237.00, \
                                                    date(2004, 12, 31):237.00, \
                                                    date(2003, 12, 31):237.00, \
                                                    date(2002, 12, 31):237.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCommonStock("DD"), {date(2007, 12, 31):296.00, \
                                    date(2006, 12, 31):303.00, \
                                    date(2005, 12, 31):302.00, \
                                    date(2004, 12, 31):324.00, \
                                    date(2003, 12, 31):325.00, \
                                    date(2002, 12, 31):324.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualAdditionalPaidInCapital("DD"), {date(2007, 12, 31):8179.00, \
                                                date(2006, 12, 31):7797.00, \
                                                date(2005, 12, 31):7679.00, \
                                                date(2004, 12, 31):7784.00, \
                                                date(2003, 12, 31):7522.00, \
                                                date(2002, 12, 31):7377.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualRetainedEarnings("DD"), {date(2007, 12, 31):9945.00, \
                                         date(2006, 12, 31):9679.00, \
                                         date(2005, 12, 31):7990.00, \
                                         date(2004, 12, 31):10182.00, \
                                         date(2003, 12, 31):10185.00, \
                                         date(2002, 12, 31):10619.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTreasuryStock("DD"), {date(2007, 12, 31):-6727.00, \
                                      date(2006, 12, 31):-6727.00, \
                                      date(2005, 12, 31):-6727.00, \
                                      date(2004, 12, 31):-6727.00, \
                                      date(2003, 12, 31):-6727.00, \
                                      date(2002, 12, 31):-6727.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualOtherEquity("DD"), {date(2007, 12, 31):-794.00, \
                                    date(2006, 12, 31):-1867.00, \
                                    date(2005, 12, 31):-518.00, \
                                    date(2004, 12, 31):-423.00, \
                                    date(2003, 12, 31):-1761.00, \
                                    date(2002, 12, 31):-2767.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalEquity("DD"), {date(2007, 12, 31):11136.00, \
                                    date(2006, 12, 31):9422.00, \
                                    date(2005, 12, 31):8963.00, \
                                    date(2004, 12, 31):11377.00, \
                                    date(2003, 12, 31):9781.00, \
                                    date(2002, 12, 31):9063.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalLiabilitiesAndShareholdersEquity("DD"), {date(2007, 12, 31):34131.00, \
                                                              date(2006, 12, 31):31777.00, \
                                                              date(2005, 12, 31):33292.00, \
                                                              date(2004, 12, 31):35632.00, \
                                                              date(2003, 12, 31):37039.00, \
                                                              date(2002, 12, 31):34621.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualSharesOuts("DD"), {date(2007, 12, 31):'-', \
                                   date(2006, 12, 31):'-', \
                                   date(2005, 12, 31):'-', \
                                   date(2004, 12, 31):'-', \
                                   date(2003, 12, 31):'-', \
                                   date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalCommonSharesOutstanding("DD"), {date(2007, 12, 31):899.29, \
                                                     date(2006, 12, 31):922.07, \
                                                     date(2005, 12, 31):919.61, \
                                                     date(2004, 12, 31):994.34, \
                                                     date(2003, 12, 31):997.28, \
                                                     date(2002, 12, 31):993.94}) 
assert res[0], res[1]
#cash flow
res = compareDicts(totest.getAnnualNetIncomeStartingLine("DD"), {date(2007, 12, 31):2988.00, \
                                              date(2006, 12, 31):3148.00, \
                                              date(2005, 12, 31):2056.00, \
                                              date(2004, 12, 31):1780.00, \
                                              date(2003, 12, 31):973.00, \
                                              date(2002, 12, 31):-1103.00})
assert res[0], res[1] 
res = compareDicts(totest.getAnnualDepreciationDepletion("DD"), {date(2007, 12, 31):1158.00, \
                                              date(2006, 12, 31):1157.00, \
                                              date(2005, 12, 31):1128.00, \
                                              date(2004, 12, 31):1124.00, \
                                              date(2003, 12, 31):1355.00, \
                                              date(2002, 12, 31):1297.00})
assert res[0], res[1] 
res = compareDicts(totest.getAnnualAmortization("DD"), {date(2007, 12, 31):213.00, \
                                     date(2006, 12, 31):227.00, \
                                     date(2005, 12, 31):230.00, \
                                     date(2004, 12, 31):223.00, \
                                     date(2003, 12, 31):229.00, \
                                     date(2002, 12, 31):218.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualDeferredTaxes("DD"), {date(2007, 12, 31):-1.00, \
                                      date(2006, 12, 31):-615.00, \
                                      date(2005, 12, 31):109.00, \
                                      date(2004, 12, 31):'-', \
                                      date(2003, 12, 31):'-', \
                                      date(2002, 12, 31):'-'}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualNonCashItems("DD"), {date(2007, 12, 31):88.00, \
                                     date(2006, 12, 31):-93.00, \
                                     date(2005, 12, 31):-1703.00, \
                                     date(2004, 12, 31):732.00, \
                                     date(2003, 12, 31):2278.00, \
                                     date(2002, 12, 31):3752.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualChangesInWorkingCapital("DD"), {date(2007, 12, 31):-156.00, \
                                                date(2006, 12, 31):-88.00, \
                                                date(2005, 12, 31):722.00, \
                                                date(2004, 12, 31):-628.00, \
                                                date(2003, 12, 31):-2246.00, \
                                                date(2002, 12, 31):-1725.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCashFromOperatingActivities("DD"), {date(2007, 12, 31):4290.00, \
                                                    date(2006, 12, 31):3736.00, \
                                                    date(2005, 12, 31):2542.00, \
                                                    date(2004, 12, 31):3231.00, \
                                                    date(2003, 12, 31):2589.00, \
                                                    date(2002, 12, 31):2439.00})
assert res[0], res[1] 
res = compareDicts(totest.getAnnualCapitalExpenditures("DD"), {date(2007, 12, 31):-1585.00, \
                                            date(2006, 12, 31):-1532.00, \
                                            date(2005, 12, 31):-1340.00, \
                                            date(2004, 12, 31):-1232.00, \
                                            date(2003, 12, 31):-1713.00, \
                                            date(2002, 12, 31):-1280.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualOtherInvestingCashFlow("DD"), {date(2007, 12, 31):-165.00, \
                                               date(2006, 12, 31):187.00, \
                                               date(2005, 12, 31):738.00, \
                                               date(2004, 12, 31):3168.00, \
                                               date(2003, 12, 31):-1662.00, \
                                               date(2002, 12, 31):-1312.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCashFromInvestingActivities("DD"), {date(2007, 12, 31):-1750.00, \
                                                    date(2006, 12, 31):-1345.00, \
                                                    date(2005, 12, 31):-602.00, \
                                                    date(2004, 12, 31):1936.00, \
                                                    date(2003, 12, 31):-3375.00, \
                                                    date(2002, 12, 31):-2592.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualFinancingCashFlowItems("DD"), {date(2007, 12, 31):-67.00, \
                                               date(2006, 12, 31):-22.00, \
                                               date(2005, 12, 31):-13.00, \
                                               date(2004, 12, 31):-79.00, \
                                               date(2003, 12, 31):-2005.00, \
                                               date(2002, 12, 31):0.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualTotalCashDividendsPaid("DD"), {date(2007, 12, 31):-1409.00, \
                                               date(2006, 12, 31):-1378.00, \
                                               date(2005, 12, 31):-1439.00, \
                                               date(2004, 12, 31):-1404.00, \
                                               date(2003, 12, 31):-1407.00, \
                                               date(2002, 12, 31):-1401.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualIssuanceOfStock("DD"), {date(2007, 12, 31):-1250.00, \
                                        date(2006, 12, 31):-132.00, \
                                        date(2005, 12, 31):-3171.00, \
                                        date(2004, 12, 31):-260.00, \
                                        date(2003, 12, 31):52.00, \
                                        date(2002, 12, 31):-436.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualIssuanceOfDebt("DD"), {date(2007, 12, 31):-343.00, \
                                       date(2006, 12, 31):-791.00, \
                                       date(2005, 12, 31):1772.00, \
                                       date(2004, 12, 31):-3807.00, \
                                       date(2003, 12, 31):3391.00, \
                                       date(2002, 12, 31):-281.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCashFromFinancingActivities("DD"), {date(2007, 12, 31):-3069.00, \
                                                    date(2006, 12, 31):-2323.00, \
                                                    date(2005, 12, 31):-2851.00, \
                                                    date(2004, 12, 31):-5550.00, \
                                                    date(2003, 12, 31):31.00, \
                                                    date(2002, 12, 31):-2118.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualForeignExchangeEffects("DD"), {date(2007, 12, 31):20.00, \
                                               date(2006, 12, 31):10.00, \
                                               date(2005, 12, 31):-722.00, \
                                               date(2004, 12, 31):404.00, \
                                               date(2003, 12, 31):425.00, \
                                               date(2002, 12, 31):186.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualNetChangeInCash("DD"), {date(2007, 12, 31):-509.00, \
                                        date(2006, 12, 31):78.00, \
                                        date(2005, 12, 31):-1633.00, \
                                        date(2004, 12, 31):21.00, \
                                        date(2003, 12, 31):-330.00, \
                                        date(2002, 12, 31):-2085.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCashInterestPaid("DD"), {date(2007, 12, 31):527.00, \
                                         date(2006, 12, 31):295.00, \
                                         date(2005, 12, 31):479.00, \
                                         date(2004, 12, 31):366.00, \
                                         date(2003, 12, 31):357.00, \
                                         date(2002, 12, 31):402.00}) 
assert res[0], res[1]
res = compareDicts(totest.getAnnualCashTaxesPaid("DD"), {date(2007, 12, 31):795.00, \
                                      date(2006, 12, 31):899.00, \
                                      date(2005, 12, 31):355.00, \
                                      date(2004, 12, 31):521.00, \
                                      date(2003, 12, 31):278.00, \
                                      date(2002, 12, 31):1691.00}) 
assert res[0], res[1]



































#quarterly
#incomestatement
res =compareDicts(totest.getQuarterlyRevenue("DD"), {date(2007, 12, 31):6983.00, \
                                             date(2007, 9, 30):6675.00, \
                                             date(2007, 6, 30):7875.00, \
                                             date(2007, 3, 31):7845.00, \
                                             date(2006, 12, 31):6276.00})
                                             
assert res[0], res[1] 
res = compareDictsres = compareDicts(totest.getQuarterlyOtherRevenue("DD"), {date(2007, 12, 31):230.00, \
                                     date(2007, 9, 30):365.00, \
                                     date(2007, 6, 30):364.00, \
                                     date(2007, 3, 31):316.00, \
                                     date(2006, 12, 31):559.00})
                                        
assert res[0], res[1]                                          
res = compareDicts(totest.getQuarterlyTotalRevenue("DD"), {date(2007, 12, 31):7213.00, \
                                     date(2007, 9, 30):7040.00, \
                                     date(2007, 6, 30):8239.00, \
                                     date(2007, 3, 31):8161.00, \
                                     date(2006, 12, 31):6835.00})
                                      
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCostOfRevenue("DD"), {date(2007, 12, 31):5349.00, \
                                      date(2007, 9, 30):5115.00, \
                                      date(2007, 6, 30):5555.00, \
                                      date(2007, 3, 31):5546.00, \
                                      date(2006, 12, 31):5114.00})
                                       
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyGrossProfit("DD"), {date(2007, 12, 31):1634.00, \
                                    date(2007, 9, 30):1560.00, \
                                    date(2007, 6, 30):2320.00, \
                                    date(2007, 3, 31):2299.00, \
                                    date(2006, 12, 31):1162.00})
                                    
assert res[0], res[1] 
res = compareDicts(totest.getQuarterlySGAExpenses("DD"), {date(2007, 12, 31):852.00, \
                                    date(2007, 9, 30):797.00, \
                                    date(2007, 6, 30):877.00, \
                                    date(2007, 3, 31):838.00, \
                                    date(2006, 12, 31):824.00})
                                    
assert res[0], res[1] 
res = compareDicts(totest.getQuarterlyResearchAndDevelopment("DD"), {date(2007, 12, 31):359.00, \
                                               date(2007, 9, 30):332.00, \
                                               date(2007, 6, 30):337.00, \
                                               date(2007, 3, 31):310.00, \
                                               date(2006, 12, 31):341.00})
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDepreciationAmortization("DD"), {date(2007, 12, 31):50.00, \
                                                 date(2007, 9, 30):53.00, \
                                                 date(2007, 6, 30):54.00, \
                                                 date(2007, 3, 31):56.00, \
                                                 date(2006, 12, 31):55.00})
                                                  
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyInterestNetOperating("DD"), {date(2007, 12, 31):110.00, \
                                             date(2007, 9, 30):113.00, \
                                             date(2007, 6, 30):108.00, \
                                             date(2007, 3, 31):99.00, \
                                             date(2006, 12, 31):113.00})
                                             
assert res[0], res[1] 
res = compareDicts(totest.getQuarterlyUnusualExpense("DD"), {date(2007, 12, 31):'-', \
                                       date(2007, 9, 30):'-', \
                                       date(2007, 6, 30):'-', \
                                       date(2007, 3, 31):'-', \
                                       date(2006, 12, 31):0.00})
                                       
assert res[0], res[1] 
res = compareDicts(totest.getQuarterlyOtherOperatingExpenses("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                               
assert res[0], res[1] 
res = compareDicts(totest.getQuarterlyTotalOperatingExpense("DD"), {date(2007, 12, 31):6720.00, \
                                              date(2007, 9, 30):6410.00, \
                                              date(2007, 6, 30):6931.00, \
                                              date(2007, 3, 31):6849.00, \
                                              date(2006, 12, 31):6447.00})
                                               
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyOperatingIncome("DD"), {date(2007, 12, 31):493.00, \
                                        date(2007, 9, 30):630.00, \
                                        date(2007, 6, 30):1308.00, \
                                        date(2007, 3, 31):1312.00, \
                                        date(2006, 12, 31):388.00})
                                         
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyInterestIncome("DD"), {date(2007, 12, 31):'-', \
                                       date(2007, 9, 30):'-', \
                                       date(2007, 6, 30):'-', \
                                       date(2007, 3, 31):'-', \
                                       date(2006, 12, 31):'-'})
                                        
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyGainOnSaleOfAssets("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyOtherNet("DD"), {date(2007, 12, 31):'-', \
                                 date(2007, 9, 30):'-', \
                                 date(2007, 6, 30):'-', \
                                 date(2007, 3, 31):'-', \
                                 date(2006, 12, 31):'-'})
                                  
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyIncomeBeforeTax("DD"), {date(2007, 12, 31):493.00, \
                                        date(2007, 9, 30):630.00, \
                                        date(2007, 6, 30):1308.00, \
                                        date(2007, 3, 31):1312.00, \
                                        date(2006, 12, 31):388.00})
                                         
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyIncomeAfterTax("DD"), {date(2007, 12, 31):547.00, \
                                       date(2007, 9, 30):528.00, \
                                       date(2007, 6, 30):973.00, \
                                       date(2007, 3, 31):947.00, \
                                       date(2006, 12, 31):853.00})
                                        
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyMinorityInterest_Inc("DD"), {date(2007, 12, 31):-2.00, \
                                         date(2007, 9, 30):-2.00, \
                                         date(2007, 6, 30):-1.00, \
                                         date(2007, 3, 31):-2.00, \
                                         date(2006, 12, 31):18.00})
                                          
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyEquityInAffiliates("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyNetIncomeBeforeExtraItems("DD"), {date(2007, 12, 31):545.00, \
                                                  date(2007, 9, 30):526.00, \
                                                  date(2007, 6, 30):972.00, \
                                                  date(2007, 3, 31):945.00, \
                                                  date(2006, 12, 31):871.00})
                                                   
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyAccountingChange("DD"), {date(2007, 12, 31):'-', \
                                         date(2007, 9, 30):'-', \
                                         date(2007, 6, 30):'-', \
                                         date(2007, 3, 31):'-', \
                                         date(2006, 12, 31):'-'})
                                          
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDiscontinuedOperations("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyExtraordinaryItem("DD"), {date(2007, 12, 31):'-', \
                                          date(2007, 9, 30):'-', \
                                          date(2007, 6, 30):'-', \
                                          date(2007, 3, 31):'-', \
                                          date(2006, 12, 31):'-'})
                                           
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyNetIncome("DD"), {date(2007, 12, 31):545.00, \
                                  date(2007, 9, 30):526.00, \
                                  date(2007, 6, 30):972.00, \
                                  date(2007, 3, 31):945.00, \
                                  date(2006, 12, 31):871.00})
                                   
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyPreferredDividends("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyIncomeAvailToCommonExclExtraItems("DD"), {date(2007, 12, 31):543.00, \
                                                          date(2007, 9, 30):524.00, \
                                                          date(2007, 6, 30):969.00, \
                                                          date(2007, 3, 31):942.00, \
                                                          date(2006, 12, 31):869.00})
                                                           
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyIncomeAvailToCommonInclExtraItems("DD"), {date(2007, 12, 31):543.00, \
                                                          date(2007, 9, 30):524.00, \
                                                          date(2007, 6, 30):969.00, \
                                                          date(2007, 3, 31):942.00, \
                                                          date(2006, 12, 31):869.00})
                                                           
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyBasicWeightedAverageShares("DD"), {date(2007, 12, 31):'-', \
                                                   date(2007, 9, 30):'-', \
                                                   date(2007, 6, 30):'-', \
                                                   date(2007, 3, 31):'-', \
                                                   date(2006, 12, 31):'-'})
                                                    
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyBasicEPSExclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyBasicEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDilutionAdjustment("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDilutedWeightedAverageShares("DD"), {date(2007, 12, 31):906.48, \
                                                     date(2007, 9, 30):929.32, \
                                                     date(2007, 6, 30):932.81, \
                                                     date(2007, 3, 31):933.27, \
                                                     date(2006, 12, 31):941.43})
                                                      
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDilutedEPSExclExtraItems("DD"), {date(2007, 12, 31):0.60, \
                                                 date(2007, 9, 30):0.56, \
                                                 date(2007, 6, 30):1.04, \
                                                 date(2007, 3, 31):1.01, \
                                                 date(2006, 12, 31):0.92})
                                                  
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDilutedEPSInclExtraItems("DD"), {date(2007, 12, 31):'-', \
                                                 date(2007, 9, 30):'-', \
                                                 date(2007, 6, 30):'-', \
                                                 date(2007, 3, 31):'-', \
                                                 date(2006, 12, 31):'-'})
                                                  
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDividendsPerShare("DD"), {date(2007, 12, 31):0.41, \
                                          date(2007, 9, 30):0.37, \
                                          date(2007, 6, 30):0.37, \
                                          date(2007, 3, 31):0.37, \
                                          date(2006, 12, 31):0.37})
                                           
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyGrossDividends("DD"), {date(2007, 12, 31):'-', \
                                       date(2007, 9, 30):'-', \
                                       date(2007, 6, 30):'-', \
                                       date(2007, 3, 31):'-', \
                                       date(2006, 12, 31):'-'})
                                        
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyNetIncomeAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                              date(2007, 9, 30):'-', \
                                              date(2007, 6, 30):'-', \
                                              date(2007, 3, 31):'-', \
                                              date(2006, 12, 31):'-'})
                                               
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyBasicEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                             date(2007, 9, 30):'-', \
                                             date(2007, 6, 30):'-', \
                                             date(2007, 3, 31):'-', \
                                             date(2006, 12, 31):'-'})
                                              
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDilutedEPSAfterCompExp("DD"), {date(2007, 12, 31):'-', \
                                               date(2007, 9, 30):'-', \
                                               date(2007, 6, 30):'-', \
                                               date(2007, 3, 31):'-', \
                                               date(2006, 12, 31):'-'})
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDepreciationSupplemental("DD"), {date(2007, 12, 31):'-', \
                                                 date(2007, 9, 30):'-', \
                                                 date(2007, 6, 30):'-', \
                                                 date(2007, 3, 31):'-', \
                                                 date(2006, 12, 31):'-'})
                                                  
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                          date(2007, 9, 30):'-', \
                                          date(2007, 6, 30):'-', \
                                          date(2007, 3, 31):'-', \
                                          date(2006, 12, 31):'-'})
                                           
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyNormalizedIncomeBeforeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                    date(2007, 9, 30):'-', \
                                                    date(2007, 6, 30):'-', \
                                                    date(2007, 3, 31):'-', \
                                                    date(2006, 12, 31):'-'})
                                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyEffectsOfSpecialItemsOnIncomeTaxes("DD"), {date(2007, 12, 31):'-', \
                                                           date(2007, 9, 30):'-', \
                                                           date(2007, 6, 30):'-', \
                                                           date(2007, 3, 31):'-', \
                                                           date(2006, 12, 31):'-'})
                                                            
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyIncomeTaxesExSpecialItems("DD"), {date(2007, 12, 31):'-', \
                                                  date(2007, 9, 30):'-', \
                                                  date(2007, 6, 30):'-', \
                                                  date(2007, 3, 31):'-', \
                                                  date(2006, 12, 31):'-'})
                                                   
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyNormalizedIncomeAfterTaxes("DD"), {date(2007, 12, 31):'-', \
                                                   date(2007, 9, 30):'-', \
                                                   date(2007, 6, 30):'-', \
                                                   date(2007, 3, 31):'-', \
                                                   date(2006, 12, 31):'-'})
                                                    
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyNormalizedIncomeAvailableCommon("DD"), {date(2007, 12, 31):'-', \
                                                        date(2007, 9, 30):'-', \
                                                        date(2007, 6, 30):'-', \
                                                        date(2007, 3, 31):'-', \
                                                        date(2006, 12, 31):'-'})
                                                         
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyBasicNormalizedEPS("DD"), {date(2007, 12, 31):'-', \
                                           date(2007, 9, 30):'-', \
                                           date(2007, 6, 30):'-', \
                                           date(2007, 3, 31):'-', \
                                           date(2006, 12, 31):'-'})
                                            
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDilutedNormalizedEPS("DD"), {date(2007, 12, 31):0.60, \
                                             date(2007, 9, 30):0.56, \
                                             date(2007, 6, 30):1.04, \
                                             date(2007, 3, 31):1.01, \
                                             date(2006, 12, 31):0.92})
                                              
assert res[0], res[1]

#testing balance sheet
res = compareDicts(totest.getQuarterlyCashAndEquivalents("DD"), {date(2007, 12, 31):1305.00, \
                                           date(2007, 9, 30):1209.00, \
                                           date(2007, 6, 30):987.00, \
                                           date(2007, 3, 31):883.00, \
                                           date(2006, 12, 31):1814.00})
                                            
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyShortTermInvestments("DD"), {date(2007, 12, 31):131.00, \
                                             date(2007, 9, 30):109.00, \
                                             date(2007, 6, 30):102.00, \
                                             date(2007, 3, 31):71.00, \
                                             date(2006, 12, 31):79.00})
                                              
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCashAndShortTermInvestments("DD"), {date(2007, 12, 31):1436.00, \
                                                    date(2007, 9, 30):1318.00, \
                                                    date(2007, 6, 30):1089.00, \
                                                    date(2007, 3, 31):954.00, \
                                                    date(2006, 12, 31):1893.00})
                                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyAccountsReceivableTrade("DD"), {date(2007, 12, 31):5683.00, \
                                                date(2007, 9, 30):6990.00, \
                                                date(2007, 6, 30):7370.00, \
                                                date(2007, 3, 31):6813.00, \
                                                date(2006, 12, 31):5198.00})
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyReceivablesOther("DD"), {date(2007, 12, 31):'-', \
                                         date(2007, 9, 30):'-', \
                                         date(2007, 6, 30):'-', \
                                         date(2007, 3, 31):'-', \
                                         date(2006, 12, 31):'-'})
                                          
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalReceivablesNet("DD"), {date(2007, 12, 31):5683.00, \
                                            date(2007, 9, 30):6990.00, \
                                            date(2007, 6, 30):7370.00, \
                                            date(2007, 3, 31):6813.00, \
                                            date(2006, 12, 31):5198.00})
                                             
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalInventory("DD"), {date(2007, 12, 31):5278.00, \
                                       date(2007, 9, 30):4963.00, \
                                       date(2007, 6, 30):4481.00, \
                                       date(2007, 3, 31):4855.00, \
                                       date(2006, 12, 31):4941.00})
                                        
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyPrepaidExpenses("DD"), {date(2007, 12, 31):199.00, \
                                        date(2007, 9, 30):195.00, \
                                        date(2007, 6, 30):199.00, \
                                        date(2007, 3, 31):213.00, \
                                        date(2006, 12, 31):182.00})
                                         
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyOtherCurrentAssetsTotal("DD"), {date(2007, 12, 31):564.00, \
                                                date(2007, 9, 30):665.00, \
                                                date(2007, 6, 30):675.00, \
                                                date(2007, 3, 31):697.00, \
                                                date(2006, 12, 31):656.00})
                                                 
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalCurrentAssets("DD"), {date(2007, 12, 31):13160.00, \
                                           date(2007, 9, 30):14131.00, \
                                           date(2007, 6, 30):13814.00, \
                                           date(2007, 3, 31):13532.00, \
                                           date(2006, 12, 31):12870.00})
                                            
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyPPE("DD"), {date(2007, 12, 31):26593.00, \
                            date(2007, 9, 30):26302.00, \
                            date(2007, 6, 30):26053.00, \
                            date(2007, 3, 31):25876.00, \
                            date(2006, 12, 31):25719.00})
                             
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyGoodwill("DD"), {date(2007, 12, 31):2074.00, \
                                 date(2007, 9, 30):2110.00, \
                                 date(2007, 6, 30):2108.00, \
                                 date(2007, 3, 31):2108.00, \
                                 date(2006, 12, 31):2108.00})
                                  
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyIntangibles("DD"), {date(2007, 12, 31):2856.00, \
                                    date(2007, 9, 30):2904.00, \
                                    date(2007, 6, 30):2381.00, \
                                    date(2007, 3, 31):2436.00, \
                                    date(2006, 12, 31):2479.00})
                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyLongTermInvestments("DD"), {date(2007, 12, 31):818.00, \
                                            date(2007, 9, 30):791.00, \
                                            date(2007, 6, 30):802.00, \
                                            date(2007, 3, 31):790.00, \
                                            date(2006, 12, 31):803.00})
                                             
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyOtherLongTermAssets("DD"), {date(2007, 12, 31):4363.00, \
                                            date(2007, 9, 30):3411.00, \
                                            date(2007, 6, 30):3267.00, \
                                            date(2007, 3, 31):3182.00, \
                                            date(2006, 12, 31):3019.00})
                                            
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalAssets("DD"), {date(2007, 12, 31):34131.00, \
                                    date(2007, 9, 30):33915.00, \
                                    date(2007, 6, 30):32850.00, \
                                    date(2007, 3, 31):32473.00, \
                                    date(2006, 12, 31):31777.00})
                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyAccountsPayable("DD"), {date(2007, 12, 31):3172.00, \
                                        date(2007, 9, 30):2873.00, \
                                        date(2007, 6, 30):2539.00, \
                                        date(2007, 3, 31):2782.00, \
                                        date(2006, 12, 31):2711.00})
                                         
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyAccruedExpenses("DD"), {date(2007, 12, 31):3823.00, \
                                        date(2007, 9, 30):2972.00, \
                                        date(2007, 6, 30):2921.00, \
                                        date(2007, 3, 31):3020.00, \
                                        date(2006, 12, 31):3534.00})
                                         
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyNotesPayable("DD"), {date(2007, 12, 31):1349.00, \
                                     date(2007, 9, 30):3618.00, \
                                     date(2007, 6, 30):1226.00, \
                                     date(2007, 3, 31):429.00, \
                                     date(2006, 12, 31):354.00})
                                      
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCurrentPortLTDebtToCapital("DD"), {date(2007, 12, 31):21.00, \
                                                   date(2007, 9, 30):'-', \
                                                   date(2007, 6, 30):1149.00, \
                                                   date(2007, 3, 31):1161.00, \
                                                   date(2006, 12, 31):1163.00})
                                                    
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyOtherCurrentLiabilities("DD"), {date(2007, 12, 31):176.00, \
                                                date(2007, 9, 30):334.00, \
                                                date(2007, 6, 30):369.00, \
                                                date(2007, 3, 31):422.00, \
                                                date(2006, 12, 31):178.00})
                                                 
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalCurrentLiabilities("DD"), {date(2007, 12, 31):8541.00, \
                                                date(2007, 9, 30):9797.00, \
                                                date(2007, 6, 30):8204.00, \
                                                date(2007, 3, 31):7814.00, \
                                                date(2006, 12, 31):7940.00})
                                                 
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                     date(2007, 9, 30):5367.00, \
                                     date(2007, 6, 30):5664.00, \
                                     date(2007, 3, 31):6010.00, \
                                     date(2006, 12, 31):6013.00})
                                      
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCapitalLeaseObligations("DD"), {date(2007, 12, 31):'-', \
                                                date(2007, 9, 30):'-', \
                                                date(2007, 6, 30):'-', \
                                                date(2007, 3, 31):'-', \
                                                date(2006, 12, 31):'-'})
                                                 
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalLongTermDebt("DD"), {date(2007, 12, 31):5955.00, \
                                          date(2007, 9, 30):5367.00, \
                                          date(2007, 6, 30):5664.00, \
                                          date(2007, 3, 31):6010.00, \
                                          date(2006, 12, 31):6013.00})
                                           
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalDebt("DD"), {date(2007, 12, 31):7325.00, \
                                  date(2007, 9, 30):8985.00, \
                                  date(2007, 6, 30):8039.00, \
                                  date(2007, 3, 31):7600.00, \
                                  date(2006, 12, 31):7530.00})
                                   
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDeferredIncomeTax("DD"), {date(2007, 12, 31):802.00, \
                                          date(2007, 9, 30):404.00, \
                                          date(2007, 6, 30):395.00, \
                                          date(2007, 3, 31):402.00, \
                                          date(2006, 12, 31):269.00})
                                           
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyMinorityInterest_Bal("DD"), {date(2007, 12, 31):442.00, \
                                         date(2007, 9, 30):445.00, \
                                         date(2007, 6, 30):442.00, \
                                         date(2007, 3, 31):442.00, \
                                         date(2006, 12, 31):441.00})
                                          
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyOtherLiabilities("DD"), {date(2007, 12, 31):7255.00, \
                                         date(2007, 9, 30):7984.00, \
                                         date(2007, 6, 30):7455.00, \
                                         date(2007, 3, 31):7629.00, \
                                         date(2006, 12, 31):7692.00})
                                          
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalLiabilities("DD"), {date(2007, 12, 31):22995.00, \
                                         date(2007, 9, 30):23997.00, \
                                         date(2007, 6, 30):22160.00, \
                                         date(2007, 3, 31):22297.00, \
                                         date(2006, 12, 31):22355.00})
                                          
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyRedeemablePreferredStock("DD"), {date(2007, 12, 31):'-', \
                                                 date(2007, 9, 30):'-', \
                                                 date(2007, 6, 30):'-', \
                                                 date(2007, 3, 31):'-', \
                                                 date(2006, 12, 31):'-'})
                                                  
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyPreferredStockNonRedeemable("DD"), {date(2007, 12, 31):237.00, \
                                                    date(2007, 9, 30):237.00, \
                                                    date(2007, 6, 30):237.00, \
                                                    date(2007, 3, 31):237.00, \
                                                    date(2006, 12, 31):237.00})
                                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCommonStock("DD"), {date(2007, 12, 31):296.00, \
                                    date(2007, 9, 30):296.00, \
                                    date(2007, 6, 30):302.00, \
                                    date(2007, 3, 31):303.00, \
                                    date(2006, 12, 31):303.00})
                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyAdditionalPaidInCapital("DD"), {date(2007, 12, 31):8179.00, \
                                                date(2007, 9, 30):8121.00, \
                                                date(2007, 6, 30):8187.00, \
                                                date(2007, 3, 31):8072.00, \
                                                date(2006, 12, 31):7797.00})
                                                 
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyRetainedEarnings("DD"), {date(2007, 12, 31):9945.00, \
                                         date(2007, 9, 30):9772.00, \
                                         date(2007, 6, 30):10516.00, \
                                         date(2007, 3, 31):10142.00, \
                                         date(2006, 12, 31):9679.00})
                                          
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTreasuryStock("DD"), {date(2007, 12, 31):-6727.00, \
                                      date(2007, 9, 30):-6727.00, \
                                      date(2007, 6, 30):-6727.00, \
                                      date(2007, 3, 31):-6727.00, \
                                      date(2006, 12, 31):-6727.00})
                                       
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyOtherEquity("DD"), {date(2007, 12, 31):-794.00, \
                                    date(2007, 9, 30):-1781.00, \
                                    date(2007, 6, 30):-1825.00, \
                                    date(2007, 3, 31):-1851.00, \
                                    date(2006, 12, 31):-1867.00})
                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalEquity("DD"), {date(2007, 12, 31):11136.00, \
                                    date(2007, 9, 30):9918.00, \
                                    date(2007, 6, 30):10690.00, \
                                    date(2007, 3, 31):10176.00, \
                                    date(2006, 12, 31):9422.00})
                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalLiabilitiesAndShareholdersEquity("DD"), {date(2007, 12, 31):34131.00, \
                                                              date(2007, 9, 30):33915.00, \
                                                              date(2007, 6, 30):32850.00, \
                                                              date(2007, 3, 31):32473.00, \
                                                              date(2006, 12, 31):31777.00})
                                                               
assert res[0], res[1]
res = compareDicts(totest.getQuarterlySharesOuts("DD"), {date(2007, 12, 31):'-', \
                                   date(2007, 9, 30):'-', \
                                   date(2007, 6, 30):'-', \
                                   date(2007, 3, 31):'-', \
                                   date(2006, 12, 31):'-'})
                                    
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalCommonSharesOutstanding("DD"), {date(2007, 12, 31):899.29, \
                                                     date(2007, 9, 30):898.93, \
                                                     date(2007, 6, 30):920.27, \
                                                     date(2007, 3, 31):923.60, \
                                                     date(2006, 12, 31):922.07}, prnt=True)
                                                      
assert res[0], res[1]
#cash flow
res = compareDicts(totest.getQuarterlyNetIncomeStartingLine("DD"), {date(2007, 12, 31):545.00, \
                                              date(2007, 9, 30):526.00, \
                                              date(2007, 6, 30):972.00, \
                                              date(2007, 3, 31):945.00}, prnt=True)
                                              
                                              
assert res[0], res[1] 
res = compareDicts(totest.getQuarterlyDepreciationDepletion("DD"), {date(2007, 12, 31):292.00, \
                                              date(2007, 9, 30):287.00, \
                                              date(2007, 6, 30):289.00, \
                                              date(2007, 3, 31):290.00})
                                              
                                              
assert res[0], res[1] 
res = compareDicts(totest.getQuarterlyAmortization("DD"), {date(2007, 12, 31):50.00, \
                                     date(2007, 9, 30):53.00, \
                                     date(2007, 6, 30):54.00, \
                                     date(2007, 3, 31):56.00})
                                     
                                      
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyDeferredTaxes("DD"), {date(2007, 12, 31):'-', \
                                      date(2007, 9, 30):'-', \
                                      date(2007, 6, 30):'-', \
                                      date(2007, 3, 31):'-'})
                                      
                                       
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyNonCashItems("DD"), {date(2007, 12, 31):164.00, \
                                     date(2007, 9, 30):-32.00, \
                                     date(2007, 6, 30):-33.00, \
                                     date(2007, 3, 31):-11.00})
                                     
                                      
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyChangesInWorkingCapital("DD"), {date(2007, 12, 31):1814.00, \
                                                date(2007, 9, 30):209.00, \
                                                date(2007, 6, 30):-659.00, \
                                                date(2007, 3, 31):-1520.00})
                                                
                                                 
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCashFromOperatingActivities("DD"), {date(2007, 12, 31):2864.00, \
                                                    date(2007, 9, 30):1043.00, \
                                                    date(2007, 6, 30):623.00, \
                                                    date(2007, 3, 31):-240.00})
                                                    
                                                    
assert res[0], res[1] 
res = compareDicts(totest.getQuarterlyCapitalExpenditures("DD"), {date(2007, 12, 31):-566.00, \
                                            date(2007, 9, 30):-398.00, \
                                            date(2007, 6, 30):-348.00, \
                                            date(2007, 3, 31):-273.00})
                                            
                                             
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyOtherInvestingCashFlow("DD"), {date(2007, 12, 31):-164.00, \
                                               date(2007, 9, 30):50.00, \
                                               date(2007, 6, 30):-55.00, \
                                               date(2007, 3, 31):4.00})
                                               
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCashFromInvestingActivities("DD"), {date(2007, 12, 31):-730.00, \
                                                    date(2007, 9, 30):-348.00, \
                                                    date(2007, 6, 30):-403.00, \
                                                    date(2007, 3, 31):-269.00})
                                                    
                                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyFinancingCashFlowItems("DD"), {date(2007, 12, 31):5.00, \
                                               date(2007, 9, 30):8.00, \
                                               date(2007, 6, 30):-11.00, \
                                               date(2007, 3, 31):-69.00})
                                               
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyTotalCashDividendsPaid("DD"), {date(2007, 12, 31):-372.00, \
                                               date(2007, 9, 30):-345.00, \
                                               date(2007, 6, 30):-345.00, \
                                               date(2007, 3, 31):-347.00})
                                               
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyIssuanceOfStock("DD"), {date(2007, 12, 31):14.00, \
                                        date(2007, 9, 30):-1029.00, \
                                        date(2007, 6, 30):-185.00, \
                                        date(2007, 3, 31):-50.00})
                                        
                                         
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyIssuanceOfDebt("DD"), {date(2007, 12, 31):-1673.00, \
                                       date(2007, 9, 30):858.00, \
                                       date(2007, 6, 30):431.00, \
                                       date(2007, 3, 31):41.00})
                                       
                                        
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCashFromFinancingActivities("DD"), {date(2007, 12, 31):-2026.00, \
                                                    date(2007, 9, 30):-508.00, \
                                                    date(2007, 6, 30):-110.00, \
                                                    date(2007, 3, 31):-425.00})
                                                    
                                                     
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyForeignExchangeEffects("DD"), {date(2007, 12, 31):-12.00, \
                                               date(2007, 9, 30):35.00, \
                                               date(2007, 6, 30):-6.00, \
                                               date(2007, 3, 31):3.00})
                                               
                                                
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyNetChangeInCash("DD"), {date(2007, 12, 31):96.00, \
                                        date(2007, 9, 30):222.00, \
                                        date(2007, 6, 30):104.00, \
                                        date(2007, 3, 31):-931.00})
                                        
                                         
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCashInterestPaid("DD"), {date(2007, 12, 31):'-', \
                                         date(2007, 9, 30):'-', \
                                         date(2007, 6, 30):'-', \
                                         date(2007, 3, 31):'-'})
                                         
                                          
assert res[0], res[1]
res = compareDicts(totest.getQuarterlyCashTaxesPaid("DD"), {date(2007, 12, 31):'-', \
                                      date(2007, 9, 30):'-', \
                                      date(2007, 6, 30):'-', \
                                      date(2007, 3, 31):'-'})
                                      
                                       
assert res[0], res[1]