from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float, Column, Unicode
from sqlalchemy import Date as sql_date

Base = declarative_base()
class HistoricalPrices(Base):
    __tablename__ = 'dailyprices'

    Symbol = Column(Unicode(10), primary_key=True)
    Date = Column(sql_date, primary_key=True)
    High = Column(Float)
    Low = Column(Float)
    Open = Column(Float)
    Close = Column(Float)
    Volume = Column(Float)
    
    PreviousBalanceSheetIssueDate = Column(sql_date)
    NextBalanceSheetIssueDate = Column(sql_date)
    PreviousIncomeStatementIssueDate = Column(sql_date)
    NextIncomeStatementIssueDate = Column(sql_date)
    PreviousCashFlowStatementIssueDate = Column(sql_date)
    NextCashFlowStatementIssueDate = Column(sql_date)

    def __init__(self, symbol, date, high, low, open, close, volume):
        self.Symbol = symbol
        self.Date = date
        self.High = high
        self.Low = low
        self.Open = open
        self.Close = close
        self.Volume = volume
         

    def __repr__(self):
        return ("<PriceEntry (\n\tName: '%s',\n\tDate:'%s',\n\tHigh:'%f',\n\tLow:'%f',\n\tOpen:'%f',\n\tClose:'%f',\n\tVolume:'%f'\n)\n>" %
               (self.Symbol, str(self.Date), self.High, self.Low, self.Open, self.Close, self.Volume))
        
