# -*- coding: utf-8 -*-

import pytest
import cafe.farm as cf
import numpy as np

__author__ = "Mathematical Michael"
__copyright__ = "Mathematical Michael"
__license__ = "mit"


def test_farm_instantiation_defaults():
    test_farm = cf.Farm()
    # TODO: add some basics here and assert them
    assert test_farm.totalCuerdas == 1
    assert test_farm.pruneYear == 1
    #with pytest.raises(AssertionError):

