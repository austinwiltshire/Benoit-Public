""" This module defines the IncomeStatement financial document, which holds stuff like NetIncome and PreferredDividends """

from SECFiling import PersistantHost, Require, Provide
from elixir import Float, Unicode
from elixir import Date as DateT

Float4 = lambda : Float(Precision=4) 

class IncomeStatement(object):
	""" Holds NetIncome and other Income Statement information in a declarative syntax. """
	
	Symbol = Require(Unicode(60))
	Date = Require(DateT)
	
#	PreferredDividends = Provide(Float(precision=4))
#	NetIncome = Provide(Float(precision=4))
#	Revenue = Provide(Float(precision=4))
#	UnusualExpense = Provide(Float(precision=4))

	Revenue = Provide(Float4())
 	OtherRevenue = Provide(Float4())
 	TotalRevenue = Provide(Float4())
 	CostOfRevenue = Provide(Float4())
 	GrossProfit = Provide(Float4())
 	SGAExpenses = Provide(Float4())
 	ResearchAndDevelopment = Provide(Float4())
 	DepreciationAmortization = Provide(Float4())
 	InterestNetOperating = Provide(Float4())
 	UnusualExpense = Provide(Float4())
 	OtherOperatingExpenses = Provide(Float4())
 	TotalOperatingExpense = Provide(Float4())
 	OperatingIncome = Provide(Float4())
 	InterestIncome = Provide(Float4())
 	GainOnSaleOfAssets = Provide(Float4())
 	OtherNet = Provide(Float4())
 	IncomeBeforeTax = Provide(Float4())
 	IncomeAfterTax = Provide(Float4())
 	MinorityInterest_Inc = Provide(Float4())
 	EquityInAffiliates = Provide(Float4())
 	NetIncomeBeforeExtraItems = Provide(Float4())
 	AccountingChange = Provide(Float4())
 	DiscontinuedOperations = Provide(Float4())
 	ExtraordinaryItem = Provide(Float4())
 	NetIncome = Provide(Float4())
 	PreferredDividends = Provide(Float4())
 	IncomeAvailToCommonExclExtraItems = Provide(Float4())
 	IncomeAvailToCommonInclExtraItems = Provide(Float4())
 	BasicWeightedAverageShares = Provide(Float4())
 	BasicEPSExclExtraItems = Provide(Float4())
 	BasicEPSInclExtraItems = Provide(Float4())
 	DilutionAdjustment = Provide(Float4())
 	DilutedWeightedAverageShares = Provide(Float4())
 	DilutedEPSExclExtraItems = Provide(Float4())
 	DilutedEPSInclExtraItems = Provide(Float4())
 	DividendsPerShare = Provide(Float4())
 	GrossDividends = Provide(Float4())
 	NetIncomeAfterCompExp = Provide(Float4())
 	BasicEPSAfterCompExp = Provide(Float4())
 	DilutedEPSAfterCompExp = Provide(Float4())
 	DepreciationSupplemental = Provide(Float4())
 	TotalSpecialItems = Provide(Float4())
 	NormalizedIncomeBeforeTaxes = Provide(Float4())
 	EffectsOfSpecialItemsOnIncomeTaxes = Provide(Float4())
 	IncomeTaxesExSpecialItems = Provide(Float4())
 	NormalizedIncomeAfterTaxes = Provide(Float4())
 	NormalizedIncomeAvailableCommon = Provide(Float4())
 	BasicNormalizedEPS = Provide(Float4())
 	DilutedNormalizedEPS = Provide(Float4())

