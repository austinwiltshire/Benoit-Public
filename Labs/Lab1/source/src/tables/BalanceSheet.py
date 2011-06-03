from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Date, Float, String, Column, Boolean, Unicode, Integer
Base = declarative_base()

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
     Date = Column(Date, primary_key=True)
        
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
