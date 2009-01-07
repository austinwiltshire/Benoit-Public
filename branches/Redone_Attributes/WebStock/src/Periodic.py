""" Helper functions for checking out dates available to any particular persistant host document. """

from Registry import Registry
from Bloomberg import PersistantHost

def WebDates(cls, symbol):
	""" This returns a list of ALL available dates from the web, generally where the latest information is stored. """
	
	dateFunc = Registry.get("".join([cls.__name__,"Dates"]))
	
	return dateFunc(symbol)
	
def NewDates(cls, symbol):
	""" This is a helper function to discriminate between webdates and available dates.  I.e., the dates currently NOT stored in the database. """
	
	available = set(cls.AvailableDates(symbol))
	onTheWeb = set(cls.WebDates(symbol))
	return list(onTheWeb - available)

def AvailableDates(cls, symbol):
	""" This is a helper function to return all dates currently available in the database. """
	
	return [toDate(x.Date) for x in cls.query().filter_by(Symbol=symbol).all()]