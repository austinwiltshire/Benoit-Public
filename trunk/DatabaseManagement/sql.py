import MySQLdb, datetime, math, fundie, random, time

def normalize(toNormalize):
    arrayMax = max(toNormalize)
    arrayMin = min(toNormalize)
    arrayRange = arrayMax - arrayMin
    

    for i in range(len(toNormalize)):
         toNormalize[i] = (toNormalize[i] - arrayMin)/arrayRange
    return toNormalize

class DateOutOfIndex(Exception):
    pass

class SQLUpdateError(Exception):
	def __init__(self, args):
		self.args = args
	def __str__(self):
		return repr(self.args)

class InvalidSymbol(Exception):
	def __init__(self, args, symbol=None):
		self.args = args
		self.symbol = symbol
	def __str__(self):
		return repr(self.args)

class stockDB:

	def __init__(self):
		self.openConnection()

	def close(self):
		self.myConnection.close()
    
        def stockByRandomDates(self, symbol, number):
            "Returns an array of stocks size number from a random date"
            date = self.randomDate(symbol, 0, number)
            #print date
            return self.stockByDates(symbol, date, number)
    
        def randomDate(self, symbol, ldlim, rdlim):
            "Returns a random date out stock info of symbol from database"
#            dates = database['stocks'][symbol].keys()
#            dates.sort()
            allDates = self.getStockDates(symbol)
            pick = allDates[random.randint(ldlim, len(allDates)-(1+rdlim))]
            return pick

        def randomSymbolDate(self, ldlim, rdlim):
            stock = self.randomStock()
            date = self.randomDate(stock, ldlim, rdlim)
            return (stock, date)

        def randomStock(self):
            "Returns a random stock out of the database"
            pick = self.stockTable[random.randint(0, len(self.stockTable)-1)]
            return pick
        
        def stockByDates(self, symbol, date, length):
            
#    "Returns the stock info of symbol at date and then for length dates before it"
            toReturn = []
            allDates = self.getStockDates(symbol)
            if(date not in allDates):
                raise DateOutOfIndex()
            date = allDates.index(date)
            if(date + length > len(allDates)):
                raise DateOutOfIndex
#                print "Date is ", allDates[date]
 #               print "Price is out of datetable's index"
  #              return None
            for i in range(length):
 #               print allDates[date]
                toReturn.append(self.getNormalizedContinuousGain(symbol, allDates[date]))
#                toReturn.append(self.getGain(symbol, allDates[date]))
                date+=1
            return toReturn

    	def cleanup(self, arrayToClean):
		toReturn = []
		for element in arrayToClean:
			toReturn.append(element[0])
		for element in toReturn:
			if element == None:
				raise EntryNotFound("cant find a data entry");
		return toReturn

	def compareDates(self, availableDates, potentialNewDates):
		toReturn = []
		for date in potentialNewDates:
			if date not in availableDates:
				toReturn.append(date)
		return toReturn

	def getIndecies(self, newDates, webDates):
		"Represents dates to add as booleans in an array the same size, true for add and false for not."
		toReturn = []
		for date in webDates:
			toReturn.append((False, None));

		for date in newDates:
			toReturn[webDates.index(date)] = (True, date);

		return toReturn

	def updateAllDatabase(self, start=None):
		priceErrorList, priceInvalidList = self.updateAllPrices(start)
		fundamentalErrorList, fundamentalInvalidList = self.updateAllFundamentals(start)


		return fundamentalErrorList + priceErrorList, fundamentalInvalidList + priceInvalidList

	def updateAllFundamentals(self, symbolToStart=None):
		errorList = []
		invalidList = []
		if(symbolToStart == None):
			symbolToStart = self.stockTable[0]
		for symbol in self.stockTable[self.stockTable.index(symbolToStart):]:
			print "Updating financials for " + symbol
			loaded = False
			while(not loaded):
				try:
					self.updateFundamentals(symbol)
				except fundie.WebInfoNotFound, e:
					errorList.append("Can't find fundamentals for" + e.symbol)
					loaded = True
				except InvalidSymbol, e:
					invalidList.append(e.symbol)
					loaded = True
				except httplib.BadStatusLine, e:
#					print "Server disconnected..."
					time.sleep(15)
#					print "Trying again..."
					continue
				except fundie.WebAccessError, e:
#					print "Network connection lost... "
					print e
					time.sleep(15)
#					print "Trying again..."
					continue
				else:
					loaded = True
		return errorList, invalidList

	def updateAllPrices(self, symbolToStart=None):
		errorList = []
		invalidList = []
		if(symbolToStart == None):
			symbolToStart = self.stockTable[0]
		for symbol in self.stockTable[self.stockTable.index(symbolToStart):]:
			print "Updating prices for " + symbol
			loaded = False
			while(not loaded):
				try:
					self.updatePrices(symbol)
				except fundie.WebInfoNotFound, e:
					errorList.append(str(e))
					loaded = True
				except InvalidSymbol, e:
					invalidList.append(e.symbol)
					loaded = True
			#	except httplib.BadStatusLine, e:
			#		print "Server disconnected..."
			#		print e
			#		time.sleep(15)
			#		print "Trying again..."
			#		continue
				except fundie.WebAccessError, e:
					print "Network connection lost... "
					print e
					time.sleep(15)
					print "Trying again..."
					continue
				else:
					loaded = True
		return errorList, invalidList
	
	def updatePrices(self, symbol):
		if(not fundie.isValid(symbol)):
				raise InvalidSymbol("Invalid Symbol", symbol)
				#TODO FIXTHIS : invalid symbol management should either delete the symbol, report it to me, or follow yahoo's 
				# "new symbol is" dialogue and save it to the database retroactively.  like AEOS is now AEO
				return
		#"Used to bring prices up to date after a long time dormant.  Not used for every day updates."

		#get today, set up constants
		oneDay = datetime.timedelta(1)
		today = datetime.date.today()

		#get latest price from database
		query = "SELECT DATE FROM stockprices WHERE SYMBOL = \'" + symbol + "\' ORDER BY date DESC LIMIT 1"
		self.myCursor.execute(query)
		firstMissingDate = self.cleanup(self.myCursor.fetchall())[0] + oneDay

		#check to see if i need updates
		if(firstMissingDate > today): #already updated
			return
	
		#build a webpage based off of those two dates
		newPrices = fundie.getLatestPrices(symbol, firstMissingDate, today)


		for date in newPrices.keys():
			pricesDatum = newPrices[date]
			executeString = " INSERT INTO STOCKPRICES VALUE(\'" + symbol + "\',\'" + str(date) + "\',\'"
			executeString += str(pricesDatum['open']) + "\',\'" + str(pricesDatum['close']) + "\',\'" + str(pricesDatum['high']) +\
					"\',\'" + str(pricesDatum['low']) + "\',\'" + str(int(pricesDatum['volume'])) + "\'," +\
					"\'0.0\',\'0.0\',\'0.0\',\'0.0\',\'0.0\',\'0.0\',\'0.0\',\'0.0\',\'0.0\',\'0.0\')"
#			print executeString
			self.myCursor.execute(executeString)
			self.myConnection.commit()
		return

		return newPrices
		#CHECk to make sure that info isn't empty!
		#turn the webpage into a proper array, parse it.

		#update data in database - DO THIS.

    	
    	def updateFundamentals(self, symbol):
		if(not fundie.isValid(symbol)):
				raise InvalidSymbol("Invalid Symbol", symbol)
				#TODO FIXTHIS : invalid symbol management should either delete the symbol, report it to me, or follow yahoo's 
				# "new symbol is" dialogue and save it to the database retroactively.  like AEOS is now AEO
				return
		#setup
		webpage = fundie.getFinancialWebsite(symbol)

		# get latest date for this symbol
		query = "SELECT DATE FROM stockfinancials WHERE SYMBOL = \'" + symbol + "\'"
		self.myCursor.execute(query);
		availableDates = self.cleanup(self.myCursor.fetchall())
		availableDates.sort()
		availableDates.reverse()

		# download latest from the web and compare.
#		webDates = fundie.getWebpageDates(webpage)
		incomeDates = fundie.getIncomeDates(webpage)
		balanceDates = fundie.getBalanceDates(webpage)
		cashDates = fundie.getCashDates(webpage)

		#comparing the two
		incomeAddDates = self.compareDates(availableDates, incomeDates)	
		balanceAddDates = self.compareDates(availableDates, balanceDates)
		cashAddDates = self.compareDates(availableDates, cashDates)

		if(incomeAddDates == [] and balanceAddDates == [] and cashAddDates == []):
			return

		#setting up a tuple index for each date for easy looping in the website.  shouldn't this be in the website part of the function?
		incomeDateIndecies = self.getIndecies(incomeAddDates, incomeDates)
		balanceDateIndecies = self.getIndecies(balanceAddDates, balanceDates)
		cashDateIndecies = self.getIndecies(cashAddDates, cashDates)

		incomeStatement = fundie.getIncomeStatement(webpage, symbol, incomeDateIndecies)
		balanceSheet = fundie.getBalanceSheet(webpage, symbol, balanceDateIndecies)
		cashFlows = fundie.getCashFlows(webpage, symbol, cashDateIndecies)

		fundamentals = {}
		for date in incomeStatement.keys():
			fundamentals[date] = fundie.seedFundamentals()
			fundamentals[date].update(incomeStatement[date])
		for date in balanceSheet.keys():
			if(not fundamentals.has_key(date)):
				fundamentals[date] = fundie.seedFundamentals()
			fundamentals[date].update(balanceSheet[date])
		for date in cashFlows.keys():
			if(not fundamentals.has_key(date)):
				fundamentals[date] = fundie.seedFundamentals()
			fundamentals[date].update(cashFlows[date])
			
#		return fundamentals
		fundamentalsList = {}
		for date in fundamentals.keys():
			fundamentalsList[date] = fundie.marshall(fundamentals[date])

		for date in fundamentals.keys():
			executeString = " INSERT INTO STOCKFINANCIALS VALUE(\'" + symbol + "\',\'" + str(date) + "\',\'"
			for fundamentalDatum in fundamentalsList[date]:
				#FIX THIS, until i figure out how to do 'unions' or something in the database, 0.0 is 0.0 and 'unknown'
				if(fundamentalDatum == '-'):
					executeString += '0.0' + "\',\'" #set unknowns to 0.0
				else:
					executeString += str(fundamentalDatum) + "\',\'"
			executeString = executeString.rstrip(",\'")
			executeString += "\')"

		self.myCursor.execute(executeString)
		self.myConnection.commit()
		return

        def addFundiesToDatabase(self, stocks):
            deletethis = []
            for symbol in stocks:
                print "Adding ", symbol
                toAdd = fundie.getFinancials(symbol)
                if(toAdd is not None):
                    self.addFundamentals(toAdd, symbol)
                else:
                    print symbol, " doesn't have fundamental data."
                    deletethis.append(symbol)
                self.myConnection.commit()
            return deletethis
                
    
        def addFundamentals(self, financials, stock):
            for date in financials.keys():
                temp = financials[date]
                executeString = " INSERT INTO STOCKFINANCIALS VALUE(\'" + stock + "\',\'" + str(date) + "\',\'" #the date
		for entry in range(106): #all 109 entries on my financials
                    if (temp[entry] == -0.001):
                        print "PANIC!!!!"
                    if (temp[entry] == '-'):
                        executeString += '-0.001' + "\',\'" # this value is reserved
                    else:
                        executeString += str(temp[entry]) + "\',\'"
                if(temp[106] == '-0.001'):
                   print "PANIC!!!!"
                if(temp[106] == '-'):
                    executeString += '-0.001' + "\') "
                else:
                    executeString += str(temp[106]) + "\') "
#                print executeString
                self.myCursor.execute(executeString)
                    
        def syncDates(self):
                self.myCursor.execute( " SELECT DISTINCT DATE FROM STOCKPRICES ")
                alldates = self.myCursor.fetchall()
                for date in alldates:
                    self.myCursor.execute( " INSERT INTO DATETABLE VALUE(\'"
#                    print ( " INSERT INTO DATETABLE VALUE(\'"
                                           + str(date[0]) + "\')" )
                self.myConnection.commit()

        def syncStocks(self):
                self.myCursor.execute( " SELECT DISTINCT SYMBOL FROM STOCKPRICES ")
                allstocks = self.myCursor.fetchall()
                for stock in allstocks:
                    self.myCursor.execute( " INSERT INTO STOCKTABLE VALUE(\'"
                                           + str(stock[0]) + "\')" )
                self.myConnection.commit()

        def check200Avg(self, symbol):
            self.myCursor.execute( " SELECT OPEN FROM STOCKPRICES WHERE SYMBOL=\'"
                                   + symbol + "\' ORDER BY DATE DESC" )
            allprices = self.myCursor.fetchall()
            toRtn = []
            for price in allprices:
                toRtn.append(float(price[0]))

            return toRtn

        def build200avg(self):
            for symbol in self.stockTable:
                print "Calculating ", symbol
                self.myCursor.execute( " SELECT CLOSE,DATE FROM STOCKPRICES WHERE SYMBOL=\'"
                                           + symbol + "\' ORDER BY DATE ASC" )
                allprices = self.myCursor.fetchall()
                toRtn = []
                for price in allprices: #unwrap this
                    toRtn.append([float(price[0]), (price[1])])
            
                toRtn[0].append(toRtn[0][0]) #200
                toRtn[0].append(toRtn[0][0]) #50
                toRtn[0].append(toRtn[0][0]) #15

                for i in range(len(toRtn)-1):
                    toRemove200 = toRtn[max(i-199, 0)][0] #after 200, begin taking away the 200th stock, otherwise the first
                    toRemove50 = toRtn[max(i-49, 0)][0] #after 50, begin taking away the 50th stock away historically, otherwise the first
                    toRemove15 = toRtn[max(i-14, 0)][0]#after 15, begin taking away the 15th stock historically, otherwise the first
#                    print toRtn[i][2], "ajkj", toRtn[i+1][0]
                    toRtn[i+1].append( toRtn[i][2] + (toRtn[i+1][0] - toRemove200)/200 ) #continuous return
                    toRtn[i+1].append( toRtn[i][3] + (toRtn[i+1][0] - toRemove50)/50 )  #simple return
                    toRtn[i+1].append( toRtn[i][4] + (toRtn[i+1][0] - toRemove15)/15 )
            
                for price in toRtn:
                    self.myCursor.execute( " UPDATE STOCKPRICES SET 200_day_avg=\'" +
                                           str(price[2]) + "\', 50_day_avg=\'" +
                                           str(price[3]) + "\', 15_day_avg=\'" +
                                           str(price[4]) + "\' WHERE SYMBOL=\'" +
                                            symbol + "\' AND DATE=\'" + str(price[1]) + "\'" )
                self.myConnection.commit()
                
            return

        def calcNormSCReturn(self): #calculates returns normalized on the stock's max and min
            for symbol in self.stockTable:
                self.myCursor.execute( " SELECT SIMPLE_RETURN,CONTINUOUS_RETURN, DATE \
                    FROM STOCKPRICES WHERE SYMBOL=\'" + symbol + "\' ORDER BY DATE ASC" )
                allprices = self.myCursor.fetchall()
                
                dates = []
                simple_gains = []
                continuous_gains = []
                
                for price in allprices: #unwrap this
                    simple_gains.append(float(price[0]))
                    continuous_gains.append(float(price[1]))
                    dates.append(price[2])

                try:    
                    simple_gains = normalize(simple_gains)
                    continuous_gains = normalize(continuous_gains)
                except ZeroDivisionError:
                    continue

                for i in range(len(dates)):
                    self.myCursor.execute( " UPDATE STOCKPRICES SET NORMALIZED_CONTINUOUS_RETURN=\'" +
                        str(continuous_gains[i]) + "\', NORMALIZED_SIMPLE_RETURN=\'" +
                        str(simple_gains[i]) + "\' WHERE SYMBOL=\'" +
                        symbol + "\' AND DATE=\'" + str(dates[i]) + "\'" )
                self.myConnection.commit()
            return
            
        def calcSACReturn(self):
            for symbol in self.stockTable:
                print "Calculating ", symbol
                self.myCursor.execute( " SELECT CLOSE,DATE FROM STOCKPRICES WHERE SYMBOL=\'"
                                       + symbol + "\' ORDER BY DATE ASC" )
                allprices = self.myCursor.fetchall()
                toRtn = []
                for price in allprices: #unwrap this
                    toRtn.append([float(price[0]), (price[1])])
            
#                toRtn.append(float(price[0]))
                toRtn[0].append('0.0')
                toRtn[0].append('0.0')
                for i in range(len(toRtn)-1):
                    toRtn[i+1].append(  math.log(toRtn[i+1][0]/toRtn[i][0]) ) #continuous return
                    toRtn[i+1].append( (toRtn[i+1][0]-toRtn[i][0])/toRtn[i][0] )  #simple return

            
                for price in toRtn:
#                    print price
                    self.myCursor.execute( " UPDATE STOCKPRICES SET CONTINUOUS_RETURN=\'" +
                                           str(price[-2]) + "\', SIMPLE_RETURN=\'" +
                                           str(price[-1]) + "\' WHERE SYMBOL=\'" +
                                            symbol + "\' AND DATE=\'" + str(price[1]) + "\'" )
                self.myConnection.commit()
            return
        
            avglist.append(toRtn[0])
            i=0
            for i in range(1,len(toRtn)):
                avglist.append(avglist[i-1] + (toRtn[i] - toRtn[max(0, i-50)] / 200))

            return avglist
            

        def syncMinMax(self):
                for stock in self.stockTable:
                    self.myCursor.execute( " SELECT PRICE_MOVEMENT FROM STOCKPRICES WHERE SYMBOL=\'"
                                           + stock + "\'" )
                    allPrices = self.myCursor.fetchall()
                    maxPriceMovement = max(allPrices)
                    minPriceMovement = min(allPrices)
                    self.myCursor.execute( " SELECT HIGH FROM STOCKPRICES WHERE SYMBOL=\'"
                                           + stock + "\'" )
                    allPrices = self.myCursor.fetchall()
                    maxHigh = max(allPrices)
                    self.myCursor.execute( " SELECT LOW FROM STOCKPRICES WHERE SYMBOL=\'"
                                           + stock + "\'" )
                    allPrices = self.myCursor.fetchall()
                    minLow = min(allPrices)
                    self.myCursor.execute( " SELECT VOLUME FROM STOCKPRICES WHERE SYMBOL=\'"
                                           + stock + "\'" )
                    allPrices = self.myCursor.fetchall()
                    maxVol = max(allPrices)
                    minVol = min(allPrices)

                    self.myCursor.execute( " UPDATE STOCKTABLE SET PRICE_MOVEMENT_MAX=\'"
                                           + str(maxPriceMovement[0]) + "\', PRICE_MOVEMENT_MIN=\'"
                                           + str(minPriceMovement[0]) + "\', MAX_HIGH=\'"
                                           + str(maxHigh[0]) + "\', MIN_LOW=\'"
                                           + str(minLow[0]) + "\', MAX_VOLUME=\'"
                                           + str(maxVol[0]) + "\', MIN_VOLUME=\'"
                                           + str(minVol[0]) +
                                           "\' WHERE SYMBOL=\'"
                                           + stock + "\'" )
                    self.myConnection.commit();
                                           
	def openConnection(self, _db='STOCKINFO', _user='root', _passwd='', _host="localhost"):
		#TO DO: find out why the user on this machine can't sign in using host austinwiltshire
                self.dateTable = []
                self.stockTable = []
		try:
			self.myConnection = MySQLdb.connect(user=_user, db=_db, passwd=_passwd, host=_host)
		except:
			raise SQLUpdateError("Could not connect to database.")
		self.myCursor = self.myConnection.cursor()
		self.myCursor.execute( " SELECT * FROM STOCKTABLE ")
		stockTable = self.myCursor.fetchall()
		self.myCursor.execute( " SELECT * FROM DATETABLE ")
		dateTable = self.myCursor.fetchall()
		for stock in stockTable:
                    self.stockTable.append(stock[0])
                for date in dateTable:
                    self.dateTable.append(date[0])

        def getNormalizedContinuousGain(self, stock, date):
            try:
                toReturn = float(self.priceInfo(stock, date)[13])
            except DateOutOfIndex:
                print "Date not in database"
            return toReturn
        
        def getGain(self, stock, date):
            try:
                toReturn = float(self.priceInfo(stock, date)[8])
            except DateOutOfIndex:
                print "Date not in database"
            return toReturn
                

        def getStockDates(self, stock):
            self.myCursor.execute( " SELECT date FROM STOCKPRICES WHERE SYMBOL=\'" + stock + "\'")
            toReturnWrapped = self.myCursor.fetchall()
            if(toReturnWrapped==None):
                print "No records were returned"
                return
            toReturnUnwrapped = []
            for date in toReturnWrapped:
                toReturnUnwrapped.append(date[0])
            return toReturnUnwrapped

        def getNormalizedContinuousReturn(self, stock, date):
            return float(self.priceInfo(stock, date)[13])
        
	def priceInfo(self, stock, date):
                if(stock not in self.stockTable):
                    print "Stock not in database"
                    return
                
                if(date not in self.dateTable):
                    raise DateOutOfIndex()
                    
		self.myCursor.execute( " SELECT * FROM STOCKPRICES WHERE SYMBOL=\'" + stock + "\'" + " AND DATE=\'" + str(date) + "\' " )
#		print " SELECT * FROM STOCKPRICES WHERE SYMBOL=\'" + stock + "\'" + "AND DATE=\'" + str(date) + "\' "
		#should check and see if i got anything returned here.
		toReturn = self.myCursor.fetchall()
		if(toReturn==None):
                    print "No records were returned"
                    return
                return toReturn[0]

	def financialInfo(self, stock, date):
		cursor.execute( " SELECT * FROM STOCKFINANCIALS WHERE NAME=\'" + stock + "\'" + "AND DATE<\'" + str(date) + "\' LIMIT 1")
		#should check and see if i got anything returned here.
		return cursor.fetchall()

#	def checkSymbol(self, stock):
#                cursor.execute( " SELECT NAME FROM STOCKFINANCIALS

	def addPriceInfo(self, stock, date, open, close, high, low, volume):
		self.myCursor.execute( " INSERT INTO STOCKPRICES VALUE(\'"
		#print( " INSERT INTO STOCKPRICES VALUE(\'"
				+ stock + "\',\'"
				+ str(date) + "\',\'"
				+ str(open) + "\',\'"
				+ str(close) + "\',\'"
				+ str(high) + "\',\'"
				+ str(low) + "\',\'"
				+ str(volume) + "\') ")
	
	def addFinancialInfo(stock, date):  #obviously i have no idea what else to put here yet.
		cursor.execute ( " INSERT INTO STOCKFINANCIALS VALUE(\'"
				+ stock + "\',\'"
				+ str(date) + "\' ")

	def commitInfo(self):
		self.myConnection.commit()
