from SECFiling import SECFiling, Annual, Quarterly, Field, Float

#TODO:
# run test that uniqueness is enforced

""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """

class IncomeStatement(SECFiling):
	Revenue = Field(Float(precision=4))

AnnualIncomeStatement = SECFiling("AnnualIncomeStatement",IncomeStatement, Annual)
QuarterlyIncomeStatement = SECFiling("QuarterlyIncomeStatement",IncomeStatement, Quarterly)