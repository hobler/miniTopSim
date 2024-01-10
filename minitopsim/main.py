"""
Main script and function to run miniTopSim.
"""
from . import parameters as par
from minitopsim.advance import advance, timestep
from minitopsim.io_surface import init_surface, write_surface
from minitopsim.plot import plot
from minitopsim.surface import Shadow_Error

import sys

def minitopsim():
    par.load_parameters(sys.argv[1])
    
    time = 0
    tend = par.TOTAL_TIME
    dt = timestep(par.TIME_STEP, time, tend)
    filename = sys.argv[1].replace('.cfg', '')

    # Initialize the surface
    surface = init_surface()

    # Write and plot initial surface
    if not write_surface(surface, 0, filename + '.srf'):
        exit()

    try:
        while dt > 0:
            surface, dt = advance(surface, dt)
            time += dt
            if not write_surface(surface, time, filename + '.srf'):
                exit()
            print(f'time = {time}, dt = {dt}')
            dt = timestep(par.TIME_STEP, time, tend)
    except Shadow_Error as err_msg:
        print(f"A Shadow_Error occurred: {err_msg}")
        print(f"Simulation was stopped at {time}s.")
        print(f"Please change xmin/xmax parameters and try again.")
    finally:
        if par.PLOT_SURFACE:
            plot(filename + '.srf')

    return True