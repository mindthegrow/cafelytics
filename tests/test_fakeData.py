# -*- coding: utf-8 -*-

import pytest
import cafe.fakeData as fd


__author__ = "Mathematical Michael"
__copyright__ = "Mathematical Michael"
__license__ = "mit"


def test_farm_instantiation_defaults():
    fakedata = fd.fakeData()
    with pytest.raises(AssertionError):
        len(fakedata) == 1 # check num farms in dataframe
