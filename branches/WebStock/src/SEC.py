#import stuff needed to register SEC stuff
import Website #for sec data from google
import Yahoo #for price data from yahoo
import Ratios #for fundamentals
import Registry

#import ORM stuff
import Quarter
import Annual
import Daily
import TradingDay
import Metadata
import Fundamentals

#setup ORM
from elixir import metadata, setup_all

metadata.bind = "sqlite:///SEC.sqlite"
metadata.bind.echo = False #used to debug SQL statements

setup_all(True)