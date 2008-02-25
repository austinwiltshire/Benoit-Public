import Query

#loosely follows a chain of command pattern, which  means IT MATTERS WHAT ORDER YOU PUT THESE
#CACHEING POLICIES IN!

class CachePolicy(object):
    def __init__(self, subordinate=None):
        self.subordinate = subordinate
        self.table = {}
    
    def Append(self, aCachePolicy):
        if(self.subordinate):
            self.subordinate.append(aCachePolicy)
        else:
            self.subordinate = aCachePolicy
            
    def IsCached(self, query):
        if self.__localIsCached__(query):
            return True
        elif(self.subordinate):
            return self.subordinate.IsCached(query)
        else:
            return False
    
    def Cache(self, query):
        if self.__localCanCache__(query):
            self.__localCache__(query)
        elif(self.subordinate):
            self.subordinate.Cache(query)
            
    def __cacheKey__(self, query):
        """ Turns the query into a specific key to store in the cache's table """
        pass
        
    def Get(self, query):
        if self.__localIsCached__(query):
            return Query.CachedQuery(self.__localGet__(query))
        elif(self.subordinate):
            return self.subordinate.Get(query)
        else:
            return Query
        
    def __clearCache__(self):
        pass
        
class DefaultCachePolicy(CachePolicy):
    def __localIsCached__(self, query): #this 'links' check
        return False
    
    def __localGet__(self, query):
        return None
    
    def __localCanCache__(self, query):
        return False
    
    def __localCache__(self, query):
        return None
    
class SimpleCachePolicy(CachePolicy):
    """ This cache policy simply cache's the last X queries """
    def __init__(self, number=10000, subordinate=None):
        super(SimpleCachePolicy, self).__init__(subordinate)
        self.limit = number
        
    def __localIsCached__(self, query):
        if self.__cacheKey__(query) in self.table:
            return True
        else:
        #    print "cacheMiss!"
            return False
        
    def __localGet__(self, query):
        (value, needed) = self.table[self.__cacheKey__(query)]
        self.table[self.__cacheKey__(query)] = (value, needed+1)
        #print "cacheHit!" + str(value)
        return value
    
    def __localCanCache__(self, query):
        return True # no consraints on why this guy might cache something
    
    def __localCache__(self, query):
        if len(self.table) >= self.limit:
            self.__clearCache__()
        #print "cacheing" + str(query) + str(query.getValue())
        self.table[self.__cacheKey__(query)] = (query.getValue(), 0)
        
    def __cacheKey__(self, query):
        return "".join(map(str, [query.fields, query.tables, query.clauses]))
        
    def __clearCache__(self):
        neededArray = [value[1] for value in self.values()]
        neededArray.sort()
        neededThreshhold = neededArray[len(neededArray)/3]
        #roughly this gets the '33rd percentile'
        toDelete = [key for (key,value) in self.table if value[1] < neededThreshhold]
        #compiles a list of keys in the cache who have not been hit above the 'threshhold'
        for elem in toDelete:
            del self.table[elem]
        for key in self.table.keys():
            (value, needed ) = self.table[key]
            self.table[key] = (value, 0) #reset all needed counts
        print "!!!!!!!!!!!!!!Clearing Cache!!!!!!!!!!!!!!!!!"
            
        #print "to prove the cache is working, currently cacheing " + str(self.table)