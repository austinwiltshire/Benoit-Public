import table

from tables import BalanceSheet

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
import SnP500

#here's how to create a new table
#first declare the new table in a new module with the fields you want - don't forget to add period since i'm getting rid of different tables for different periods
#then create an engine like below
#then call this table.metadata.create_all(engine) where table is the name of your table

to_engine = create_engine("mysql://austinwiltshire@richie:3306/bloomberg_v2")
from_engine = create_engine("mysql://austinwiltshire@richie:3306/bloomberg_test")

ToSession = sessionmaker(to_engine)
to_session = ToSession()

FromSession = sessionmaker(from_engine)
from_session = FromSession()

metadata = MetaData(bind=from_engine,reflect=True)

#TODO: change to annual balance sheet table
old_bs_table = metadata.tables['annualbalancesheet']

symbols = SnP500.symbols

def transfer_symbol(symbol):

    print "Transferring %s" % symbol
    additions = []
    
    for Symbol, \
        Date, \
        CashAndEquivalents, \
        ShortTermInvestments, \
        CashAndShortTermInvestments, \
        AccountsReceivableTrade, \
        ReceivablesOther, \
        TotalReceivablesNet, \
        TotalInventory, \
        PrepaidExpenses, \
        OtherCurrentAssetsTotal, \
        TotalCurrentAssets, \
        PPE, \
        Goodwill, \
        Intangibles, \
        LongTermInvestments, \
        OtherLongTermAssets, \
        TotalAssets, \
        AccountsPayable, \
        AccruedExpenses, \
        NotesPayable, \
        CurrentPortLTDebtToCapital, \
        OtherCurrentLiabilities, \
        TotalCurrentLiabilities, \
        LongTermDebt, \
        CapitalLeaseObligations, \
        TotalLongTermDebt, \
        TotalDebt, \
        DeferredIncomeTax, \
        MinorityInterest, \
        OtherLiabilities, \
        TotalLiabilities, \
        RedeemablePreferredStock, \
        PreferredStockNonRedeemable, \
        CommonStock, \
        AdditionalPaidInCapital, \
        RetainedEarnings, \
        TreasuryStock, \
        OtherEquity, \
        TotalEquity, \
        TotalLiabilitiesAndShareholdersEquity, \
        SharesOuts, \
        TotalCommonSharesOutstanding in (from_session.query(old_bs_table.c._Symbol,
                                                            old_bs_table.c._Date,
                                                            old_bs_table.c._CashAndEquivalents,
                                                            old_bs_table.c._ShortTermInvestments,
                                                            old_bs_table.c._CashAndShortTermInvestments,
                                                            old_bs_table.c._AccountsReceivableTrade,
                                                            old_bs_table.c._ReceivablesOther,
                                                            old_bs_table.c._TotalReceivablesNet,
                                                            old_bs_table.c._TotalInventory,
                                                            old_bs_table.c._PrepaidExpenses,
                                                            old_bs_table.c._OtherCurrentAssetsTotal,
                                                            old_bs_table.c._TotalCurrentAssets,
                                                            old_bs_table.c._PPE,
                                                            old_bs_table.c._Goodwill,
                                                            old_bs_table.c._Intangibles,
                                                            old_bs_table.c._LongTermInvestments,
                                                            old_bs_table.c._OtherLongTermAssets,
                                                            old_bs_table.c._TotalAssets,
                                                            old_bs_table.c._AccountsPayable,
                                                            old_bs_table.c._AccruedExpenses,
                                                            old_bs_table.c._NotesPayable,
                                                            old_bs_table.c._CurrentPortLTDebtToCapital,
                                                            old_bs_table.c._OtherCurrentLiabilities,
                                                            old_bs_table.c._TotalCurrentLiabilities,
                                                            old_bs_table.c._LongTermDebt,
                                                            old_bs_table.c._CapitalLeaseObligations,
                                                            old_bs_table.c._TotalLongTermDebt,
                                                            old_bs_table.c._TotalDebt,
                                                            old_bs_table.c._DeferredIncomeTax,
                                                            old_bs_table.c._MinorityInterest_Bal,
                                                            old_bs_table.c._OtherLiabilities,
                                                            old_bs_table.c._TotalLiabilities,
                                                            old_bs_table.c._RedeemablePreferredStock,
                                                            old_bs_table.c._PreferredStockNonRedeemable,
                                                            old_bs_table.c._CommonStock,
                                                            old_bs_table.c._AdditionalPaidInCapital,
                                                            old_bs_table.c._RetainedEarnings,
                                                            old_bs_table.c._TreasuryStock,
                                                            old_bs_table.c._OtherEquity,
                                                            old_bs_table.c._TotalEquity,
                                                            old_bs_table.c._TotalLiabilitiesAndShareholdersEquity,
                                                            old_bs_table.c._SharesOuts,
                                                            old_bs_table.c._TotalCommonSharesOutstanding).order_by(old_bs_table.c._Symbol)
                                                                                                         .order_by(old_bs_table.c._Date)
                                                                                                         .filter(old_bs_table.c._Symbol==unicode(symbol))):
        additions.append(BalanceSheet.BalanceSheet(Symbol,
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
                                                   BalanceSheet.Annual.Enumeration))
    
    to_session.add_all(additions)
    to_session.commit()

for stock in symbols:
    transfer_symbol(unicode(stock))

from_session.close()
to_session.close()