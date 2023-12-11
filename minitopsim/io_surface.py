"""
Module cotaining functions for calculating a surface and writing it to
a file.
"""
from surface import Surface

import numpy as np
from math import cos, pi
from math import cos, pi


def init_surface():
    """
    Initially implements the surface for x values between -50 and 50.

    Returns:
        Surface: The initial surface.
    """
    x = np.linspace(-50, 50, 100)

    # Define the surface
    y = np.zeros_like(x)
    y[25:76] = -50 * (1 + np.cos(2 * np.pi * x[25:76] / 50))

    return Surface(x, y)


def write_surface(surface, time, srf_fobject):
    """
    Writes the surface evaluated at a given time to the
    file-object srf_fobject.

    Args:
        surface (Surface): The surface to be written.
        time (float): The time that passed since initial evaluation.
        srf_fobject (file-object): The .srf-file to which the surface
            is written.

    Returns:
        bool: True if the surface was written successfully,
            False otherwise.

    The File is formatted in the following way:
        surface: time npoints x-positions y-positions
        x[0] y[0]
        x[1] y[1]
        ...
        x[npoints-1] y[npoints-1]

    Here, time is the time that has passed since the initial,
    and npoints is the number of points on the surface.

    The name of the file should have the format
    "basic_<tend>_<dt>.srf", where <tend> is the end time and
    <dt> is the time step size.
    """
    try:
        mode = 'w' if time == 0 else 'a'
        with open(srf_fobject, mode) as file:
            file.write("surface: " + str(time) + " " + str(len(surface.x))
                       + "x-positions y-positions\n")
            for i in range(len(surface.x)):
                file.write(str(surface.x[i]) + " " + str(surface.y[i]) + "\n")
    except Exception as e:
        print("An error occurred while writing the surface to the file:",
              str(e))
        return False

    print("Surface written to file.")
    return True

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