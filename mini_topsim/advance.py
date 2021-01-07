"""
Implements the functions to calculate the surface movement

function advance: calculates the movement of the surface
function timestep: calculates the timestep for a given time  

"""


import numpy as np
import mini_topsim.sputtering as sputter
import scipy.constants as sciconst

import mini_topsim.parameters as par


def advance(surface, dtime):
    """
    calculates the movement of the surface for a timestep dtime

    :param surface: surface that is being calculated
    :param dtime: timstep of the calculation
    """

    nx, ny = surface.normal_vector()
    costheta = np.abs(ny)
    sintheta = np.abs(nx)

    v, v_deriv = get_velocities(costheta, sintheta)

    if par.TIME_INTEGRATION == 'normal':
        surface.xvals += nx * v * dtime
        surface.yvals += ny * v * dtime
    elif par.TIME_INTEGRATION == 'vertical':
        surface.yvals += v / ny * dtime
    elif par.TIME_INTEGRATION == 'characteristics':
        surface.xvals += (v * sintheta + v_deriv * costheta) * dtime
        surface.yvals += (-v * costheta + v_deriv * sintheta) * dtime

    surface.deloop()


def timestep(dtime, time, end_time):
    """
    calculates the timestep for a given time

    Returns the timestep if the calculation isnt overstepping the endtime
    if it would overstep it returns the resttime to calculte to the endtime.

    :param dtime: timestep
    :param time: current time in simulation
    :param end_time: endtime of the simulation

    :returns: correct timestep to reach the calculation endtime
    """
    return dtime if (time + dtime) <= end_time else (end_time - time)


def get_velocities(costheta, sintheta):
    """
    returns the surface velocities for each point

    Depending on the ETCHING parameter this function either returns the value
    of the ETCH_RATE parameter for etching, or calculates the surface
    velocity depending on the sputter flux density.

    :param costheta: the cosine of the angle between the surface normal
    and the sputter beam direction.
    :param sintheta: the sine of the angle between the surface normal
    and the sputter beam direction (default value None).

    :returns: surface velocity for each surface point
    """

    if par.ETCHING is True:
        v = np.full_like(costheta, par.ETCH_RATE)
        v_deriv = np.zeros_like(v)
    else:
        y, y_deriv = sputter.get_sputter_yield(costheta, sintheta)
        f_beam = par.BEAM_CURRENT_DENSITY/sciconst.e

        v = (f_beam * y * costheta) / par.DENSITY
        v = v*1e7  # converting cm/s --> nm/s

        v_deriv = (1e7*f_beam*y) / par.DENSITY * (-sintheta*y+costheta*y_deriv)

    return v, v_deriv
