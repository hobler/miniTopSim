import pytest
import numpy as np
from numpy.testing import assert_almost_equal
import minitopsim.surface as srf

@pytest.fixture
def set_surface1():
    """
    initiate a test surface1 with points from check_deloop.
    """
    x = np.array([0, 3, 2, 2, 7, 7, 6, 9])
    y = np.array([2, 1, 3, 0, 0, 3, 1, 2])
    surface = srf.Surface(x, y)
    return surface

@pytest.fixture
def set_surface2():
    """
    initiate a test surface2 with points from check_deloop.
    """
    x = np.array([0, 5, 3, 2, 6, 8])
    y = np.array([1, 1, 3, 0, 3, 1])
    surface = srf.Surface(x, y)
    return surface


@pytest.mark.unittest
def test_deloop(set_surface1, set_surface2):
    """
    test surface.deloop()

    Args:
        set_surface1(fixture): to init a surface1
        set_surface2(fixture): to init a surface2
    """
    # get test data
    delooped_x1, delooped_y1 = set_surface1.deloop()
    delooped_x2, delooped_y2 = set_surface2.deloop()

    # define reference data
    delooped_y_muster1 = np.array([2, 1.3333, 0, 0, 1.3333, 2])
    delooped_x_muster1 = np.array([0, 2, 2, 7, 7, 9])
    delooped_y_muster2 = np.array([1, 1, 1, 1.7142, 3, 1])
    delooped_x_muster2 = np.array([0, 2.3333, 3.3333, 4.2857, 6, 8])

    # Raises: AssertionError if arrays are not Equal up to the defined decimal
    assert_almost_equal(delooped_x1, delooped_x_muster1, decimal=3)
    assert_almost_equal(delooped_y1, delooped_y_muster1, decimal=3)
    assert_almost_equal(delooped_x2, delooped_x_muster2, decimal=3)
    assert_almost_equal(delooped_y2, delooped_y_muster2, decimal=3)
