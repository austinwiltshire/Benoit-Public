"""
Can retrospective free cash flow growth predict prospective total return?
"""

#bring in database stuff
import sqlalchemy
import sqlalchemy.orm

MEMORY_ENGINE = sqlalchemy.create_engine("sqlite://" \
                                  "" \
                                  "" \
                                  "" \
                                  "/:memory:",
                                  echo = True)

MEMORY_SESSION = sqlalchemy.orm.sessionmaker(MEMORY_ENGINE)()

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float, Column, Unicode
from sqlalchemy import Date as sql_date
from sqlalchemy.orm import aliased

Base = declarative_base()


#generate table of free cash flow growth with begin date, end date, symbol and value
class FreeCashFlowGrowth(Base):
    __tablename__ = 'freecashflow'

    Symbol = Column(Unicode(10), primary_key=True)
    EndDate = Column(sql_date, primary_key=True)
    BeginDate = Column(sql_date)
    Growth = Column(Float)
    
    def __init__(self, symbol, begin, end, growth):
        
        
        self.Symbol = symbol
        self.EndDate = end
        self.BeginDate = begin
        self.Growth = growth
        
        if not isinstance(self.Growth, float):
            print self.Growth 
        
    def __repr__(self):

        return ("<FreeCashFlowGrowth (\n\tName: '%s',\n\tStartDate:'%s',\n\tEndDate:'%s',\n\tGrowth:'%s'\n)\n>" %
                (self.Symbol, str(self.BeginDate), str(self.EndDate), str(self.Growth)))
    
FreeCashFlowGrowth.metadata.create_all(MEMORY_ENGINE)

print "Created table"

import basics
import financials
from bloomberg import SESSION

#run the below against the database to ensure i don't get crap!
previous_cfs = aliased(financials.CashFlowStatement)
current_cfs = financials.CashFlowStatement

def free_cash_flow(cash_flow_statement):
    #capex is negative
    
    return cash_flow_statement.CashFromOperatingActivities + cash_flow_statement.CapitalExpenditures

results = [FreeCashFlowGrowth(*row) for row in SESSION.query(current_cfs.Symbol,
                         previous_cfs.Date,
                         current_cfs.Date,
                         (free_cash_flow(current_cfs) - free_cash_flow(previous_cfs)) / 
                          free_cash_flow(previous_cfs)) \
                  .filter(current_cfs.Symbol == previous_cfs.Symbol) \
                  .filter(current_cfs.PreviousIssueDate == previous_cfs.Date)
                  .filter(current_cfs.CapitalExpenditures != None)
                  .filter(previous_cfs.CapitalExpenditures != None)]

MEMORY_SESSION.add_all(results)
MEMORY_SESSION.commit()

current_bs = financials.BalanceSheet
next_bs = aliased(financials.BalanceSheet)
next_cfs = aliased(financials.CashFlowStatement)

def average_common_shares(current, next):
    return (current.TotalCommonSharesOutstanding + next.TotalCommonSharesOutstanding) / 2

#for dividend paying stocks
results_with_dividends = [row for row in SESSION.query(current_bs.Symbol,
                                        current_bs.Date,
                                        next_bs.Date,
                                        current_bs.TotalCommonSharesOutstanding,
                                        next_bs.TotalCommonSharesOutstanding,
                                        next_cfs.TotalCashDividendsPaid / average_common_shares(current_bs, next_bs)) #average dividends for the period
                                 .filter(current_bs.Symbol == next_bs.Symbol)
                                 .filter(current_bs.NextIssueDate == next_bs.Date)
                                 .filter(next_bs.Date == next_cfs.Date)
                                 .filter(current_bs.Symbol == next_cfs.Symbol)
                                 .filter(next_cfs.TotalCashDividendsPaid != None)]

results_without_dividends = [row for row in SESSION.query(current_bs.Symbol,
                                        current_bs.Date,
                                        next_bs.Date,
                                        current_bs.TotalCommonSharesOutstanding,
                                        next_bs.TotalCommonSharesOutstanding)
                                 .filter(current_bs.Symbol == next_bs.Symbol)
                                 .filter(current_bs.NextIssueDate == next_bs.Date)
                                 .filter(next_bs.Date == next_cfs.Date)
                                 .filter(current_bs.Symbol == next_cfs.Symbol)
                                 .filter(next_cfs.TotalCashDividendsPaid == None)]

print results_without_dividends


#generate all new tables as sqllite tables

#create a function that, given a date, returns market cap growth of a stock one year from that date (or throws exception if doesn't exist?)
#preferably inside the database
#create a function that, given a date, returns dividend yield for that stock one year from that date
#preferably inside the database
#create a function that adds those two
#preferably inside the database
#generate a table of total return with begin date, end date, symbol and total return
#generate table from join the two tables where fcf growth end date = total return begin date,
#run a regression  
