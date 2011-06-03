
#    db.query(Prices.NextIncomeStatement).filter(Prices.Symbol="IRBT").order_by(Prices.Date)

from financials import BalanceSheet as BS
from basics import HistoricalPrices as Prices
from bloomberg import SESSION as DB

class BalanceSheetDateFinder(object):
    """
    Takes a collection of balance sheets and offers two services on them - for any particular date, finding the
    next and previous balance sheet issue.
    """
    
    def __init__(self, balance_sheets):
        """
        Assumes balance sheets are in order by date
        """
        
        bs_dates = [bs.Date for bs in balance_sheets]
        assert sorted(bs_dates) == bs_dates
        
        self._balance_sheets = balance_sheets
        
    def get_next_bs_for(self, date):
        """
        Given a date, finds the bs issued after that, or None if it doesn't exist.
        If the bs's date is the same as date, returns that bs.
        """
        
        #date is before the first balance sheet
        if date <= self._balance_sheets[0].Date:
            return self._balance_sheets[0]
        
        #date is after the last balance sheet
        if date > self._balance_sheets[-1].Date:
            return None
        
        date_spans = zip(self._balance_sheets[:-1], self._balance_sheets[1:])
        
        for bs_span in date_spans:
            if bs_span[0].Date < date <= bs_span[1].Date:
                return bs_span[1]
        
    def get_prev_bs_for(self, date):
        """
        given a date, finds the bs issued *before* that, or None if it doesn't exist.
        If the bs's date is the same as date, returns that bs.
        """
        
        #date is before the first balance sheet
        if date < self._balance_sheets[0].Date:
            return None
        
        #date is after the last balance sheet
        if date >= self._balance_sheets[-1].Date:
            return self._balance_sheets[-1]
        
        date_spans = zip(self._balance_sheets[:-1], self._balance_sheets[1:])
        
        for bs_span in date_spans:
            if bs_span[0].Date <= date < bs_span[1].Date:
                return bs_span[0]

import SnP500
ALL_SYMBOLS = [unicode(s) for s in SnP500.symbols]

#ALL_SYMBOLS = [u'SBUX', u'IBM', u'AMZN', u'BAC', u'DELL', u'LMT']

def main():
    """
    Executes script.
    """
    
    print "Starting"
    
    for symbol in ALL_SYMBOLS:
        print "On %s" % symbol
        
        balance_sheets = (DB.query(BS)
                            .filter(BS.Symbol==symbol)
                            .order_by(BS.Date)
                            .all())
        
        finder = BalanceSheetDateFinder(balance_sheets)
        
        prices = (DB.query(Prices)
                    .filter(Prices.Symbol==symbol)
                    .order_by(Prices.Date)
                    .all())
        
        iteration = 0
        
        for price in prices:
            prev = finder.get_prev_bs_for(price.Date)
            next = finder.get_next_bs_for(price.Date)
#            
#            if prev and price.Date == prev.Date:
#                print prev.Date, price.Date, price.Symbol
#                if next:
#                    print next.Date
#                    
#            if next and price.Date == next.Date:
#                print next.Date, price.Date, price.Symbol
#                if prev:
#                    print prev.Date
#            
#            if prev and next and prev.Date == next.Date:
#                print next.Date, price.Date, price.Symbol, next.Date
            
            
#            if iteration % 1000 == 0:
#                print "Price date:"
#                print price.Date
        
            
            if prev:
                price.PreviousBalanceSheetIssueDate = prev.Date
                price.PreviousCashFlowStatementIssueDate = prev.ConcurrentCashFlowStatementIssueDate
                price.PreviousIncomeStatementIssueDate = prev.ConcurrentIncomeStatementIssueDate
                
                
                
#                if iteration % 1000 == 0:
#                    
#                    print "Previous dates:"
#                    print x
#                    print y
#                    print z
                
            if next:
                price.NextBalanceSheetIssueDate = next.Date
                price.NextCashFlowStatementIssueDate = next.ConcurrentCashFlowStatementIssueDate
                price.NextIncomeStatementIssueDate = next.ConcurrentIncomeStatementIssueDate
                
#                if iteration % 1000 == 0:
#                
#                    print "Next dates:"
#                    print x
#                    print y
#                    print z
            
            if iteration % 1000 == 0:
                DB.commit()
            
            iteration += 1
            
            
if __name__ == "__main__":
    main()
    
    #TODO:
    #load the balance sheets brought in above into the balance sheet finder object thing
    #then just iterate through all the prices for each symbol and find the appropriate next and prev
    #balance shseet.  find the next and prev inc and cfs by getting the 'current' inc and cfs for each balance
    #sheet found.  remember that not all prices will have a next and prev so check for none