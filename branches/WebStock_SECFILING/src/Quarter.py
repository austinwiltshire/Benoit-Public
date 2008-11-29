from SECFiling import Quarterly
from BalanceSheet import BalanceSheet
from IncomeStatement import IncomeStatement
from CashFlowStatement import CashFlowStatement
from utilities import ClassAccess
from functools import partial

#BalanceSheet = Quarterly(BalanceSheet)
#CashFlowStatement = Quarterly(CashFlowStatement)
#IncomeStatement = Quarterly(IncomeStatement)

class Meta(object):
	BalanceSheet = partial(ClassAccess, BalanceSheet)
	CashFlowStatement = partial(ClassAccess, CashFlowStatement)
	IncomeStatement = partial(ClassAccess, IncomeStatement)