"""Read config from file and propagate data as python variables.

Configuration variables can be accessed using 'parameters.<name>'.

Variables:
    depend on content from parameters.db.

Functions:
    load_parameters(): Has to be called before variables are accessed.
        Otherwise default values are used instead of values from the
        .cfg file (this may lead to wrong data, e.g. when only a type
        is specified as default value).
"""
import os

import configparser

_categories = dict()


def load_parameters(file):
    """Load parameters from file.

    Args:
        file (string): the .cfg to load the configuration from. May be
            relative to minitopsim directory or absolute.
    """
    # join directory if file is not absolute path
    if not os.path.isabs(file):
        file = os.path.join(os.path.dirname(__file__), file)

    # read config from file
    cfg_config = configparser.ConfigParser()
    cfg_config.read(file)

    new_values = dict()

    # get all attributes defined in the cfg file
    for section in cfg_config.sections():
        for attribute in cfg_config[section]:
            attribute = attribute.upper()
            new_values[attribute] = eval(cfg_config[section].get(attribute))

    for attribute, value in new_values.items():
        if value is not None:
            globals()[attribute] = value


# load default config from file
_file = os.path.join(os.path.dirname(__file__), "parameters.db")
_def_config = configparser.ConfigParser()
_def_config.read(_file)

# get all attributes defined in the db file
for _section in _def_config.sections():
    for _attribute in _def_config[_section]:
        _attribute = _attribute.upper()
        _categories[_attribute] = _section
        globals()[_attribute] = eval(_def_config[_section].get(_attribute))[0]
