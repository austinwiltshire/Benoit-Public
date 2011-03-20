from SECFiling import Require, Provide
from Bloomberg import PersistantHost
from elixir import DateTime, Float, Unicode #Field, DateTime, Float, Entity, Unicode
from elixir import Date as DateT

Float4 = lambda : Float(precision=4)

""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """


class BalanceSheet(object):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	
	Symbol = Require(Unicode(60))
	Date = Require(DateT)
		
	CashAndEquivalents = Provide(Float4())
 	ShortTermInvestments = Provide(Float4())
 	CashAndShortTermInvestments = Provide(Float4())
 	AccountsReceivableTrade = Provide(Float4())
 	ReceivablesOther = Provide(Float4())
 	TotalReceivablesNet = Provide(Float4())
 	TotalInventory = Provide(Float4())
 	PrepaidExpenses = Provide(Float4())
 	OtherCurrentAssetsTotal = Provide(Float4())
 	TotalCurrentAssets = Provide(Float4())
 	PPE = Provide(Float4())
 	Goodwill = Provide(Float4())
 	Intangibles = Provide(Float4())
 	LongTermInvestments = Provide(Float4())
 	OtherLongTermAssets = Provide(Float4())
 	TotalAssets = Provide(Float4())
 	AccountsPayable = Provide(Float4())
 	AccruedExpenses = Provide(Float4())
 	NotesPayable = Provide(Float4())
 	CurrentPortLTDebtToCapital = Provide(Float4())
 	OtherCurrentLiabilities = Provide(Float4())
 	TotalCurrentLiabilities = Provide(Float4())
 	LongTermDebt = Provide(Float4())
 	CapitalLeaseObligations = Provide(Float4())
 	TotalLongTermDebt = Provide(Float4())
 	TotalDebt = Provide(Float4())
 	DeferredIncomeTax = Provide(Float4())
 	MinorityInterest_Bal = Provide(Float4())
 	OtherLiabilities = Provide(Float4())
 	TotalLiabilities = Provide(Float4())
 	RedeemablePreferredStock = Provide(Float4())
 	PreferredStockNonRedeemable = Provide(Float4())
 	CommonStock = Provide(Float4())
 	AdditionalPaidInCapital = Provide(Float4())
 	RetainedEarnings = Provide(Float4())
 	TreasuryStock = Provide(Float4())
 	OtherEquity = Provide(Float4())
 	TotalEquity = Provide(Float4())
 	TotalLiabilitiesAndShareholdersEquity = Provide(Float4())
 	SharesOuts = Provide(Float4())
 	TotalCommonSharesOutstanding = Provide(Float4())