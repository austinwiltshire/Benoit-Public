from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float, String, Column, Boolean, Unicode, Integer
Base = declarative_base()

from sqlalchemy import Date as sql_date

#enumerated classes
#TODO: i wonder if i could make an enumerated class metaclass that would automatically register the enumerations in a table?
class Period(object):
    pass

class Quarter(Period):
    Enumeration = 0

class Annual(Period):
    Enumeration = 1

class BalanceSheet(Base):
    """ Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
    semantic reference """
    
    __tablename__ = 'balancesheet'
    
    Symbol = Column(Unicode(10), primary_key=True)
    Date = Column(sql_date, primary_key=True)
       
    CashAndEquivalents = Column(Float)
    ShortTermInvestments = Column(Float)
    CashAndShortTermInvestments = Column(Float)
    AccountsReceivableTrade = Column(Float)
    ReceivablesOther = Column(Float)
    TotalReceivablesNet = Column(Float)
    TotalInventory = Column(Float)
    PrepaidExpenses = Column(Float)
    OtherCurrentAssetsTotal = Column(Float)
    TotalCurrentAssets = Column(Float)
    PPE = Column(Float)
    Goodwill = Column(Float)
    Intangibles = Column(Float)
    LongTermInvestments = Column(Float)
    OtherLongTermAssets = Column(Float)
    TotalAssets = Column(Float)
    AccountsPayable = Column(Float)
    AccruedExpenses = Column(Float)
    NotesPayable = Column(Float)
    CurrentPortLTDebtToCapital = Column(Float)
    OtherCurrentLiabilities = Column(Float)
    TotalCurrentLiabilities = Column(Float)
    LongTermDebt = Column(Float)
    CapitalLeaseObligations = Column(Float)
    TotalLongTermDebt = Column(Float)
    TotalDebt = Column(Float)
    DeferredIncomeTax = Column(Float)
    MinorityInterest = Column(Float)
    OtherLiabilities = Column(Float)
    TotalLiabilities = Column(Float)
    RedeemablePreferredStock = Column(Float)
    PreferredStockNonRedeemable = Column(Float)
    CommonStock = Column(Float)
    AdditionalPaidInCapital = Column(Float)
    RetainedEarnings = Column(Float)
    TreasuryStock = Column(Float)
    OtherEquity = Column(Float)
    TotalEquity = Column(Float)
    TotalLiabilitiesAndShareholdersEquity = Column(Float)
    SharesOuts = Column(Float)
    TotalCommonSharesOutstanding = Column(Float)
    
    Period = Column(Integer)
    
    NextIssueDate = Column(sql_date)
    PreviousIssueDate = Column(sql_date)
    ConcurrentCashFlowStatementIssueDate = Column(sql_date)
    ConcurrentIncomeStatementIssueDate = Column(sql_date)
    NextCashFlowStatementIssueDate = Column(sql_date)
    PreviousCashFlowStatementIssueDate = Column(sql_date)
    NextIncomeStatementIssueDate = Column(sql_date)
    PreviousIncomeStatementIssueDate = Column(sql_date)
     
    def __init__(self, Symbol,
                       Date,
                       CashAndEquivalents,
                       ShortTermInvestments,
                       CashAndShortTermInvestments,
                       AccountsReceivableTrade,
                       ReceivablesOther,
                       TotalReceivablesNet,
                       TotalInventory,
                       PrepaidExpenses,
                       OtherCurrentAssetsTotal,
                       TotalCurrentAssets,
                       PPE,
                       Goodwill,
                       Intangibles,
                       LongTermInvestments,
                       OtherLongTermAssets,
                       TotalAssets,
                       AccountsPayable,
                       AccruedExpenses,
                       NotesPayable,
                       CurrentPortLTDebtToCapital,
                       OtherCurrentLiabilities,
                       TotalCurrentLiabilities,
                       LongTermDebt,
                       CapitalLeaseObligations,
                       TotalLongTermDebt,
                       TotalDebt,
                       DeferredIncomeTax,
                       MinorityInterest,
                       OtherLiabilities,
                       TotalLiabilities,
                       RedeemablePreferredStock,
                       PreferredStockNonRedeemable,
                       CommonStock,
                       AdditionalPaidInCapital,
                       RetainedEarnings,
                       TreasuryStock,
                       OtherEquity,
                       TotalEquity,
                       TotalLiabilitiesAndShareholdersEquity,
                       SharesOuts,
                       TotalCommonSharesOutstanding,
                       Period):
        self.Symbol = Symbol
        self.Date = Date
        self.CashAndEquivalents = CashAndEquivalents
        self.ShortTermInvestments = ShortTermInvestments
        self.CashAndShortTermInvestments = CashAndShortTermInvestments
        self.AccountsReceivableTrade = AccountsReceivableTrade
        self.ReceivablesOther = ReceivablesOther
        self.TotalReceivablesNet = TotalReceivablesNet
        self.TotalInventory = TotalInventory
        self.PrepaidExpenses = PrepaidExpenses
        self.OtherCurrentAssetsTotal = OtherCurrentAssetsTotal
        self.TotalCurrentAssets = TotalCurrentAssets
        self.PPE = PPE
        self.Goodwill = Goodwill
        self.Intangibles = Intangibles
        self.LongTermInvestments = LongTermInvestments
        self.OtherLongTermAssets = OtherLongTermAssets
        self.TotalAssets = TotalAssets
        self.AccountsPayable = AccountsPayable
        self.AccruedExpenses = AccruedExpenses
        self.NotesPayable = NotesPayable
        self.CurrentPortLTDebtToCapital = CurrentPortLTDebtToCapital
        self.OtherCurrentLiabilities = OtherCurrentLiabilities
        self.TotalCurrentLiabilities = TotalCurrentLiabilities
        self.LongTermDebt = LongTermDebt
        self.CapitalLeaseObligations = CapitalLeaseObligations
        self.TotalLongTermDebt = TotalLongTermDebt
        self.TotalDebt = TotalDebt
        self.DeferredIncomeTax = DeferredIncomeTax
        self.MinorityInterest = MinorityInterest
        self.OtherLiabilities = OtherLiabilities
        self.TotalLiabilities = TotalLiabilities
        self.RedeemablePreferredStock = RedeemablePreferredStock
        self.PreferredStockNonRedeemable = PreferredStockNonRedeemable
        self.CommonStock = CommonStock
        self.AdditionalPaidInCapital = AdditionalPaidInCapital
        self.RetainedEarnings = RetainedEarnings
        self.TreasuryStock = TreasuryStock
        self.OtherEquity = OtherEquity
        self.TotalEquity = TotalEquity
        self.TotalLiabilitiesAndShareholdersEquity = TotalLiabilitiesAndShareholdersEquity
        self.SharesOuts = SharesOuts
        self.TotalCommonSharesOutstanding = TotalCommonSharesOutstanding
        self.Period = Period

class CashFlowStatement(Base):
   
    __tablename__ = "cashflowstatement"
    
    Symbol = Column(Unicode(10), primary_key=True)
    Date = Column(sql_date, primary_key=True)
    
    NetIncomeStartingLine = Column(Float)
    DepreciationDepletion = Column(Float)
    Amortization = Column(Float)
    DeferredTaxes = Column(Float)
    NonCashItems = Column(Float)
    ChangesInWorkingCapital = Column(Float)
    CashFromOperatingActivities = Column(Float)
    CapitalExpenditures = Column(Float)
    OtherInvestingCashFlow = Column(Float)
    CashFromInvestingActivities = Column(Float)
    FinancingCashFlowItems = Column(Float)
    TotalCashDividendsPaid = Column(Float)
    IssuanceOfStock = Column(Float)
    IssuanceOfDebt = Column(Float)
    CashFromFinancingActivities = Column(Float)
    ForeignExchangeEffects = Column(Float)
    NetChangeInCash = Column(Float)
    CashInterestPaid = Column(Float)
    CashTaxesPaid = Column(Float)
    
    Period = Column(Integer)
    
    NextIssueDate = Column(sql_date)
    PreviousIssueDate = Column(sql_date)
    ConcurrentBalanceSheetIssueDate = Column(sql_date)
    ConcurrentIncomeStatementIssueDate = Column(sql_date)
    NextBalanceSheetIssueDate = Column(sql_date)
    PreviousBalanceSheetIssueDate = Column(sql_date)
    NextIncomeStatementIssueDate = Column(sql_date)
    PreviousIncomeStatementIssueDate = Column(sql_date) 
    
    def __init__(self, Symbol, 
                       Date,
                       NetIncomeStartingLine,
                       DepreciationDepletion,
                       Amortization,
                       DeferredTaxes,
                       NonCashItems,
                       ChangesInWorkingCapital,
                       CashFromOperatingActivities,
                       CapitalExpenditures,
                       OtherInvestingCashFlow,
                       CashFromInvestingActivities,
                       FinancingCashFlowItems,
                       TotalCashDividendsPaid,
                       IssuanceOfStock,
                       IssuanceOfDebt,
                       CashFromFinancingActivities,
                       ForeignExchangeEffects,
                       NetChangeInCash,
                       CashInterestPaid,
                       CashTaxesPaid,
                       Period):     
        self.Symbol = Symbol
        self.Date = Date
        self.NetIncomeStartingLine = NetIncomeStartingLine
        self.DepreciationDepletion = DepreciationDepletion
        self.Amortization = Amortization
        self.DeferredTaxes = DeferredTaxes
        self.NonCashItems = NonCashItems
        self.ChangesInWorkingCapital = ChangesInWorkingCapital
        self.CashFromOperatingActivities = CashFromOperatingActivities
        self.CapitalExpenditures = CapitalExpenditures
        self.OtherInvestingCashFlow = OtherInvestingCashFlow
        self.CashFromInvestingActivities = CashFromInvestingActivities
        self.FinancingCashFlowItems = FinancingCashFlowItems
        self.TotalCashDividendsPaid = TotalCashDividendsPaid
        self.IssuanceOfStock = IssuanceOfStock
        self.IssuanceOfDebt = IssuanceOfDebt
        self.CashFromFinancingActivities = CashFromFinancingActivities
        self.ForeignExchangeEffects = ForeignExchangeEffects
        self.NetChangeInCash = NetChangeInCash
        self.CashInterestPaid = CashInterestPaid
        self.CashTaxesPaid = CashTaxesPaid
        self.Period = Period
        
        
class IncomeStatement(Base):
    """ Holds NetIncome and other Income Statement information in a declarative syntax. """
    
    __tablename__ = "incomestatement"
    
    Symbol = Column(Unicode(60), primary_key=True)
    Date = Column(sql_date, primary_key=True)
    
    Revenue = Column(Float)
    OtherRevenue = Column(Float)
    TotalRevenue = Column(Float)
    CostOfRevenue = Column(Float)
    GrossProfit = Column(Float)
    SGAExpenses = Column(Float)
    ResearchAndDevelopment = Column(Float)
    DepreciationAmortization = Column(Float)
    InterestNetOperating = Column(Float)
    UnusualExpense = Column(Float)
    OtherOperatingExpenses = Column(Float)
    TotalOperatingExpense = Column(Float)
    OperatingIncome = Column(Float)
    InterestIncome = Column(Float)
    GainOnSaleOfAssets = Column(Float)
    OtherNet = Column(Float)
    IncomeBeforeTax = Column(Float)
    IncomeAfterTax = Column(Float)
    MinorityInterest_Inc = Column(Float)
    EquityInAffiliates = Column(Float)
    NetIncomeBeforeExtraItems = Column(Float)
    AccountingChange = Column(Float)
    DiscontinuedOperations = Column(Float)
    ExtraordinaryItem = Column(Float)
    NetIncome = Column(Float)
    PreferredDividends = Column(Float)
    IncomeAvailToCommonExclExtraItems = Column(Float)
    IncomeAvailToCommonInclExtraItems = Column(Float)
    BasicWeightedAverageShares = Column(Float)
    BasicEPSExclExtraItems = Column(Float)
    BasicEPSInclExtraItems = Column(Float)
    DilutionAdjustment = Column(Float)
    DilutedWeightedAverageShares = Column(Float)
    DilutedEPSExclExtraItems = Column(Float)
    DilutedEPSInclExtraItems = Column(Float)
    DividendsPerShare = Column(Float)
    GrossDividends = Column(Float)
    NetIncomeAfterCompExp = Column(Float)
    BasicEPSAfterCompExp = Column(Float)
    DilutedEPSAfterCompExp = Column(Float)
    DepreciationSupplemental = Column(Float)
    TotalSpecialItems = Column(Float)
    NormalizedIncomeBeforeTaxes = Column(Float)
    EffectsOfSpecialItemsOnIncomeTaxes = Column(Float)
    IncomeTaxesExSpecialItems = Column(Float)
    NormalizedIncomeAfterTaxes = Column(Float)
    NormalizedIncomeAvailableCommon = Column(Float)
    BasicNormalizedEPS = Column(Float)
    DilutedNormalizedEPS = Column(Float)
    
    Period = Column(Integer)
    
    NextIssueDate = Column(sql_date)
    PreviousIssueDate = Column(sql_date)
    ConcurrentBalanceSheetIssueDate = Column(sql_date)
    ConcurrentCashFlowStatementIssueDate = Column(sql_date)
    NextBalanceSheetIssueDate = Column(sql_date)
    PreviousBalanceSheetIssueDate = Column(sql_date)
    NextCashFlowStatementIssueDate = Column(sql_date)
    PreviousCashFlowStatementIssueDate = Column(sql_date) 
    
    def __init__(self,
                 symbol,
                 date,
                 Revenue,                
                 OtherRevenue,
                 TotalRevenue,
                 CostOfRevenue,
                 GrossProfit,
                 SGAExpenses,
                 ResearchAndDevelopment,
                 DepreciationAmortization,
                 InterestNetOperating,
                 UnusualExpense,
                 OtherOperatingExpenses,
                 TotalOperatingExpense,
                 OperatingIncome,
                 InterestIncome,
                 GainOnSaleOfAssets,
                 OtherNet,
                 IncomeBeforeTax,
                 IncomeAfterTax,
                 MinorityInterest_Inc,
                 EquityInAffiliates,
                 NetIncomeBeforeExtraItems,
                 AccountingChange,
                 DiscontinuedOperations,
                 ExtraordinaryItem,
                 NetIncome,
                 PreferredDividends,
                 IncomeAvailToCommonExclExtraItems,
                 IncomeAvailToCommonInclExtraItems,
                 BasicWeightedAverageShares,
                 BasicEPSExclExtraItems,
                 BasicEPSInclExtraItems,
                 DilutionAdjustment,
                 DilutedWeightedAverageShares,
                 DilutedEPSExclExtraItems,
                 DilutedEPSInclExtraItems,
                 DividendsPerShare,
                 GrossDividends,
                 NetIncomeAfterCompExp,
                 BasicEPSAfterCompExp,
                 DilutedEPSAfterCompExp,
                 DepreciationSupplemental,
                 TotalSpecialItems,
                 NormalizedIncomeBeforeTaxes,
                 EffectsOfSpecialItemsOnIncomeTaxes,
                 IncomeTaxesExSpecialItems,
                 NormalizedIncomeAfterTaxes,
                 NormalizedIncomeAvailableCommon,
                 BasicNormalizedEPS,
                 DilutedNormalizedEPS,
                 period):
        
        self.Symbol = symbol
        self.Date = date
        self.Revenue = Revenue
        self.OtherRevenue = OtherRevenue
        self.TotalRevenue = TotalRevenue
        self.CostOfRevenue = CostOfRevenue
        self.GrossProfit = GrossProfit
        self.SGAExpenses = SGAExpenses
        self.ResearchAndDevelopment = ResearchAndDevelopment
        self.DepreciationAmortization = DepreciationAmortization
        self.InterestNetOperating = InterestNetOperating
        self.UnusualExpense = UnusualExpense
        self.OtherOperatingExpenses = OtherOperatingExpenses
        self.TotalOperatingExpense = TotalOperatingExpense
        self.OperatingIncome = OperatingIncome
        self.InterestIncome = InterestIncome
        self.GainOnSaleOfAssets = GainOnSaleOfAssets
        self.OtherNet = OtherNet
        self.IncomeBeforeTax = IncomeBeforeTax
        self.IncomeAfterTax = IncomeAfterTax
        self.MinorityInterest_Inc = MinorityInterest_Inc
        self.EquityInAffiliates = EquityInAffiliates
        self.NetIncomeBeforeExtraItems = NetIncomeBeforeExtraItems
        self.AccountingChange = AccountingChange
        self.DiscontinuedOperations = DiscontinuedOperations
        self.ExtraordinaryItem = ExtraordinaryItem
        self.NetIncome = NetIncome
        self.PreferredDividends = PreferredDividends
        self.IncomeAvailToCommonExclExtraItems = IncomeAvailToCommonExclExtraItems
        self.IncomeAvailToCommonInclExtraItems = IncomeAvailToCommonInclExtraItems
        self.BasicWeightedAverageShares = BasicWeightedAverageShares
        self.BasicEPSExclExtraItems = BasicEPSExclExtraItems
        self.BasicEPSInclExtraItems = BasicEPSInclExtraItems
        self.DilutionAdjustment = DilutionAdjustment
        self.DilutedWeightedAverageShares = DilutedWeightedAverageShares
        self.DilutedEPSExclExtraItems = DilutedEPSExclExtraItems
        self.DilutedEPSInclExtraItems = DilutedEPSInclExtraItems
        self.DividendsPerShare = DividendsPerShare
        self.GrossDividends = GrossDividends
        self.NetIncomeAfterCompExp = NetIncomeAfterCompExp
        self.BasicEPSAfterCompExp = BasicEPSAfterCompExp
        self.DilutedEPSAfterCompExp = DilutedEPSAfterCompExp
        self.DepreciationSupplemental = DepreciationSupplemental
        self.TotalSpecialItems = TotalSpecialItems
        self.NormalizedIncomeBeforeTaxes = NormalizedIncomeBeforeTaxes
        self.EffectsOfSpecialItemsOnIncomeTaxes = EffectsOfSpecialItemsOnIncomeTaxes
        self.IncomeTaxesExSpecialItems = IncomeTaxesExSpecialItems
        self.NormalizedIncomeAfterTaxes = NormalizedIncomeAfterTaxes
        self.NormalizedIncomeAvailableCommon = NormalizedIncomeAvailableCommon
        self.BasicNormalizedEPS = BasicNormalizedEPS
        self.DilutedNormalizedEPS = DilutedNormalizedEPS
        self.Period = period