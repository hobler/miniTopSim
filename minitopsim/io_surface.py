"""
File: io_surface.py

A module providing functions to read surface information from a file-like object.
"""

from minitopsim.surface import Surface
import numpy as np

def read_surface(srf_fobj):
    """
    Reads surface information from a file-like object.

    Args:
        srf_fobj (file): A file-like object containing surface information.

    Returns:
        tuple: A tuple containing a Surface object and the current time.
               If no surface information is available, returns (None, None).
    """
    surface_info = srf_fobj.readline().split()

    if not surface_info:
        return None, None

    current_time = float(surface_info[1])
    npoints = int(surface_info[2])

    x_coords = np.zeros(npoints)
    y_coords = np.zeros(npoints)

    for i in range(npoints):
        line = srf_fobj.readline().split()
        x_coords[i] = float(line[0])
        y_coords[i] = float(line[1])

    return Surface(x_coords, y_coords), current_time