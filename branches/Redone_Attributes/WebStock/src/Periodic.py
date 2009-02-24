""" Helper functions for checking out dates available to any particular persistant host document. """

import Registry
from Bloomberg import PersistantHost
from Adapt import Adapt
import datetime


def WebDates(cls, symbol):
	""" This returns a list of ALL available dates from the web, generally where the latest information is stored. """
	
	dateFunc = Registry.Get("".join([cls.__name__,"Dates"]))
	
	return sorted(dateFunc(symbol))
	
def NewDates(cls, symbol):
	""" This is a helper function to discriminate between webdates and available dates.  I.e., the dates currently NOT stored in the database. """
	
	available = set(AvailableDates(cls, symbol))
	onTheWeb = set(WebDates(cls, symbol))
	return sorted(list(onTheWeb - available))

def AvailableDates(cls, symbol):
	""" This is a helper function to return all dates currently available in the database. """
	return sorted([Adapt(x.Date,datetime.date) for x in cls.query().filter_by(_Symbol=symbol).all()])