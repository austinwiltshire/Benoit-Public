from SECFiling import Field, Float


""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """

class BalanceSheet(object):
	""" Balance sheet contains ... well, balance sheet information.  There are two types, Quarterly and Annual, and this is just a 
	semantic reference """
	CashAndEquivalents = Field(Float(precision=4))