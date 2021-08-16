.. image:: https://img.shields.io/pypi/v/cafelytics
    :alt: PyPI
    :target: https://pypi.org/project/cafelytics/

.. image:: https://github.com/mindthegrow/cafelytics/actions/workflows/main.yml/badge.svg
    :alt: Test Actions Status
    :target: https://github.com/mindthegrow/cafelytics/actions

.. image:: https://github.com/mindthegrow/cafelytics/actions/workflows/build.yml/badge.svg
    :alt: Build Actions Status
    :target: https://github.com/mindthegrow/cafelytics/actions

.. image:: https://github.com/mindthegrow/cafelytics/actions/workflows/publish.yml/badge.svg
    :alt: Publish Actions Status
    :target: https://github.com/mindthegrow/cafelytics/actions

.. image:: https://readthedocs.org/projects/cafelytics/badge/?version=stable
    :alt: Documentation Status
    :target: https://cafelytics.readthedocs.io/en/stable/?badge=stable

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :alt: Code Style: black
    :target: https://github.com/psf/black

.. image:: https://coveralls.io/repos/github/mindthegrow/cafelytics/badge.svg?branch=main
    :alt: Coverage Status
    :target: https://coveralls.io/github/mindthegrow/cafelytics?branch=main

.. image:: https://static.pepy.tech/personalized-badge/cafelytics?period=total&units=abbreviation&left_color=gray&right_color=blue&lef    t_text=downloads
    :alt: Total Downloads
    :target: https://pepy.tech/project/cafelytics


.. badge-header


cafélytics ☕️
**************

A basic simulation of a coffee operation. Please pardon the mess as this is a work in progress.
This is a model that enables forecasting and experimentation under uncertainty, with the goal of steady year-over-year agricultural yields.
It can help address questions such as:

* *when should I expand / how much?*
* *what will the impacts of various crop diversification strategies be?*
* *how can I plan around disaster recovery and mitigation of lost income?*
* *what would cooperative-wide yields look like if more farmers joined? what about if some left?*


usage (python cli)
==================

The dataset provided can be used for forecasting with

.. code-block:: bash

   make run


which is equivalent to

.. code-block:: bash

   python3 simulate.py --farm data/fakeData.csv --years 75 --output testNewFarm.png


and will output this plot, representing the outputs of a collective of farmers over a seventy-five year time span:

.. image:: https://user-images.githubusercontent.com/40366263/126934177-7353103f-bd90-4a7a-9085-f409a69d1b66.png


Some farmers who joined the cooperative had trees that were already very mature, so this simulation starts back in 1991 to show their hypothetical contributions towards the total yield of the group (in other words, their membership start date is not considered as a factor in this simulation at this time).


contributing
============
Contributions are welcome. There are many aspects of this project to improve, please see `CONTRIBUTING.md <https://github.com/mindthegrow/cafelytics/blob/main/CONTRIBUTING.md>`_ for a list of places to start.
You may also raise an `issue <https://github.com/mindthegrow/cafelytics/issues/>`_ if you have questions or suggestions about this code.


license
=======
This software is released as-is, with no guarantee nor warranty. For more details, please see `LICENSE.txt <https://github.com/mindthegrow/cafelytics/blob/main/LICENSE.txt>`_.


demo
====
Try it in your browser!

.. raw:: html

   <a href="https://mybinder.org/v2/gh/mindthegrow/cafelytics/HEAD/?urlpath=/lab"><img alt="Launch Binder" src="https://mybinder.org/badge_logo.svg"></a>


