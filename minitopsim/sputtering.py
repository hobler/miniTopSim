"""Module used for calculating sputtering yield."""

import numpy as np
from . import parameters as par

def get_sputter_yield(cos_theta):
    """Calculates Sputtering Yield according to Yamamura Function.

    Evaluates the yamamura function using the parameters from parameters.py.

    Args:
        cos_theta (array-like): cosine of tilt angle theta

    Returns:
        array-like: value of the yamamura function
    """
    y0 = par.SPUTTER_YIELD_0
    f = par.SPUTTER_YIELD_F
    b = par.SPUTTER_YIELD_B

    sputter_yield = y0 * cos_theta**(-f) * np.exp(b*(1-1/cos_theta))
    return sputter_yield