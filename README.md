Classic: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mindthegrow/cafelytics/binder/?urlpath=git-pull?repo=https://github.com/mindthegrow/cafelytics)

Jupyterlab: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mindthegrow/cafelytics/master?urlpath=lab/tree/index.ipynb)


<p align="left">
<a href="https://pypi.org/project/cafelytics/"><img alt="PyPI" src="https://img.shields.io/pypi/v/cafelytics"></a>
<a href="https://github.com/mindthegrow/cafelytics/actions"><img alt="Test Actions Status" src="https://github.com/mindthegrow/cafelytics/actions/workflows/main.yml/badge.svg"></a>
<a href="https://github.com/mindthegrow/cafelytics/actions"><img alt="Build Actions Status" src="https://github.com/mindthegrow/cafelytics/actions/workflows/build.yml/badge.svg"></a>
<a href="https://github.com/mindthegrow/cafelytics/actions"><img alt="Publish Actions Status" src="https://github.com/mindthegrow/cafelytics/actions/workflows/publish.yml/badge.svg"></a>
<a href="https://cafelytics.readthedocs.io/en/stable/?badge=stable"><img alt="Documentation Status" src="https://readthedocs.org/projects/cafelytics/badge/?version=stable"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://coveralls.io/github/mindthegrow/cafelytics?branch=main"><img alt="Coverage Status" src="https://coveralls.io/repos/github/mindthegrow/cafelytics/badge.svg?branch=main"></a>
<a href="https://codecov.io/gh/mindthegrow/cafelytics"><img alt="Coverage Status" src="https://codecov.io/gh/mindthegrow/cafelytics/branch/main/graph/badge.svg?token=HT880PYHPG"></a>
<a href="https://pepy.tech/project/cafelytics"><img alt="Total Downloads" src="https://static.pepy.tech/personalized-badge/cafelytics?period=total&units=abbreviation&left_color=gray&right_color=blue&left_text=downloads"></a>
</p>


# cafélytics ☕️
A basic simulation of a coffee operation. Please pardon the mess as this is a work in progress.


## usage (python cli)

after you have installed the repository and necessary modules (more on this later),first create a fake dataset to run the simulation on using:

```bash
python3 src/cafe/fakeData.py --farms 100 --year 2020 --output data/fakeData.csv
```

Feel free to replace arguments to suit your taste. The arguments above are the defaults that will be ran without specification.

After you've created this dataset, run the simulation using:

```bash
python3 src/cafe/simulateCoOp.py --farm data/fakeData.csv --trees data/trees.yml --years 30 --output testNewFarm.png
```

once again, these are the default arguments.


## contributing
Contributions are welcome. There are many aspects of this project to improve, please see [CONTRIBUTING](/info/CONTRIBUTING.md) for a list of places to start. You may also raise an issue if you have questions or suggestions about this code. 


## license
This software is released as-is, with no guarantee nor warranty. For more details, please see [LICENSE](/info/LICENSE.txt).

