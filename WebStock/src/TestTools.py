def assertClose(x,y,message="Assert Close Failed", e=0.05, prnt=False, reverse=False):
    """ Checks to see if the difference between x and y is below some error threshhold """
    diff = x - y
    if not reverse:
        assert diff >= -e and diff <= e , message
    if reverse:
        assert not (diff >= -e and diff <= e), message
    if prnt:
        print x, ",", y, ",", diff
        
def compareDicts(x,y, compareFunc = lambda x,y: (x - y < 0.05 and x - y > -0.05) if isinstance(x,float) else x==y, prnt=False):
    """ Compares two dicts to ensure they are equal in every way """
    xkeys = x.keys()
    ykeys = y.keys()
    
    for key in xkeys:
        if key not in ykeys:
            if prnt:
                print "False xkeys = ", xkeys, " ykeys = ", ykeys
            return (False,"Keys do not match in dicts")
    
    for key in ykeys:
        if key not in xkeys:
            if prnt:
                print "False xkeys = ", xkeys, " ykeys = ", ykeys
            return (False,"Keys do not match in dicts")
        
    for k in xkeys:
        if not compareFunc(x[k],y[k]):
            if prnt:
                print "False, xval = ", x[k], " yval ", y[k], " key ", k
            return (False,"Values do not match in dicts")
        
    return (True,"Passed Test")

def checkForError(func, args, error,msg=None):
    try:
        func(args)
    except error, e:
        if msg:
            if e.message == msg:
                print "returning true"
                return True
            else:
                print "returning false, message didn't match"
                print e.message, msg, e.message == msg
                return False
        print "returning true"
        return True
    print "no exception was thrown"
    print "returning false"
    return False
        