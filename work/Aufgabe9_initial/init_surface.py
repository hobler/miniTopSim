"""
File: init_surface.py

Module that initializes the surface depending on the specified dtructure in the .cfg file
"""
import minitopsim.parameters as par
from minitopsim.surface import Surface
from minitopsim.io_surface import read_surface

import numpy as np

def init_surface():
    """
    Initializes the surface depending on the specified strucutre in the .cfg file

    Returns:
        Surface: The initial surface.
    """
    # Generate x values based on specified parameters
    x = np.arange(par.XMIN, par.XMAX, par.DELTA_X)
    # Define a mask based on x values within a specified range
    mask = (par.FUN_XMIN <= x) & (x < par.FUN_XMAX)
    # Initialize y as an array of zeros with the same shape as x
    y = np.zeros_like(x)

    # Check the specified surface type and initialize y accordingly
    
    # Case: Flat surface (no change needed)
    if par.INITIAL_SURFACE_TYPE == 'Flat':
        pass # surface already initialized

    # Case: Cosine surface
    elif par.INITIAL_SURFACE_TYPE == 'Cosine':
        y[mask] = par.FUN_PEAK_TO_PEAK/2 * \
            (1 - np.cos(2 * np.pi * (x[mask] - par.FUN_XMIN) / (par.FUN_XMAX - par.FUN_XMIN)))

    # Case: Double Cosine surface
    elif par.INITIAL_SURFACE_TYPE == 'DoubleCosine':
        y[mask] = par.FUN_PEAK_TO_PEAK/2 * \
            (1 - np.cos(4 * np.pi * (x[mask] - par.FUN_XMIN) / (par.FUN_XMAX - par.FUN_XMIN)))

    # Case: Step surface
    elif par.INITIAL_SURFACE_TYPE == 'Step':
        y[mask] = np.arange(par.FUN_PEAK_TO_PEAK, 0, -par.FUN_PEAK_TO_PEAK/(par.FUN_XMAX - par.FUN_XMIN))
        y[par.FUN_XMIN > x] = par.FUN_PEAK_TO_PEAK
    
    # Case: V-Shape surface
    elif par.INITIAL_SURFACE_TYPE == 'V-Shape':
        mask = (par.FUN_XMIN <= x) & (x < (par.FUN_XMAX-par.FUN_XMIN)/2 + par.FUN_XMIN)
        y[mask] = np.arange(0, par.FUN_PEAK_TO_PEAK, 2*par.FUN_PEAK_TO_PEAK/(par.FUN_XMAX - par.FUN_XMIN))
        mask = ((par.FUN_XMAX-par.FUN_XMIN)/2 + par.FUN_XMIN <= x) & (x < par.FUN_XMAX)
        y[mask] = np.arange(par.FUN_PEAK_TO_PEAK, 0, -2*par.FUN_PEAK_TO_PEAK/(par.FUN_XMAX - par.FUN_XMIN))
    
    # Case: File surface (read from a file)
    elif par.INITIAL_SURFACE_TYPE == 'File':
        with open(par.INITIAL_SURFACE_FILE) as file:
            temp = 1
            while temp is not None:
                srf, temp = read_surface(file) # extract only last surface
                if srf is not None:
                    surface = srf
        return surface
    
    # Case: Invalid surface type
    else:
        print('Error: Wrong Surface Type')

    # Return the initialized Surface object
    return Surface(x, y)