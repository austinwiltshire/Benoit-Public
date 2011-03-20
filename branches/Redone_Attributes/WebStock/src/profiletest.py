import unittest
#import MarketUnitTest
import time

#suite = unittest.TestLoader().loadTestsFromTestCase(MarketUnitTest.MarketTestCase)

import Module2
import Database
Database.Remote()

def timeit():
	begin = time.clock()
	runsuite()
	return time.clock() - begin

def runsuite():
#	suite.run(unittest.TestResult())
	symbols = [u'IRBT', u'SBUX', u'YHOO', u'GOOG', u'LMT', u'DD', u'GM', u'GE', u'MRK', u'AAPL']
	for symbol in symbols:
		print "Prefetching ", symbol
		Module2.Symbol(symbol).prefetch()

def avg(lst):
	return sum(lst) / len(lst)

def multi(num):
	for i in range(num):
		yield timeit()

