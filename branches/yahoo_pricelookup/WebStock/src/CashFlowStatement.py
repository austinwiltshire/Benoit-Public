""" CashFlowStatement holds data that is held in a company's Cash Flow Statement.  It is accessed using a declarative mechanism and expects to be further
specialized by a Bloomberg Metaclass such as Annual or Quarterly. """

from SECFiling import PersistantHost, Provide, Require
from elixir import Float, Unicode
from elixir import Date as DateT

Float4 = lambda : Float(precision=4)

class CashFlowStatement(object):
	""" Holds Cash Flow Statement information using a declarative syntax and the Bloomberg Framework. The name assigned to, per attribute, is the name to use
	when using any instances of this class, while the type of attribute is Required if the class needs it to be created, or provided if a created class can do
	lookup for that data.  Finally, the attributes themselves also require field information for persistance.  """
	
	Symbol = Require(Unicode(60))
	Date = Require(DateT)
	
	NetIncomeStartingLine = Provide(Float4())
 	DepreciationDepletion = Provide(Float4())
 	Amortization = Provide(Float4())
 	DeferredTaxes = Provide(Float4())
 	NonCashItems = Provide(Float4())
 	ChangesInWorkingCapital = Provide(Float4())
 	CashFromOperatingActivities = Provide(Float4())
 	CapitalExpenditures = Provide(Float4())
 	OtherInvestingCashFlow = Provide(Float4())
 	CashFromInvestingActivities = Provide(Float4())
 	FinancingCashFlowItems = Provide(Float4())
 	TotalCashDividendsPaid = Provide(Float4())
 	IssuanceOfStock = Provide(Float4())
 	IssuanceOfDebt = Provide(Float4())
 	CashFromFinancingActivities = Provide(Float4())
 	ForeignExchangeEffects = Provide(Float4())
 	NetChangeInCash = Provide(Float4())
 	CashInterestPaid = Provide(Float4())
 	CashTaxesPaid = Provide(Float4())