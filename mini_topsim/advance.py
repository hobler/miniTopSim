"""
Implements the functions to calculate the surface movement

function advance: calculates the movement of the surface
function timestep: calculates the timestep for a given time  

"""


import numpy as np
import mini_topsim.sputtering as sputter
import mini_topsim.beam as beam
import scipy.constants as sciconst
import mini_topsim.parameters as par


def advance(surface, dtime):
    """
    calculates the movement of the surface for a timestep dtime

    :param surface: surface that is being calculated
    :param dtime: timestep of the calculation
    """

    nx, ny = surface.normal_vector()
    v, v_deriv = get_velocities(surface)

    if par.TIME_INTEGRATION == 'normal':
        surface.xvals += nx * v * dtime
        surface.yvals += ny * v * dtime
    elif par.TIME_INTEGRATION == 'vertical':
        surface.yvals += v / ny * dtime
    elif par.TIME_INTEGRATION == 'characteristics':
        costheta = -ny
        costheta = np.where(costheta < 0, 0, costheta)  # eliminate overhangs
        sintheta = nx
        surface.xvals += (v * sintheta + v_deriv * costheta) * dtime
        surface.yvals += (-v * costheta + v_deriv * sintheta) * dtime

    surface.deloop()
    surface.eliminate_overhangs()


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


def get_velocities(surface):
    """
    returns the surface velocities for each point

    Depending on the ETCHING parameter this function either returns the value
    of the ETCH_RATE parameter for etching, or calculates the surface
    velocity depending on the sputter flux density.
    REDEP allows: accounting for redeposition

    costheta: the cosine of the angle between the surface normal
    and the sputter beam direction.

    sintheta: the sine of the angle between the surface normal
    and the sputter beam direction (default value None).

    :param surface: surface object

    :returns: surface velocity and its derivative for each surface point
    in a tuple
    """

    nx, ny = surface.normal_vector()

    if par.ETCHING is True:
        v = np.full_like(ny, par.ETCH_RATE)
        v_deriv = np.zeros_like(v)
        return v, v_deriv

    costheta = -ny
    costheta = np.where(costheta < 0, 0, costheta)
    sintheta = nx

    y, y_deriv = sputter.get_sputter_yield(costheta, sintheta)

    n = par.DENSITY

    f_beam = beam.beam_profile(surface.xvals)
    f_sput = f_beam * costheta * y
    f_sput_deriv = f_beam * (-sintheta * y + costheta * y_deriv)
    # f_beam ortsabhängig?

    if par.REDEP is True:
        v_factor, v_factor_deriv = surface.view_factor()
        f_redep = v_factor @ f_sput    # matrix multiplication '@'
        # assert f_redep.ndim == 1
        f_redep_deriv = v_factor_deriv @ f_sput + v_factor @ f_sput_deriv
        v = 1e7 * (f_sput - f_redep) / n
        v_deriv = 1e7 * (f_sput_deriv - f_redep_deriv) / n

    else:
        # f_beam = beam.beam_profile(surface.xvals)
        # f_sput = f_beam * y * costheta
        v = 1e7 * f_sput / n
        v_deriv = 1e7 * f_sput_deriv / n

    return v, v_deriv
