""" This module contains specializations of various documents on a daily basis, configured as such that lookup should be able to occur on a semi-daily basis
(excluding weekends and holidays).

Implementation Note:
Currently only Prices and Fundamentals(which indirectly relies on Prices) are defined.  However, another addition here would be technicals. 
"""

from Bloomberg import Daily
from TradingDay import Prices
from Fundamentals import Fundamentals

Prices = Daily(Prices)
Fundamentals = Daily(Fundamentals)