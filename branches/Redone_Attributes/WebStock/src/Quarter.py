""" This module configures financials for quarterly access. """

from Bloomberg import Quarterly
from BalanceSheet import BalanceSheet
from IncomeStatement import IncomeStatement
from CashFlowStatement import CashFlowStatement

BalanceSheet = Quarterly(BalanceSheet)
CashFlowStatement = Quarterly(CashFlowStatement)
IncomeStatement = Quarterly(IncomeStatement)