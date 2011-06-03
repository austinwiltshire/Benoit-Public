from financials import IncomeStatement, Annual

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

old_is_table = metadata.tables['annualincomestatement']

symbols = SnP500.symbols

def transfer_symbol(symbol):

    print "Transferring %s" % symbol
    additions = []
    
    for IS in (from_session.query(old_is_table)
                           .order_by(old_is_table.c._Symbol)
                           .order_by(old_is_table.c._Date)
                           .filter(old_is_table.c._Symbol==unicode(symbol))):

        additions.append(IncomeStatement(IS._Symbol, 
                                         IS._Date,
                                         IS._Revenue,                
                                         IS._OtherRevenue,
                                         IS._TotalRevenue,
                                         IS._CostOfRevenue,
                                         IS._GrossProfit,
                                         IS._SGAExpenses,
                                         IS._ResearchAndDevelopment,
                                         IS._DepreciationAmortization,
                                         IS._InterestNetOperating,
                                         IS._UnusualExpense,
                                         IS._OtherOperatingExpenses,
                                         IS._TotalOperatingExpense,
                                         IS._OperatingIncome,
                                         IS._InterestIncome,
                                         IS._GainOnSaleOfAssets,
                                         IS._OtherNet,
                                         IS._IncomeBeforeTax,
                                         IS._IncomeAfterTax,
                                         IS._MinorityInterest_Inc,
                                         IS._EquityInAffiliates,
                                         IS._NetIncomeBeforeExtraItems,
                                         IS._AccountingChange,
                                         IS._DiscontinuedOperations,
                                         IS._ExtraordinaryItem,
                                         IS._NetIncome,
                                         IS._PreferredDividends,
                                         IS._IncomeAvailToCommonExclExtraItems,
                                         IS._IncomeAvailToCommonInclExtraItems,
                                         IS._BasicWeightedAverageShares,
                                         IS._BasicEPSExclExtraItems,
                                         IS._BasicEPSInclExtraItems,
                                         IS._DilutionAdjustment,
                                         IS._DilutedWeightedAverageShares,
                                         IS._DilutedEPSExclExtraItems,
                                         IS._DilutedEPSInclExtraItems,
                                         IS._DividendsPerShare,
                                         IS._GrossDividends,
                                         IS._NetIncomeAfterCompExp,
                                         IS._BasicEPSAfterCompExp,
                                         IS._DilutedEPSAfterCompExp,
                                         IS._DepreciationSupplemental,
                                         IS._TotalSpecialItems,
                                         IS._NormalizedIncomeBeforeTaxes,
                                         IS._EffectsOfSpecialItemsOnIncomeTaxes,
                                         IS._IncomeTaxesExSpecialItems,
                                         IS._NormalizedIncomeAfterTaxes,
                                         IS._NormalizedIncomeAvailableCommon,
                                         IS._BasicNormalizedEPS,
                                         IS._DilutedNormalizedEPS,
                                         Annual.Enumeration))
    
    to_session.add_all(additions)
    to_session.commit()

for stock in symbols:
    transfer_symbol(unicode(stock))

from_session.close()
to_session.close()