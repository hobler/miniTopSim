import pytest
import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..')
sys.path.insert(0, codedir)
from minitopsim.main import minitopsim
import minitopsim.parameters as par
import minitopsim.beam as beam
from numpy.testing import assert_almost_equal


@pytest.fixture
def set_gauss_beam():
    par.load_parameters('gauss.cfg')
    beam_gauss = beam.init(par)
    return beam_gauss

@pytest.fixture
def set_erf_beam():
    par.load_parameters('erf.cfg')
    beam_erf = beam.init(par)
    return beam_erf


def test_gaussian_beam_max(set_gauss_beam):
    res_numeric = set_gauss_beam.find_maxima(0)
    res_numeric = res_numeric.fun * (-1) / 1e16
    res_analytic = 0.6253429469e16 / 1e16
    assert_almost_equal(res_numeric, res_analytic, decimal=10)

def test_erf_beam_max(set_erf_beam):
    res_numeric = set_erf_beam.find_maxima(0)
    res_numeric = res_numeric.fun * (-1) / 1e16
    res_analytic = 0.6241509074e16 / 1e16
    assert_almost_equal(res_numeric, res_analytic, decimal=10)
    
def test_gaussian_beam_arbitrary_point(set_gauss_beam):
    arbitrary_point = 100 * 1e-7 #in cm
    F_gauss = set_gauss_beam(arbitrary_point) / 1e15
    F_analytic = 0.3908393418e15 / 1e15
    assert_almost_equal(F_gauss, F_analytic, decimal=10)

def test_erf_beam_arbitrary_point(set_erf_beam):
    arbitrary_point = 100 * 1e-7 #in cm
    F_erf = set_erf_beam(arbitrary_point) / 1e16
    F_analytic = 0.6241509074e16 / 1e16
    assert_almost_equal(F_erf, F_analytic, decimal=10)
    
@pytest.fixture()
def set_param():
    """Set parameter value."""
    par.TestParameter = 56

def test_set_param(set_param):
    """Test setting a parameter value."""
    assert par.TestParameter == 56