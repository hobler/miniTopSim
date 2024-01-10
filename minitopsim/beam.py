
import numpy as np
from scipy.constants import e
from scipy.special import erf
from scipy.optimize import minimize_scalar


def init(par):
    """
    Initialize a beam object based on parameters.

    This function creates a beam object using the parameters provided. It supports
    different types of beams like constant, Gaussian, and error function beams.

    Parameters:
    par (module): A module or object that contains beam parameters including 
                  beam type, current, scan width, beam center, full width at half 
                  maximum (FWHM), and error function beam width.

    Returns:
    beam: An instance of the beam class with specified parameters.
    """
    beam_type = par.BEAM_TYPE
    if(beam_type == 'constant'):
        beam_current = par.BEAM_CURRENT_DENSITY
    else:
        beam_current = par.BEAM_CURRENT
    scan_width = par.SCAN_WIDTH
    beam_center = par.BEAM_CENTER
    FWHM = par.FWHM
    erf_beam_width = par.ERF_BEAM_WIDTH
    return beam(beam_type, beam_current, scan_width, beam_center, 
                FWHM, erf_beam_width)

class beam:
    """
    A class representing different types of beam profiles.

    This class supports constant, Gaussian, and error function beam profiles. It
    calculates the beam flux density based on the given parameters and beam type.

    Attributes:
    beam_type (str): Type of the beam ('constant', 'Gaussian', 'error function').
    beam_current (float): Beam current or current density, depending on beam type.
    scan_width (float): The scan width of the beam.
    beam_center (float): The center position of the beam.
    FWHM (float): Full width at half maximum, applicable for Gaussian and 
    error function beams.
    erf_beam_width (float): The width of the error function beam.
    """

    def __init__(self, beam_type, beam_current, scan_width, beam_center, 
                 FWHM, erf_beam_width):
        """
        Initialize the beam with specified parameters.

        Parameters:
        beam_type (str): The type of the beam.
        beam_current (float): The beam current or current density.
        scan_width (float): The scan width of the beam.
        beam_center (float): The center position of the beam.
        FWHM (float): Full width at half maximum.
        erf_beam_width (float): The width of the error function beam.
        """
        self.beam_type = beam_type
        self.beam_current = beam_current
        self.scan_width = scan_width
        self.beam_center = beam_center
        self.FWHM = FWHM
        self.erf_beam_width = erf_beam_width
    
    def __call__(self, x):
        """
        Calculate the beam flux density at a given position or positions.

        Depending on the beam type, this function calculates 
        the flux density using the appropriate formula. It can handle 
        both scalar values and NumPy arrays as input.

        Parameters:
        x (float or ndarray): The position(s) at which to calculate 
        the beam flux density.

        Returns:
        float or ndarray: The calculated beam flux density at position x. 
                          The return type matches the input type 
                          (scalar for a float input, array for an ndarray input).
        """
        if self.beam_type == 'constant':
            return self.beam_current / e
        elif self.beam_type == 'Gaussian':
            sigma = (self.FWHM / np.sqrt(8*np.log(2))) * 1e-7 # from nm to cm
            scan_width = self.scan_width * 1e-7 # from nm to cm
            return (self.beam_current / (e*np.sqrt(2*np.pi)*sigma*scan_width))*\
                   np.exp(-(x - self.beam_center)**2/(2*sigma**2))
        elif self.beam_type == 'error function':
            scan_width = self.scan_width * 1e-7 # from nm to cm
            erf_beam_width = self.erf_beam_width * 1e-7 # from nm to cm
            x1 = self.beam_center - erf_beam_width/2
            x2 = self.beam_center + erf_beam_width/2
            sigma = (self.FWHM / np.sqrt(8*np.log(2))) * 1e-7 # from nm to cm
            return (self.beam_current / (e*2*scan_width*erf_beam_width))*\
                   (erf(-(x-x2)/(np.sqrt(2)*sigma)) - erf(-(x-x1)/(np.sqrt(2)*sigma)))
        else: 
            return 0
        
    def find_maxima(self, x0):
       """
        Find the maximum flux density near a given position.

        This function uses a minimization algorithm to find the position of the 
        maximum flux density near the given starting point.

        Parameters:
        x0 (float): The starting point for the maximization algorithm.

        Returns:
        OptimizationResult: The result of the minimization algorithm.
        """
       res = minimize_scalar(lambda x: -self.__call__(x0))
       return res