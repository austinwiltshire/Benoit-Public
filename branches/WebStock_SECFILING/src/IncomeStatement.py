from SECFiling import Field, Float

#TODO:
# run test that uniqueness is enforced

""" A Balance Sheet has a Symbol and a Date associated with it, as well as Balance Sheet information.  There are two types: Quarterly
and Annual Balance Sheets.  A Balance sheet can be represented as a row in a database. """

class IncomeStatement(object):
	Revenue = Field(Float(precision=4))
	UnusualExpense = Field(Float(precision=4))

#how might prefetch work?
#  given any SECFiling, a prefetch should first gather
# that filing's dates that are important, so i need a date service
# for each type of date - a meta would just have a 'once'
# daily would have all valid trading days - this i have a calender for, 
# but i also need ranges available from yahoo
# quarter would get quarterly dates from the web
# a\nnual would get annual dates for the web
# then a prefetch would go ahead and create an array of the SECfilings
# one for each date.
# well, there's really two kinds of prefetch, i'd need one that would 
# prefetch all the stuff for an SECFiling, this would probably be easy
# and another to find all available dates and build an array of them
# this prefetch doesn't need to be saved, just the act of getting things
# will commit it to the database.  

# a potential benefit might be having whether SECFiling/registry commits
# or not as a class variable inside, as either true or false.  usually
# it'd be true, but for prefetch it'd make sense to turn it off so things
# can pile up for commits.  i could commit manually.