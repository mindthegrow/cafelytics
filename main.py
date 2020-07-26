import pandas as pd
import numpy as np
import statistics as stats
import matplotlib.pyplot as plt
import importlib

import farm as farm
import functions as functions

importlib.reload(farm)

demoData = functions.readData('demoData.csv')
demoData
lsOfPlots = []

# create a list of plots using class Cuerdas
for i in range(len(demoData)):
    tempName = str(demoData['farmerName'][i])
    tempCuerdas = float(demoData['numCuerdas'][i])
    tempTree = str(demoData['treeType'][i])
    tempAge = float(demoData['ageOfTrees'][i])
    
    plot = farm.Cuerdas(_farmerName=tempName, _cuerdas=tempCuerdas, _treeType=tempTree, _initialAgeOfTrees=tempAge)
    lsOfPlots.append(plot)
    
numPlots = len(lsOfPlots)
demoYears = 30

annualHarvest = []
harvestYear = []

for i in range(demoYears):
    thisYearsHarvest = 0
    
    for j in range(numPlots):
        lsOfPlots[j].oneYear() # run this plot through one year of the demo
        tempHarvest = lsOfPlots[j].totalHarvest
        lsOfPlots[j].setHarvestZero() # not culminating sum, but instead reset
        thisYearsHarvest += tempHarvest
        
    
    annualHarvest.append(thisYearsHarvest)
    harvestYear.append(i)
    
plt.rcParams["figure.figsize"] = (20,10)
#mpl.rcParams.update(mpl.rcParamsDefault)

plt.plot(harvestYear, annualHarvest)
fsize = 20
plt.style.use('ggplot')
plt.title("Thirty-year prediction with no action by demo co-op", fontsize =(fsize * 1.25))
plt.xlabel("Year", fontsize =fsize)
plt.ylabel("Total pounds of coffee berry produced", fontsize =fsize)
plt.savefig("demoPred", dpi = 100)
