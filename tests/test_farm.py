# -*- coding: utf-8 -*-

import pytest
from cafe.farm import Config, Plot, Farm, find_config
# import cafe.importData as importData
import numpy as np
import warnings

__author__ = "Mathematical Michael <Pilosov>"
__copyright__ = "Mind the Math, LLC"
__license__ = "mit"


@pytest.fixture()
def configs():
   return (
       Config('a', 'a-sparse'), 
       Config('b', 'b-intercroppped'),
       Config('c', 'c'),
       Config('d', 'd'),
          )


# CONFIG TESTS

def test_that_membership_is_based_on_species_when_name_unspecified():
    assert Config('a') == Config('a')
    assert Config('a') == Config('a', 'a-details')
    assert Config('a', 'a-details') in [Config('a')]


def test_that_membership_is_based_on_species_and_name_when_both_supplied():
    # test that if name present, assertion happens on species and name
    assert Config('a', 'a-standard') != Config('a', 'a-other-details')
    assert Config('a', 'a-standard') == Config('a', 'a-standard')


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_error_thrown_when_bad_config_requested(configs):
    with pytest.raises(ValueError):
        c = find_config('f', configs)


@pytest.mark.filterwarnings("ignore::UserWarning")
def test_warning_thrown_when_species_requested_for_which_no_default_exists(configs):
    with pytest.warns(UserWarning):
        c = find_config('b', configs)

    assert c == Config(species='b',
                       name='b-intercroppped',
                       output_per_crop=1.0,
                       unit='cuerdas'
                      )

# FARM TESTS

def test_that_farm_contains_works():
    p = Plot(species='a')
    f = Farm([p])
    assert f.contains(species='a')
