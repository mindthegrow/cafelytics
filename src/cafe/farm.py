import statistics as stats

class Farm:
    
    
    def __init__(self, farmerName:str='Farmer',
                 cuerdas:float=1,
                 treeType:str='Borbón',
                 initialAgeOfTrees:int=1,
                 sowDensity:int=333,
                 pruneYear:int=None,
                 treeAttributes:dict=None): # use self to declare namespace
        self.farmerName = farmerName

        self.inheretTreeProperties(treeType, treeAttributes)

        self.totalCuerdas = cuerdas
        self.sowDensity = sowDensity 
        self.totalTrees = int(round((cuerdas * sowDensity), 0))

        
        # TODO: let these be set by user?
        # initialize variables for pruning so if/else can deal with objects
        
        
        self.pruneYear = pruneYear
        self.pruneCount = 0    
        
        self.initialAgeOfTrees= initialAgeOfTrees

        
        # initialize trees in a list so if we plant another
        # set of differently aged trees we can add (indicies must match)
        self.trees = [self.setTrees()] # quantity of trees per set
        self.ageOfTrees = [self.initialAgeOfTrees] # age of trees
        
        
        self.treesInProd = self.getTreesInProd()
        
        # pull initial sow density because the other will change
        self.harvestPerTree = self.cuerdaHarvestCap / sowDensity 
        
        # if plants are added or if others die
        self.totalHarvest = 0 # pounds

        
    def setTrees(self):
        
        
        numTreesRaw = self.totalCuerdas * self.sowDensity
        numTrees = int(round(numTreesRaw, 0))
        
        return(numTrees)
        
    def inheretTreeProperties(self, treeType, treeAttributes):
        
        """
        Based on the argument treeType in the initializer function, assign parameters for the respective
        life & production patterns of the trees on the cuerda.
        
        The following property assignments were developed from data collected from the co-op in 2014
    
        """
        treeType = treeType.lower() # convert to lower case for easier parsing
        
        if treeAttributes:
            keys = list(treeAttributes.keys())
            altOrth = [treeAttributes[key]['altOrth'] for key in treeAttributes]
            # tipos = keys + altOrth # all of the possible spellings for the tree types
            
            if treeType in keys:
                treeDict = treeAttributes[treeType]
                
            elif treeType in altOrth:
                keyPair = [(key, treeAttributes[key]['altOrth']) for key in treeAttributes]
                _treeType = ''
                for i,e in enumerate(keyPair):
                    if treeType == e[1]:
                        _treeType = e[0]
                
                treeDict = treeAttributes[_treeType]
                
            else:
                raise AttributeError(
                """
                '%s' is not a recognized value (orthography) in the `treeAttributes` dict.
                
                """%(treeType))
                
            self.treeType = treeDict['treeType']
            self.firstHarvest = treeDict['firstHarvest']
            self.fullHarvest = treeDict['fullHarvest']
            self.descentHarvest = treeDict['descentHarvest']
            self.death = treeDict['death']
            self.cuerdaHarvestCap = treeDict['cuerdaHarvestCap']
        
        # as soon as yaml imports are tested, this can be deleted:
        # temporary stand-in for variable testing
        else:
            if (treeType =='borbon') or (treeType == 'borbón'):
                # year of first harvest and proportion of harvest until full
                self.firstHarvest = {'year': 4, 'proportion': 0.2} 
                # year of first harvest and proportion of harvest
                self.fullHarvest = {'year': 5, 'proportion': 1.0}  
                 # year that production descends and annual proportion descent
                self.descentHarvest = {'year': 28, 'proportionDescent': 0.2}
                # self.pruneHarvest = {'yearShift': -5, 'proportionAscent': 0.2} 
                # year in which trees are expelled from dataset
                self.death = {'year': 30} 
                self.cuerdaHarvestCap = 200 # units, in this case lbs, per cuerda
                self.treeType = 'borbon'

                loop = False
                
                
            elif (treeType =='catuaí') or (treeType == 'catuai'):
                # year of first harvest and proportion of harvest until full
                self.firstHarvest = {'year': 3, 'proportion': 0.2} 
                # year of first harvest and proportion of harvest
                self.fullHarvest = {'year': 4, 'proportion': 1.0} 
                # year that production descends and annual proportion descent
                self.descentHarvest = {'year': 15, 'proportionDescent': 0.2} 
                # self.pruneHarvest = {'yearShift': -5, 'proportionAscent': 0.2} #
                self.death = {'year': 17} 
                self.cuerdaHarvestCap = 125 # units, in this case lbs, per cuerda
                self.treeType = 'catuai'

                loop = False

            elif (treeType == 'e14'):
                self.firstHarvest = {'year': 4, 'proportion': 0.2} 
                self.fullHarvest = {'year': 5, 'proportion': 1.0}  
                self.descentHarvest = {'year': 13, 'proportionDescent': 0.2} 
                # self.pruneHarvest = {'yearShift': -5, 'proportionAscent': 0.2} 
                self.death = {'year': 15} 
                self.cuerdaHarvestCap = 125 
                self.treeType = 'e14'
                
                loop = False

            elif (treeType == 'caturra') or (treeType == 'catura'):
                self.firstHarvest = {'year': 3, 'proportion': 0.2} 
                self.fullHarvest = {'year': 4, 'proportion': 1.0}  
                self.descentHarvest = {'year': 14, 'proportionDescent': 0.2} 
                # self.pruneHarvest = {'yearShift': -5, 'proportionAscent': 0.2} 
                self.death = {'year': 16}

                self.cuerdaHarvestCap = 125 
                self.treeType = 'caturra'                    
                    
    def oneYear(self):
        """
        
        This function takes this entire set of trees and adjusts the member values in the class to grow/change/produce accordingly.
        The function uses preset parameters for the specific tree type to guide the flow-control.
        
        """
        if len(self.trees) == len(self.ageOfTrees):
        
            for treeIndex, treeQuant in enumerate(self.trees):
                treeAge = self.ageOfTrees[treeIndex]
                
                if (self.pruneYear) or (self.pruneYear == 0):
                    # make sure to:
                    # (1) still age the trees
                    # (2) make them produce less for a bit!? How!?
                    # (3) increase total production or lifespan long-term

                    # trees still age when they're pruned
                    self.ageOfTrees[treeIndex] += 1 
                    
                    # lower the countdown to full yield by one year
                    self.pruneCount -= 1 

                    # it is no longer a prune year and so this shifts it back to cycle
                    self.pruneYear = False 
                    
                    # do trees produce year they're pruned? How much?
                    product = 0 
                    self.totalHarvest += product

                elif (self.pruneCount > 0):

                    subtract = self.pruneDelay * self.pruneCount

                    if (subtract > 1.0):
                        break
                        print("Impossible proportion as a result of pruneCount and pruneDelay.")
                        print("Please assure product of pruneCount and pruneDelay is always <= 1.0")

                    product = (self.harvestPerTree * treeQuant) - (self.harvestPerTree * (subtract))

                    # trees still age when they're pruned
                    self.ageOfTrees[treeIndex] += 1 
                    # lower the countdown to full yield by one year
                    self.pruneCount -= 1

                elif (treeAge < self.firstHarvest['year']):


                    # product = 0 #in this range the trees produce nothing, but they still move up in age for the year
                    # self.totalHarvest += product
                    product = 0
                    self.totalHarvest += product
                    self.ageOfTrees[treeIndex] += 1
                    


                elif (treeAge >= self.firstHarvest['year']) and (treeAge < self.fullHarvest['year']):

                    
                    product = (self.harvestPerTree * treeQuant) * self.firstHarvest['proportion']
                    self.totalHarvest += product
                    # assure to reference the list and not the copy

                    self.ageOfTrees[treeIndex] += 1 

                elif ((treeAge >= self.fullHarvest['year']) and (treeAge < self.descentHarvest['year'])):

                    product = (self.harvestPerTree * treeQuant) * self.fullHarvest['proportion']
                    self.totalHarvest += product
                    self.ageOfTrees[treeIndex] += 1


                elif ((treeAge >= self.descentHarvest['year']) and (treeAge < self.death['year'])):

                    yearsIntoDescent = self.ageOfTrees[treeIndex] - self.descentHarvest['year']
                    proportion = self.fullHarvest['proportion'] - (yearsIntoDescent * self.descentHarvest['proportionDescent'])
                    product = (self.harvestPerTree * treeQuant) * proportion
                    self.totalHarvest += product
                    self.ageOfTrees[treeIndex] += 1


                elif (treeAge == self.death['year']):
                    self.ageOfTrees[treeIndex] += 1
                    continue


                elif (treeAge >= (self.death['year'] + 1)):
                    # if it is the year after the tree died...
                    
                    self.ageOfTrees[treeIndex] = 0 # plant new trees

                else:
                    print("""The number: %d, list index: %d is out of range:
                    a tree can not be less than 0 years old, and a tree of this type can not be more than
                    %d years of age"""%(treeAge, treeIndex, self.death['year']))
                    break

            #self.trees[:] = [age for age in self.trees if (age < self.death['year'])] # call-by-reference overwrite of ls removing dead trees. 
            # assure this ^ is outside of the loop & assure the list references the full index with '[:]'
            #livingTrees = [age for age in self.trees if (age < self.death['year'])]
            #self.totalTrees = len(livingTrees)
            
            
            #if self.totalTrees > 0:
                #self.averageAgeOfTrees = stats.mean(self.trees)
                #self.sowDensity = self.totalTrees / self.totalCuerdas

                
    def addTreesAuto(self, numTrees: int, ages: int): 
        """
        Automatically add a new set of trees to existing cuerdas: this implies an increase in sowing density. Possible implications are intercropping between existing trees/rows.
        
        Note: this function will adjust the average age of trees, the sow/plant density, 
        and the total # of trees stored in self.averageAgeOfTrees, self.sowDensity, and self.totalTrees 
        
        Parameters
        ----------
        self : class
            required to change-by-reference members of the class
            
        number: int
            the number of trees the user will add to the plot
            
        ages : int
            the age of the trees (which translates to the element in the list)
            the user will add to the set. default value is 0 because most
            trees are planted/added as seeds/saplings, however the param
            is adjustable because it might be useful if adding new land with
            existing trees.
            
        """
                        
        self.trees.append(numTrees)
        self.ageOfTrees.append(ages)
            
        self.totalTrees += numTrees
        self.sowDensity = self.totalTrees * self.totalCuerdas
        
        #self.averageAgeOfTrees = stats.mean(self.ageOfTrees)
            
    
    
    def setPruneTrees(self):
        """
        Takes in `pruneYear` bool, sets self.pruneYear to equiveleant value. 
        
        """
        self.pruneYear = True
        
        # how much the total yield will increase after trees grow back from pruning (i.e. after pruneCount years)
        self.pruneGrowth = 0.10 
        
        # current yield - (current yield * (this proportion * countyear)) = yield for that year.
        self.pruneDelay = 0.20
        # caution! The product of this proportion ^^^ and count year SHANT EXCEED 1.0 otherwise the 
        # program will simulate impossibilities
        
       
        self.pruneCount = 3
            
            # increase total yield-per-tree to 10% higher
        self.harvestPerTree = self.harvestPerTree + (self.pruneGrowth * self.harvestPerTree)
            
    def getTreesInProd(self):
        """
        Returns the total number of trees that are in production. Does not care whether the trees are producing at 100% or 5%, if they are producing, they are 'in production.' See Farm.getProdData() for more statistics. 
        """
        treesInProd = 0
            
            
            
        if len(self.ageOfTrees) == len(self.trees): # indicies must match
            for index,age in enumerate(self.ageOfTrees):
                if (self.pruneYear == True):
                    prod = 0
                    treesInProd += prod
                    
                elif ((age >= self.firstHarvest['year']) and (age <= self.death['year'])):
                    prod = self.trees[index]
                    treesInProd += prod
                    
                    
        return(treesInProd)
        
            
    def getHarvest(self):
        """
        
        return the total harvest
        
        """
        return(self.totalHarvest)
    
    def setHarvestZero(self):
        """
        
        You must set Harvest to zero after each iteration of oneYear if you want to keep track of annual production
        as opposed to total time production
        
        """
        self.totalHarvest = 0
        
        
        
