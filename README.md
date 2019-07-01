[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/mathematicalmichael/coffeecode/binder/?urlpath=git-pull?repo=https://github.com/mathematicalmichael/coffeecode?filepath=index.ipynb?urlpath=lab/)

# coffeecode
A basic simulation of a coffee operation.


## caveats
- This code was initially written in 2012, when I had only a semester's worth of coding experience. It is not pretty, nor efficient, but it does work.
- This code has been re-formatted to work with GNU Octave but was originally written in Matlab.

## dependencies
Listed in [binder/apt.txt](/binder/apt.txt)

## usage
Suggested: Click the binder badge.

Option 1: Open the [Worksheet](/src/Worksheet.m), which has annotated instructions for setting up the conditions for the simulation. It is meant to be run top-down, first computing a reference baseline before comparing it to some intervention strategy. If you are using the binder badge (or simply editing in your own Octave-equipped Jupyterlab instance), you can right-click in this file and select "Create Console for Editor," which will give you a Matlab-like interface that is attached to this file.

Option 2: Open the [index.ipynb](index.ipynb) and use it to interact with the simulations directly.