from Analysis import DescriptiveStats, LinearRegression
from result import MEMORY_SESSION, Result
import itertools 

results = DescriptiveStats("Prospective Total Return", "Retrospective Free Cash Flow Growth")
linreg = LinearRegression("Prospective Total Return", "Retrospective Free Cash Flow Growth")
r1,r2 = itertools.tee(MEMORY_SESSION.query(Result.ProspectiveTotalReturn, Result.RetrospectiveFreeCashFlowGrowth))
results.load_measurements(r1)
linreg.load_measurements(r2)               
print results
linreg.plot()
