""""
testing for correct parameters handling
# todo: docstring schreiben für test_parameters modul"""

import pytest
import os
import glob
import configparser

import minitopsim.parameters as par

# specify cfg-folder and read file names
path = os.path.join(os.getcwd(), 'cfg_test_files')
if os.path.exists(path):
    if not os.path.isdir(path):
        raise FileNotFoundError(f'"{path}" is not a directory.')
else:
    raise FileNotFoundError(f'Directory "{path}" does not exist.')
good_files = glob.glob(os.path.join(path, 'good*.cfg'))
good_names = [os.path.basename(file) for file in good_files]
bad_files = glob.glob(os.path.join(path, 'bad*.cfg'))
bad_names = [os.path.basename(file) for file in bad_files]


@pytest.fixture()
def load_data_bank():
    """
    since the Constuction of the path to the db is not accurate if not
    called by the correct funktion it has to be done here like this
    """
    mintopsim_dir = os.path.join(os.path.dirname(__file__),
                                 os.path.pardir,
                                 os.path.pardir,
                                 'minitopsim')
    _file = os.path.join(mintopsim_dir, 'parameters.db')
    _def_config = configparser.ConfigParser()
    _def_config.read(_file)

    _categories = dict()

    # get all attributes defined in the db file
    for _section in _def_config.sections():
        for _attribute in _def_config[_section]:
            _attribute = _attribute.upper()
            _categories[_attribute] = _section
            globals()[_attribute] = \
                eval(_def_config[_section].get(_attribute))[0]


@pytest.mark.parametrize('cfg_file'
    , good_files
    , ids=good_names)
def test_load_good_parameters(load_data_bank, cfg_file):
    """"
    # todo: wirte docstring for good parameter tests
    """
    if len(good_files) == 0:
        assert False, (f'No good*.cfg files in "{path}"'
                       f'\n    no test can be preformed')
    # unit under test
    par.load_parameters(cfg_file)

    # get compare values
    cfg_config = configparser.ConfigParser()
    cfg_config.read(cfg_file)

    test_values = dict()

    # get all attributes(also values) defined in the cfg file
    for section in cfg_config.sections():
        for attribute in cfg_config[section]:
            attribute = attribute.upper()

            if attribute in globals():
                test_values[attribute] = eval(
                    cfg_config[section].get(attribute))
            else:
                assert False, (f'Attribute {attribute} not defined in '
                               f'default values!')

    # assert test for values
    for key, value in test_values.items():
        # print(f'{key} : | {eval(f'par.{key}')} = {value}')
        assert eval(f'par.{key}') == value, (f'{key} has a different value '
                                             f'than '
                                             f'{os.path.basename(cfg_file)} '
                                             f'suggests')
    # todo erweiterung auf den test der default variablen todo check via a
    #  series of files, if first loading a cfg with a new value for a
    #  attribute with default values and then loading a cfg which does not
    #  overwrite this value provides the programm with the default value and
    #  and not the value of the cfg


@pytest.mark.parametrize('cfg_file'
    , bad_files
    , ids=bad_names)
def test_load_bad_parameters(cfg_file, load_data_bank):
    """
    # todo: wirte docstring for bad parameter tests
    """
    #todo: test failure with missung_value, my suspicoun is dat if data is
    # read once it has residuals, dat let the following test pass,
    # but it should not

    try:
        par.load_parameters(cfg_file)
    except ValueError:
        assert True
        return
    except:
        assert True
        return
    # no Exception
    assert False, f'{os.path.basename(cfg_file)} threw no exception'

