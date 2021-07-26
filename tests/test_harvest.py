# -*- coding: utf-8 -*-
import datetime
import pytest
from typing import Callable, Tuple, List, Dict
from cafe.farm import (
    Config,
    Plot,
    Farm,
    Event,
    predict_yield_for_farm,
    guate_harvest_function,
)


@pytest.fixture()
def start_date():
    return datetime.datetime(2020, 1, 1)


@pytest.fixture()
def farm(start_date):
    return Farm([Plot(species="borbon", start=start_date)])


def guate_growth_target(
    lifespan: float = 30, mature: float = 5, retire: float = 28
) -> Tuple[List[float], List[float]]:
    test_periods = [
        0,
        mature - 2,
        mature - 1,
        mature,
        mature + 1,
        retire - 1,
        retire,
        retire + 1,
        lifespan,
        lifespan + 1,
    ]
    years = [2020 + y for y in test_periods]
    proportion = [0.0, 0.0, 0.2, 1.0, 1.0, 1.0, 1.0, 0.75, 0.5, 0.0]
    return years, proportion


@pytest.fixture()
def borbon_harvest_function() -> Callable:
    return guate_harvest_function()


@pytest.fixture()
def borbon_scope() -> Dict:
    return {"type": "species", "def": "borbon"}


def test_borbon_harvest_returns(farm, borbon_harvest_function, borbon_scope):
    # Arrange
    years, proportions = guate_growth_target()
    borbon_max_yield = 200
    expected_harvest = [p * borbon_max_yield for p in proportions]

    events = [
        Event("borbon harvest", impact=borbon_harvest_function, scope=borbon_scope)
    ]
    configs = (Config("borbon", "borbon", output_per_crop=borbon_max_yield),)

    # Act
    predicted_harvest = [
        predict_yield_for_farm(farm, configs, events, time=date)[0] for date in years
    ]
    print(expected_harvest, predicted_harvest)
    # Assert
    for i, (t, p) in enumerate(zip(expected_harvest, predicted_harvest)):
        assert t == p, f"MISMATCH @ time {i}: target {t} | prediction {p} mismatch"
