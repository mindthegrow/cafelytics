Classic: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mathematicalmichael/cafelytics/binder/?urlpath=git-pull?repo=https://github.com/mathematicalmichael/cafelytics)

Jupyterlab: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mathematicalmichael/cafelytics/master?urlpath=lab/tree/index.ipynb)

# cafélytics ☕️
A basic simulation of a coffee operation. Run it right in your browser by clicking on the Binder badge above.


## caveats
- This code was initially written in 2012, when I had only a semester's worth of coding experience. It is not pretty, nor efficient, but it does work.
- This code has been re-formatted to work with GNU Octave but was originally written in Matlab.
- By all means feel free to contribute to this code. For more details, please see the [contributing](#contributing) section.

## dependencies
Listed in [binder/apt.txt](/binder/apt.txt)

## usage
Suggested: Click the binder badge.

Option 1: Open the [Worksheet](/src/Worksheet.m), which has annotated instructions for setting up the conditions for the simulation. It is meant to be run top-down, first computing a reference baseline before comparing it to some intervention strategy. If you are using the binder badge (or simply editing in your own Octave-equipped Jupyterlab instance), you can right-click in this file and select "Create Console for Editor," which will give you a Matlab-like interface that is attached to this file.

Option 2: Open the [index.ipynb](index.ipynb) and use it to interact with the simulations directly.

## contributing
Contributions are welcome. There are many aspects of this project to improve, please see [CONTRIBUTING](/info/CONTRIBUTING.md) for a list of places to start. You may also raise an issue if you have questions or suggestions about this code. 

## license
This software is released as-is, with no guarantee nor warranty. For more details, please see [LICENSE](/info/LICENSE.txt).

## python cli

after you have installed the repository and necessary modules (more on this later),first create a fake dataset to run the simulation on using:

```bash
python3 src/cafe/fakeData.py --farms 100 --year 2020 --output data/fakeData.csv
```

Feel free to replace arguments to suit your taste. The arguments above are the defaults that will be ran without specification.

After you've created this dataset, run the simulation using:

```bash
python3 src/cafe/simulateCoOp.py --farm data/fakeData.csv --years 30 --output testNewFarm.png
```

once again, these are the default arguments.
