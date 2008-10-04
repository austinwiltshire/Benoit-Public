from SECFiling import SECFiling, Annual, Quarterly, Field, Float


""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """



class CashFlowStatement(SECFiling):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	NetIncomeStartingLine = Field(Float(precision=4))

QuarterlyCashFlowStatement = SECFiling("QuarterlyCashFlowStatement",CashFlowStatement, Quarterly)
AnnualCashFlowStatement = SECFiling("AnnualCashFlowStatement",CashFlowStatement, Annual)