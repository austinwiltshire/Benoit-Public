#import stuff needed to register SEC stuff
import Website #for sec data from google
import Yahoo #for price data from yahoo
import Ratios #for fundamentals
import Registry
import sqlalchemy.orm


#import ORM stuff
from Financials import FinancialPeriod
import Quarter
import Annual
import Daily
#import TradingDay
from Metadata import Metadata
#import Fundamentals

#setup ORM
#from elixir import metadata, setup_all, session
import elixir

elixir.metadata.bind = "sqlite:///SEC.sqlite"
elixir.metadata.bind.echo = True #used to debug SQL statements
#elixir.session = sqlalchemy.orm.scoped_session(sqlalchemy.orm.create_session(transactional=False, autoflush=True))

elixir.setup_all(True)