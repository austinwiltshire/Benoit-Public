import MySQLdb
import Query
import datetime
import CachePolicy

class SQLDatabase(object):
    def __init__(self, _host, _user, _password, _db):
#        try:
        self.myConnection = MySQLdb.connect(host=_host, user=_user,\
                                                passwd=_password, db=_db)
        #except:
        #    raise "Cannot connect to database"
        
        self.myCursor = self.myConnection.cursor()
        self.cachePolicy = CachePolicy.DefaultCachePolicy()

    def closeConnection(self):
	    del self.myCursor
	    self.myConnection.close()
	    del self.myConnection

        
    def checkCache(self, query):
        if not self.cachePolicy.IsCached(query):
            #print "missed on " + str(query)
            self.cachePolicy.Cache(query)
        return self.cachePolicy.Get(query)
        
    def Select(self, fields, tables, clauses, cast=None):
        #not cacheing at this level because it might slow things down for no good
        return Query.Select(self.myCursor, fields, tables, clauses, cast).getValue()
        #return self.checkCache(Query.Select(self.myCursor, fields, tables, clauses, cast)).getValue()
    
    def SelectAll(self, fields, tables, cast=None):
        return Query.SelectAll(self.myCursor, fields, tables, cast).getValue()
        #return self.checkCache(Query.SelectAll(self.myCursor, fields, tables, cast)).getValue()
    
    def CreateTable(self, fields, tablename):
        #Create table might be better done as a builder pattern
        """ Fields are a dict of name mapped to SQLType """
        command = "CREATE TABLE IF NOT EXISTS %s (%s)" % (tablename,\
                                ", ".join([" ".join([name, SQLType(atype)]) for (name,atype) in fields.items()]))
        self.myCursor.execute(command)
        self.myConnection.commit()

    def DropTable(self, tablename):
        command = " ".join(["DROP TABLE",tablename])
        self.myCursor.execute(command)
        self.myConnection.commit()
        
    def ShowTables(self):
        self.myCursor.execute("SHOW TABLES")
        return Query.sanitize(str, self.myCursor.fetchall())
    
    def DescTable(self, tablename):
        command = " ".join(["DESC", tablename])
        self.myCursor.execute(command)
        return Query.sanitize(str, self.myCursor.fetchall())
    
    def Insert(self, tablename, toAdd):
        """ Values should be a dict of name:values """
        keys = []
        values = []
        for (key,value) in toAdd.items():
            keys.append(key)
            values.append(value)
        keystring = ",".join(keys)
        keystring = "".join(["(",keystring,")"])
        valuestring = ",".join(map(Quote,map(str,values)))
        valuestring = "".join(["(",valuestring,")"])
        
        command = " ".join(["INSERT INTO",tablename,keystring,"VALUES",valuestring])
        self.myCursor.execute(command)
        self.myConnection.commit()
        
    def Replace(self, tablename, toAdd):
        keys = []
        values = []
        for (key,value) in toAdd.items():
            keys.append(key)
            values.append(value)
        keystring = ",".join(keys)
        keystring = "".join(["(",keystring,")"])
        valuestring = ",".join(map(Quote,map(str,values)))
        valuestring = "".join(["(",valuestring,")"])
        
        command = " ".join(["REPLACE INTO",tablename,keystring,"VALUES",valuestring])
        self.myCursor.execute(command)
        
    def commit(self):
        self.myConnection.commit()
        
            
    def __del__(self):
        self.myConnection.close()
        
def Quote(astring):
    return "".join(["\"",astring,"\""])

def SQLType(atype):
    #TODO: this typechecker could be broken up easy peasy.  DOIT
    SQLDefaultValues = {"decimal":"(9,3)", "int":"(10)", "varchar":"(20)"}
    SQLMappedTypes = {float:"decimal", int:"int", str:"varchar", datetime.date:"date"}
    SQLSupportedTypes = SQLDefaultValues.keys()
    #for each python type, what type is that in SQL, and what is the default 'length' value
    
    if isinstance(atype, str): #sql type, check to make sure its one i support
        #strip off first argument in string, should be one of my supported types
        checkType = atype.split(" ")[0]
        if checkType not in SQLSupportedTypes():
            raise checkType + " Not supported"
        else: 
            if len(atype.split(" ")) == 1:
                #sql name, default size
                return "".join([atype,(SQLDefaultValues[atype])])
            else:
                #sql name with size passed in
                return atype
    elif isinstance(atype, type):
        #simple python type, use default size
        sqlType = SQLMappedTypes[atype]
        sqlValue = SQLDefaultValues.get(sqlType, "")
        return "".join([sqlType,sqlValue])
    elif isinstance(atype, tuple):
        #tuple python type, python type + size
        if isinstance(atype[0], type):
            sqlType = SQLMappedTypes[atype[0]]
            sqlValue = "".join(["(",str(atype[1]),")"])
            return"".join([sqlType,sqlValue])
    else:
        raise str(atype) + " Not supported"
