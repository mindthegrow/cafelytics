# -*- coding: utf-8 -*-

import pytest
import cafe.farm as cf
import cafe.importData as importData
import numpy as np

__author__ = "Mathematical Michael"
__copyright__ = "Mathematical Michael"
__license__ = "mit"


def test_farm_instantiation_defaults():
    # object with automatic defaults
    test_farm = cf.Farm()
    # TODO: add some basics here and assert them
    assert test_farm.totalCuerdas == 1
    assert test_farm.pruneYear == None
    assert test_farm.treeType == 'borbon'
    assert test_farm.getHarvest() == 0
    
    # tests search from root directory as the working directory
    testDict = importData.openYaml("data/trees.yml")
    # object where a dictionary is imported for treeAttributes
    test_farm02 = cf.Farm(treeAttributes = testDict)
    assert test_farm02.treeType == 'borbon'
    
    # run through a five year simulation
    years = 5
    for i in range(years):
        test_farm.setHarvestZero()
        test_farm.oneYear()
        
    assert test_farm.ageOfTrees[0] == (years + 1)
    assert test_farm.getHarvest() == 200
    

    # this is another syntax structure to accomplish the above
    # but it is new to me, personally -- mm
    #with pytest.raises(AssertionError):

