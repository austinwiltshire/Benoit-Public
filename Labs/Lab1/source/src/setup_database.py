from table import Prices

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine("mysql://austinwiltshire@richie:3306/bloomberg_v2")

Session = sessionmaker(engine)
session = Session()
