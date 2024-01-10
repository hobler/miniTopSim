"""
Template for testing miniTopSim using pytest.

"""
import pytest
import sys
import os
from minitopsim.main import minitopsim
import minitopsim.parameters as par

def test_run(set_config):
    """Test running miniTopSim."""
    success = minitopsim()
    assert success, 'Error during executing miniTopSim.'
    
def test_redep_1_surface_data():
    """Compare surface data with redeposition"""
    
    # get paths of srf files
    dir_path = os.path.dirname(__file__)
    test_file_path = os.path.join(dir_path, 'yamamura_interp_redep_1.srf')
    ref_file_path = os.path.join(dir_path, 'yamamura_interp_redep_1.srf_save')
    
    # open surface files and compare
    with open(test_file_path, 'r') as test_file:
        test_data = test_file.read()
    with open(ref_file_path, 'r') as ref_file:
        ref_data = ref_file.read()
    assert test_data == ref_data, 'Error: Redeposition surface is wrong.'

@pytest.fixture()
def set_config():
    # append config-file for test surface
    sys.argv.append('yamamura_interp_redep_1.cfg')
