import Module2
import EmailLogger
import logging
import datetime
import Database
import time
import traceback
import sys

Database.Remote()

import SnP500
symbols = []
symbols+= SnP500.symbols

log = logging.getLogger("main")
log.setLevel(logging.INFO)
eml = EmailLogger.EmailLogger("Bloomberg Update Log")
handler = logging.StreamHandler(eml)
handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s -> %(levelname)s POSTED: %(message)s'))
log.addHandler(handler)

numErrors = 0
numStocks = 0

log.info("Begining download of new data for date %s" % str(datetime.date.today()))
log.info("Begining download for S&P 500 data.")

#notes:
#it'd be nice if i could use a context on the email, logger or find out if 'shutdown' is always automatically called.  then i can put the email finalize in there.
#it'd be nice if i could start a new transaction per prefetch, such that the exception handler can roll back anything.
#it'd be nice if i set the logger i have there as the base logger, so if i want to log somewhere else it will be included in the email
#i need to improve the formatting of the logging as per the example too.

symbols = list(set(symbols))

timePerStock = 0
time.clock()

for symbol in symbols:
	try:
		print symbol, "(", numStocks+1, "of", len(symbols), ")",
		print "%.2f%s done" % (((float(numStocks+1) / float(len(symbols)))*100.00), "%"), 
		numStocks += 1
		Module2.Symbol(unicode(symbol)).prefetch(True)
		curTime = time.clock()
		timePerStock = curTime / numStocks
		timeRemaining = timePerStock * (len(symbols) - numStocks)
		print "est. %.2f minutes remaining." % (timeRemaining / 60)
	except Exception, e:
		print e
		log.error("On symbol %s" % symbol)
		log.error("Discovered error: %s : %s" % (str(type(e)), str(e)))
		log.error("Traceback:")
		log.error("******************************************************************")
		traceback.print_tb(sys.exc_info()[2], file=eml)
		log.error("******************************************************************")
		numErrors += 1
		continue
	
if numErrors > 0:
	log.error("Found %d errors" % numErrors)
else:
	log.info("No errors found.")
log.info("Downloaded information pertaining to %d stocks." % numStocks)
log.info("Download took %s minutes" % (str(time.clock() / 60)))
log.info("Ending download of new data.")
eml.finalize()

print "Total time spent updating ", (time.clock() / 60)