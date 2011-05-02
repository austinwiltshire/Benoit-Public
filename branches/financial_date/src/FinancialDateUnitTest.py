""" Tests the FinancialDate package. """

import doctest
import contract
import unittest
import FinancialDate
import datetime

contract.checkmod(FinancialDate)

class DoctestWrapper(unittest.TestSuite):
	def __init__(self):
		unittest.TestSuite.__init__(self, doctest.DocTestSuite(FinancialDate))
        
class FinancialDateUnitTest(unittest.TestCase):
    """
    Tests cases for the financial_date module.
    """
    
    def test_5_after(self):
        """
        Test a week in advance from a sunday
        """
        
        self.assertEqual(FinancialDate.NthTradingDayAfter(datetime.datetime(2011, 5, 1), 0), datetime.datetime(2011, 5, 2))
        self.assertEqual(FinancialDate.NthTradingDayAfter(datetime.datetime(2011, 5, 1), 1), datetime.datetime(2011, 5, 3))
        self.assertEqual(FinancialDate.NthTradingDayAfter(datetime.datetime(2011, 5, 1), 2), datetime.datetime(2011, 5, 4))
        self.assertEqual(FinancialDate.NthTradingDayAfter(datetime.datetime(2011, 5, 1), 3), datetime.datetime(2011, 5, 5))
        self.assertEqual(FinancialDate.NthTradingDayAfter(datetime.datetime(2011, 5, 1), 4), datetime.datetime(2011, 5, 6))
        
    def test_5_before(self):
        """
        Test a week before from a saturday
        """
        self.assertEqual(FinancialDate.NthTradingDayBefore(datetime.datetime(2011, 4, 30), 0), datetime.datetime(2011, 4, 29))
        self.assertEqual(FinancialDate.NthTradingDayBefore(datetime.datetime(2011, 4, 30), 1), datetime.datetime(2011, 4, 28))
        self.assertEqual(FinancialDate.NthTradingDayBefore(datetime.datetime(2011, 4, 30), 2), datetime.datetime(2011, 4, 27))
        self.assertEqual(FinancialDate.NthTradingDayBefore(datetime.datetime(2011, 4, 30), 3), datetime.datetime(2011, 4, 26))
        self.assertEqual(FinancialDate.NthTradingDayBefore(datetime.datetime(2011, 4, 30), 4), datetime.datetime(2011, 4, 25))
        
    def test_before_sunday(self):
        """
        Test that we find a friday before a sunday
        """
        
        self.assertEqual(FinancialDate.FirstTradingDayBefore(datetime.datetime(1983, 4, 17)), datetime.datetime(1983, 4, 15))
        
    def test_after_saturday(self):
        """
        Test that we find a monday after a saturday
        """
        
        self.assertEqual(FinancialDate.FirstTradingDayAfter(datetime.datetime(1998, 1, 31)), datetime.datetime(1998,2,2))
        
    def test_before_2002_good_friday(self):
        """
        Test before date for floating holiday
        """
        
        self.assertEqual(FinancialDate.NthTradingDayBefore(datetime.datetime(2002, 3, 29), 0), datetime.datetime(2002, 3, 28))
        self.assertEqual(FinancialDate.FirstTradingDayBefore(datetime.datetime(2002, 3, 29)), datetime.datetime(2002, 3, 28))
    
    def test_after_2002_good_friday(self):
        """
        Test after date for floating holiday
        """

        self.assertEqual(FinancialDate.NthTradingDayAfter(datetime.datetime(2002, 3, 29), 0), datetime.datetime(2002, 4, 1))
        self.assertEqual(FinancialDate.FirstTradingDayAfter(datetime.datetime(2002, 3, 29)), datetime.datetime(2002, 4, 1))
    
    def test_7_before_1978_christmas(self):
        """
        Test combination of non-trivial N and static holiday in non-recent history for before dates
        """
        
        self.assertEqual(FinancialDate.NthTradingDayBefore(datetime.datetime(1978, 12, 25), 7), datetime.datetime(1978, 12, 13))
            
    def test_7_after_1978_christmas(self):
        """
        Test combination of non-trivial N and static holiday in non-recent history for after dates
        """
        
        self.assertEqual(FinancialDate.NthTradingDayAfter(datetime.datetime(1978, 12, 25), 7), datetime.datetime(1979, 1,  5))
        
    def test_is_trading_day(self):
        """
        Test inclusion of specific trading days
        """
        
        self.assertTrue(FinancialDate.IsTradingDay(datetime.datetime(1965, 8, 17)))
        
        
if __name__ == "__main__": #for coverage tests
	unittest.main()
        