import random
from faker import Faker
import pandas as pd

"""

Copmpile a fake dataset resembling the dataset Michael collected on his trip to Guatemala in.

The fake dataset uses relative proportions of the tree types in the original dataset as
probabilities for selection of the tree types of this dataset. So, although it is not the original data--
and the names are fake!--it resembles the patterns of the co-op.

"""

fake = Faker('es_MX')

def fakeData(startYear, numFarms, numFarmers):
    # utilize probabilities of original dataset
    freqProb = {'borbon': 0.5534, 'catuai': 0.4191, 'e14': 0.0046, 'catura': 0.02299}
    treeNames = list(freqProb.keys())
    trees = random.choices(treeNames, weights = list(freqProb.values()), k = numFarms)
    farmers = [fake.name() for i in range(numFarmers)]
    randFarmers = rand.choices(farmers, k = numFarms)

    yearPlanted = []
    cuerdas = []
    plotID = []

    for i,e in enumerate(trees):
        # (1) get year planted
        # borbons have a longer lifespan
        if e == 'borbon':
            age = random.randint(0,29)

        else:
            age = random.randint(0, 14)

        _yearPlanted = startYear - ages
        yearPlanted.append(_yearPlanted)

        # (2) get number of  cuerdas
        _cuerdas = random.randint(0,10)
        cuerdas.append(_cuerdas)

        # (3) get unique plot ID
        _plotID = i
        plotID.append(_plotID)

    fakeFarms = pd.DataFrame(zip(plotID, randFarmers, trees, cuerdas, yearPlanted),
    columns = ["plotID", "farmerName", "treeType", "cuerdas", "yearPlanted"])
