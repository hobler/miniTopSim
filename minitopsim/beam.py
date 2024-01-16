import numpy as np
from scipy.constants import e
from scipy.special import erf
from scipy.optimize import minimize_scalar
import minitopsim.parameters as par

beam_obj = None

def init():
    """Initialize the beam object based on user-defined parameters.

    This function initializes a global beam object based on the BEAM_TYPE parameter.
    It supports three types of beams: 'constant', 'Gaussian', and 'error function'.
    """
    global beam_obj
    if(par.BEAM_TYPE == 'constant'):
        beam_obj = constant_beam(par.BEAM_CURRENT_DENSITY)
    elif(par.BEAM_TYPE == 'Gaussian'):
        beam_obj = gaussian_beam(par.BEAM_CURRENT, par.SCAN_WIDTH, 
                                 par.BEAM_CENTER, par.FWHM)
    elif(par.BEAM_TYPE == 'error function'):
        beam_obj = erf_beam(par.BEAM_CURRENT, par.SCAN_WIDTH, par.BEAM_CENTER,
                            par.FWHM, par.ERF_BEAM_WIDTH)

class beam():
    def find_maxima(self, x0):
        """Find the maximum value of the beam function.

        Parameters:
            x0 (float): Initial guess for the maximization problem.
        Returns:
            object: The result of the maximization problem.
        """
        res = minimize_scalar(lambda x: -self(x0))
        res.fun = res.fun * (-1)
        return res
    
class constant_beam(beam):

    def __init__(self, beam_current):
        """Initialize a constant beam.

        Parameters:
            beam_current (float): The current of the beam.
        """
        self.beam_current = beam_current

    def __call__(self, x):
        """Calculate the beam value at a given point for a constant beam.

        Parameters:
            x (float, ndarray): The point(s) in nm at which to calculate
            the beam value.

        Returns:
            float: The beam flux density value at the given point(s)
            in atoms/(cm^2 s).
        """
        return self.beam_current / e

class gaussian_beam(beam):
    
    def __init__(self, beam_current, scan_width, beam_center, FWHM):
        """Initialize an Gaussian beam.

        Parameters:
            beam_current (float): The current of the beam.
            scan_width (float): The scanwidth of the beam in z-direction.
            beam_center (float): The center of the beam.
            FWHM (float): Full width at half maximum of the beam.
        """
        self.beam_current = beam_current
        self.scan_width = scan_width
        self.beam_center = beam_center
        self.FWHM = FWHM
    
    def __call__(self, x):
        """Calculate the beam value at a given point for a Gaussian beam.

        Parameters:
            x (float, ndarray): The point(s) in nm at which to calculate
            the beam value.

        Returns:
            float: The beam flux density value at the given point(s)
            in atoms/(cm^2 s).
        """
        sigma = (self.FWHM / np.sqrt(8*np.log(2)))
        const = (self.beam_current / (e*np.sqrt(2*np.pi)*sigma*self.scan_width))
        const1 = 2*sigma**2
        return const*np.exp(-(x - self.beam_center)**2/const1) * 1e14 #from nm to cm 

class erf_beam(beam):

    def __init__(self, beam_current, scan_width, beam_center, FWHM, erf_beam_width):
        """Initialize an error function beam.

        Parameters:
            beam_current (float): The current of the beam.
            scan_width (float): The scanwidth of the beam in z-direction.
            beam_center (float): The center of the beam.
            FWHM (float): Full width at half maximum of the beam.
            erf_beam_width (float): The scan width of the error function beam
            in x-direction.
        """
        self.beam_current = beam_current
        self.scan_width = scan_width
        self.beam_center = beam_center
        self.FWHM = FWHM
        self.erf_beam_width = erf_beam_width

    def __call__(self, x): 
        """Calculate the beam value at a given point for an error function beam.

        Parameters:
            x (float, ndarray): The point(s) in nm at which to calculate
            the beam value.

        Returns:
            float: The beam flux density value at the given point(s)
            in atoms/(cm^2 s).
        """
        x1 = self.beam_center - self.erf_beam_width/2
        x2 = self.beam_center + self.erf_beam_width/2
        sigma = (self.FWHM / np.sqrt(8*np.log(2)))
        const = (self.beam_current / (e*2*self.scan_width*self.erf_beam_width))
        const1 = np.sqrt(2)*sigma
        return const*(erf(-(x-x2)/const1) - erf(-(x-x1)/const1)) * 1e14 #from nm to cm