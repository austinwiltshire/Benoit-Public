from SECFiling import Annual 
from BalanceSheet import BalanceSheet
from IncomeStatement import IncomeStatement
from CashFlowStatement import CashFlowStatement
from utilities import ClassAccess

BalanceSheet = Annual(BalanceSheet)
CashFlowStatement = Annual(CashFlowStatement)
IncomeStatement = Annual(IncomeStatement)

class Meta(object):
	BalanceSheet = ClassAccess(BalanceSheet)
	CashFlowStatement = ClassAccess(CashFlowStatement)
	IncomeStatement = ClassAccess(IncomeStatement)