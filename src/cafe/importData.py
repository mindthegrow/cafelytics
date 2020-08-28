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


def isolateAttributes(attributes:dict, treeType:str):
    """
    Takes in a dictionary containing all of the tree attributes, as well as the name of
    the tree type, then returns a dictionary with only the attributes of the tree
    `treeType`.
    """
    
    keys = list(treeAttributes.keys())
    altOrth = [treeAttributes[key]['altOrth'] for key in treeAttributes]
    # tipos = keys + altOrth # all of the possible spellings for the tree types
            
    if treeType in keys:
        treeDict = treeAttributes[treeType]
                
    elif treeType in altOrth:
        keyPair = [(key, treeAttributes[key]['altOrth']) for key in treeAttributes]
        _treeType = ''
        for i,e in enumerate(keyPair):
            if treeType == e[1]: # if it's the altOrth
                _treeType = e[0] # key to the key
                
            
            if len(_treeType) > 0:
                treeDict = treeAttributes[_treeType]
                
            else:
                raise AttributeError(
                """
                '%s' is not a recognized value (orthography) in the `treeAttributes` dict.
                
                """%(treeType))
                
    else:
        raise AttributeError(
        """
        '%s' is not a recognized value (orthography) in the `treeAttributes` dict.
                
        """%(treeType))
        
    return(treeDict)


def transformData(year:int,
                  simulationYears:int,
                  farmData:pd.DataFrame,
                  treeAttributes:dict=None,
                  strategyAttributes:dict=None):
    """
    takes in data from repository and returns a new,  transformed dataframe that
    tracks events.
    
    year is an int of the  year where the simulation starts.  if the simulation moves forward
    from  the present, the year is the current year. else it is  the  year the simulation
    begins.
    
    simulationYears is the amount of years that the simulation will iterate through. This
    is necessary to make sure the transformed data only captures events within this range. 
    
    farm data is data frame with farmer's plots
    
    tree attributes is dictionary opened from yaml file with attritbutes of trees.
    
    strategy attributes is dictionary opened from yaml file with attributes of strategies.
    
    returns dataframe with events
    
    
    Notes
    -----
    
    as of now, the condition is that intercrop year and prune year are not in the same. but I might be able to figure out how to work that out. 
    """
    
    endYear = year + simulationYears
    
    # iterate through each row of the original plot dataframe
    for i in range(len(farmData)):
        plotID = farmData["plotID"][i]
        farmerName = farmData["farmerName"][i]
        treeType = farmData["treeType"][i]
        numCuerdas =  farmData["numCuerdas"][i]
        startYear = farmData["yearPlanted"][i]
        
        # assume all are planted for initialization
        status = "plant" 

        treeAge = year - startYear

        # check to see that this tree exists in config file
        # _altOrth = [treeAttributes[item]["altOrth"] for item in treeAttributes]
        
        if treeAttributes:
            # isolate the dictionary we are concerned with on this plot
            treeDict = isolateAttributes(attributes=treeAttributes, treeType=treeType)

            # isolate individual variables from this dict
            cuerdaHarvestCap  = treeDict["cuerdaHarvestCap"]
            firstHarvest = treeDict["firstHarvest"]
            fullHarvest = treeDict["fullHarvest"]
            descentHarvest = treeDict["descentHarvest"]
            death = treeDict["death"]

            # calculate death year
            yearsTillDeath = death["year"] - treeAge
            deathYear = year + yearsTillDeath

            # create the initial row for the transformed dataframe
            row = pd.DataFrame([[plotID, farmerName, treeType, numCuerdas, status, 
                                      startYear, deathYear]], columns=["plotID", "farmerName", "treeType", 
                                                "numCuerdas", "status", "startYear",
                                               "deathYear"])
           
            # if this is the first row of the whole transformation
            if (i == 0):
                # initialize the transformation dataframe
                transformedData = row

            else:
                transformedData = pd.concat([transformedData, row], ignore_index=True)
                #transformedData  = transformedData.reset_index(drop = True, inplace = True)
                
                
            # now you've transformed all of the original entries to the new format
            # now you should be iterating through transformed data to add events

            # check to see if replant is in strategy (it always should be)
            if strategyAttributes["replant"]["isReplant"] ==  True:
                replantYear = (deathYear + 1)
            else:
                replantYear = None

            # check to see if prune  is in strategy config
            if strategyAttributes["prune"]["isPrune"] ==  True:
                pruneAge = strategyAttributes["prune"]["age"]
                lifeExtend = strategyAttributes["prune"]["lifeExtend"]
            else:
                pruneAge = None

            # check to see if  intercrop is in strategy config
            if strategyAttributes["intercrop"] == True:
                intercropAge = strategyAttributes["prune"]["age"]
            else:
                intercropAge = None

            # for this specific plot (see plotID),
            # create a row to check against to see if the program needs to continue creating events
            checkRow = row

            # create a  new var for the year of transformation for this plot
            simYear = year
            # create a new var for the tree's age for this plot
            simTreeAge = treeAge

            # iterate through all years of the simulation to check event sequences
            while (simYear < endYear):
               #  isolate dict
                deathYear = checkRow["deathYear"][0]


                if (replantYear):
                    # death takes precedence over pruning 
                    if (simYear == deathYear):
                        # update death year
                        simTreeAge = -1
                        deathYear = (simYear +  1) + death["year"]
                        status = "replant"
                        nextRow = pd.DataFrame([[plotID, farmerName, treeType, numCuerdas, status, replantYear, deathYear]], 
                                            columns=["plotID", "farmerName","treeType", "numCuerdas", "status", "startYear","deathYear"])
                        transformedData  = pd.concat([transformedData, nextRow],  ignore_index=True)
                        checkRow = nextRow
                        simYear += 1
                        simTreeAge += 1
                        
                        # no more than one action per year IF action is death
                        continue


                    elif (pruneAge):
                        if (simTreeAge == pruneAge):
                            # add years proportional to tree's lifespan:
                            addedYears = round((death["year"] * lifeExtend))
                            adjustedDeathYear = (checkRow["deathYear"][0]) + addedYears
                            pruneYear = simYear
                            status = "prune"
                            nextRow = pd.DataFrame([[plotID, farmerName,treeType, numCuerdas, status, pruneYear, adjustedDeathYear]], 
                                                   columns=["plotID", "farmerName","treeType", "numCuerdas", "status", "startYear","deathYear"])
                            transformedData  = pd.concat([transformedData, nextRow],  ignore_index=True)
                            checkRow  = nextRow
                            simYear += 1
                            simTreeAge += 1
                            continue

                        else:
                            simYear += 1
                            simTreeAge += 1
                            continue
                            
                    else:
                        simYear += 1
                        simTreeAge += 1
                        continue

                else:
                    simYear += 1
                    simTreeAge += 1
                    continue



        else:
            print("No tree attributes!!!")
            print(treeType)
            break
            
        
    return(transformedData)