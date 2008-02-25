class EmptyReturns(Exception):
    pass

class Duplicate(Exception):
    pass

def checkNotEmpty(arg):
    """ Is used to ensure arguments are not empty and to alert of that condition """
    if arg == () or arg == [] or arg == None:
        raise EmptyReturns()
    else:
        return arg