"""Read config from file and propagate data as python variables.

Configuration variables can be accessed using 'parameters.<name>'.
"""
import os

import configparser

_categories = dict()

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
