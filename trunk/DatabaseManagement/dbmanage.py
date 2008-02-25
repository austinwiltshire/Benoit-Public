import datetime, sql, fundie, time, httplib, os

logOpen = False
log = None

def markTime():
	timeLog = file(r"c:\service\time.log", "a")
	Now = time.strftime("%c")
	Now += "\n"
	timeLog.write(Now)
	timeLog.close()
	del timeLog
	#open time log, mark the time, close time log

def checkTime(forceUpdate = False):
	if(not os.access(r"c:\service\time.log", os.F_OK)):
		markTime()
		forceUpdate = True
	
	timeLog = file(r"c:\service\time.log", "r")
	Now = time.localtime()

	allDates = timeLog.readlines()
#	print allDates
	lastDate = allDates[-1]
	lastDate = lastDate.rstrip("\n")

	lastDate = time.strptime(lastDate, "%c")

	print lastDate, Now

	if((Now[6] == 6 or Now[6] == 0) and not forceUpdate): #don't update sunday or monday mornings
		return False;

	if(lastDate[2] != Now[2] or forceUpdate): #different days, I haven't updated yet today
		if(Now[3] > 3 or forceUpdate): #update only after 3 am.
			return True
		else:
			return False
	print "havent gotten anything"
	
	#open time log, retrieve the last time, close the time log
	#compares this time with now, returns true if an update is needed
	#false if it is not

def markInvalids(symbols):
	print symbols
	invalidLog = file(r"c:\service\invalid.log", "a")
	for symbol in symbols:
		invalidLog.write(symbol + "\n")
	invalidLog.close()


def openLog():
	globals()['logOpen'] = True
	Now = time.localtime()
	logName =  str(Now[1]) + "_" + str(Now[2]) + "_" + str(Now[0]) + ".log"
	globals()['log'] = file(r"c:\service\\" + logName, "w")
	#opens the log file

def markLog(text):
	if(globals()['logOpen']):
		globals()['log'].write(text + "\n")
	else:
		pass
		#throw an exception here
	#marks the log file with 'text'

def closeLog():
	if(globals()['logOpen']):
		globals()['logOpen'] = False
		globals()['log'].close()
	#closes the log file

while(True):
#def test(start=None):
	#check time
	lastSymbol = None
	timecheck = checkTime(True)
	if(timecheck): #its time to update
#	if(True):
	#TODO: figure out why i can't connect to the SQL database when i run 
	#this as a service
#		print "Updating"
		markTime() #mark this update time
		openLog() #open the log to record results
		#open new log
		#open new connection to the database

		try:
			db = sql.stockDB()
			notes, invalids = db.updateAllDatabase(lastSymbol)
			db.close()
		except sql.SQLUpdateError, e:
			markLog("SQLUpdateError: " + str(e))
			closeLog()
			break
		except fundie.WebAccessError, e:
			print "Lost connection to the net at " + e.symbol
			markLog("WebAccessError: " + str(e))
			closeLog()
			lastSymbol = e.symbol
			break
		except fundie.WebDataError, e:
			markLog("WebDataError: " + str(e))
			closeLog()
			lastSymbol = e.symbol
			break
		else:
			markLog("Notes: " + repr(notes))
			markInvalids(invalids)
			closeLog()
			lastSymbol = None
			break
		#retrieve symbol table
		#for each symbol
			#update the fundamentals for this stock
			#update prices for this stock
		#run update functions on the database
			#200 day avg, etc.
		#close log
	else:
		time.sleep(1800)
	#if it is not time to update
		#sleep for 30 minutes
