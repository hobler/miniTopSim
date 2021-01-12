"""
Implementation of three beam classes to calculate  the beam flux density

This script is used to implement three different types of beams - broad beam,
Gaussian beam and error function beam through classes and calculates the beam
flux density in atoms/cm^2s according to the corresponding formula and
parameters.

The BeamConstant class is dependent on the beam current density J.
The BeamGaussian class is dependent on the beam current I, scan width Wz, beam
center xc and the Full Width at half maximum FWHM.
The BeamError class is dependent on the beam current I, scan width Wz, beam
width Wx, beam center xc and the Full Width at half maximum FWHM.

The initialisation function selects the beam profile based on the loaded
parameters.
Other functions include the get_sigma to calculate the required standard
deviation.

This file contains the following functions:
    * init_beam_profile - initializes the beam profile
    * get_sigma - calculates the standard deviation

It also includes these classes and methods:
    * BeamConstant - class used to represent the broad beam
        * __call__ - returns the calculated beam flux density for the broad
                     beam
    * BeamGaussian - class used to represent the Gaussian beam
        * __call__ - returns the calculated beam flux density for the Gaussian
                     beam
    * BeamError - class used to represent the error function beam
        * __call__ - returns the calculated beam flux density for the error
                     function beam
"""

import numpy as np
from scipy import constants as const
from scipy import special as sp
import parameters as par


def init_beam_profile():
    """
    Initialising the beam profile according to the config parameters

    :return:
    """
    global beam_profile

    if par.BEAM_TYPE == 'constant':
        beam_profile = BeamConstant()
    elif par.BEAM_TYPE == 'Gaussian':
        beam_profile = BeamGaussian()
    elif par.BEAM_TYPE == 'error function':
        beam_profile = BeamError()
    else:
        exit('Error: BEAM_TYPE invalid\n')


def get_sigma(fwhm):
    """
    Calculating the standard deviation from the Full Width at half maximum

    Keyword arguments:
    :param fwhm: Full Width at half maximum
    :return: standard deviation
    """
    return fwhm / (np.sqrt(8 * np.log(2)))


class BeamConstant:
    """
    Class to describe the broad beam with associated callable object

    Attributes:
    J: beam current density in A/cm^2
    const_f: constant factor J / e

    Methods:
    __call__(self, x): Callable object for calculating the beam flux density
    """

    def __init__(self, J=None):
        """
        The constructor for the BeamConstant class

        If the arguments are not passed in, the loaded parameters from the
        config file will be used instead.

        Keyword arguments:
        :param J: beam current density in A/cm^2 (default None)
        """
        self.J = par.BEAM_CURRENT_DENSITY if J is None else J
        self.const_f = self.J / const.e

    def __call__(self, x):
        """
        Callable object for calculating the beam flux density

        Keyword arguments:
        :param x: x-values in nm
        :return: beam flux density in atoms/cm^2s
        """
        fbeam = np.ones_like(x) * self.const_f

        return fbeam


class BeamGaussian:
    """
    Class to describe the Gaussian beam with associated callable object

    Attributes:
    I: beam current in A
    Wz: scan width in nm
    xc: beam center in nm
    fwhm: Full Width at half maximum in nm
    sigma: calculated standard deviation in nm
    const_f : constant factor I / (e * sqrt(2 * sigma) * Wz)

    Methods:
    __call__(self, x): Callable object for calculating the beam flux density
    """

    def __init__(self, I=None, fwhm=None, Wz=None, xc=None):
        """
        The constructor for the BeamGaussian class

        If the arguments are not passed in, the loaded parameters from the
        config file will be used instead.

        Keyword arguments:
        :param I: beam current in A (default None)
        :param fwhm: Full Width at half maximum in nm (default None)
        :param Wz: scan width in nm (default None)
        :param xc: beam center in nm (default None)
        """
        self.I = par.BEAM_CURRENT if I is None else I
        self.fwhm = par.FWHM if fwhm is None else fwhm
        self.Wz = par.SCAN_WIDTH if Wz is None else Wz
        self.xc = par.BEAM_CENTER if xc is None else xc
        self.sigma = get_sigma(self.fwhm)
        self.const_f = self.I / (const.e * np.sqrt(2 * self.sigma) * self.Wz)

    def __call__(self, x):
        """
        Callable object for calculating the beam flux density

        Keyword arguments:
        :param x: x-values in nm
        :return: beam flux density in atoms/cm^2s
        """
        fbeam = self.const_f * np.exp(-(x - self.xc) ** 2
                                      / (2 * self.sigma ** 2))

        # Converting beam flux density to atoms/cm^2s
        return fbeam * 1e14


class BeamError:
    """
    Class to describe the error function beam with associated callable object

    Attributes:
    I: beam current in A
    Wx: beam width in nm
    Wz: scan width in nm
    xc: beam center in nm
    fwhm: Full Width at half maximum in nm
    sigma: calculated standard deviation in nm
    const_f : constant prefactor I / (2 * e * Wx * Wz)
    x1: lower limit of the scan interval xc - Wx / 2
    x2: upper limit of the scan interval xc + Wx / 2
    """

    def __init__(self, I=None, fwhm=None, Wx=None, Wz=None, xc=None):
        """
        The constructor for the BeamError class

        If the arguments are not passed in, the loaded parameters from the
        config file will be used instead.

        Keyword arguments:
        :param I: beam current in A (default None)
        :param fwhm: Full Width at half maximum in nm (default None)
        :param Wx: beam width in nm (default None)
        :param Wz: scan width in nm (default None)
        :param xc: beam center in nm (default None)
        """
        self.I = par.BEAM_CURRENT if I is None else I
        self.fwhm = par.FWHM if fwhm is None else fwhm
        self.Wx = par.ERF_BEAM_WIDTH if Wx is None else Wx
        self.Wz = par.SCAN_WIDTH if Wz is None else Wz
        self.xc = par.BEAM_CENTER if xc is None else xc
        self.sigma = get_sigma(self.fwhm)
        self.const_f = self.I / (2 * const.e * self.Wx * self.Wz)
        self.x1 = self.xc - self.Wx / 2
        self.x2 = self.xc + self.Wx / 2

    def __call__(self, x):
        """
        Callable object for calculating the beam flux density

        Keyword arguments:
        :param x: x-values in nm
        :return: beam flux density in atoms/cm^2s
        """
        fbeam = self.const_f * \
                 (sp.erf(-(x - self.x2) / (np.sqrt(2) * self.sigma))
                   - sp.erf(- (x - self.x1) / (np.sqrt(2) * self.sigma)))

        # Converting beam flux density to atoms/cm^2s
        return fbeam * 1e14
