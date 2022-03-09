"""
Template for testing miniTopSim using pytest.

"""
import pytest
from minitopsim.main import minitopsim
import minitopsim.parameters as par

def test_run():
    """Test running miniTopSim."""
    success = minitopsim()
    assert success, 'Error during executing miniTopSim.'

@pytest.fixture()
def set_param():
    """Set parameter value."""
    par.TestParameter = 56

def test_set_param(set_param):
    """Test setting a parameter value."""
    assert par.TestParameter == 56

