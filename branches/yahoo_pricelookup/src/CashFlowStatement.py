""" CashFlowStatement holds data that is held in a company's Cash Flow Statement.  It is accessed using a declarative mechanism and expects to be further
specialized by a Bloomberg Metaclass such as Annual or Quarterly. """

from SECFiling import PersistantHost, Provided, Required
from elixir import Float, Unicode, DateTime

class CashFlowStatement(PersistantHost):
	""" Holds Cash Flow Statement information using a declarative syntax and the Bloomberg Framework. The name assigned to, per attribute, is the name to use
	when using any instances of this class, while the type of attribute is Required if the class needs it to be created, or provided if a created class can do
	lookup for that data.  Finally, the attributes themselves also require field information for persistance.  """
	
	Symbol = Required(Unicode(60))
	Date = Required(DateTime)
	NetIncomeStartingLine = Provided(Float(precision=4))