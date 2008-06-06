import Yahoo
from TestTools import assertClose, compareDicts
from datetime import date
import datetime
import doctest
import contract
import unittest
import utilities

contract.checkmod(utilities)
contract.checkmod(Yahoo)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Yahoo))

class YahooTestCase(unittest.TestCase):
	def setUp(self):
		pass
	
	def tearDown(self):	
		pass
	
	def testRandom(self):
		""" Randomly sample different stocks and attributes """
		scraper = Yahoo.Yahoo()

		self.assertEqual(scraper.getHigh("DD", datetime.date(2008,4,14)), 49.41)
		self.assertEqual(scraper.getHigh("DD", datetime.date(2007,12,31)), 44.29)
		self.assertEqual(scraper.getHigh("DD", datetime.date(2007,9,28)), 50.27)
		self.assertEqual(scraper.getHigh("DD", datetime.date(2007,6,22)), 52.74)
		self.assertEqual(scraper.getHigh("DD", datetime.date(2007,4,2)), 49.68)
		self.assertEqual(scraper.getLow("DD", datetime.date(2006,12,12)), 46.70)
		self.assertEqual(scraper.getLow("DD", datetime.date(2006,11,13)), 46.77)
		self.assertEqual(scraper.getLow("DD", datetime.date(2006,11,10)), 46.80)
		self.assertEqual(scraper.getLow("DD", datetime.date(2006,9,1)), 40.00)
		self.assertEqual(scraper.getLow("DD", datetime.date(2006,6,30)), 41.57)
		self.assertEqual(scraper.getOpen("DD", datetime.date(2006,5,11)), 45.52)
		self.assertEqual(scraper.getOpen("DD", datetime.date(2006,5,10)), 45.56)
		self.assertEqual(scraper.getOpen("DD", datetime.date(2006,2,13)), 39.53)
		self.assertEqual(scraper.getOpen("DD", datetime.date(2006,2,10)), 40.27)
		self.assertEqual(scraper.getOpen("DD", datetime.date(2005,11,10)), 41.90)
		self.assertEqual(scraper.getClose("DD", datetime.date(2005,11,9)), 42.08)
		self.assertEqual(scraper.getClose("DD", datetime.date(2005,8,11)), 41.79)
		self.assertEqual(scraper.getClose("DD", datetime.date(2005,8,10)), 42.51)
		self.assertEqual(scraper.getClose("DD", datetime.date(2005,5,11)), 47.43)
		self.assertEqual(scraper.getClose("DD", datetime.date(2005,5,10)), 47.59)
		self.assertEqual(scraper.getVolume("DD", datetime.date(2005,2,11)), 5877100.0)
		self.assertEqual(scraper.getVolume("DD", datetime.date(2005,2,10)), 5226400.0)
		self.assertEqual(scraper.getVolume("DD", datetime.date(2004,11,10)), 3647700.0)
		self.assertEqual(scraper.getVolume("DD", datetime.date(2004,11,9)), 3191400.0)
		self.assertEqual(scraper.getVolume("DD", datetime.date(2004,8,11)), 3942200.0)
		self.assertEqual(scraper.getAdjustedClose("DD", datetime.date(2004,8,10)), 36.63)
		self.assertEqual(scraper.getAdjustedClose("DD", datetime.date(2004,5,12)), 36.50)
		self.assertEqual(scraper.getAdjustedClose("DD", datetime.date(2004,5,11)), 36.42)
		self.assertEqual(scraper.getAdjustedClose("DD", datetime.date(1969,12,31)), 1.25)
		self.assertEqual(scraper.getAdjustedClose("DD", datetime.date(2008,6,4)), 46.77)
		
		self.assertEqual(scraper.getHigh("NTDOY.PK", datetime.date(2008,6,4)), 69.35)
		self.assertEqual(scraper.getHigh("NTDOY.PK", datetime.date(1996,11,18)), 9.00)
		self.assertEqual(scraper.getHigh("NTDOY.PK", datetime.date(1997,1,15)), 8.87)
		self.assertEqual(scraper.getHigh("NTDOY.PK", datetime.date(1997,4,21)), 9.13)
		self.assertEqual(scraper.getHigh("NTDOY.PK", datetime.date(1997,1,16)), 8.38)
		self.assertEqual(scraper.getLow("NTDOY.PK", datetime.date(1997,7,28)), 11.75)
		self.assertEqual(scraper.getLow("NTDOY.PK", datetime.date(1997,4,22)), 8.62)
		self.assertEqual(scraper.getLow("NTDOY.PK", datetime.date(1997,11,11)), 11.00)
		self.assertEqual(scraper.getLow("NTDOY.PK", datetime.date(1997,7,29)), 12.00)
		self.assertEqual(scraper.getLow("NTDOY.PK", datetime.date(1998,2,18)), 11.50)
		self.assertEqual(scraper.getOpen("NTDOY.PK", datetime.date(1998,11,12)), 11.50)
		self.assertEqual(scraper.getOpen("NTDOY.PK", datetime.date(1998,5,28)), 11.75)
		self.assertEqual(scraper.getOpen("NTDOY.PK", datetime.date(1998,2,19)), 11.75)
		self.assertEqual(scraper.getOpen("NTDOY.PK", datetime.date(1998,8,31)), 11.62)
		self.assertEqual(scraper.getOpen("NTDOY.PK", datetime.date(1998,5,29)), 11.50)
		self.assertEqual(scraper.getClose("NTDOY.PK", datetime.date(1998,12,3)), 12.00)
		self.assertEqual(scraper.getClose("NTDOY.PK", datetime.date(1998,9,1)), 11.38)
		self.assertEqual(scraper.getClose("NTDOY.PK", datetime.date(1999,3,12)), 10.25)
		self.assertEqual(scraper.getClose("NTDOY.PK", datetime.date(1998,12,4)), 12.00)
		self.assertEqual(scraper.getClose("NTDOY.PK", datetime.date(1999,6,17)), 15.75)
		self.assertEqual(scraper.getVolume("NTDOY.PK", datetime.date(1999,3,15)), 16100)
		self.assertEqual(scraper.getVolume("NTDOY.PK", datetime.date(1999,9,22)), 195200)
		self.assertEqual(scraper.getVolume("NTDOY.PK", datetime.date(1999,6,18)), 31000)
		self.assertEqual(scraper.getVolume("NTDOY.PK", datetime.date(1999,12,27)), 106000)
		self.assertEqual(scraper.getVolume("NTDOY.PK", datetime.date(1999,9,23)), 25300)
		self.assertEqual(scraper.getAdjustedClose("NTDOY.PK", datetime.date(2000,4,4)), 18.84)
		self.assertEqual(scraper.getAdjustedClose("NTDOY.PK", datetime.date(1999,12,28)), 17.67)
		self.assertEqual(scraper.getAdjustedClose("NTDOY.PK", datetime.date(2000,7,12)), 19.96)
		self.assertEqual(scraper.getAdjustedClose("NTDOY.PK", datetime.date(2000,4,5)), 19.32)
		self.assertEqual(scraper.getAdjustedClose("NTDOY.PK", datetime.date(2000,10,17)), 20.38)
		
		self.assertEqual(scraper.getHigh("BRK-A", datetime.date(2008,6,4)), 133640.0)
		self.assertEqual(scraper.getHigh("BRK-A", datetime.date(1990,1,12)), 8350.0)
		self.assertEqual(scraper.getHigh("BRK-A", datetime.date(2007,10,22)), 127000.0)
		self.assertEqual(scraper.getHigh("BRK-A", datetime.date(2007,10,19)), 129000.0)
		self.assertEqual(scraper.getHigh("BRK-A", datetime.date(2007,10,18)), 129500.0)
		self.assertEqual(scraper.getLow("BRK-A", datetime.date(1990,1,12)), 8175.0)
		self.assertEqual(scraper.getLow("BRK-A", datetime.date(2008,6,4)), 130700.0)
		self.assertEqual(scraper.getLow("BRK-A", datetime.date(2007,10,17)), 127700)
		self.assertEqual(scraper.getLow("BRK-A", datetime.date(2007,10,16)), 126200)
		self.assertEqual(scraper.getLow("BRK-A", datetime.date(2007,10,15)), 125500)
		self.assertEqual(scraper.getOpen("BRK-A", datetime.date(1990,1,12)), 8350.0)
		self.assertEqual(scraper.getOpen("BRK-A", datetime.date(2008,6,4)), 133000.0)
		self.assertEqual(scraper.getOpen("BRK-A", datetime.date(2007,10,12)), 126500.0)
		self.assertEqual(scraper.getOpen("BRK-A", datetime.date(2007,10,11)), 125000.0)
		self.assertEqual(scraper.getOpen("BRK-A", datetime.date(2007,10,10)), 122550.0)
		self.assertEqual(scraper.getClose("BRK-A", datetime.date(1990,1,12)), 8200.00)
		self.assertEqual(scraper.getClose("BRK-A", datetime.date(2008,6,4)), 132990.00)
		self.assertEqual(scraper.getClose("BRK-A", datetime.date(2007,10,9)), 122615.00)
		self.assertEqual(scraper.getClose("BRK-A", datetime.date(2007,10,8)), 123390.00)
		self.assertEqual(scraper.getClose("BRK-A", datetime.date(2007,10,5)), 121100.00)
		self.assertEqual(scraper.getVolume("BRK-A", datetime.date(1990,1,12)), 46000.00)
		self.assertEqual(scraper.getVolume("BRK-A", datetime.date(2008,6,4)), 50900.00)
		self.assertEqual(scraper.getVolume("BRK-A", datetime.date(2007,10,4)), 43000)
		self.assertEqual(scraper.getVolume("BRK-A", datetime.date(2007,10,3)), 16000)
		self.assertEqual(scraper.getVolume("BRK-A", datetime.date(2007,10,2)), 22000)
		self.assertEqual(scraper.getAdjustedClose("BRK-A", datetime.date(1990,1,12)), 8200.00)
		self.assertEqual(scraper.getAdjustedClose("BRK-A", datetime.date(2008,6,4)), 132990)
		self.assertEqual(scraper.getAdjustedClose("BRK-A", datetime.date(2007,10,1)), 118790)
		self.assertEqual(scraper.getAdjustedClose("BRK-A", datetime.date(2007,9,28)), 118510)
		self.assertEqual(scraper.getAdjustedClose("BRK-A", datetime.date(2007,9,27)), 117200)	   
		
class Yahoo_SoupFactoryTestCase(unittest.TestCase):
	def setUp(self):
		self.factory = Yahoo.Yahoo.SoupFactory()
	   
	def tearDown(self):
		del self.factory
		self.factory = None
		
	def test_buildYahooURL(self):
		""" Test that the Yahoo base URL is correct """
		self.assertEqual(self.factory._buildYahooURL("/check"), "http://finance.yahoo.com/check")
		
	def test_buildBasicURL(self):
		""" Test that the BasicURL's build correctly """
		self.assertEqual(self.factory._buildBasicURL("IRBT"),"http://finance.yahoo.com/q?s=IRBT")
		
	def test_buildPriceURL(self):
		""" Test that the PriceURL's build correctly """
		self.assertEqual(self.factory._buildPriceURL("DD"),"http://finance.yahoo.com/q/hp?s=DD")
	
class Yahoo_TradingDayCollection(unittest.TestCase):
	def setUp(self):
		self.soupFactory = Yahoo.Yahoo.SoupFactory()
		self.collection = Yahoo.Yahoo.TradingDayCollection(self.soupFactory, "IRBT")
		
		class fileLike:
			def readlines(self):
				return ["date,open,high,low,close,volume,adjclose","2000-01-01,19.5,20.0,15.0,15.5,1000,15.5"]
			
		self.fileLike = fileLike
	
	def tearDown(self):
		del self.soupFactory
		self.soupFactory = None
		del self.collection
		self.collection = None
		
	def testParse(self):
		""" Test that the parser works correctly """
		parsedInfo = self.collection._parseCSV(self.fileLike())
		self.assertEqual(parsedInfo[datetime.date(2000,1,1)].getDate(), datetime.date(2000,1,1))
		self.assertEqual(parsedInfo[datetime.date(2000,1,1)].getHigh(), 20.0)
		self.assertEqual(parsedInfo[datetime.date(2000,1,1)].getLow(), 15.0)
		self.assertEqual(parsedInfo[datetime.date(2000,1,1)].getClose(), 15.5)
		self.assertEqual(parsedInfo[datetime.date(2000,1,1)].getOpen(), 19.5)
		self.assertEqual(parsedInfo[datetime.date(2000,1,1)].getVolume(), 1000.0)
		self.assertEqual(parsedInfo[datetime.date(2000,1,1)].getAdjustedClose(), 15.5)				
	
	def testGetItem(self):
		""" Test that [] accessor works on both slices and dates """
		#by date
		self.assertEqual(self.collection[datetime.date(2005,11,14)].getHigh(), 36.20)
		
		#by slice
		self.assertEqual([x.getLow() for x in self.collection[datetime.date(2005,11,10):datetime.date(2005,11,20)]],[31.33,32.99,32.70,29.98,29.25,30.15,29.50])
		
	def testIter(self):
		""" Test that the iterator behaves correctly """
		newcol = []
		x=0
		for tradingDay in self.collection:
			x+=1
			newcol.append(tradingDay)
			if(x>=3):
				break
		
		#since its a generator its harder to check the return value in a DBC and i do it here.
		self.assertTrue(isinstance(newcol[0],Yahoo.Yahoo.TradingDay))
		self.assertTrue(isinstance(newcol[1],Yahoo.Yahoo.TradingDay))
		self.assertTrue(isinstance(newcol[2],Yahoo.Yahoo.TradingDay))
		self.assertEqual(newcol[0].getDate(), datetime.date(2005,11,9))
		self.assertEqual(newcol[1].getDate(), datetime.date(2005,11,10))
		self.assertEqual(newcol[2].getDate(), datetime.date(2005,11,11))
		
	def testHasDate(self):
		""" Test that the has date predicate works """
		self.assertTrue(self.collection.hasDate(datetime.date(2008,4,24)))
		
	def testGetDates(self):
		"""Test that get dates returns the proper range """
		self.assertEqual(self.collection.getDates(datetime.date(2005,11,10),datetime.date(2005,11,20)),[datetime.date(2005,11,10),datetime.date(2005,11,11),datetime.date(2005,11,14),datetime.date(2005,11,15),datetime.date(2005,11,16),datetime.date(2005,11,17),datetime.date(2005,11,18)])
		
	def testBeginingDate(self):
		""" Test that I can find the begining date """
		#use a test on this because its a little too heavy duty to simply put in a doctest
		self.assertEqual(self.collection.getBeginingDate(), date(2005,11,9))
		
	def testEndingDate(self):
		""" Test that ending date is kinda sorta correct """
		self.assertTrue(self.collection.getEndingDate() <= datetime.date.today())
		self.assertTrue(self.collection.getEndingDate() - datetime.date.today() <= datetime.timedelta(5))#this is a guess...
		
class Yahoo_TradingDay(unittest.TestCase):
	def setUp(self):
		self.trophy = Yahoo.Yahoo.TradingDay(datetime.date(2000,1,1), 19.5, 20.0, 15.0, 15.5, 1000.0, 15.5)
	
	def tearDown(self):
		del self.trophy
		self.trophy = None
		
	def testHigh(self):
		""" Test that I can get the High for this Trading Day """
		self.assertEqual(self.trophy.getHigh(),20.0)
		
	def testLow(self):
		""" Test that I can get the Low for this Trading Day """
		self.assertEqual(self.trophy.getLow(),15.0)
		
	def testClose(self):
		""" Test that I can get the Close for this Trading Day """
		self.assertEqual(self.trophy.getClose(),15.5)
		
	def testOpen(self):
		""" Test that I can get the Open for this Trading Day """
		self.assertEqual(self.trophy.getOpen(), 19.5)
		
	def testVolume(self):
		""" Test that I can get the Volume for this Trading Day """
		self.assertEqual(self.trophy.getVolume(), 1000.0)
	
	def testAdjClose(self):
		""" Test that I can get the Adjusted Close for this Trading Day """
		self.assertEqual(self.trophy.getAdjustedClose(), 15.5)
		
	def testIsValid(self):
		""" Test that the isvalid predicate works """
		self.assertTrue(self.trophy.isValid())
		#invariant error via contract will buzz in the bad case.
		
if __name__ == "__main__": #for coverage tests
	unittest.main()
									   
