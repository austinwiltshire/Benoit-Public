""" Contains data about a company, such as it's industry and sector.  Currently this is derived from Google information, whom I'm assuming is deriving it from 
some sort of official tally. Metadata also specializes itself in this module.

Implementation Notes:
In this case, it may be cleaner if Metadata inherits from a class that declares its own __metaclass__.  Since Metadata is specialized as soon as it's declared,
it's make sense and would be insanely easy to switch between the two methods should something change in the future.  In fact, Daily can be done in the same way.
It's only quarterly and annually that need to be delayed."""

from SECFiling import Require, Provide, PersistantHost
from Bloomberg import Meta
from elixir import Unicode

class Metadata(PersistantHost):
	""" Contains Industry, Sector and other information. """
	
	Symbol = Require(Unicode(60))
	
	Industry = Provide(Unicode(60))
	CurrencyReported = Provide(Unicode(60))
	Exchange = Provide(Unicode(60))
	Sector = Provide(Unicode(60))
	ProperName = Provide(Unicode(60))

#def getCompetitors(symbol):
#	return getMetadata(symbol).competitors
	
Metadata = Meta(Metadata)

	