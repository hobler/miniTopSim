"""
Test to compare the erf_1 simulation values to a saved erf_1.srf_save file

This script allows user to compare the current simulation of the erf_1.cfg
with saved values from erf_1.srf_save and utilizes the error function beam
profile. If the tests fail, an assert statement will be printed out.

This file contains the following functions:
    *test_run - test the execution of the miniTopSim simulation
    *test_erf_1 - tests the values from erf_1.cfg and erf_1.srf_save
"""

import pytest
import os
import sys

# Adding the code directory to sys.path
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

import mini_topsim.plot as srfplot
from mini_topsim.surface import Surface
from mini_topsim.main import mini_topsim


def test_run():
    """
    Test running miniTopSim.

    :return:
    """
    config_file = os.path.join(filedir, 'erf_1.cfg')
    success = mini_topsim(config_file)
    assert success is None, 'Error during executing miniTopSim'


def test_erf_1():
    """
    Compares the the values from erf_1.cfg and erf_1.srf_save through distance

    :return:
    """
    srf_filename_1 = os.path.join(filedir, 'erf_1.srf')
    srf_filename_2 = os.path.join(filedir, 'erf_1.srf_save')
    srfplotter = srfplot._SurfacePlotter(srf_filename_1, srf_filename_2)

    srf1 = Surface()
    srf1.xvals = srfplotter.xpoints_list[-1]
    srf1.yvals = srfplotter.ypoints_list[-1]

    srf2 = Surface()
    srf2.xvals = srfplotter.refsrf.xpoints_list[-1]
    srf2.yvals = srfplotter.refsrf.ypoints_list[-1]

    dist = srf1.distance(srf2)

    assert len(srf1.xvals) == len(srf2.xvals), \
        'number of x-values from simulation and erf_1.srf_save do not match'
    assert len(srf1.yvals) == len(srf2.yvals), \
        'number of y-values from simulation and erf_1.srf_save do not match'
    assert dist <= 0.005, \
        'values from simulation and erf_1.srf_save do not match' \
        + ' distance %.3f is too great' % dist
