from Registry import Registry
from Bloomberg import PersistantHost

def WebDates(cls, symbol):
	dateFunc = Registry.get("".join([cls.__name__,"Dates"]))
	return dateFunc(symbol)
	
def NewDates(cls, symbol):
	available = set(cls.AvailableDates(symbol))
	onTheWeb = set(cls.WebDates(symbol))
	return list(onTheWeb - available)

def AvailableDates(cls, symbol):
	return [toDate(x.Date) for x in cls.query().filter_by(Symbol=symbol).all()]

#class Periodic(PersistantHost):
#	@classmethod
#	def AvailableDates(cls, symbol):
#		return [toDate(x.Date) for x in cls.query().filter_by(Symbol=symbol).all()]