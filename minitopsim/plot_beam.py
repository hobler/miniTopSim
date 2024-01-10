"""
This module provides functionality for initializing and plotting different types 
of beam profiles used in minitopsim simulations. It includes capabilities to 
initialize beams with constant, Gaussian, and error function profiles and 
plot their flux densities for comparison.

Functions:
    init_beams(const_cfg, gauss_cfg, erf_cfg) - Initializes beams with the 
        specified configuration files for constant, Gaussian, and 
        error function profiles.
    plot_beam(beam_const, beam_gauss, beam_erf) - Plots the flux density for 
        the given beam profiles over a specified range.
"""


import numpy as np
import matplotlib.pyplot as plt
import minitopsim.parameters as par
from minitopsim.beam import init

def init_beams(const_cfg, gauss_cfg, erf_cfg):
    """
    Initialize beams with constant, Gaussian, and error function profiles.

    Parameters:
    const_cfg (str): File path for the constant beam configuration.
    gauss_cfg (str): File path for the Gaussian beam configuration.
    erf_cfg (str): File path for the error function beam configuration.

    Returns:
    tuple: A tuple containing three initialized beams (constant, Gaussian, error function).
    """
    par.load_parameters(const_cfg)
    beam_const = init(par)

    par.load_parameters(gauss_cfg)
    beam_gauss = init(par)

    par.load_parameters(erf_cfg)
    beam_erf = init(par)
    
    return beam_const, beam_gauss, beam_erf

def plot_beam(beam_const, beam_gauss, beam_erf):
    """
    Plot the beam flux density for constant, Gaussian, and error function 
    beam profiles.

    This function creates a plot comparing the beam flux density across different 
    beam profiles over a specified range. The plot is saved as 'plot_beam.png'.

    Parameters:
    beam_const (callable): The constant beam profile function.
    beam_gauss (callable): The Gaussian beam profile function.
    beam_erf (callable): The error function beam profile function.
    """
    x = np.linspace(-1000, 1000, 10000) * 1e-7 # Convert from nm to cm
    F_const = np.full(len(x), beam_const(x))
    F_gauss = beam_gauss(x)
    F_erf = beam_erf(x)
    x = x * 1e7 # Convert back from cm to nm
    plt.title('Beam flux density for different beam profiles', fontsize=12)
    plt.plot(x, F_const, label='constant')
    plt.plot(x, F_gauss, label='gaussian')
    plt.plot(x, F_erf, label='error function')
    plt.ylabel('Beam flux density $F_{beam}$ in atoms/cm$^2$s', fontsize=12)
    plt.xlabel('Position $x$ in nm', fontsize=12)
    plt.grid()
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig('plot_beam.png')
    plt.legend()
    plt.show()
