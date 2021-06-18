import matplotlib.pyplot as plt

from cafe.farm import Config, Farm, predict_yield_for_farm


def simulateCoOp(plotList, numYears, pruneYear=None, growthPattern=None, strategy=None):
    """
    Uses a list of plots, `plotList`, to simulate a cooperative over `numFarms` number of years.

    Returns a list of two lists: `simulation`
        list one, `harvestYear`, represents the year range in the simulation.
        list two, `annualHarvest`, represents the amount of coffee (in lbs) harvested for that  year

    """

    # numPlots = len(plotList)

    annualHarvest = []
    harvestYear = []

    for year in range(numYears):
        #         # each year reset harvest
        #         thisYearsHarvest = 0
        #
        #         for j in range(numPlots):
        #             if pruneYear:
        #                 if j == pruneYear:  # if it's the prune year
        #                     # isPrune = True
        #                     plotList[j].setPruneTrees()
        #
        #             plotList[j].oneYear()  # run this plot through one year of the demo
        #             tempHarvest = plotList[j].totalHarvest
        #             plotList[j].setHarvestZero()  # not cumulative sum, but instead reset
        #             thisYearsHarvest += tempHarvest

        configs = (
            Config("e14", "e14"),
            Config("borbon", "borbon"),
            Config("catuai", "catuai"),
        )
        farm = Farm(plotList)
        thisYearsHarvest = predict_yield_for_farm(farm, configs, events=None)
        print(plotList)
        harvestYear.append(year)
        annualHarvest.append(sum(thisYearsHarvest))

    simulation = [harvestYear, annualHarvest]

    return simulation


def main(args):

    import os

    farmData = args.farm
    # trees = args.trees
    # strategy = args.strategy
    years = args.years
    output = args.output

    if not os.path.exists(farmData):
        raise ValueError(
            (
                f"File: {farmData} does not exist.\n"
                "If you are running default commands and this is your first time"
                "running the simulation, assure you have run:\n"
                "`python3 src/cafe/fakeData.py --farms 100"
                "--year 2020 --output data/fakeData.csv`\n"
                "in the core directory before calling"
                "simulateCoOp.py from the command line."
            )
        )

    print("Importing Data")
    farm_example = Farm.from_csv(farmData)
    farmList = farm_example.plots

    print("Simulating Cooperative")
    simData = simulateCoOp(farmList, years)

    print("Plotting")
    pltYears = simData[0]
    pltHarvests = simData[1]

    # get parameters for axes
    mnYear, mxYear = min(pltYears), max(pltYears)
    mxHarvest = max(pltHarvests)

    plt.rcParams["figure.figsize"] = (20, 10)
    fsize = 20  # font size

    plt.axes(xlim=(mnYear, mxYear), ylim=(0, (mxHarvest + (mxHarvest * 0.10))))
    plt.plot(pltYears, pltHarvests, linewidth=4)
    plt.style.use("ggplot")
    plt.title(
        "Prediction of %d years with no action by demo co-op" % (years),
        fontsize=(fsize * 1.25),
    )
    plt.xlabel("Year", fontsize=fsize)
    plt.ylabel("Total pounds of green coffee produced", fontsize=fsize)
    plt.savefig(output, dpi=100)
    # plt.show()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Parse growth data for simulation.")
    parser.add_argument(
        "-f",
        "--farm",
        default="data/fakeData.csv",
        type=str,
        help="""
           Path to data containing plot details.
           e.g.,  cuerdas, tree types, etc.\n
        """,
    )

    parser.add_argument(
        "-t",
        "--trees",
        default="data/trees.yml",
        type=str,
        help="""
            Name of file (and path from current directory)
            to data containing tree attributes.\n
            Example (& default): --trees data/trees.yml
        """,
    )
    parser.add_argument(
        "-s",
        "--strategy",
        default="data/strategy1.yml",
        type=str,
        help="""
            Name of file (and path from current directory)
            to data containing method, strategy, & approach data.\n
            Example (& default): --strategy intervention/strategy1.yml
        """,
    )

    parser.add_argument(
        "-y",
        "--years",
        default=30,
        type=int,
        help="""
            Number of years that should be iterated
            through in the simulation (default=30).\n
        """,
    )

    parser.add_argument(
        "-o",
        "--output",
        default="testNewFarm.png",
        type=str,
        help="Desired name of plot output file (default=testNewFarm.png).",
    )

    args = parser.parse_args()

    main(args)
