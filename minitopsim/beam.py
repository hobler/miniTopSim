
import numpy as np
import scipy
from scipy.constants import e
from scipy.special import erf
from scipy.optimize import minimize_scalar


def init(par):
    beam_type = par.BEAM_TYPE
    if(beam_type == 'constant'):
        beam_current = par.BEAM_CURRENT_DENSITY
    else:
        beam_current = par.BEAM_CURRENT
    scan_width = par.SCAN_WIDTH
    beam_center = par.BEAM_CENTER
    FWHM = par.FWHM
    erf_beam_width = par.ERF_BEAM_WIDTH
    return beam(beam_type, beam_current, scan_width, beam_center, FWHM, erf_beam_width)

class beam:
    def __init__(self, beam_type, beam_current, scan_width, beam_center, FWHM, erf_beam_width):
        self.beam_type = beam_type
        self.beam_current = beam_current
        self.scan_width = scan_width
        self.beam_center = beam_center
        self.FWHM = FWHM
        self.erf_beam_width = erf_beam_width
    
    def __call__(self, x):
        if self.beam_type == 'constant':
            return self.beam_current / e
        elif self.beam_type == 'Gaussian':
            sigma = (self.FWHM / np.sqrt(8*np.log(2))) * 1e-7 # from nm to cm
            scan_width = self.scan_width * 1e-7 # from nm to cm
            return (self.beam_current / (e*np.sqrt(2*np.pi)*sigma*scan_width)) * np.exp(-(x - self.beam_center)**2/(2*sigma**2))
        elif self.beam_type == 'error function':
            scan_width = self.scan_width * 1e-7 # from nm to cm
            erf_beam_width = self.erf_beam_width * 1e-7 # from nm to cm
            x1 = self.beam_center - erf_beam_width/2
            x2 = self.beam_center + erf_beam_width/2
            sigma = (self.FWHM / np.sqrt(8*np.log(2))) * 1e-7 # from nm to cm
            return (self.beam_current / (e*2*scan_width*erf_beam_width)) * (erf(-(x-x2)/(np.sqrt(2)*sigma)) - erf(-(x-x1)/(np.sqrt(2)*sigma)))
        else: 
            return 0
        
    def find_maxima(self, x0):
       res = minimize_scalar(lambda x: -self.__call__(x0))
       return res