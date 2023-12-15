"""Read config from file and propagate data as python variables.

When the module is imported, the configuration is automatically loaded
from parameters.db. load_parameters() MUST be called before variables
are accessed.
Configuration variables can be accessed using 'parameters.<name>'.

Variables:
    depend on default configuration from parameters.db.

Functions:
    load_parameters(): Has to be called before variables are accessed.
        Otherwise default values are used instead of values from the
        .cfg file (this may lead to wrong data, e.g. when only a type
        is specified as default value).
"""
import os

import configparser

_categories = dict()


def _check_and_set_attributes(new_values):
    """Check if new attributes meet conditions and set variables if so.

    Args:
        new_values(dict): the new values, which should be applied.
    """
    type_err = False
    val_err = False
    err_msg = ''

    for key, value in new_values.items():
        if value is None:
            continue

        # check data type
        if type(value) is int and type(globals()[key]) is float:
            # original data type was float, new is int -> cast to float
            value = float(value)
        elif type(globals()[key]) is type:
            if type(value) is int and globals()[key] is float:
                # data type definition was float, new is int -> cast to float
                value = float(value)
            elif type(value) is not globals()[key]:
                # data type was specified without default value and new data
                # type is wrong
                err_msg = f'{err_msg}ERROR: type of {key} '\
                    f'({type(value).__name__}) does '\
                    f'not match {globals()[key]}!\n'
                type_err = True
                continue
        elif type(value) is not type(globals()[key]):
            # new data type does not match original data type
            err_msg = f'{err_msg}ERROR: type of {key} '\
                f'({type(value).__name__}) does not '\
                f'match {type(globals()[key]).__name__}!'
            type_err = True
            continue

        # check condition
        section = _categories[key]
        condition = eval(_def_config[section].get(key))[1]
        # has to be set before, otherwise condition is checked for default
        # value
        globals()[key] = value

        # if condition is None, eval(condition) is not executed
        if condition is not None and not eval(condition):
            err_msg = f'{err_msg}ERROR: Attribute {key} '\
                f'({new_values[key]}) doesn\'t meet '\
                f'condition {condition}!'
            val_err = True

    if type_err and val_err:
        # Exception is in the hierarchy above TypeError and ValueError
        raise Exception(err_msg)
    elif type_err:
        raise TypeError(err_msg)
    elif val_err:
        raise ValueError(err_msg)

    # raise an error if a variable still is not assigned
    for key, value in globals().items():
        if key.isupper() and not key.startswith("_") and type(value) is type:
            raise ValueError(f'Attribute {key} is not assigned')


def load_parameters(file: object) -> object:
    """Load parameters from file.

    Args:
        file (string): the .cfg to load the configuration from. May be
            relative to minitopsim directory or absolute.
    """
    # join directory if file is not absolute path
    if not os.path.isabs(file):
        file = os.path.join(os.getcwd(), file)

    # read config from file
    cfg_config = configparser.ConfigParser()
    cfg_config.read(file)

    new_values = dict()

    # get all attributes defined in the cfg file
    for section in cfg_config.sections():
        for attribute in cfg_config[section]:
            attribute = attribute.upper()

            if attribute in globals():
                new_values[attribute] = eval(cfg_config[section]
                                             .get(attribute))
            else:
                raise KeyError(f'Attribute {attribute} not defined in '
                               f'default values!')

    _check_and_set_attributes(new_values)


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
