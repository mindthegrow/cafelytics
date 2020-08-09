import pandas as pd
import cafe.farm as farm

def readData(filePath:str):
    """
    Takes a filepath in the form of a string (e.g. 'data/demoData.csv') that represents a spreadsheet and returns a pandas dataframe. 
    
    """
    pathExt = filePath.split('.')
    ext = pathExt[1]
    
    if ext == 'csv':
        data = pd.read_csv(filePath)
    elif (ext == 'xlsx') or (ext == 'xls') or (ext == 'xlsm') or (ext == 'xlsb'):
        #sheet = input("Please enter the sheet name or number (first sheet = 0, second = 1, etc.)")
        data  = pd.read_excel(filePath)

    return(data)

def compileCoOp(farmStr: str): # strategyStr = None, treeStr = None):
    """
    Takes a string argument (file paths) and compiles the data into a list of classes of type : farm.Farm, assigning the parameters respective to the data in the spreadsheet (farmer names, tree types, number of cuerdas, and age of trees).
    
    Parameters
    ----------
    farmStr : str
        string of filepath (from current working directory) to spreadsheet with data. Spreadsheet must correspond with template to run function. 
        
        
    Returns
    -------
    plotList : list of farm.Cuerdas
        a list of class type Cuerdas that have been initialized with their respective parameters and attributes.
    
    """
    farmData = readData(farmStr)

    plotList = []

    # create a list of plots using class Cuerdas
    for i in range(len(farmData)):
        tempName = str(farmData['farmerName'][i])
        tempCuerdas = float(farmData['numCuerdas'][i])
        tempTree = str(farmData['treeType'][i])
        tempAge = float(farmData['ageOfTrees'][i])
    
        plot = farm.Farm(farmerName=tempName, cuerdas=tempCuerdas, treeType=tempTree, initialAgeOfTrees=tempAge)
        
        plotList.append(plot)
        
    return(plotList)

