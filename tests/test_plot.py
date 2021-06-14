import pytest
from cafe.farm import Plot
import pandas as pd


@pytest.fixture
def series_fixture():
    return pd.Series(
        {
            "plotID": 0,
            "treeType": "borbon",
            "numCuerdas": 1.0,
            "yearPlanted": 2020,
        }
    )


def test_we_can_instantiate_plot_from_series(series_fixture):
    plot = Plot.from_series(series_fixture)

    info = series_fixture.to_dict()
    assert plot.species == info["treeType"]
    assert plot.size == info["numCuerdas"]
    assert plot.year_planted == info["yearPlanted"]
    assert plot.plot_id == info["plotID"]
