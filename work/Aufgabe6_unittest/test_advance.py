"""

"""
import pytest
import minitopsim.surface as srf
import numpy as np


@pytest.fixture
def _set_surface():
    """
    """
    surface = None
    x = np.array((-1., 0., 1.))
    y = np.array((0., 0., 2.))
    surface = srf.Surface(x, y)
    return surface


@pytest.mark.unittest
def test_surface_normal(_set_surface):
    """
    test for the normal vector for a set of 3 points defined in _set_surface.

    Args:
        _set_surface: fixture that sets the surface points
    """
    # todo improve readability
    #   get rid of arrays
    surf = _set_surface
    # calc surface normal
    x_ref = np.diff(surf.x)
    y_ref = np.diff(surf.y)
    # make an array for norm function
    temp = np.vstack((x_ref, y_ref))
    temp /= np.linalg.norm(temp, axis=0)

    x_ref = temp[0][:-1] + temp[0][1:]
    y_ref = temp[1][:-1] + temp[1][1:]

    n_vec_ref = np.vstack((y_ref, -x_ref))
    n_vec_ref /= np.linalg.norm(n_vec_ref, axis=0)
    x_ref = n_vec_ref[0][0]
    y_ref = n_vec_ref[1][0]

    n_vecs = surf.normal_vector()
    x = n_vecs[:, 1][0]
    y = n_vecs[:, 1][1]

    # define the max error
    delta = 0.001

    # test for x in range
    assert abs(x_ref-x) <= delta, \
        f'diff in x:{abs(x_ref-x)} is not in limit {delta}'
    # test for y in range
    assert abs(y_ref-y) <= delta, \
        f'diff in y:{abs(y_ref-y)} is not in limit {delta}'


@pytest.fixture
def _set_advance_param():
    """

    """


@pytest.mark.workinprogress
def test_advance(_set_advance_param):
    assert False, f'emtpy test_advance'
