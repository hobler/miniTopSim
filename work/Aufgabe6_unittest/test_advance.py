"""
Test cases for etching algorithm (surface advancement and direction).

tests:
    surface_normal:
        tests direction of etching
    advance:
        tests the progression of etching

fixtures:
    set_surface:
        init a test surface with 3 points
    set_advance_param:
        sets etching progression parameters
"""
import pytest
import numpy as np
from numpy.testing import assert_almost_equal

import minitopsim.parameters as par
import minitopsim.surface as srf
import minitopsim.advance as adv


@pytest.fixture
def set_surface():
    """
    initiate a test surface with points (-1,0) , (0,0) und (1,2).
    """
    x = np.array((-1., 0., 1.))
    y = np.array((0., 0., 2.))
    surface = srf.Surface(x, y)
    return surface


@pytest.mark.unittest
def test_surface_normal(set_surface):
    """
    test for the normal vector for a set of 3 points defined in _set_surface.

    Args:
        set_surface(fixture): init a surface
    """
    # define reference values
    x_ref = np.array([0., 0.52573111, 0.])
    y_ref = np.array([-1., -0.85065081, -1.])
    bisec_ref = np.vstack((x_ref, y_ref))

    # get test data
    bisec = set_surface.normal_vector()

    # Raises: AssertionError if arrays are not Equal up to the defined decimal
    assert_almost_equal(bisec, bisec_ref, decimal=3)


@pytest.fixture
def set_advance_param():
    """
    setting ETCH_RATE=5 and TIME_STEP=1
    """
    par.ETCH_RATE = 5
    par.TIME_STEP = 1
    par.ETCHING = True


@pytest.mark.unittest
def test_advance(set_advance_param, set_surface):
    """
    test etching progression

    Args:
        set_advance_param(fixture): to set parameters
        set_surface(fixture): to init a surface
    """
    # define reference data
    x_ref = np.array([-1., 2.62865556, 1.])
    y_ref = np.array([-5., -4.25325404, -3.])

    # get test data
    surf_adv, _ = adv.advance(set_surface, par.TIME_STEP)
    x = surf_adv.x
    y = surf_adv.y

    # Raises: AssertionError if arrays are not Equal up to the defined decimal
    assert_almost_equal(x, x_ref, decimal=3)
    assert_almost_equal(y, y_ref, decimal=3)
