import datetime

import matplotlib.pyplot as plt

from cafe.farm import (
    Config,
    Event,
    Farm,
    guate_harvest_function,
    predict_yield_for_farm,
)


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
    start_year = min([plot.start.year for plot in plotList])
    # start_year = 2020
    for current_year in range(start_year, start_year + numYears + 1):

        configs = (
            Config("e14", name="e14", output_per_crop=125, unit="cuerdas"),
            Config("borbon", name="borbon", output_per_crop=200, unit="cuerdas"),
            Config("catuai", name="catuai", output_per_crop=125, unit="cuerdas"),
            Config("catura", name="catura", output_per_crop=125, unit="cuerdas"),
        )

        species_list = [config.species for config in configs]

        scopes = {
            species: {"type": "species", "def": species} for species in species_list
        }

        harvest_functions = {
            "e14": guate_harvest_function(lifespan=15, mature=5),
            "catura": guate_harvest_function(lifespan=16, mature=4),
            "catuai": guate_harvest_function(lifespan=17, mature=4),
            "borbon": guate_harvest_function(lifespan=30, mature=5),
        }

        events = [
            Event(
                name=f"{species} harvest",
                impact=harvest_functions[species],
                scope=scopes[species],
            )
            for species in species_list
        ]

        start_year = datetime.datetime(2020, 1, 1)
        end_year = datetime.datetime(2021, 1, 1)
        events.append(
            Event(
                "catastrophic overfertilization",
                impact=0.001,
                scope={"type": "species", "def": "borbon"},
                start=start_year,
                end=end_year,
            )
        )

        farm = Farm(plotList)
        thisYearsHarvest = predict_yield_for_farm(
            farm=farm,
            configs=configs,
            events=events,
            time=datetime.datetime(current_year, 1, 1),
        )

        harvestYear.append(current_year)
        # annualHarvest.append(thisYearsHarvest[0])  # inspect single plot
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
    pltYears, pltHarvests = simData

    # get parameters for axes
    mnYear, mxYear = min(pltYears), max(pltYears)
    mxHarvest = max(pltHarvests)

    plt.rcParams["figure.figsize"] = (20, 10)
    fsize = 20  # font size

    plt.axes(xlim=(mnYear, mxYear), ylim=(0, (mxHarvest + (mxHarvest * 0.10))))
    plt.plot(pltYears, pltHarvests, linewidth=4)
    plt.style.use("ggplot")
    plt.title("Yield Forecast", fontsize=(fsize * 1.25))
    plt.xlabel("Year", fontsize=fsize)
    plt.xticks(pltYears, rotation=45)
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
        "-y",
        "--years",
        default=75,
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
