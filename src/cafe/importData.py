import pandas as pd
import yaml
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

def openYaml(yamlFilePath : str) -> dict: 
    """
    Arguments: filepath str from pwd
    
    Returns: dictionary with the information contained in the YAML file
    
    Opens a .yaml/.yml file and returns a dictionary
    
    """
    yamlFile = open(yamlFilePath)
    parsed = yaml.load(yamlFile, Loader =yaml.FullLoader)
    return(parsed)


def compileCoOp(farmStr:str, treeStr:str): # strategyStr = None, treeStr = None):
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
    # a pd.DataFrame from spredsheet file
    farmData = readData(farmStr) 
    # a dictionary from yaml file
    treeData = openYaml(treeStr)

    plotList = []

    # create a list of plots using class Cuerdas
    for i in range(len(farmData)):
        tempName = str(farmData['farmerName'][i])
        tempCuerdas = float(farmData['numCuerdas'][i])
        tempTree = str(farmData['treeType'][i])
        tempAge = float(farmData['ageOfTrees'][i])
    
        plot = farm.Farm(farmerName=tempName, cuerdas=tempCuerdas, treeType=tempTree, initialAgeOfTrees=tempAge, treeAttributes=treeData)
        
        plotList.append(plot)
        
    return(plotList)

