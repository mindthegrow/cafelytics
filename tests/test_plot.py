import pytest
from cafe.farm import Plot
import pandas as pd
import datetime


@pytest.fixture
def series_fixture():
    return pd.Series(
        {"plotID": 0, "treeType": "borbon", "numCuerdas": 1.0, "yearPlanted": 2020}
    )


def test_we_can_instantiate_plot_from_series(series_fixture):
    plot = Plot.from_series(series_fixture)

    info = series_fixture.to_dict()
    assert plot.species == info["treeType"]
    assert plot.size == info["numCuerdas"]
    assert plot.year_planted == info["yearPlanted"]
    assert plot.plot_id == info["plotID"]


def test_that_plots_inherit_time_properties():
    # Arrange
    plot = Plot("a", start=datetime.datetime(2000, 1, 1))
    current_time = datetime.datetime(2020, 1, 1)

    # Act
    age = plot.age(current_time)
    years = plot.years(current_time)
    days = plot.days(current_time)
    mins = plot.mins(current_time)

    # Assert
    assert age == datetime.timedelta(days=7305)
    assert years == 20
    assert days == 20 * 365.25
    assert mins == days * 24 * 60


def test_that_plots_without_start_time_raises_error():
    # Arrange
    plot = Plot("a")
    current_time = datetime.datetime(2020, 1, 1)

    # Act

    # Assert
    with pytest.raises(ValueError):
        plot.age(current_time)
