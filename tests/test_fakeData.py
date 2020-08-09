# -*- coding: utf-8 -*-

import pytest
import cafe.fakeData as fd
import os

__author__ = "Mathematical Michael"
__copyright__ = "Mathematical Michael"
__license__ = "mit"


def test_empty_fake_data():
    fakedata = fd.fakeData()
    assert len(fakedata) == 1 # check num farms in dataframe
    # things below here will pass if they RAISE an error.
    # these are expected "failure modes", e.g. check that an error message was printed.    
    # with pytest.raises(TypeError):
    os.system('python src/cafe/fakeData.py')
