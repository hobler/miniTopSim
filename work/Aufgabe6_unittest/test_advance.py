"""

"""
import pytest
import numpy as np

import minitopsim.surface as srf
import minitopsim.parameters as par
import minitopsim.advance as adv


_FLOATING_ERROR = 0.001


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

    # test for x in range
    assert abs(x_ref - x) <= _FLOATING_ERROR, \
        f'diff in x:{abs(x_ref - x)} is not in limit {_FLOATING_ERROR}'
    # test for y in range
    assert abs(y_ref - y) <= _FLOATING_ERROR, \
        f'diff in y:{abs(y_ref - y)} is not in limit {_FLOATING_ERROR}'


@pytest.fixture
def _set_advance_param():
    """
    setting ETCH_RATE and TIME_STEP
    """
    par.__dict__['ETCH_RATE'] = 5
    par.__dict__['TIME_STEP'] = 1


@pytest.mark.unittest
def test_advance(_set_advance_param, _set_surface):
    """
    todo: docstring test_advance

    Args:
        _set_advance_param:
        _set_surface:
    """
    # todo _test_advance: cleanup ref stuff
    # get referenz values
    d_t = par.TIME_STEP
    etch_r = par.ETCH_RATE
    surf = _set_surface
    n_vecs = surf.normal_vector()
    x_ref = surf.x
    y_ref = surf.y

    x_ref += n_vecs[0]*d_t*etch_r
    y_ref += n_vecs[1]*d_t*etch_r

    # get test values
    surf_adv = adv.advance(surf, d_t, etch_r)
    x = surf_adv.x
    y = surf_adv.y

    assert np.all(abs(x_ref - x) <= _FLOATING_ERROR), \
        f'diff in x:{abs(x_ref - x)} is not in limit {_FLOATING_ERROR}'
    assert np.all(abs(y_ref - y) <= _FLOATING_ERROR), \
        f'diff in y:{abs(y_ref - y)} is not in limit {_FLOATING_ERROR}'
