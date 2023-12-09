""""
Provides 2 parameterized test for loading parameters from *.cfg files

test-cfg files will be loaded from the directory "cfg_test_files" which
hast to be located in the same directory as this file.
Files are split in good and bad, according to their key format
    filename: key*.cfg
        e.g.:good_int_statt_float.cfg; bad_str_value.cfg

tests:
    def test_load_good_parameters()
        checks if values in parameters.py are correct for given good*.cfg
        marks:
            unittest
            parameterized

    def test_load_bad_parameters()
        checks if exceptions are raised for bad*.cfg files
        marks:
            unittest
            parameterized
"""

import pytest
import os
import glob
import configparser

import minitopsim.parameters as par

# read test files
path = os.path.join(os.path.dirname(__file__), 'cfg_test_files')
if os.path.exists(path):
    if not os.path.isdir(path):
        raise FileNotFoundError(f'"{path}" is not a directory.')
else:
    raise FileNotFoundError(f'Directory "{path}" does not exist.')

good_files = glob.glob(os.path.join(path, 'good*.cfg'))
good_names = [os.path.basename(file) for file in good_files]
bad_files = glob.glob(os.path.join(path, 'bad*.cfg'))
bad_names = [os.path.basename(file) for file in bad_files]

default_values = dict()


@pytest.fixture()
def _set_default_values_par():
    """
    Sets the default values from the parameters.db to the parameters namespace

    this is necessary to clean up residual values for testing
    """
    # construct the path to databank via parameters.py
    file = os.path.join(os.path.dirname(par._file), 'parameters.db')
    def_config = configparser.ConfigParser()
    def_config.read(file)

    categories = dict()

    # get all attributes defined in the db file
    for section in def_config.sections():
        for attribute in def_config[section]:
            attribute = attribute.upper()
            categories[attribute] = section
            default_values[attribute] = (
                eval(def_config[section].get(attribute)))[0]
    # write default in parameters namespace
    for key, value in default_values.items():
        par.__dict__[key] = value


@pytest.mark.parametrize('cfg_file',
                         good_files,
                         ids=good_names
                         )
@pytest.mark.unittest
def test_load_good_parameters(_set_default_values_par, cfg_file):
    """
    check if the variables in parameters.py have the same value as in cfg_file.

    uses file names as ids

    fixtures:
        _set_default_values_par(object)
    parameters:
        cfg_file(str):
    marks:
        unittest
    """
    # unit under test
    par.load_parameters(cfg_file)

    # read cfg to get compare values
    cfg_config = configparser.ConfigParser()
    cfg_config.read(cfg_file)

    cfg_param = dict()

    # get all attributes defined in the cfg file
    for section in cfg_config.sections():
        for attribute in cfg_config[section]:
            attribute = attribute.upper()

            if attribute in default_values:
                cfg_param[attribute] = eval(
                    cfg_config[section].get(attribute))
            else:
                assert False, (f'Attribute {attribute} not defined in '
                               f'default values!')

    # assert test for values
    for key, value in cfg_param.items():
        assert par.__dict__[key] == value, (f'{key} has a different value '
                                            f'than '
                                            f'{os.path.basename(cfg_file)} '
                                            f'suggests')


@pytest.mark.parametrize('cfg_file',
                         bad_files,
                         ids=bad_names)
@pytest.mark.unittest
def test_load_bad_parameters(_set_default_values_par, cfg_file):
    """
    checks if a bad*.cfg raises an Exception.

    uses file names as ids

    fixtures:
        _set_default_values_par(object)
    parameters:
        cfg_file(str):
    marks:
        unittest
    """
    # with pytest.raises(Exception) as excinfo:
    #     par.load_parameters(cfg_file)
    # print(f'\tRaised: {excinfo.typename}')
    with pytest.raises(Exception):
        par.load_parameters(cfg_file)
