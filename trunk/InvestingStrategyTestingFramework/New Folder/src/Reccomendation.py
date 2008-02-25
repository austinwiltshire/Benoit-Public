class ReccomendationSetting(object):
    Buy = 3
    Hold = 2
    Sell = 1

class Reccomendation(object):
    # TODO: figure out how to do enums in python
    
    # Whats my scale going to be on strength?  1-100?
    
    """ A container for stock reccomendations """
    def __init__(self, symbol, strength):
        self.symbol = symbol
        self.setting = self.getSetting()
        self.strength = strength
    
    def __cmp__(self, other):
        """ Sorts on setting first and strength second """
        return  -cmp([self.setting, self.strength],[other.setting, other.strength])
    
    def __eq__(self, other):
        """ Checks equality based totally on setting """
        return self.setting == other.setting
    
    def __str__(self):
        return " ".join([self.getSettingString(),("Rating for %s : %f" % (self.symbol,self.strength))])
    
    def getSymbol(self):
        return self.symbol
    
    def __repr__(self):
        return self.__str__()
    
    def getSetting(self):
        pass
    
    def getSettingString(self):
        pass
            

class Buy(Reccomendation):
    def getSetting(self):
        return 3.0
        
    def getSettingString(self):
        return "Buy"
    
class Hold(Reccomendation):
    def getSetting(self):
        return 2.0
    
    def getSettingString(self):
        return "Hold"
    
class Sell(Reccomendation):
    def getSetting(self):
        return 1.0
        
    def getSettingString(self):
        return "Sell"
        

    #short
    #put
    #call
    #hedge
    
        
        