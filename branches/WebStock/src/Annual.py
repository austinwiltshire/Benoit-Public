from SECFiling import Annual 
from BalanceSheet import BalanceSheet
from IncomeStatement import IncomeStatement
from CashFlowStatement import CashFlowStatement

BalanceSheet = Annual(BalanceSheet)
CashFlowStatement = Annual(CashFlowStatement)
IncomeStatement = Annual(IncomeStatement)