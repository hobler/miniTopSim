from work.Aufgabe1_basic.surface import Surface
from work.Aufgabe1_basic.io_surface import write_surface

"""
Module containing functions for moving the surface over time.
"""

def advance(surface, dtime):
    """
    Calculates the new surface after a time step.

    Args:
        surface (Surface): The surface to be moved.
        dtime (float): The time step size.
    
    Returns:
        Surface: The new surface. 
    """
    x = surface.x
    y = surface.y

    normal_v = surface.normal_vector()

    x += normal_v[0] * dtime
    y += normal_v[1] * dtime

    return Surface(x, y)

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