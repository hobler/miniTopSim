"""
Module containing functions for moving the surface over time.
"""

import numpy as np
from scipy.constants import elementary_charge
from minitopsim.surface import Surface
from . import parameters as par
from . import sputtering as sput

def advance(surface, dtime):
    """
    Calculates the new surface after a time step.

    If INTERPLATION is set, the function recursively calls itself,
    with half dtime, until the new_surface has no shadows.

    Args:
        surface (Surface): The surface to be moved.
        dtime (float): The time step size.

    Returns:
        new_surface (Surface): The new, moved surface.
        dtime (float): The actually used time step size
                       (can differ from arg when using interpolation).
    """
    x = np.copy(surface.x)
    y = np.copy(surface.y)

    velocity = get_velocities(surface)

    x += velocity[0] * dtime
    y += velocity[1] * dtime

    new_surface = Surface(x, y)

    if par.INTERPOLATION:
        if new_surface.has_shadows():
            return advance(surface, dtime/2)
        else:
            new_surface.interpolate(surface.x)

    return new_surface, dtime

def timestep(dt, time, tend):
    """
    Calculates the time step at a given time.

    Args:
        dt (float): The time step size.
        time (float): The time that has passed since initial evaluation.
        tend (float): The end time of the simulation.

    Returns:
        float: The time step size at the given time.

    The return normally is just dt, except when time + dt > tend. In
    that case, a timestep is returned so that tend is reached exactly.
    """
    if time + dt > tend:
        return tend - time

    return dt

def get_velocities(surface):
    """ Calculates the velocities used for advancing the surface.

    Calculates the velocities used for advancing in x- & y-direction,
    using the parameters from parameters.py.

    Args:
        surface (Surface): surface for which to calculate the velocities.

    Returns:
        array-like (2xn): velocities in x- & y-direction (row 1/2)
    """
    normal_vec = surface.normal_vector()

    if par.ETCHING:
        v_normal = np.full_like(surface.x, par.ETCH_RATE) #normal velocity [nm/s]
    else:
        cos_theta = -normal_vec[1]
        Y_s = sput.get_sputter_yield(cos_theta)
        Y_s = np.nan_to_num(Y_s)    #prevents wierd behavoir from loops
        F_beam = par.BEAM_CURRENT_DENSITY / elementary_charge
        F_sput = F_beam * Y_s * cos_theta
        
        if par.REDEP:
            F_redep = np.matmul(surface.view_factor(), F_sput)
            v_normal = (F_sput - F_redep)/ par.DENSITY     #[cm/s]                             
        else:
            v_normal = F_sput/ par.DENSITY                 #[cm/s]
                                        
    v_normal *= 1e7  #[nm/s]   
                                   
    if not par.INTERPOLATION: 
        if surface.has_shadows():
            msk = surface.get_shadows()
            v_normal[msk] = 0

    return np.matmul(normal_vec , v_normal)