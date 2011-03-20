""" This module configures financials for quarterly access. """

from Bloomberg import Quarterly
from BalanceSheet import BalanceSheet
from IncomeStatement import IncomeStatement
from CashFlowStatement import CashFlowStatement
from Derived import Derived

BalanceSheet = Quarterly(BalanceSheet)
CashFlowStatement = Quarterly(CashFlowStatement)
IncomeStatement = Quarterly(IncomeStatement)
Derived = Quarterly(Derived)