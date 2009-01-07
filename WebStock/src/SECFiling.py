""" This is a mess.  Combine with Bloomberg and attributes, as this logic is just all over the place.  This might dissapear completely with proper metaclasses. """

from Registry import Registry
import Website
import copy

import elixir
from elixir import Entity, Field

from Bloomberg import Required, Provided, Attribute, PersistantHost, DecorateServices, ServicesDetected, DecoratePersistantHost
from Periodic import AvailableDates

def MakePeriodical(document_type):
	def _(document):
		
		document_name = "".join([document_type,document.__name__])
		document = type(document_name,(document,Entity),{})
		
		staticHost = DecoratePersistantHost(document, document_type)
		#staticHost.AvailableDates = AvailableDates
		return staticHost
	return _

def Meta(document):
	
	document = type(document.__name__,(document,Entity),{})
	
	return DecoratePersistantHost(document, "Meta")

Daily = MakePeriodical("Daily")
#Annual = MakePeriodical("Annual")
Quarterly = MakePeriodical("Quarterly")

	
