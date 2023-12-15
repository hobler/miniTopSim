"""
Provides 2 parameterized test for loading parameters from *.cfg files

Test configuration files are loaded from the 'cfg_test_files' directory in
the same directory as this file.
Files are split in good and bad, according to their format 'key*.cfg'
    key=good:
        will be tested with test_load_good_parameters.
    key=bad:
        will be tested with test_load_bad_parameters.

tests:
    load_good_parameters:
        checks if values are correct for given good*.cfg
        is parameterized

    load_bad_parameters:
        checks if exceptions are raised for bad*.cfg files
        is parameterized

fixtures:
    _set_default_values_par:
        loads the default values form the database
"""
import configparser
import pytest
import os
import glob

import minitopsim.parameters as par

# read test files and sort them in to good and bad cases
path = os.path.join(os.path.dirname(__file__), 'cfg_test_files')
if os.path.exists(path):
    if not os.path.isdir(path):
        raise FileNotFoundError(f'"{path}" is not a directory.')
else:
    raise FileNotFoundError(f'Directory "{path}" does not exist.')

# sort in good and bad files, and fetch names
good_files = glob.glob(os.path.join(path, 'good*.cfg'))
good_names = [os.path.basename(file) for file in good_files]

bad_files = glob.glob(os.path.join(path, 'bad*.cfg'))
bad_names = [os.path.basename(file) for file in bad_files]


@pytest.fixture()
def set_default_values_par():
    """
    Set default values from database to parameters-namespace.

    to clean up residual values for next test case.
    """
    # construct the path to database via parameters.py
    file = os.path.join(os.path.dirname(par._file), 'parameters.db')
    def_config = configparser.ConfigParser()
    def_config.read(file)

    categories = dict()
    default_values = dict()

    # get all attributes defined in database file
    for section in def_config.sections():
        for attribute in def_config[section]:
            attribute = attribute.upper()
            categories[attribute] = section
            default_values[attribute] = \
                (eval(def_config[section].get(attribute)))[0]

    # write default values to parameters namespace
    for key, value in default_values.items():
        vars(par)[key] = value


@pytest.mark.unittest
@pytest.mark.parametrize('cfg_file',
                         good_files,
                         ids=good_names
                         )
def test_load_good_parameters(set_default_values_par, cfg_file):
    """
    checks if cfg-values are correctly loaded to parameters namespace

    uses cfg-file-names as ids

    Args:
        set_default_values_par(fixture): sets the default values.
        cfg_file(string): path to cfg-file
    """
    par.load_parameters(cfg_file)

    # get compare values from cfg-file
    cfg_config = configparser.ConfigParser()
    cfg_config.read(cfg_file)

    cfg_param = dict()

    # get all attributes defined in the cfg file
    for section in cfg_config.sections():
        for attribute in cfg_config[section]:
            attribute = attribute.upper()
            cfg_param[attribute] = eval(cfg_config[section].get(attribute))

    # assert test for values
    for key, value in cfg_param.items():
        assert vars(par)[key] == value, (f'{key} has a different value '
                                            f'than '
                                            f'{os.path.basename(cfg_file)} '
                                            f'suggests it should have.')


@pytest.mark.unittest
@pytest.mark.parametrize('cfg_file',
                         bad_files,
                         ids=bad_names)
def test_load_bad_parameters(set_default_values_par, cfg_file):
    """
    checks if a bad*.cfg raises an Exception.

    uses file names as ids

    Args:
        set_default_values_par(fixture): sets the default values.
        cfg_file(string): path to cfg-file
    """
    with pytest.raises(Exception):
        par.load_parameters(cfg_file)
