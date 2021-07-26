# -*- coding: utf-8 -*-
import datetime
import pytest
from cafe.farm import (
    Config,
    Plot,
    Farm,
    Event,
    find_config,
    predict_yield_for_farm,
    predict_yield_for_plot,
)
from typing import Union, Callable

# import warnings

from unittest import mock
from pandas import DataFrame

__author__ = "Mathematical Michael <Pilosov>"
__copyright__ = "Mind the Math, LLC"
__license__ = "mit"


@pytest.fixture()
def configs():
    return (
        Config("a", "a"),
        Config("b", "b-intercroppped"),
        Config("c", "c"),
        Config("d", "d"),
    )


@pytest.fixture()
def farm(start_date):
    return Farm([Plot(species="a", start=start_date)])


@pytest.fixture()
def farm_dict():
    return {
        "plotID": {0: 0, 1: 1, 2: 2, 3: 3, 4: 4},
        "farmerName": {
            0: "Lic. Catalina Arce",
            1: "Dr. Francisca Molina",
            2: "Gilberto Leonel Márquez Vásquez",
            3: "Eloisa Aldonza Lozada",
            4: "Elsa Emilia Barrera Bahena",
        },
        "treeType": {0: "catuai", 1: "borbon", 2: "catuai", 3: "borbon", 4: "catuai"},
        "numCuerdas": {0: 0, 1: 3, 2: 4, 3: 3, 4: 3},
        "yearPlanted": {0: 2016, 1: 2015, 2: 2014, 3: 2020, 4: 2013},
        "ageOfTrees": {0: 4, 1: 5, 2: 6, 3: 0, 4: 7},
        "productionProportion": {0: 0.95, 1: 0.75, 2: 0.95, 3: 0.95, 4: 0.87},
    }


@pytest.fixture()
def event_impact_function():
    def f(time, **kwargs):
        start = kwargs["start"].year
        age = time - start
        if age == 0:
            return 0
        if age < 3:
            return 0.25 * age
        if age < 30:
            return 1.0
        if age < 33:
            return 1 - 0.25 * (age - 30)
        return 0

    return f


@pytest.fixture()
def growth_function() -> Callable:
    def f(time: Union[datetime.datetime, float], plot: Plot, **kwargs):
        start = plot.start.year
        year = time if isinstance(time, (float, int)) else time.year
        age = year - start
        if age == 0:
            return 0
        if age < 3:
            return 0.25 * age
        if age < 30:
            return 1.0
        if age < 33:
            return 1 - 0.25 * (age - 30)
        return 0

    return f


@pytest.fixture()
def start_date():
    return datetime.datetime(2020, 1, 1)


@pytest.fixture()
def dummy_event(start_date):
    return Event("some_event", start_date)


# CONFIG TESTS
@pytest.fixture()
def expected_proportions_for_harvest():
    proportion = [0.0, 0.25, 0.5, 1.0, 1.0, 0.75, 0.5, 0.0]
    years = [2020, 2021, 2022, 2023, 2050, 2051, 2052, 2053]
    return years, proportion


@pytest.fixture()
def expected_proportions_for_event():
    proportion = [0.0, 0.25, 0.5, 1.0, 1.0, 0.75, 0.5, 0.0]
    years = [2020, 2021, 2022, 2023, 2050, 2051, 2052, 2053]
    return years, proportion


# some of the below are integration tests
def test_that_event_impact_works_with_callables(
    start_date, event_impact_function, expected_proportions_for_event
):
    # Arrange
    e = Event("some_event", start_date, impact=event_impact_function)
    list_of_years, expected_harvest_proportion = expected_proportions_for_event

    # Act
    actual_harvest_proportion = [e.eval(y) for y in list_of_years]

    # Assert
    assert_on_pair(expected_harvest_proportion, actual_harvest_proportion)


def assert_on_pair(targets, predictions):
    for i, (t, p) in enumerate(zip(targets, predictions)):
        assert t == p, f"MISMATCH @ time {i}: target {t} | prediction {p} mismatch"


def test_that_event_impact_works_with_floats(dummy_event):
    # Arrange
    dummy_event.impact = 2

    # Act
    impact = dummy_event.eval(2020)

    # Assert
    assert impact == 2.0


def test_that_event_impact_default_has_no_impact(dummy_event):
    # Arrange

    # Act

    # Assert
    assert dummy_event.eval(2020) == 1.0
    assert dummy_event.eval(2021) == 1.0


# integration


def test_that_event_impacts_harvest(
    growth_function, farm, expected_proportions_for_harvest
):
    # Arrange
    configs = (Config("a", "a", output_per_crop=200),)
    # scope = {"type": "species", "def": "a"}
    dummy_event = Event("harvest event", impact=growth_function, scope=True)

    years, proportions = expected_proportions_for_harvest

    dates = [datetime.datetime(y, 8, 1) for y in years]
    targets = [p * 200 for p in proportions]

    # Act
    harvests = [
        predict_yield_for_farm(farm, configs, [dummy_event], time=date)[0]
        for date in dates
    ]

    # Assert
    assert_on_pair(targets, harvests)


def test_that_membership_is_based_on_species_when_name_unspecified():
    assert Config("a") == Config("a")
    assert Config("a") == Config("a", "a-details")
    assert Config("a", "a-details") in [Config("a")]


def test_that_membership_is_based_on_species_and_name_when_both_supplied():
    # test that if name present, assertion happens on species and name
    assert Config("a", "a-standard") != Config("a", "a-other-details")
    assert Config("a", "a-standard") == Config("a", "a-standard")


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_error_thrown_when_bad_config_requested(configs):
    with pytest.raises(ValueError):
        c = find_config("f", configs)
        assert c is None


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_warning_thrown_when_species_requested_for_which_no_default_exists(configs):
    with pytest.warns(UserWarning):
        c = find_config("b", configs)

    assert c == Config(
        species="b", name="b-intercroppped", output_per_crop=1.0, unit="cuerdas"
    )


# FARM TESTS


def test_that_farm_contains_works():
    p = Plot(species="a")
    f = Farm([p])
    assert f.contains(species="a")


def test_that_we_can_simulate_a_single_harvest_with_defaults(farm, configs):
    harvest = predict_yield_for_farm(farm, configs)
    assert harvest == [1]


def test_that_we_can_simulate_a_single_harvest_with_double_area(configs):
    farm = Farm([Plot(species="a", area=2, num=2)])
    harvest = predict_yield_for_farm(farm, configs)
    assert harvest == [2]


def test_that_we_can_simulate_a_single_harvest_with_different_density(configs):
    farm = Farm([Plot(species="a", num=2)])
    harvest = predict_yield_for_farm(farm, configs)
    assert harvest == [2]


@mock.patch("pandas.read_csv")
def test_that_we_can_use_farm_loaded_from_legacy_csv_file(mock_csv, farm_dict):
    mock_csv.return_value = DataFrame(farm_dict)
    farm = Farm.from_csv(mock_csv)
    assert farm.size == 5


# PREDICTION TESTS


def test_lifecycle(configs):
    # Arrange
    farm = Farm([Plot(species="a", num=1)])
    harvest = predict_yield_for_farm(farm, configs)
    # Act

    # Assert
    assert harvest[0] > 0
    pass


# WARNINGS TESTS


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_that_prediction_against_wrong_species_raise_value_error():
    p, c = Plot(species="a"), Config("b")
    with pytest.raises(ValueError):
        harvest = predict_yield_for_plot(p, c)
        assert harvest is None


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_that_predicting_yield_against_config_without_canonical_definition_still_works():
    p, c = Plot(species="c", num=7), Config("c")
    assert predict_yield_for_plot(p, c) == 7.0
