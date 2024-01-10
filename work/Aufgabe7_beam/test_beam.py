import pytest
import os, sys
import math
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..')
sys.path.insert(0, codedir)
from minitopsim.main import minitopsim
import minitopsim.parameters as par
import minitopsim.beam as beam
from numpy.testing import assert_almost_equal

@pytest.fixture
def set_gauss_beam():
    """
    A pytest fixture to initialize a Gaussian beam.

    Loads the parameters for a Gaussian beam from 'gauss.cfg', 
    initializes the beam, and returns it for testing.

    Returns:
    beam: An instance of the beam class configured as a Gaussian beam.
    """
    dirname = os.path.dirname(__file__)
    par.load_parameters(dirname + '/gauss.cfg')
    beam_gauss = beam.init(par)
    return beam_gauss

@pytest.fixture
def set_erf_beam():
    """
    A pytest fixture to initialize an error function beam.

    Loads the parameters for an error function beam from 'erf.cfg', 
    initializes the beam, and returns it for testing.

    Returns:
    beam: An instance of the beam class configured as an error function beam.
    """
    dirname = os.path.dirname(__file__)
    par.load_parameters(dirname + '/erf.cfg')
    beam_erf = beam.init(par)
    return beam_erf

#Test should pass
def test_gaussian_beam_max(set_gauss_beam):
    """
    Test the maximum value of a Gaussian beam.

    This test compares the numerically found maximum beam value with the
    analytically calculated value to ensure accuracy of the beam implementation.

    Parameters:
    set_gauss_beam (fixture): The Gaussian beam fixture to test.
    """
    res_analytic = 0.6253429469e16
    exponent = int(math.log10(res_analytic))+1
    res_analytic = res_analytic / 10**exponent
    res_numeric = set_gauss_beam.find_maxima(0)
    res_numeric = res_numeric.fun / 10**exponent
    assert_almost_equal(res_numeric, res_analytic, decimal=10)

#test should pass
def test_erf_beam_max(set_erf_beam):
    """
    Test the maximum value of an error function beam.

    This test compares the numerically found maximum beam value with the 
    analytically calculated value to ensure accuracy of the beam implementation.

    Parameters:
    set_erf_beam (fixture): The error function beam fixture to test.
    """
    res_analytic = 0.6241509074e16
    exponent = int(math.log10(res_analytic))+1
    res_analytic = res_analytic / 10**exponent
    res_numeric = set_erf_beam.find_maxima(0)
    res_numeric = res_numeric.fun / 10**exponent
    assert_almost_equal(res_numeric, res_analytic, decimal=10)

#test should pass
def test_gaussian_beam_arbitrary_point(set_gauss_beam):
    """
    Test the Gaussian beam value at an arbitrary point.

    Compares the beam value at a specific point with the expected analytic value
    to validate the beam's implementation.

    Parameters:
    set_gauss_beam (fixture): The Gaussian beam fixture to test.
    """
    F_analytic = 0.3908393418e15
    exponent = int(math.log10(F_analytic))+1
    F_analytic = F_analytic / 10**exponent
    arbitrary_point = 100 * 1e-7 # in cm
    F_gauss = set_gauss_beam(arbitrary_point) / 10**exponent
    assert_almost_equal(F_gauss, F_analytic, decimal=10)

#test should pass
def test_erf_beam_arbitrary_point(set_erf_beam):
    """
    Test the error function beam value at an arbitrary point.

    Compares the beam value at a specific point with the expected analytic value
    to validate the beam's implementation.

    Parameters:
    set_erf_beam (fixture): The error function beam fixture to test.
    """
    F_analytic = 0.6241509074e16
    exponent = int(math.log10(F_analytic))+1
    F_analytic = F_analytic / 10**exponent
    arbitrary_point = 100 * 1e-7 # in cm
    F_erf = set_erf_beam(arbitrary_point) / 10**exponent
    assert_almost_equal(F_erf, F_analytic, decimal=10)
