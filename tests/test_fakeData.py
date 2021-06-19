# -*- coding: utf-8 -*-

# import pytest
import cafe.fakeData as fd
from unittest import mock
import pandas as pd

__author__ = "Mathematical Michael"
__copyright__ = "Mathematical Michael"
__license__ = "mit"


@mock.patch.object(pd.DataFrame, "to_csv")
def test_empty_fake_data(mock_to_csv):
    # Arrange

    # Act
    fakedata = fd.fakeData()

    # Assert
    assert len(fakedata) == 1
    mock_to_csv.assert_called_once_with("data/fakeData.csv", index=False)
