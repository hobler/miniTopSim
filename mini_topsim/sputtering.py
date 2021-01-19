import os

import mini_topsim.parameters as par

import numpy as np
from scipy.interpolate import interp1d


def init_sputtering():
    """
    initializes the get_sputter_yield module variable

    Depending on the set parameters this function either attaches a callable
    object that implements the yamamura function to the get_sputter_yield
    variable, or one that reads the sputter yields from a given table.
    """
    global get_sputter_yield
    if par.SPUTTER_YIELD_FILE == '':
        get_sputter_yield = Sputter_yield_Yamamura(par.SPUTTER_YIELD_0,
            par.SPUTTER_YIELD_F, par.SPUTTER_YIELD_B)
    else:
        get_sputter_yield = Sputter_yield_table(par.SPUTTER_YIELD_FILE)


class Sputter_yield_Yamamura():
    """
    describes a callable object that implements the yamamura function
    """
    def __init__(self, y0, f, b):
        self.y0 = y0
        self.f = f
        self.b = b
    
    def __call__(self, costheta, sintheta=None):
        """
        calculates the sputter yield and its derivative

        Calculates the sputter yield according to the yamamura function
        and its derivative with respect to theta.

        :param costheta: the cosine of the angle between the surface normal 
        and the sputter beam direction.
        :param sintheta: the sine of the angle between the surface normal
        and the sputter beam direction (default value None).
    
        :returns: Sputter yield Y and its derivative
        """
        y = self.y0 * costheta**(-self.f) * np.exp(self.b * (1 - 1/costheta))

        if sintheta is None:
            theta = np.arccos(costheta)
            sintheta = np.sin(theta)

        y_deriv = self.y0 * sintheta * np.exp(self.b * (1 - 1/costheta)) * \
                  costheta**(-self.f - 2) * (self.f * costheta - self.b)

        # removes division by 0 errors. If costheta = 0 -> Y should be 0
        y[np.isnan(y)] = 0
        y_deriv[np.isnan(y_deriv)] = 0

        return y, y_deriv


class Sputter_yield_table():
    """
    describes a callable object that interpolates sputter yields from a given file
    """
    def __init__(self, filename):
        filepath = os.path.join(os.path.dirname(__file__), 'tables/', filename)
        print(filepath)
        data = np.genfromtxt(filepath, skip_header=1)
        tiltvals = data[:, 0]
        yieldvals = data[:, 1]
        self.yfunc = interp1d(tiltvals, yieldvals)

    def __call__(self, costheta, sintheta=None):
        """
        interpolates sputter yields from given data in a file

        :param costheta: the cosine of the angle between the surface normal 
        and the sputter beam direction
        :param sintheta: the sine of the angle between the surface normal
        and the sputter beam direction (default value None).

        :returns: Sputter yield Y
        """
        if sintheta is not None:
            # if sintheta available, calculate with it because
            # sine is injective in the relevant interval [-pi/2,pi/2]
            theta = np.arcsin(sintheta)
        else:
            theta = np.arccos(costheta)
        return self.yfunc(theta)
