import random
from faker import Faker
import pandas as pd
from datetime import date

"""

Copmpile a fake dataset resembling the dataset
Michael collected on his trip to Guatemala in.

The fake dataset uses relative proportions of the
tree types in the original dataset as

probabilities for selection of the tree types of this dataset.

So, although it is not the original data--
and the names are fake!--it resembles the patterns of the co-op.
"""
# get current year for auto assgn
currentDate = date.today()
defaultYear = currentDate.year

fake = Faker("es_MX")


def fakeData(
    numFarms=1, numFarmers=1, startYear=defaultYear, outputFile="data/fakeData.csv"
):
    """
    Takes in the desired number of farms (i.e. rows) and farmers, as well as the year
    that the simulation is to start in, and returns a pandas DataFrame with all of the
    information required to run the simulation.

    """
    # utilize probabilities of original dataset
    freqProb = {"borbon": 0.5534, "catuai": 0.4191, "e14": 0.0046, "catura": 0.02299}
    treeNames = list(freqProb.keys())
    trees = random.choices(treeNames, weights=list(freqProb.values()), k=numFarms)
    farmers = [fake.name() for i in range(numFarmers)]
    randFarmers = random.choices(farmers, k=numFarms)

    age = []
    yearPlanted = []
    cuerdas = []
    plotID = []
    proportion = []

    for i, e in enumerate(trees):
        # (1) get year planted and age
        # borbons have a longer lifespan
        _age = random.randint(0, 14)

        _yearPlanted = startYear - _age
        yearPlanted.append(_yearPlanted)
        age.append(_age)

        # (2) get number of  cuerdas
        _cuerdas = random.randint(0, 10)
        cuerdas.append(_cuerdas)

        # (3) get unique plot ID
        _plotID = i
        plotID.append(_plotID)

        # (4) get random proportion
        _proportion = random.uniform(0.7, 1.0)
        proportion.append(_proportion)

    fakeFarms = pd.DataFrame(
        zip(plotID, randFarmers, trees, cuerdas, yearPlanted, age, proportion),
        columns=[
            "plotID",
            "farmerName",
            "treeType",
            "numCuerdas",
            "yearPlanted",
            "ageOfTrees",
            "productionProportion",
        ],
    )

    fakeFarms.to_csv(outputFile, index=False)
    return fakeFarms


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Parse arguments for creating fake data spreadsheet"
    )
    parser.add_argument(
        "-f",
        "--farms",
        default=100,
        type=int,  # string type works well for
        help="""
            Number of farms (i.e. the number of rows)
            desired for the output dataset.
        """,
    )

    parser.add_argument(
        "-n",
        "--names",  # currently this information is stored in the Cuerdas class
        default=40,
        type=int,  # string type works well for
        help="""
            Number of fake names (farmers) desired as owners of of the farms.
        """,
    )

    parser.add_argument(
        "-y",
        "--year",
        default=defaultYear,
        type=int,  # string type works well for
        help="""
            The year in which the simulation will begin
            (this is important because all of the trees are
            'planted' relative to this date)
        """,
    )
    parser.add_argument(
        "-o",
        "--output",
        default="data/fakeData.csv",
        type=str,  # string type works well for
        help="""
            Desired name of file (and path from current directory)
            for the output CSV file.
        """,
    )

    args = parser.parse_args()

    farms = args.farms
    names = args.names
    year = args.year
    output = args.output
    df = fakeData(numFarms=farms, numFarmers=names, startYear=year, outputFile=output)
    print("Demonstration of output data:")
    print(df)
