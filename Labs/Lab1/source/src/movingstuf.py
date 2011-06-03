import table

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData
import SnP500

to_engine = create_engine("mysql://austinwiltshire@richie:3306/bloomberg_v2")
from_engine = create_engine("mysql://austinwiltshire@richie:3306/bloomberg_test")

ToSession = sessionmaker(to_engine)
to_session = ToSession()

FromSession = sessionmaker(from_engine)
from_session = FromSession()

metadata = MetaData(bind=from_engine,reflect=True)

old_price_table = metadata.tables['dailyprices']

symbols = SnP500.symbols

def transfer_symbol(symbol):

	print "Transferring %s" % symbol
	additions = []
	for date, high, low, open, close, volume in (from_session.query(old_price_table.c._Date,
																	old_price_table.c._High,
													 			    old_price_table.c._Low,
																	old_price_table.c._Open,
																	old_price_table.c._Close,
																	old_price_table.c._Volume).order_by(old_price_table.c._Symbol)
																    	                      .order_by(old_price_table.c._Date)
	   	   	   	   	   	   	   	   	   	   	   	   	   	   	   	   	        	   	   	   	  .filter(old_price_table.c._Symbol==unicode(symbol))):
		additions.append(table.Prices(symbol, date, high, low, open, close, volume))
	
	to_session.add_all(additions)
	to_session.commit()

for symbol in symbols:
	transfer_symbol(unicode(symbol))

from_session.close()
to_session.close()