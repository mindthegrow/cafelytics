# -*- coding: utf-8 -*-

import pytest
import cafe.fakeData as fd


__author__ = "Mathematical Michael"
__copyright__ = "Mathematical Michael"
__license__ = "mit"


def test_empty_fake_data():
    fakedata = fd.fakeData()
    with pytest.raises(AssertionError):
        assert len(fakedata) == 1 # check num farms in dataframe
