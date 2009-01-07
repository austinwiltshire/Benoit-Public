""" Annual is apart of our general abuse of the module system.  It provides versions of financial documents that are specialized to hold and access annual 
information. """

from SECFiling import MakePeriodical 
from BalanceSheet import BalanceSheet
from IncomeStatement import IncomeStatement
from CashFlowStatement import CashFlowStatement

Annual = MakePeriodical("Annual")

BalanceSheet = Annual(BalanceSheet)
CashFlowStatement = Annual(CashFlowStatement)
IncomeStatement = Annual(IncomeStatement)
