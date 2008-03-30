import Website
from datetime import date
from TestTools import assertClose, compareDicts, checkForError, failUnlessRaises
import BeautifulSoup
import re


x = Website.Google()

#basic tests
assertClose(x.getAnnualNetIncome("MRK", date(2007,12,31)), 3275.4, "Failed on MRK Annual Net Income")
assertClose(x.getQuarterlyGoodwill("IBM", date(2007,9,30)), 13843.00, "Failed on IBM quarterly goodwill")
assertClose(x.getQuarterlyChangesInWorkingCapital("SBUX", date(2007,07,01)), -4.09, "Failed on SBUX quarterly changes in working capital")

#fail above
assertClose(x.getQuarterlyChangesInWorkingCapital("SBUX", date(2007,07,01)), -5.09, "Failed on SBUX quarterly changes in working capital", reverse=True)


	

print "got thru"

#test to make sure that all SEC docs and periods exist and can be accessed

#annuals
assertClose(x.getAnnualRevenue("CICI", date(2006,12,31)), 2.34, "Failed on CICI checking annual revenue")
assertClose(x.getAnnualCashAndEquivalents("CICI", date(2006,12,31)), 0.73, "Failed on CICI checking annual cash and cash equivalents")
assertClose(x.getAnnualNetIncomeStartingLine("CICI", date(2006,12,31)), -3.29, "Failed on CICI checking net income starting line")
            
assertClose(x.getAnnualNetIncomeStartingLine("CICI", date(2006,12,31)), 3.29, "Failed on CICI checking net income starting line", reverse=True)

#quarterly's

assertClose(x.getQuarterlyRevenue("CICI", date(2007,9,30)), .46, "Failed on CICI checking quarterly revenue") 
assertClose(x.getQuarterlyCashAndEquivalents("CICI", date(2007,9,30)), 3.24, "Failed on CICI checking quarterly cash and equivalents") 
assertClose(x.getQuarterlyNetIncomeStartingLine("CICI", date(2007,9,30)), -1.10, "Failed on CICI checking quarterly net income starting line")

assertClose(x.getQuarterlyNetIncomeStartingLine("CICI", date(2007,9,30)), -1.5, "Failed on CICI checking quarterly net income starting line", reverse=True)

#check caching
x.getAnnualDepreciationDepletion("B")
assert x.cachedPages.has_key("B"), "Failed on checking of cached pages for B"

#check anticaching
assert not x.cachedPages.has_key("C"), "Failed on checking of cached pages, found C"

#check dict results - 3 annuals, 3 quarterlyes
#annuals
res = compareDicts(x.getAnnualOtherRevenue("XOM"), {date(2007,12,31):14224.0,\
                                                    date(2006,12,31):12168.0,\
                                                    date(2005,12,31):11725.0,\
                                                    date(2004,12,31):6783.0,\
                                                    date(2003,12,31):9684.0,\
                                                    date(2002,12,31):3557.0})
assert res[0], res[1]

res = compareDicts(x.getAnnualShortTermInvestments("CVX"), {date(2007,12,31):732.0,\
                                                            date(2006,12,31):953.0,\
                                                            date(2005,12,31):1101.0,\
                                                            date(2004,12,31):1451.0,\
                                                            date(2003,12,31):1001.0,\
                                                            date(2002,12,31):824.0})
assert res[0], res[1]

res = compareDicts(x.getAnnualDeferredTaxes("RDS.A"), {date(2007,12,31):-773.00,\
                                                       date(2006,12,31):1833.0,\
                                                       date(2005,12,31):-1515.0,\
                                                       date(2004,12,31):-1007.0})
assert res[0], res[1]

res = compareDicts(x.getAnnualDeferredTaxes("RDS.A"), {date(2006,12,31):1833.0,\
                                                       date(2004,12,31):-1007.0})
assert not res[0], res[1]

res = compareDicts(x.getQuarterlyOtherRevenue("BP"), {date(2007,12,31):3938.0,\
                                                      date(2007,6,30):1610.0,\
                                                      date(2007,3,31):1076.0,\
                                                      date(2006,12,31):602.0,\
                                                      date(2006,9,30):2584.0})
assert res[0], res[1]

res = compareDicts(x.getQuarterlyShortTermInvestments("MSFT"), {date(2007,12,31):13616.0,\
                                                                date(2007,9,30):14937.0,\
                                                                date(2007,6,30):17300.0,\
                                                                date(2007,3,31):20625.0,\
                                                                date(2006,12,31):22014.0})
assert res[0], res[1]

res = compareDicts(x.getQuarterlyDeferredTaxes("YHOO"), {date(2007,12,31):-78.16,\
                                                         date(2007,9,30):-43.75,\
                                                         date(2007,6,30):-48.54,\
                                                         date(2007,3,31):-42.30})
assert res[0], res[1]

#fail test - fail value

res = compareDicts(x.getQuarterlyAmortization("GOOG"), {date(2007,12,31):48.03,\
                                                         date(2007,9,30):41.96,\
                                                         date(2007,6,30):35.22,\
                                                         date(2007,3,31):35.70})

assert not res[0], "Test should have failed"

#fail test - fail key

res = compareDicts(x.getQuarterlyAmortization("GOOG"), {date(2007,12,31):48.03,\
                                                         date(2007,9,30):41.96,\
                                                         date(2007,6,30):35.22,\
                                                         date(2007,3,30):34.70})

assert not res[0], "Test should have failed"

#check for negatives * 6
#quarterlies
#ALSO CHECKING FOR EXTREME DATE 2008
assertClose(x.getQuarterlyOtherNet("CSCO", date(2008,01,26)), -28.00, "Failed on CSCO checking negative other net")
assertClose(x.getQuarterlyRetainedEarnings("CSCO", date(2008,01,26)), -1073.00, "Failed on CSCO checking negative retained earnings")
assertClose(x.getQuarterlyIssuanceOfStock("CSCO", date(2008,01,26)),-3501.00, "Failed on CSCO checking negative issuance of stock")

#annuals
assertClose(x.getAnnualOtherNet("CSCO", date(2006,07,29)), -94.00, "Failed on CSCO checking negative other net")
assertClose(x.getAnnualRetainedEarnings("CSCO", date(2006,7,29)), -617.00, "Failed on CSCO checking negative retained earnings")
assertClose(x.getAnnualIssuanceOfStock("CSCO", date(2005,07,30)),-9148.00, "Failed on CSCO checking negative issuance of stock")

#fail
assertClose(x.getAnnualIssuanceOfStock("CSCO", date(2005,07,30)),9148.00, "Failed on CSCO checking negative issuance of stock",reverse=True)

#test <span> tag embedded
#test all dashes
res = compareDicts(x.getQuarterlyOtherRevenue('S'), {date(2007,12,31):'-',\
                                                     date(2007,9,30):'-',\
                                                     date(2007,6,30):'-',\
                                                     date(2007,3,31):'-',\
                                                     date(2006,12,31):'-'}, lambda x,y: x==y)
assert res[0], "FAILED on span embedded, all dashes too"

#test <b> tag embedded
res = compareDicts(x.getQuarterlyTotalRevenue('S'), {date(2007,12,31):9847.0,\
                                                     date(2007,9,30):10044.0,\
                                                     date(2007,6,30):20255.0,\
                                                     date(2007,3,31):10091.0,\
                                                     date(2006,12,31):10438.0})
assert res[0], "FAILED on bold embedded"

#mixed span.  one span and the rest are not spanned
#mixed with <b>
res = compareDicts(x.getQuarterlyOperatingIncome('S'), {date(2007,12,31):-29625.0,\
                                                     date(2007,9,30):398.0,\
                                                     date(2007,6,30):317.0,\
                                                     date(2007,3,31):1.0,\
                                                     date(2006,12,31):569.0})
assert res[0], "FAILED on mixed between span and not spanned with bold"
#mixed with vanilla
res = compareDicts(x.getQuarterlyOtherNet('S'), {date(2007,12,31):234.0,\
                                                     date(2007,9,30):0.0,\
                                                     date(2007,6,30):13.0,\
                                                     date(2007,3,31):-4.0,\
                                                     date(2006,12,31):142.0})
assert res[0], "FAILED on span embedded but not all spanned"

#span + bold
res = compareDicts(x.getQuarterlyIncomeAfterTax('S'), {date(2007,12,31):-29452.00,\
                                                     date(2007,9,30):64.0,\
                                                     date(2007,6,30):-192.0,\
                                                     date(2007,3,31):-211.0,\
                                                     date(2006,12,31):261.0})
assert res[0], "FAILED on span + bold embedded"

#mixed between - and numbers.
res = compareDicts(x.getQuarterlyDilutionAdjustment('S'), {date(2007,12,31):0.00,\
                                                     date(2007,9,30):'-',\
                                                     date(2007,6,30):0.00,\
                                                     date(2007,3,31):0.00,\
                                                     date(2006,12,31):'-'},\
        lambda x,y: (x-y) <= 0.05 and (x-y) >= -0.05 if isinstance(x, float) else x==y)

assert res[0], "FAILED on mixing numbers and dashes"

res = compareDicts(x.getQuarterlyDilutionAdjustment('S'), {date(2007,12,31):'-',\
                                                     date(2007,9,30):'-',\
                                                     date(2007,6,30):0.00,\
                                                     date(2007,3,31):0.00,\
                                                     date(2006,12,31):'-'},\
        lambda x,y: (x-y) <= 0.05 and (x-y) >= -0.05 if (isinstance(x, float) and isinstance(y,float)) else x==y)

assert not res[0], "FAILED on mixing numbers and dashes"

res = compareDicts(x.getQuarterlyDilutionAdjustment('S'), {date(2007,12,31):0.00,\
                                                     date(2007,9,30):'-',\
                                                     date(2007,6,30):0.00,\
                                                     date(2007,3,31):0.00,\
                                                     date(2006,12,31):0.00},\
        lambda x,y: (x-y) <= 0.05 and (x-y) >= -0.05 if (isinstance(x, float) and isinstance(y,float)) else x==y)

assert not res[0], "FAILED on mixing numbers and dashes"


#test tiny numbers

res = compareDicts(x.getQuarterlyDilutedNormalizedEPS('S'), {date(2007,12,31):-3.55,\
                                                     date(2007,9,30):0.05,\
                                                     date(2007,6,30):0.0,\
                                                     date(2007,3,31):-0.03,\
                                                     date(2006,12,31):0.11})
assert res[0], "FAILED on tiny numbers"

res = compareDicts(x.getQuarterlyDilutedNormalizedEPS('S'), {date(2007,12,31):-3.55,\
                                                     date(2007,9,30):0.5,\
                                                     date(2007,6,30):0.0,\
                                                     date(2007,3,31):-0.03,\
                                                     date(2006,12,31):0.11})
assert not res[0], "FAILED on tiny numbers"

#all 0.0's
res = compareDicts(x.getQuarterlyDividendsPerShare("IRBT"), {date(2007,12,29):0.0,\
                                                     date(2007,9,29):0.0,\
                                                     date(2007,6,30):0.0,\
                                                     date(2007,3,31):0.0,\
                                                     date(2006,12,30):0.0})
assert res[0], "FAILED on all 0.0's"
#fail of above
res = compareDicts(x.getQuarterlyDividendsPerShare("IRBT"), {date(2007,12,29):-0.06,\
                                                     date(2007,9,29):0.0,\
                                                     date(2007,6,30):0.0,\
                                                     date(2007,3,31):0.0,\
                                                     date(2006,12,30):0.0})
assert not res[0], "FAILED on failure test of 0.0's"

#test that keyword total revenue behind bold is found
res = compareDicts(x.getQuarterlyTotalRevenue("IRBT"), {date(2007,12,29):98.74,\
                                                     date(2007,9,29):150.34,\
                                                     date(2007,6,30):47.01,\
                                                     date(2007,3,31):39.49,\
                                                     date(2006,12,30):61.14})
assert res[0], "FAILED on bolded keyword"

#test keyword that is spanned
res = compareDicts(x.getQuarterlyCashAndEquivalents("IRBT"), {date(2007,12,29):26.73,\
                                                     date(2007,9,29):23.20,\
                                                     date(2007,6,30):10.26,\
                                                     date(2007,3,31):9.40,\
                                                     date(2006,12,30):5.58})
assert res[0], "FAILED on spanned keyword"

#test mixed '-' and numbers, that are not 0.0
res = compareDicts(x.getAnnualLongTermInvestments("WHR"), {date(2007,12,31):'-',\
                                                     date(2006,12,31):'-',\
                                                     date(2005,12,31):28.00,\
                                                     date(2004,12,31):16.00,\
                                                     date(2003,12,31):11.00,\
                                                     date(2002,12,31):7.00},\
        lambda x,y: (x-y) <= 0.05 and (x-y) >= -0.05 if isinstance(x, float) else x==y)
assert res[0], "FAILED on mixed '-' and numbers that are not 0"

#right now CFC has more quarterly dates in its income statement than its cashflow.  need to
#test to make sure i'm getting the right keys for each.

assert len(x.getQuarterlyUnusualExpense("CFC").keys()) == 5, "FAILED checking to make sure dates line up.  This can fail in the future if CFC is updated"
assert len(x.getQuarterlyCapitalExpenditures("CFC").keys()) == 4, "FAILED checking to make sure dates lined up.  This can fail if in the future CFC is updated"

assert not len(x.getQuarterlyCapitalExpenditures("CFC").keys()) == 5, "FAILED checking to make sure dates lined up.  This can fail if in the future CFC is updated"

#check for stock that has no SEC data
trial = False
try:
    x.getAnnualForeignExchangeEffects("NTDOY")
except Exception, e:
    print "This is ok"
    print e
    trial = True
assert trial, "FAILED, should have gotten an exception when searching for NTDOY since it has no sec docs"

#check for stock that does not exist
trial = False
try:
    x.getAnnualCashInterestPaidSupplemental("BOOBS")
except Exception, e:
    print "This is ok"
    print e
    trial = True
assert trial, "FAILED, should have gotten an exception when searching for a stock that didn't exist"

#check for date on stock that does not exist
trial = False
try:
    x.getAnnualDeferredTaxes("CFC", date(2007,12,30))
except Exception, e:
    print "This is ok"
    print e
    trial = True
assert trial, "FAILED, should have gotten key error when looking up bad date"

#check for extreme dates
temp = x.getAnnualResearchAndDevelopment("PNS")
assert temp.has_key(date(2007,12,31)), "FAILED did not find extreme date"
assert temp.has_key(date(2002,12,31)), "FAILED did not find extreme date, this might just need an update to the test"

temp = x.getQuarterlyResearchAndDevelopment("PNS")
assert temp.has_key(date(2007,12,31)), "FAILED did not find extreme date"
assert temp.has_key(date(2006,12,31)), "FAILED did not find extreme date"

assert not temp.has_key(date(2006,9,29)), "FAILED did not find extreme date" #failure test



#check long term cache
assert x.cachedPages.has_key("CSCO"), "FAILED long term caching"

#check foreign stocks

res = compareDicts(x.getAnnualNotesPayable("PIF.UN"), {date(2007,12,31):0.00,\
                                                      date(2006,12,31):0.00,\
                                                      date(2005,12,31):7.31,\
                                                      date(2004,12,31):2.97,\
                                                      date(2003,12,31):0.00,\
                                                      date(2002,12,31):0.00})

assert res[0], res[1]

#check foreign/ADR AND big numbers, AND weird dates!
res = compareDicts(x.getAnnualTotalAssets("IBN"), {date(2007,3,31):3943347.0,\
                                                   date(2006,3,31):2772295.0,\
                                                   date(2005,3,31):1784337.0,\
                                                   date(2004,3,31):1409131.0,\
                                                   date(2003,3,31):1180263.0,\
                                                   date(2002,3,31):743362.0})

assert res[0], res[1]

#fail test
res = compareDicts(x.getAnnualTotalAssets("IBN"), {date(2007,3,31):3943347.0,\
                                                   date(2006,3,31):2772295.1,\
                                                   date(2005,3,31):1784337.0,\
                                                   date(2004,3,31):1409131.0,\
                                                   date(2003,3,31):1180263.0,\
                                                   date(2002,3,31):743362.0})

assert not res[0], res[1]

#check weird name
res = compareDicts(x.getAnnualCashFromInvestingActivities("BRK.B"), {date(2007,12,31):-13428.0,\
                                                                    date(2006,12,31):-14077.0,\
                                                                    date(2005,12,31):-13841.0,\
                                                                    date(2004,12,31):315.0,\
                                                                    date(2003,12,31):16029.0,\
                                                                    date(2002,12,31):-1311.0})

#checking non-negagtive numbers
res = compareDicts(x.getAnnualCashFromInvestingActivities("BRK.B"), {date(2007,12,31):-13428.0,\
                                                                    date(2006,12,31):14077.0,\
                                                                    date(2005,12,31):-13841.0,\
                                                                    date(2004,12,31):315.0,\
                                                                    date(2003,12,31):16029.0,\
                                                                    date(2002,12,31):-1311.0})

assert not res[0], "Did not detect a negative number when there ought to have been on with BRK.B"

print "All random unit tests passed"

#white box testing


x = Website.Google()
assert isinstance(x,Website.Google), "Class instantiation failed."
assert isinstance(x,Website.Website), "Class instantiation failed."
assert isinstance(x,Website.Bloomberg), "Class instantiation failed."
assert isinstance(x,object), "Class instantiation failed"

assert checkForError(x.cachedPages.__getitem__,'FDX',KeyError), "Cached pages failed"

trial = False
try:
    x.dumbname
except AttributeError, e:
    trial = True

assert trial, "Attribute error in calling dumbname"

y = x.getQuarterlyRevenue

assert hasattr(y,"__call__"), "Failed to get __call__ from one of my attributes"
assert y.func_code.co_name=='<lambda>', "Failed to get lambda from one of my attributes"

trial = False
try:
    x.__myGetAttr__("dumbname",1)
except AttributeError, e:
    trial = True
    
assert trial, "Attribute error on __myGetAttr__"

trial = False
try:
    x.___myGetAttr__("dumbname")
except AttributeError, e:
    trial= True
 
assert trial, "Attribute error on __myGetAttr__"

#check for type check of third argument, should be datetime not string
assert checkForError(x.__myGetAttr__, ("dumbname","symbol","notdict"), AttributeError), "Attribute error on __myGetAttr__"

#check for too many args
assert checkForError(x.__myGetAttr__, ("dumbname","symbol",date(2001,1,1),"toomanyargs"), AttributeError), "Attribute error on __myGetAttr__"

#check for proper return type
assert isinstance(x.__myGetAttr__("getQuarterlyRevenue","FDX"),dict), "Failed on return type"

#check for proper return type
assert isinstance(x.__myGetAttr__("getQuarterlyRevenue","FDX",date(2007,2,28)),float), "Failed on return type"

#check type in cached pages
assert isinstance(x.cachedPages["FDX"], Website.GoogleSoup)

#check type for buildsoup
assert isinstance(x.buildSoup("FDX"), BeautifulSoup.BeautifulSoup)

#check that buildURL returns the right type and is the right link
url = x.buildURL("FDX")
print url, type(url)
assert isinstance(url,str) or isinstance(url,unicode), "Google build URL failed type check" 
assert url=="http://finance.google.com/finance?fstype=ii&q=NYSE:FDX", "Google.buildURL type check and value check failed"

#check GoogleSoup
y = x.cachedPages["FDX"]
assert isinstance(y,Website.GoogleSoup)

#check that getSecDoc throws exception on garbage
assert checkForError(y.getSecDoc,"notadoc",Exception,"Not a valid SEC identifier"), "Googlesoup.getSecDoc failed on exception"

#check general values of getSecDoc
assert isinstance(y.getSecDoc("Revenue"),str) and y.getSecDoc("Revenue") == "IncomeStatement", "getSecDoc failed on IncomeStatement"
assert isinstance(y.getSecDoc("CapitalExpenditures"),str) and y.getSecDoc("CapitalExpenditures") == "CashFlowStatement", "getSecDoc failed on CashFlowStatement"
assert isinstance(y.getSecDoc("TotalLiabilities"),str) and y.getSecDoc("TotalLiabilities") == "BalanceSheet", "getSecDoc failed on Balance Sheet"

#check addAttribute has added attributes

assert hasattr(y,"getAnnualRevenue"), "addAttribute is not working"

#pull a switcheroo
y.sec_docs['BalanceSheet'].append("newAttribute")

y.addAttribute("newAttribute","regex")

assert hasattr(y,"getAnnualnewAttribute"), "Add attribute failed"
assert hasattr(y,"getQuarterlynewAttribute"), "Add attribute failed"
assert hasattr(y.getAnnualnewAttribute,"__call__"), "Add attribute failed"
assert hasattr(y.getQuarterlynewAttribute,"__call__"), "Add attribute failed"

div = y.labels['BalanceSheet']['Annual']

assert checkForError(y.getRows,(div,re.compile("boobies")), Exception), "Couldn't find searchRe"
assert isinstance(y.getRows(div,re.compile("Short Term Investments")),list), "getRows didn't return an array"

#check webparse
assert isinstance(y.webparse("quarterlyShortTermInvestments",re.compile("Short Term Investments"),div,y.getDates(div)), dict), "failed webparse return value"

#check getDates
assert isinstance(y.getDates(div),list) and isinstance(y.getDates(div)[0],date), "Failed on getDates return value"

#check for name error
assert checkForError(x.getQuarterlyRevenue, ("EFHG"), Website.SymbolNotFound), "Did not get name error"


#check for no sec docs
assert checkForError(x.getQuarterlyRevenue, ("SATR"), Website.SymbolHasNoFinancials), "Did not get has no financials error"

print "Done white box testing"
                  
trial=False
try:
	x.getQuarterlyRevenue("IRBT", date(2007,12,30))
except Website.DateNotFound:
	trial = True
	
assert trial, "Date not found error not raise properly"                  

















