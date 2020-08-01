import pandas as pd
import numpy as np
import statistics as stats
import matplotlib.pyplot as plt
import importlib

import farm as farm
import functions as functions

#importlib.reload(farm)

def compileCoOp(farmStr): # strategyStr = None, treeStr = None):
    """
    Takes string arguments (file paths) and compiles the data into a list of classes of type : Cuerdas, assigning the parameters respective to the data in the spreadsheet (farmer names, tree types, number of cuerdas, and age of trees).
    
    Parameters
    ----------
    farmStr : str
        string of filepath (from current working directory) to spreadsheet with data. Spreadsheet must correspond with template to run function. 
        
        
    Returns
    -------
    lsOfPlots : list of farm.Cuerdas
        a list of class type Cuerdas that have been initialized with their respective parameters and attributes.
    
    """
    farmData = functions.readData(farmStr)

    lsOfPlots = []

    # create a list of plots using class Cuerdas
    for i in range(len(farmData)):
        tempName = str(farmData['farmerName'][i])
        tempCuerdas = float(farmData['numCuerdas'][i])
        tempTree = str(farmData['treeType'][i])
        tempAge = float(farmData['ageOfTrees'][i])
    
        plot = farm.Cuerdas(_farmerName=tempName, _cuerdas=tempCuerdas, _treeType=tempTree, _initialAgeOfTrees=tempAge)
        lsOfPlots.append(plot)
        
    return(lsOfPlots)


def simulateCoOp(lsOfPlots, numYears, pruneYear = None, growthPattern = None, strategy = None):

    numPlots = len(lsOfPlots)

    annualHarvest = []
    harvestYear = []
    
    

    for year in range(numYears):
        thisYearsHarvest = 0 # each year reset harvest

        for j in range(numPlots):
            if (pruneYear):
                if j == pruneYear: # if it's the prune year
                    isPrune = True
                    lsOfPlots[j].setPruneTrees(isPrune)
                    
            lsOfPlots[j].oneYear() # run this plot through one year of the demo
            tempHarvest = lsOfPlots[j].totalHarvest
            lsOfPlots[j].setHarvestZero() # not cumulative sum, but instead reset
            thisYearsHarvest += tempHarvest

        harvestYear.append(year)
        annualHarvest.append(thisYearsHarvest)
       
        
    simulation = [harvestYear, annualHarvest]
    
    return(simulation)


        


def main():
    import argparse
    import os
    parser = argparse.ArgumentParser(description='Parse growth data for simulation.')
    parser.add_argument('-f', '--farm',
                        default='data/demoData.csv',
                        type=str, # string type works well for 
                        help=
                        """
                        Name of file (and path from current directory) to data containing cuerdas, tree types, etc.
                        
                        Example (& default): --farm data/demoData.csv
                        
                        """)
    
    parser.add_argument('-t', '--trees', # currently this information is stored in the Cuerdas class
                        default='data/trees.yml',
                        type=str, # string type works well for 
                        help=
                        """
                        Name of file (and path from current directory) to data containing tree attributes.
                        
                        Example (& default): --trees data/trees.yml
                        
                        """)
    parser.add_argument('-s', '--strategy',
                        default='data/strategy1.yml',
                        type=str, # string type works well for 
                        help=
                        """
                        Name of file (and path from current directory) to data containing method, strategy, & approach data.
                        
                        Example (& default): --strategy intervention/strategy1.yml
                        
                        """)
    
    parser.add_argument('-y', '--years',
                        default=30,
                        type=int, # string type works well for 
                        help=
                        """
                        Number of years that should be iterated through in the simulation (type : int).
                        
                        Example (& default): --year 30
                        
                        """)
    
    args = parser.parse_args()
    
    farm = args.farm
    trees = args.trees
    strategy = args.strategy
    years = args.years
    
    if not os.path.exists(farm):
        raise ValueError("File: %s does not exist"%farm)
    
    lsOfFarms = compileCoOp(farm)
    
    simData = simulateCoOp(lsOfFarms, years)
    
    pltYears = simData[0]
    pltHarvests = simData[1]
    
    plt.rcParams["figure.figsize"] = (20,10)
    fsize = 20 # font size 
    #mpl.rcParams.update(mpl.rcParamsDefault)
    
    plt.plot(pltYears, pltHarvests)
    plt.style.use('ggplot')
    plt.title("Thirty-year prediction with no action by demo co-op", fontsize =(fsize * 1.25))
    plt.xlabel("Year", fontsize =fsize)
    plt.ylabel("Total pounds of coffee berry produced", fontsize =fsize)
    plt.savefig("demoPredNew.png", dpi = 100)
    plt.show()

    
if __name__ == '__main__':
    main()