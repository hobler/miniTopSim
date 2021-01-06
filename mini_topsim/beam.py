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

The initialisation function selects the beam profile based on the users beam
type choice or by using the loaded parameters.
Other functions include the get_sigma to calculate the required standard
deviation and the get_fbeam to calculate the flux beam density of the selected
beam.

This file contains the following functions:
    * init_beam_profile - initializes the beam profile
    * get_sigma - calculates the standard deviation
    * get_fbeam - calculates the beam flux density

It also includes these classes and methods:
    * BeamConstant - class used to represent the broad beam
        * __init__ - initialize the class object
        * __call__ - returns the calculated beam flux density for the broad
                     beam
    * BeamGaussian - class used to represent the Gaussian beam
        * __init__ - initialize the class object
        * __call__ - returns the calculated beam flux density for the Gaussian
                     beam
    * BeamError - class used to represent the error function beam
        * __init__ - initialize the class object
        * __call__ - returns the calculated beam flux density for the error
                     function beam
"""

import numpy as np
from scipy import constants as const
from scipy import special as sp
import parameters as par


def init_beam_profile(config=None, beam_type=None):
    """
    Initialising the beam profile according to the parameters or arguments

    Keyword arguments:
    :param config: config file to read parameters from (default None)
    :param beam_type: beam profile - can be 'constant', 'Gaussian' or
                      'error function' (default None)
    :return:
    """
    global beam_profile

    if config is not None:
        par.load_parameters(config)
    if beam_type is None:
        beam_type = par.BEAM_TYPE

    if beam_type == 'constant':
        beam_profile = BeamConstant()
    elif beam_type == 'Gaussian':
        beam_profile = BeamGaussian()
    elif beam_type == 'error function':
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


def get_fbeam(x, J=None, I=None, fwhm=None, Wx=None, Wz=None, xc=None):
    """
    Calculating the beam flux density in atoms/cm^2s

    Keyword arguments:
    :param x: x-values in nm
    :param J: beam current density in A/cm^2 for broad beam profiles
              (default None)
    :param I: beam current in A (default None)
    :param fwhm: Full Width at half maximum in nm (default None)
    :param Wx: beam width in nm for error function profiles (default None)
    :param Wz: scan width in nm (default None)
    :param xc: beam center in nm (default None)
    :return: beam flux density in atoms/cm^2s
    """
    if isinstance(beam_profile, BeamConstant):
        fbeam = beam_profile(x, J)
    elif isinstance(beam_profile, BeamGaussian):
        fbeam = beam_profile(x, I, fwhm, Wz, xc)
    elif isinstance(beam_profile, BeamError):
        fbeam = beam_profile(x, I, fwhm, Wx, Wz, xc)

    return fbeam


class BeamConstant:
    """
    Class to describe the broad beam with associated callable object
    """

    def __init__(self):
        """
        The constructor for the BeamConstant class

        Attributes:
            J: beam current density in A/cm^2
        """
        self.J = par.BEAM_CURRENT_DENSITY

    def __call__(self, x, J=None):
        """
        Callable object for calculating the beam flux density

        Keyword arguments:
        :param x: x-values in nm
        :param J: beam current density in A/cm^2 (default None)
        :return: beam flux density in atoms/cm^2s
        """
        if J is None:
            J = self.J

        fbeam = np.ones_like(x) * J / const.e

        return fbeam


class BeamGaussian:
    """
    Class to describe the Gaussian beam with associated callable object
    """

    def __init__(self):
        """
        The constructor for the BeamGaussian class

        Attributes:
            I: beam current in A
            Wz: scan width in nm
            xc: beam center in nm
            fwhm: Full Width at half maximum in nm
            sigma: standard deviation in nm
        """
        self.I = par.BEAM_CURRENT
        self.Wz = par.SCAN_WIDTH
        self.xc = par.BEAM_CENTER
        self.fwhm = par.FWHM

        self.sigma = get_sigma(self.fwhm)

    def __call__(self, x, I=None, fwhm=None, Wz=None, xc=None):
        """
        Callable object for calculating the beam flux density

        Keyword arguments:
        :param x: x-values in nm
        :param I: beam current in A (default None)
        :param fwhm: Full Width at half maximum in nm (default None)
        :param Wz: scan width in nm (default None)
        :param xc: beam center in nm (default None)
        :return: beam flux density in atoms/cm^2s
        """
        if I is None:
            I = self.I
        if fwhm is None:
            sigma = self.sigma
        else:
            sigma = get_sigma(fwhm)
        if Wz is None:
            Wz = self.Wz
        if xc is None:
            xc = self.xc

        fbeam = I / (const.e * np.sqrt(2 * sigma) * Wz) \
                * np.exp(-(x - xc) ** 2 / (2 * sigma ** 2))

        # Converting beam flux density to atoms/cm^2s
        return fbeam * 1e14


class BeamError:
    """
    Class to describe the error function beam with associated callable object
    """

    def __init__(self):
        """
        The constructor for the BeamError class

        Attributes:
            I: beam current in A
            Wx: beam width in nm
            Wz: scan width in nm
            xc: beam center in nm
            fwhm: Full Width at half maximum in nm
            sigma: standard deviation in nm
        """
        self.I = par.BEAM_CURRENT
        self.Wx = par.ERF_BEAM_WIDTH
        self.Wz = par.SCAN_WIDTH
        self.xc = par.BEAM_CENTER
        self.fwhm = par.FWHM

        self.sigma = get_sigma(self.fwhm)

    def __call__(self, x, I=None, fwhm=None, Wx=None, Wz=None, xc=None):
        """
        Callable object for calculating the beam flux density

        Keyword arguments:
        :param x: x-values in nm
        :param I: beam current in A (default None)
        :param fwhm: Full Width at half maximum in nm (default None)
        :param Wx: beam width in nm (default None)
        :param Wz: scan width in nm (default None)
        :param xc: beam center in nm (default None)
        :return: beam flux density in atoms/cm^2s
        """
        if I is None:
            I = self.I
        if fwhm is None:
            sigma = self.sigma
        else:
            sigma = get_sigma(fwhm)
        if Wx is None:
            Wx = self.Wx
        if Wz is None:
            Wz = self.Wz
        if xc is None:
            xc = self.xc

        x1 = xc - Wx / 2
        x2 = xc + Wx / 2

        fbeam = I / (2 * const.e * Wx * Wz) \
                * (sp.erf(- (x - x2) / (np.sqrt(2) * sigma))
                   - sp.erf(- (x - x1) / (np.sqrt(2) * sigma)))

        # Converting beam flux density to atoms/cm^2s
        return fbeam * 1e14
