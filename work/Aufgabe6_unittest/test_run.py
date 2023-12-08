"""
Template for testing miniTopSim using pytest.

"""
import sys

import pytest
import matplotlib.pyplot as plt
from minitopsim.main import minitopsim

import minitopsim.parameters as parshow


# def test_run():
#     """Test running miniTopSim."""
#     success = minitopsim()
#     assert success, 'Error during executing miniTopSim.'


@pytest.fixture()
def set_param():
    """Set parameter value."""
    # set input .cfg
    sys.argv[1] = ('/home/pably/Documents/Python/TU-SE/miniTopSim/work/'
                   'Aufgabe6_unittest/good.cfg')


def test_set_param(set_param):
    """Test setting a parameter value."""
    success = minitopsim()
    plt.close('all')
    # TODO: cosmetic-clear console out put
    assert success, 'Error during executing miniTopSim.'
