import pandas as pd
import statistics as stats
import matplotlib.pyplot as plt

import cafe.farm as farm
import cafe.importData as importData


def simulateCoOp(plotList, numYears, pruneYear = None, growthPattern = None, strategy = None):
    """
    Uses a list of plots, `plotList`, to simulate a cooperative over `numFarms` number of years.
    
    Returns a list of two lists: `simulation`
        list one, `harvestYear`, represents the year range in the simulation.
        list two, `annualHarvest`, represents the amount of coffee (in lbs) harvested for that  year
    
    """

    numPlots = len(plotList)

    annualHarvest = []
    harvestYear = []
    
    

    for year in range(numYears):
        # each year reset harvest
        thisYearsHarvest = 0 

        for j in range(numPlots):
            if (pruneYear):
                if j == pruneYear: # if it's the prune year
                    # isPrune = True
                    plotList[j].setPruneTrees()
                    
            plotList[j].oneYear() # run this plot through one year of the demo
            tempHarvest = plotList[j].totalHarvest
            plotList[j].setHarvestZero() # not cumulative sum, but instead reset
            thisYearsHarvest += tempHarvest

        harvestYear.append(year)
        annualHarvest.append(thisYearsHarvest)
       
        
    simulation = [harvestYear, annualHarvest]
    
    return(simulation)


        


def main(args):
    
    import os
    
    farmData = args.farm
    trees = args.trees
    strategy = args.strategy
    years = args.years
    output = args.output
    
    if not os.path.exists(farmData):
        raise ValueError(
        """
        File: %s does not exist
        
        If you are running default commands and this is your first time
        running the simulation, assure you have run:
        
        `python3 src/cafe/fakeData.py --farms 100 --year 2020 --output data/fakeData.csv`
        
        in the core directory before calling simulateCoOp.py from the command line.
        
        """%farmData)
        
    if not os.path.exists(trees):
        raise ValueError(
        """
        File: %s does not exist
        
        Assure you are in the correct working directory relative to the filepath
        argument given for --trees.
        
        """%trees)
        
    
    print("Importing Data")
    farmList = importData.compileCoOp(farmStr=farmData,treeStr=trees)
    
    print("Simulating Cooperative")
    simData = simulateCoOp(farmList, years)
    
    print("Plotting")
    pltYears = simData[0]
    pltHarvests = simData[1]
    
    # get parameters for axes
    mnYear, mxYear = min(pltYears), max(pltYears)
    mxHarvest = max(pltHarvests)
    
    
    plt.rcParams["figure.figsize"] = (20,10)
    fsize = 20 # font size 
    
    plt.axes(xlim=(mnYear,mxYear),ylim=(0,(mxHarvest + (mxHarvest * 0.10))))
    plt.plot(pltYears, pltHarvests, linewidth = 4)
    plt.style.use('ggplot')
    plt.title("Prediction of %d years with no action by demo co-op"%(years), fontsize =(fsize * 1.25))
    plt.xlabel("Year", fontsize =fsize)
    plt.ylabel("Total pounds of green coffee produced", fontsize =fsize)
    plt.savefig(output, dpi = 100)
    #plt.show()

    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Parse growth data for simulation.')
    parser.add_argument('-f', '--farm',
                        default='data/fakeData.csv',
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
    
    parser.add_argument('-o', '--output',
                        default="testNewFarm.png",
                        type=str, # string type works well for 
                        help=
                        """
                        Desired name of plot output file.
                        
                        """)
    
    args = parser.parse_args()
    
    main(args)
    
    
