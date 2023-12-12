"""
Test cases to test the etching algorithm (surface advancement and direction).

tests:
    surface_normal:
        checks direction of etching
    advance:
        checks the progression of etching

fixtures:
    set_surface:
        init a test surface with 3 points
    set_advance_param:
        sets etching progression parameters
"""
import pytest
import numpy as np

import minitopsim.parameters as par
import minitopsim.surface as srf
import minitopsim.advance as adv

# parameter to set max error for float value testing
FLOATING_ERROR = 0.001


@pytest.fixture
def set_surface():
    """
    initiate a test surface with points (-1,0) , (0,0) und (1,2).
    """
    x = np.array((-1., 0., 1.))
    y = np.array((0., 0., 2.))
    surface = srf.Surface(x, y)
    return surface


@pytest.mark.showcase
def test_surface_normal(set_surface):
    """
    test for the normal vector for a set of 3 points defined in _set_surface.

    Args:
        set_surface(fixture): init a surface
    """
    surf = set_surface
    # make 2D-array and get distance to next point
    vec_diff = np.diff(np.vstack((surf.x, surf.y)), axis=1)
    vec_diff /= np.linalg.norm(vec_diff, axis=0)

    # summe of next neighbours
    x_ref = vec_diff[0][:-1] + vec_diff[0][1:]
    y_ref = vec_diff[1][:-1] + vec_diff[1][1:]

    # calculate angle bisector and normalize it
    bisec_ref = np.vstack((y_ref, -x_ref))
    bisec_n_ref = bisec_ref / np.linalg.norm(bisec_ref, axis=0)

    # match pattern from surf.normal_vector() by adding norm vecs to the edge
    edge_vec = np.array(((0.,), (-1.,)))
    bisec_n_ref = np.concatenate((edge_vec, bisec_n_ref, edge_vec),
                                 axis=1)

    # get test data
    bisec_n = surf.normal_vector()

    assert np.all(abs(bisec_n_ref - bisec_n) <= FLOATING_ERROR), \
        (f'difference :{abs(bisec_n_ref - bisec_n)} '
         f'is not in limit {FLOATING_ERROR}')


@pytest.fixture
def set_advance_param():
    """
    setting ETCH_RATE=5 and TIME_STEP=1
    """
    par.__dict__['ETCH_RATE'] = 5
    par.__dict__['TIME_STEP'] = 1


@pytest.mark.showcase
@pytest.mark.unittest
def test_advance(set_advance_param, set_surface):
    """
    test etching progression

    Args:
        set_advance_param(fixture): to set parameters
        set_surface(fixture): to init a surface
    """
    # get referenz values
    surf = set_surface
    norm_vecs = surf.normal_vector()

    # calculation of the new surface
    x_ref = surf.x + norm_vecs[0] * par.TIME_STEP * par.ETCH_RATE
    y_ref = surf.y + norm_vecs[1] * par.TIME_STEP * par.ETCH_RATE

    # get test data
    surf_adv = adv.advance(surf, par.TIME_STEP, par.ETCH_RATE)
    x = surf_adv.x
    y = surf_adv.y

    assert np.all(abs(x_ref - x) <= FLOATING_ERROR), \
        f'diff in x:{abs(x_ref - x)} is not in limit {FLOATING_ERROR}'
    assert np.all(abs(y_ref - y) <= FLOATING_ERROR), \
        f'diff in y:{abs(y_ref - y)} is not in limit {FLOATING_ERROR}'
