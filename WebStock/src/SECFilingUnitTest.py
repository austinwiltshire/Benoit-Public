""" A deep unit test(verification) that checks to make sure bloomberg is doing things how i expect them. """

import unittest
import Metadata
import BalanceSheet
from elixir import setup_all, metadata
from os import system, listdir, getcwd

#detect and see if the sql base is already set up
#if it is, delete it.

if 'SECFilingUnitTest.sqlite' in listdir(getcwd()):
	system("rm SECFilingUnitTest.sqlite")

metadata.bind = "sqlite:///SECFilingUnitTest.sqlite"
metadata.bind.echo = True
setup_all(True)

class MarketTestCase(unittest.TestCase):
	def setUp(self):
		pass
	
	def testProvidedAttributes(self):
		x = Metadata.Metadata("IRBT")
		self.assertEqual(Metadata.Metadata._provided_attributes_[0][0],"Industry")
		
	def testRequiredAttributes(self):
		self.assertEqual(Metadata.Metadata._required_attributes_[0][0],"Symbol")
		
	def testIndustry(self):
		self.assertEqual(len(Metadata.Metadata.query.all()), 0)
		#set up a NEW entry, fetch should equal 0
		x = Metadata.Metadata("IRBT")
		#x.Symbol = "IRBT"
		self.assertEqual(x.Industry, u"Appliance & Tool")
		
		self.assertEqual(len(Metadata.Metadata.query.all()), 1)
		
		y = Metadata.Metadata.fetch("IRBT")
		
		self.assertEqual(x,y)
		self.assertEqual(y.Symbol,u"IRBT")
		self.assertEqual(y.Industry,u"Appliance & Tool")
		
		self.assertEqual(len(Metadata.Metadata.query.all()), 1)
		
		#use sql to check and make sure entry exists, and exists uniquely (fetch should = 1)
		
		#create the same new metadata, ensure fetch still equals 1. check and see if you can detect whether things are committing or loading