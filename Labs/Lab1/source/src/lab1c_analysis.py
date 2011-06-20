#bring in database stuff
import sqlalchemy
import sqlalchemy.orm
import numpy, scipy, pylab
from scipy import stats

MEMORY_ENGINE = sqlalchemy.create_engine("sqlite://" \
                                  "" \
                                  "" \
                                  "" \
                                  "/lab1_results.db",
                                  echo = True)

MEMORY_SESSION = sqlalchemy.orm.sessionmaker(MEMORY_ENGINE)()

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Float, Column, Unicode
from sqlalchemy import Date as sql_date

Base = declarative_base()

class Result(Base):
    __tablename__ = 'results'

    Symbol = Column(Unicode(10), primary_key=True)
    PivotDate = Column(sql_date, primary_key=True)
    RetrospectiveDate = Column(sql_date)
    ProspectiveDate = Column(sql_date)
    RetrospectiveFreeCashFlowGrowth = Column(Float)
    ProspectiveTotalReturn = Column(Float)
    
    def __init__(self, symbol, pivot, retro, prospect, fcf_growth, total_return):
      
        self.Symbol = symbol
        self.PivotDate = pivot
        self.RetrospectiveDate = retro
        self.ProspectiveDate = prospect
        self.RetrospectiveFreeCashFlowGrowth = fcf_growth
        self.ProspectiveTotalReturn = total_return
        
    def __repr__(self):

        return ("<Lab1 Result (\n\tName: '%s',\n\tPivotDate:'%s',\n\tFree Cash Flow Growth:'%s'\n\tTotal Return:'%s'\n)\n>" %
                (self.Symbol, str(self.PivotDate), self.RetrospectiveFreeCashFlowGrowth, self.ProspectiveTotalReturn))
    
    
print MEMORY_SESSION.query(Result).all()
        
x,y = zip(*[(r[0], r[1]) for r in MEMORY_SESSION.query(Result.ProspectiveTotalReturn, Result.RetrospectiveFreeCashFlowGrowth)]) 

class DescriptiveStats(object):
    def __init__(self, x_name, x_var, y_name, y_var):
        self.x_var = x_var
        self.x_var_name = x_name
        self.y_var = y_var
        self.y_var_name = y_name
        self.slope, self.intercept, self.r_val, self.p_val, self.error = stats.linregress(x_var, y_var)
        
    def __repr__(self):
        return ("Number of measurements: %(num_measurements)d\n" 
                "Mean of %(x_name)s: %(mean_x)f\n"
                "Max of %(x_name)s: %(max_x)f\n"
                "Min of %(x_name)s: %(min_x)f\n"
                "Stddev of %(x_name)s: %(stddev_x)f\n"
                "Mean of %(y_name)s: %(mean_y)f\n"
                "Max of %(y_name)s: %(max_y)f\n"
                "Min of %(y_name)s: %(min_y)f\n"
                "Stddev of %(y_name)s: %(stddev_y)f\n"
                "Linear regression: %(y_name)s = B0 + B1(%(x_name)s) + u\n"
                "B0 = %(intercept)f\n"
                "B1 = %(slope)f\n"
                "r = %(r_val)f\n"
                "Probability B1 != 0: %(p_val)f\n"
                "Error in model is %(error)f" 
                                             % {"num_measurements": len(self.x_var),
                                                "x_name": self.x_var_name,
                                                "y_name" : self.y_var_name,
                                                "mean_x" : scipy.mean(self.x_var),
                                                "mean_y" : scipy.mean(self.y_var),
                                                "stddev_x" : scipy.std(self.x_var),
                                                "stddev_y" : scipy.std(self.y_var),
                                                "min_x" : min(self.x_var),
                                                "min_y" : min(self.y_var),
                                                "max_x" : max(self.x_var),
                                                "max_y" : max(self.y_var),
                                                "intercept" : self.intercept,
                                                "slope" : self.slope,
                                                "r_val" : self.r_val,
                                                "p_val" : self.p_val,
                                                "error" : self.error })
               
              

def LinearRegression(x,y):
    polycoeffs = scipy.polyfit(x, y, 1)
    yfit = scipy.polyval(polycoeffs, x)
    pylab.plot(x, yfit, 'r-')
    pylab.plot(x, y, 'b+')
    pylab.legend(['Regression', 'Data Points'])
    slope, intercept, r, p, err = stats.linregress(x, y)
    pylab.ylabel("Retrospective Free Cash Flow Growth")
    pylab.xlabel("Prospective Total Return")
    pylab.title("Slope %2.2f, Intercept %2.2f, R-value %2.3f P-Val %2.3f, Stderr %2.4f" % (slope, intercept, r, p, err))
    pylab.show()
    return scipy.mean(x), scipy.mean(y), scipy.std(x), scipy.std(y), max(x), min(x), max(y), min(y), len(x)

print DescriptiveStats("Retrospective Free Cash Flow Growth", x, "Prospective Total Return", y)
#print LinearRegression(x, y)