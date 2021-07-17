# -*- coding: utf-8 -*-
import datetime
import pytest
from typing import Dict
from cafe.farm import (
    Config,
    Plot,
    Farm,
    Event,
    find_config,
    predict_yield_for_farm,
    predict_yield_for_plot,
)


@pytest.fixture()
def farm():
    return Farm([Plot(species="a")])


@pytest.fixture()
def start_date():
    return datetime.datetime(2020, 1, 1)

@pytest.fixture()
def expected_harvest_info():
    proportion = [0.0, 0.25, 0.5, 1.0, 1.0, 0.75, 0.5, 0.0]
    years = [2020, 2021, 2022, 2023, 2050, 2051, 2052, 2053]
    return years, proportion

@pytest.fixture()
def borbon_harvest_info() -> tuple[float, Dict[str, float]]:
    harvest_cap = 200
    timeline = {"first_harvest": 4, "full_harvest": 5, "last_harvest": 29, "death": 30}
    return harvest_cap, timeline

def assert_on_pair(targets, predictions):
    for t, p in zip(targets, predictions):
        assert t == p, f"MISMATCH: target {t} | prediction {p} mismatch"


@pytest.fixture()
def borbon_harvest_function(borbon_harvest_info):
    def f(year, **kwargs):
        start = kwargs["start"].year
        age = year - start
        harvest_cap, timeline = borbon_harvest_info

        if age <= timeline["first_harvest"]:
            return 0
        if age >= timeline["full_harvest"]:
            return 1.0
        if age == timeline["last_harvest"]:
            return 0.5
        if age >= timeline["death"]:
            return 0
        return 0


def test_borbon_harvest_returns(
    start_date, borbon_harvest_info, farm, borbon_harvest_function
):
    harvest_cap, timeline = borbon_harvest_info

    # Arrange
    borbon_event = Event("borbon event", start_date, impact=borbon_harvest_function)
    configs = (Config("borbon", "borbon", output_per_crop=harvest_cap),)

    dates = [
        datetime.datetime((start_date.year + y), 1, 1) for y in timeline.values()
    ]

    # Act
    harvests = [
        predict_yield_for_farm(farm, configs, [borbon_event], time=date)[0]
        for date in dates
    ]

    # Assert
    assert_on_pair(targets, harvests)
