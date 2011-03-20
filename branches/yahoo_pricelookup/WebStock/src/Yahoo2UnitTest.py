import Yahoo2
from TestTools import assertClose, compareDicts
from datetime import date
import datetime
import doctest
import contract
import unittest
import utilities

contract.checkmod(utilities)
contract.checkmod(Yahoo2)
   
   
class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(Yahoo2))

class YahooTestCase(unittest.TestCase):
	def setUp(self):
		pass
	
	def tearDown(self):	
		pass
		
	
	def testRandom(self):
		""" Randomly sample different stocks and attributes """
		
		self.assertEqual(Yahoo2.getHigh("DD", datetime.date(2008,4,14)), 49.41)
		self.assertEqual(Yahoo2.getHigh("DD", datetime.date(2007,12,31)), 44.29)
		self.assertEqual(Yahoo2.getHigh("DD", datetime.date(2007,9,28)), 50.27)
		self.assertEqual(Yahoo2.getHigh("DD", datetime.date(2007,6,22)), 52.74)
		self.assertEqual(Yahoo2.getHigh("DD", datetime.date(2007,4,2)), 49.68)
		self.assertEqual(Yahoo2.getLow("DD", datetime.date(2006,12,12)), 46.70)
		self.assertEqual(Yahoo2.getLow("DD", datetime.date(2006,11,13)), 46.77)
		self.assertEqual(Yahoo2.getLow("DD", datetime.date(2006,11,10)), 46.80)
		self.assertEqual(Yahoo2.getLow("DD", datetime.date(2006,9,1)), 40.00)
		self.assertEqual(Yahoo2.getLow("DD", datetime.date(2006,6,30)), 41.57)
		self.assertEqual(Yahoo2.getOpen("DD", datetime.date(2006,5,11)), 45.52)
		self.assertEqual(Yahoo2.getOpen("DD", datetime.date(2006,5,10)), 45.56)
		self.assertEqual(Yahoo2.getOpen("DD", datetime.date(2006,2,13)), 39.53)
		self.assertEqual(Yahoo2.getOpen("DD", datetime.date(2006,2,10)), 40.27)
		self.assertEqual(Yahoo2.getOpen("DD", datetime.date(2005,11,10)), 41.90)
		self.assertEqual(Yahoo2.getClose("DD", datetime.date(2005,11,9)), 42.08)
		self.assertEqual(Yahoo2.getClose("DD", datetime.date(2005,8,11)), 41.79)
		self.assertEqual(Yahoo2.getClose("DD", datetime.date(2005,8,10)), 42.51)
		self.assertEqual(Yahoo2.getClose("DD", datetime.date(2005,5,11)), 47.43)
		self.assertEqual(Yahoo2.getClose("DD", datetime.date(2005,5,10)), 47.59)
		self.assertEqual(Yahoo2.getVolume("DD", datetime.date(2005,2,11)), 5877100.0)
		self.assertEqual(Yahoo2.getVolume("DD", datetime.date(2005,2,10)), 5226400.0)
		self.assertEqual(Yahoo2.getVolume("DD", datetime.date(2004,11,10)), 3647700.0)
		self.assertEqual(Yahoo2.getVolume("DD", datetime.date(2004,11,9)), 3191400.0)
		self.assertEqual(Yahoo2.getVolume("DD", datetime.date(2004,8,11)), 3942200.0)
		self.assertEqual(Yahoo2.getAdjustedClose("DD", datetime.date(2004,8,10)), 35.79)
		self.assertEqual(Yahoo2.getAdjustedClose("DD", datetime.date(2004,5,12)), 35.66)
		self.assertEqual(Yahoo2.getAdjustedClose("DD", datetime.date(2004,5,11)), 35.57)
		self.assertEqual(Yahoo2.getAdjustedClose("DD", datetime.date(1969,12,31)), 1.23)
		self.assertEqual(Yahoo2.getAdjustedClose("DD", datetime.date(2008,6,4)), 45.69)
		
		self.assertEqual(Yahoo2.getHigh("NTDOY.PK", datetime.date(2008,6,4)), 69.35)
		self.assertEqual(Yahoo2.getHigh("NTDOY.PK", datetime.date(1996,11,18)), 9.00)
		self.assertEqual(Yahoo2.getHigh("NTDOY.PK", datetime.date(1997,1,15)), 8.87)
		self.assertEqual(Yahoo2.getHigh("NTDOY.PK", datetime.date(1997,4,21)), 9.13)
		self.assertEqual(Yahoo2.getHigh("NTDOY.PK", datetime.date(1997,1,16)), 8.38)
		self.assertEqual(Yahoo2.getLow("NTDOY.PK", datetime.date(1997,7,28)), 11.75)
		self.assertEqual(Yahoo2.getLow("NTDOY.PK", datetime.date(1997,4,22)), 8.62)
		self.assertEqual(Yahoo2.getLow("NTDOY.PK", datetime.date(1997,11,11)), 11.00)
		self.assertEqual(Yahoo2.getLow("NTDOY.PK", datetime.date(1997,7,29)), 12.00)
		self.assertEqual(Yahoo2.getLow("NTDOY.PK", datetime.date(1998,2,18)), 11.50)
		self.assertEqual(Yahoo2.getOpen("NTDOY.PK", datetime.date(1998,11,12)), 11.50)
		self.assertEqual(Yahoo2.getOpen("NTDOY.PK", datetime.date(1998,5,28)), 11.75)
		self.assertEqual(Yahoo2.getOpen("NTDOY.PK", datetime.date(1998,2,19)), 11.75)
		self.assertEqual(Yahoo2.getOpen("NTDOY.PK", datetime.date(1998,8,31)), 11.62)
		self.assertEqual(Yahoo2.getOpen("NTDOY.PK", datetime.date(1998,5,29)), 11.50)
		self.assertEqual(Yahoo2.getClose("NTDOY.PK", datetime.date(1998,12,3)), 12.00)
		self.assertEqual(Yahoo2.getClose("NTDOY.PK", datetime.date(1998,9,1)), 11.38)
		self.assertEqual(Yahoo2.getClose("NTDOY.PK", datetime.date(1999,3,12)), 10.25)
		self.assertEqual(Yahoo2.getClose("NTDOY.PK", datetime.date(1998,12,4)), 12.00)
		self.assertEqual(Yahoo2.getClose("NTDOY.PK", datetime.date(1999,6,17)), 15.75)
		self.assertEqual(Yahoo2.getVolume("NTDOY.PK", datetime.date(1999,3,15)), 16100)
		self.assertEqual(Yahoo2.getVolume("NTDOY.PK", datetime.date(1999,9,22)), 195200)
		self.assertEqual(Yahoo2.getVolume("NTDOY.PK", datetime.date(1999,6,18)), 31000)
		self.assertEqual(Yahoo2.getVolume("NTDOY.PK", datetime.date(1999,12,27)), 106000)
		self.assertEqual(Yahoo2.getVolume("NTDOY.PK", datetime.date(1999,9,23)), 25300)
		self.assertEqual(Yahoo2.getAdjustedClose("NTDOY.PK", datetime.date(2000,4,4)), 18.84)
		self.assertEqual(Yahoo2.getAdjustedClose("NTDOY.PK", datetime.date(1999,12,28)), 17.67)
		self.assertEqual(Yahoo2.getAdjustedClose("NTDOY.PK", datetime.date(2000,7,12)), 19.96)
		self.assertEqual(Yahoo2.getAdjustedClose("NTDOY.PK", datetime.date(2000,4,5)), 19.32)
		self.assertEqual(Yahoo2.getAdjustedClose("NTDOY.PK", datetime.date(2000,10,17)), 20.38)
		
		self.assertEqual(Yahoo2.getHigh("BRK-A", datetime.date(2008,6,4)), 133640.0)
		self.assertEqual(Yahoo2.getHigh("BRK-A", datetime.date(1990,1,12)), 8350.0)
		self.assertEqual(Yahoo2.getHigh("BRK-A", datetime.date(2007,10,22)), 127000.0)
		self.assertEqual(Yahoo2.getHigh("BRK-A", datetime.date(2007,10,19)), 129000.0)
		self.assertEqual(Yahoo2.getHigh("BRK-A", datetime.date(2007,10,18)), 129500.0)
		self.assertEqual(Yahoo2.getLow("BRK-A", datetime.date(1990,1,12)), 8175.0)
		self.assertEqual(Yahoo2.getLow("BRK-A", datetime.date(2008,6,4)), 130700.0)
		self.assertEqual(Yahoo2.getLow("BRK-A", datetime.date(2007,10,17)), 127700)
		self.assertEqual(Yahoo2.getLow("BRK-A", datetime.date(2007,10,16)), 126200)
		self.assertEqual(Yahoo2.getLow("BRK-A", datetime.date(2007,10,15)), 125500)
		self.assertEqual(Yahoo2.getOpen("BRK-A", datetime.date(1990,1,12)), 8350.0)
		self.assertEqual(Yahoo2.getOpen("BRK-A", datetime.date(2008,6,4)), 133000.0)
		self.assertEqual(Yahoo2.getOpen("BRK-A", datetime.date(2007,10,12)), 126500.0)
		self.assertEqual(Yahoo2.getOpen("BRK-A", datetime.date(2007,10,11)), 125000.0)
		self.assertEqual(Yahoo2.getOpen("BRK-A", datetime.date(2007,10,10)), 122550.0)
		self.assertEqual(Yahoo2.getClose("BRK-A", datetime.date(1990,1,12)), 8200.00)
		self.assertEqual(Yahoo2.getClose("BRK-A", datetime.date(2008,6,4)), 132990.00)
		self.assertEqual(Yahoo2.getClose("BRK-A", datetime.date(2007,10,9)), 122615.00)
		self.assertEqual(Yahoo2.getClose("BRK-A", datetime.date(2007,10,8)), 123390.00)
		self.assertEqual(Yahoo2.getClose("BRK-A", datetime.date(2007,10,5)), 121100.00)
		self.assertEqual(Yahoo2.getVolume("BRK-A", datetime.date(1990,1,12)), 46000.00)
		self.assertEqual(Yahoo2.getVolume("BRK-A", datetime.date(2008,6,4)), 50900.00)
		self.assertEqual(Yahoo2.getVolume("BRK-A", datetime.date(2007,10,4)), 43000)
		self.assertEqual(Yahoo2.getVolume("BRK-A", datetime.date(2007,10,3)), 16000)
		self.assertEqual(Yahoo2.getVolume("BRK-A", datetime.date(2007,10,2)), 22000)
		self.assertEqual(Yahoo2.getAdjustedClose("BRK-A", datetime.date(1990,1,12)), 8200.00)
		self.assertEqual(Yahoo2.getAdjustedClose("BRK-A", datetime.date(2008,6,4)), 132990)
		self.assertEqual(Yahoo2.getAdjustedClose("BRK-A", datetime.date(2007,10,1)), 118790)
		self.assertEqual(Yahoo2.getAdjustedClose("BRK-A", datetime.date(2007,9,28)), 118510)
		self.assertEqual(Yahoo2.getAdjustedClose("BRK-A", datetime.date(2007,9,27)), 117200)
		
	def testGetDates(self):
		"""Test that get dates returns the proper range """
		self.assertTrue(datetime.date(2009,1,28) in Yahoo2.getDates("BRK-A"))
		self.assertTrue(Yahoo2.getDates("BRK-A")[0] == datetime.date(1990,1,12))	