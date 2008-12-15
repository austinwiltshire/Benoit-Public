import Registry
import Website #for sec data from google

from SECFiling import Meta, Bloomberg, BService , Required, Provided
from elixir import metadata, setup_all, Field, Entity, Unicode
""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """

class Metadata(Bloomberg):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	Symbol = Required(Unicode(60))
	Industry = Provided(Unicode(60))

Metadata = Meta(Metadata)

	