import Market
from datetime import datetime

IRBT = Market.Symbol("IRBT")
qtr = IRBT.Quarter(datetime(2007,9,29))
bs = qtr.BalanceSheet
print bs.CashAndEquivalents
