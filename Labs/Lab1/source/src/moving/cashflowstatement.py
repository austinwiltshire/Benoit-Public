from financials import CashFlowStatement, Annual

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

old_cfs_table = metadata.tables['annualcashflowstatement']

symbols = SnP500.symbols

def transfer_symbol(symbol):

    print "Transferring %s" % symbol
    additions = []
    
    for Symbol, \
        Date, \
        NetIncomeStartingLine, \
        DepreciationDepletion, \
        Amortization, \
        DeferredTaxes, \
        NonCashItems, \
        ChangesInWorkingCapital, \
        CashFromOperatingActivities, \
        CapitalExpenditures, \
        OtherInvestingCashFlow, \
        CashFromInvestingActivities, \
        FinancingCashFlowItems, \
        TotalCashDividendsPaid, \
        IssuanceOfStock, \
        IssuanceOfDebt, \
        CashFromFinancingActivities, \
        ForeignExchangeEffects, \
        NetChangeInCash, \
        CashInterestPaid, \
        CashTaxesPaid in (from_session.query(old_cfs_table.c._Symbol, 
                                             old_cfs_table.c._Date,
                                             old_cfs_table.c._NetIncomeStartingLine,
                                             old_cfs_table.c._DepreciationDepletion,
                                             old_cfs_table.c._Amortization,
                                             old_cfs_table.c._DeferredTaxes,
                                             old_cfs_table.c._NonCashItems,
                                             old_cfs_table.c._ChangesInWorkingCapital,
                                             old_cfs_table.c._CashFromOperatingActivities,
                                             old_cfs_table.c._CapitalExpenditures,
                                             old_cfs_table.c._OtherInvestingCashFlow,
                                             old_cfs_table.c._CashFromInvestingActivities,
                                             old_cfs_table.c._FinancingCashFlowItems,
                                             old_cfs_table.c._TotalCashDividendsPaid,
                                             old_cfs_table.c._IssuanceOfStock,
                                             old_cfs_table.c._IssuanceOfDebt,
                                             old_cfs_table.c._CashFromFinancingActivities,
                                             old_cfs_table.c._ForeignExchangeEffects,
                                             old_cfs_table.c._NetChangeInCash,
                                             old_cfs_table.c._CashInterestPaid,
                                             old_cfs_table.c._CashTaxesPaid).order_by(old_cfs_table.c._Symbol)
                                                                            .order_by(old_cfs_table.c._Date)
                                                                            .filter(old_cfs_table.c._Symbol==unicode(symbol))):
        additions.append(CashFlowStatement(Symbol, 
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
                                           Annual.Enumeration))
    
    to_session.add_all(additions)
    to_session.commit()

for stock in symbols:
    transfer_symbol(unicode(stock))

from_session.close()
to_session.close()