import numpy as np
import random
from faker import Faker
import pandas as pd

"""

Copmpile a fake dataset resembling the dataset Michael collected on his trip to Guatemala in.

The fake dataset uses relative proportions of the tree types in the original dataset as 
probabilities for selection of the tree types of this dataset. So, although it is not the original data--
and the names are fake!--it resembles the patterns of the co-op.

"""

fake = Faker('es_MX') # faker does not have options for any American Spanish varieties besides Mexico,
# so we select Mexico because (1) you can find coffee plantations in Mexico, and (2) it is just north of Guatemala

numFarmers = 40 # how many farms/farmers we want in our fake dataset


# list the species of trees plated on the co-op
treeNames = ['borbon', 'catuai', 'e14', 'catura']

# utilize probabilities of original dataset
freqProb = {'borbon': 0.5534, 'catuai': 0.4191, 'e14': 0.0046, 'catura': 0.02299} 

# even if order changes, the probabilities still correspond to the strings
#lsTreeTypes = random.choices()


lsOfFarmers = [] # create a list to append these farmers to
lsOfTrees = [] # create a list to hold lists for each farmer's trees
lsOfCuerdas = [] # creat a list to hold the number of cuerdas
lsOfAges = []
lsOfProportions = []

for i in range(numFarmers):
    lsOfFarmers.append(fake.name()) # append the fake name, who is the owner of the farm
    upperBounds = 4 # max num of tree types a farmer may have
    lowerBounds = 1 # min num of tree types a farmer may have
    numStrains = random.randint(lowerBounds,upperBounds) # decide how many tree types that one farmer will own
    
    while True:
        # create a trained but random list of farmer's trees weighted by the results from Guatemala
        # assure k is large enough that we're guarenteed to get 4 unique values without iterating too many times
        sampleLs = random.choices(treeNames, weights = (freqProb[treeNames[0]], freqProb[treeNames[1]],
                                                  freqProb[treeNames[2]], freqProb[treeNames[3]]), k = 500)
        
        sampleSet = set(sampleLs)
        
        if len(sampleSet) >= upperBounds:
            break
            
    
    
    # sample from this list to the size (also prevents repeats)
    treeLs = []#random.sample(sampleLs, numStrains)
    firstSelect = random.choice(sampleLs)
    treeLs.append(firstSelect)
    counter = len(treeLs)
    
    # fill the list to the selected sample size
    while counter < numStrains:
        selection = random.choice(sampleLs)
        if selection not in treeLs: # assure no repeats per farmer
            treeLs.append(selection)
            counter += 1
            
    
    cuerdaLs = []
    plotAgeLs = []
    proportionProduct = []
    

    for j in range(len(treeLs)): # iterate through the number of plots this farmer has
        numCuerdas = random.randint(1,10) # assign a random number
        cuerdaLs.append(numCuerdas)
        
        if treeLs[j] == 'borbon': # borbons have a longer lifespan
            plotAge = random.randint(0,29)
        
        else:
            plotAge = random.randint(0, 14)
            
        plotAgeLs.append(plotAge)
        
        _proportionProduct = random.random(0.7, 1.0)
        proportionProduct.append(_proportionProduct)
            
     
    # append the lists of len(numStrains) to their stuff
    lsOfTrees.append(treeLs)
    lsOfCuerdas.append(cuerdaLs)
    lsOfAges.append(plotAgeLs)
    lsOfProportions.append(proportionProduct)
    
    
    
totalFarmers = len(lsOfFarmers)
totalListsCuerdas = len(lsOfCuerdas)
totalListsTrees = len(lsOfTrees)
totalListsAges = len(lsOfAges)
totalProportions = len(lsOfProportions)
    
print("Farmers: ", totalFarmers)
print("Lists of Trees: ", totalListsTrees)
print("Lists of Cuerdas: ", totalListsCuerdas)
print("Lists of ages: ", totalListsAges)

print(lsOfFarmers)
print(lsOfCuerdas)
print(lsOfTrees)
print(lsOfAges)


finalFarmers = []
finalTrees = []
finalCuerdas = []
finalAges = []
finalProportions = []

# all lists need to be the same length to iterate through these
if (totalFarmers == totalListsTrees) and (totalFarmers == totalListsAges) and (totalFarmers == totalListsCuerdas) and (totalFarmers == totalProportions):
    for index, farmerName in enumerate(lsOfFarmers):
        cuerdaLs = lsOfCuerdas[index]
        treeLs = lsOfTrees[index]
        ageLs = lsOfAges[index]
        proportionLs = lsOfProportions[index]
        
        if (len(cuerdaLs) == len(treeLs)) and (len(cuerdaLs) == len(ageLs)):
            
            for j in range(len(cuerdaLs)): # each tree type for each farmer gets its own row
                finalFarmers.append(farmerName)
                finalTrees.append(treeLs[j])
                finalCuerdas.append(cuerdaLs[j])
                finalAges.append(ageLs[j])
                finalProportions.append(proportionLs[j])
                
                
                
                
finalData = pd.DataFrame(zip(finalFarmers,finalTrees,finalCuerdas,finalAges,finalProportions), columns = 
                         ['farmerName', 'treeType', 'numCuerdas', 'ageOfTrees','proportions'])              

finalData.to_csv('data/demoData.csv')
