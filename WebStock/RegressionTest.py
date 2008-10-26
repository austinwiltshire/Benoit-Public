import unittest

modulesLoaded = []
tests = unittest.TestSuite()
ldr = unittest.TestLoader()

def registerModule(module):
	module = __import__(module)
	modulesLoaded.append(module)
	tests.addTests(ldr.loadTestsFromModule(module))

#registerModule("FinancialXMLUnitTest")
registerModule("SymbolLookupUnitTest")
#registerModule("SymbolUnitTest")
registerModule("UnifiedBloombergUnitTest")
registerModule("FinancialDateUnitTest")
registerModule("WebsiteUnitTest")
registerModule("YahooUnitTest")

unittest.TextTestRunner(verbosity=3).run(tests)



