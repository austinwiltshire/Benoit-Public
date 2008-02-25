class DBCheck(Exception):
    pass

def mutable(toMutate):
    """Takes in a tuple or single immutable object and returns a mutable copy"
    " if it's a tuple of tuples, then it mutates all members of the tuple. """
    if isinstance(toMutate, tuple) and len(toMutate) > 1:
        return [mutable(x) for x in toMutate]
    elif isinstance(toMutate, tuple) and len(toMutate) == 1:
        return mutable(toMutate[0])
    elif isinstance(toMutate, tuple) and len(toMutate) == 0:
        return []
    else:
        return toMutate
    
def downCast(toCast, cast):
    """ Casts all members of a list or nests of lists to the 'cast' argument """
    if not cast:
        return toCast
    if isinstance(toCast, list):
        return [downCast(x, cast) for x in toCast]
    else:
        return cast(toCast)

def sanitize(cast, toClean):
    """ Makes 'toClean' mutable and casts its to the appropriate datatype """  
    toClean = mutable(toClean)
    return downCast(toClean, cast)

class Query(object):
    def __init__(self, database, fields, tables, clauses, cast):
        self.database = database
        self.fields = fields
        self.tables = tables
        self.clauses = clauses
        self.cast = cast
        self.value = None
        
    def __execute__(self):
        pass
    
    def getValue(self):
        if not self.value: #lazy evaluate
            self.value = self.__execute__()
        return self.value
    
    def __repr__(self):
        return " ".join(map(str, [self.fields, self.tables, self.clauses]))
    
class CachedQuery(Query):
    def __init__(self, value):
        self.value = value

class Select(Query):
    def __execute__(self):
        query = "SELECT %s FROM %s WHERE %s" % (",".join(self.fields), ",".join(self.tables), " AND ".join(self.clauses))
        self.database.execute(query)
            
        #self.database.execute("SELECT %s FROM %s WHERE %s", (",".join(self.fields),\
        #                                                     ",".join(self.tables),\
        #                                                     " AND ".join(self.clauses)))
        return sanitize(self.cast, self.database.fetchall())
    
class SelectAll(Query):
    def __init__(self, database, fields, tables, cast):
        super(SelectAll, self).__init__(database, fields, tables, None, cast)
        
    def __execute__(self):
        query = "SELECT %s FROM %s" % (",".join(self.fields), ",".join(self.tables))
        self.database.execute(query)
        
        return sanitize(self.cast, self.database.fetchall())
    