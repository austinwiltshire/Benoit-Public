import Yahoo
from TestTools import assertClose, compareDicts
from datetime import date
import datetime
import doctest
import contract
import unittest

contract.checkmod(Yahoo)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Yahoo))

class YahooTestCase(unittest.TestCase):
    def setUp(self):
		pass
	
    def tearDown(self):	
    	pass
        
class Yahoo_SoupFactoryTestCase(unittest.TestCase):
    def setUp(self):
        self.factory = Yahoo.Yahoo.SoupFactory()

        
    def tearDown(self):
        del self.factory
        self.factory = None
     
 #   def testBasicSoup(self):
  #  	""" Test that I can build/see stuff from a basicSoup """
   # 	metasoup = self.meta(self.factory.buildBasicSoup("MMM"), self.factory)
    #	self.assertEqual(metasoup.getIndustry(), u"Conglomerates")
    #	self.assertEqual(metasoup.getCurr
    
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
		self.assertEqual(self.collection[datetime.date(2005,11,14)].getHigh(), 36.20)
		
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
		#TODO: confirm this
		
	def testBeginingDate(self):
		""" Test that I can find the begining date """
		#use a test on this because its a little too heavy duty to simply put in a doctest
		self.assertEqual(self.collection.getBeginingDate(), date(2005,11,9))
		
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
		
if __name__ == "__main__": #for coverage tests
	unittest.main()
                                       
