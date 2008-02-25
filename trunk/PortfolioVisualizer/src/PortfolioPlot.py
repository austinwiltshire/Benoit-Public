import pylab
import matplotlib.dates
import Portfolio
import pickle
import numpy
import itertools

def smooth(toSmooth, base, work=True):
    if not work:
        return toSmooth
    for i in range(1, len(toSmooth)):
        if toSmooth[i] / base < .75:
            toSmooth[i] = toSmooth[i-1]
    return toSmooth

class PortfolioPlot(object):
    def __init__(self, filename=None):
        self.portfoliosLoaded = []
        afile = file(filename, 'r')
        if filename:
            self.portfoliosLoaded.append(pickle.load(afile))
        afile.close()
    
    def addPortfolio(self, filename):
        self.portfoliosLoaded.append(Portfolio.LoggedPortfolio.load(filename))
        
    def visualize(self, willsmooth=True):
        #TODO: how do you get dates to show up naturally?
        
        valueHistories = [x.valueHistory.items() for x in self.portfoliosLoaded]
        #load each portfolio's available trading dates and values
        #TODO: why aren't the dates all the same?
        
        map(lambda x: x.sort(), valueHistories) # sort each array
             
        xdates,yvalues = [],[]
        for valueHistory in valueHistories:
            (xdate,yvalue) = zip(*valueHistory)
            xdates.append(xdate)
            yvalues.append(yvalue)
        #seperate the date component from the value component into two seperate lists
        #i am such a leet haxor. zip(*(zip(x)) = x
        
        xdates = map(lambda x: pylab.date2num(x), xdates)
        #convert each date array to pylabs format
        
        coloriter = itertools.cycle(['b','r','g'])

        plotargs = [plotarg for plotarg in zip(xdates,yvalues,coloriter)]
        
#        for (x,y,color) in zip(xvalues,ydates,coloriter):
#            args.append((y,x,color))
        
        #print plotargs[0]
        
        fig = pylab.figure()
        subplot = fig.add_subplot(111)
        
        for arg in plotargs:
            subplot.plot_date(*arg)

        subplot.xaxis.set_major_locator(matplotlib.dates.MonthLocator([6,12]))
        subplot.xaxis.set_major_formatter(matplotlib.dates.DateFormatter("%m/%y"))
        subplot.autoscale_view()

        pylab.xlabel('Date')
        pylab.ylabel('Value')

        pylab.show()
        