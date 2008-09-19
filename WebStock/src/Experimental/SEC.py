#import stuff needed to register SEC stuff
import Google
import Registry

#import ORM stuff
import BalanceSheet
import IncomeStatement

#setup ORM
from elixir import metadata, setup_all

metadata.bind = "sqlite:///SEC.sqlite"
metadata.bind.echo = True

setup_all(True)