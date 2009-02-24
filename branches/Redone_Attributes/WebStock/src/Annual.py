""" Annual is apart of our general abuse of the module system.  It provides versions of financial documents that are specialized to hold and access annual 
information. """

#from SECFiling import BAnnual
from Bloomberg import Annual 
from BalanceSheet import BalanceSheet
from IncomeStatement import IncomeStatement
from CashFlowStatement import CashFlowStatement

BalanceSheet = Annual(BalanceSheet)
CashFlowStatement = Annual(CashFlowStatement)
IncomeStatement = Annual(IncomeStatement)
