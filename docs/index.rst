**********
cafelytics
**********

This is the documentation of the **cafelytics** library.


.. include:: ../README.rst
   :end-before: badge-header


.. warning::
  This website is under active construction. Please report incomplete documentation.
  Last edited: |today|


Example Usage
=============
.. code-block:: python

   from cafe.farm import Plot
   plot_data = {"plotID": 0, "treeType": "borbon", "numCuerdas": 1.0, "yearPlanted": 2000}
   plot = Plot.from_dict(plot_data)
   print(plot)


Contents
========

.. toctree::
   :hidden:

   self


.. toctree::
   :maxdepth: 2

   Project Description <about>
   Module Reference <api/modules>
   License <license>
   Authors <authors>
   Changelog <changelog>

   Github <https://github.com/mindthegrow/cafelytics>


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _toctree: http://www.sphinx-doc.org/en/master/usage/restructuredtext/directives.html
.. _reStructuredText: http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html
.. _references: http://www.sphinx-doc.org/en/stable/markup/inline.html
.. _Python domain syntax: http://sphinx-doc.org/domains.html#the-python-domain
.. _Sphinx: http://www.sphinx-doc.org/
.. _Python: http://docs.python.org/
.. _Numpy: http://docs.scipy.org/doc/numpy
.. _SciPy: http://docs.scipy.org/doc/scipy/reference/
.. _matplotlib: https://matplotlib.org/contents.html#
.. _Pandas: http://pandas.pydata.org/pandas-docs/stable
.. _Scikit-Learn: http://scikit-learn.org/stable
.. _autodoc: http://www.sphinx-doc.org/en/stable/ext/autodoc.html
.. _Google style: https://github.com/google/styleguide/blob/gh-pages/pyguide.md#38-comments-and-docstrings
.. _NumPy style: https://numpydoc.readthedocs.io/en/latest/format.html
.. _classical style: http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists
