"""
Main script and function to run miniTopSim.
"""
from . import parameters as par
from minitopsim.advance import advance, timestep
from minitopsim.io_surface import write_surface
from work.Aufgabe9_initial.init_surface import init_surface
from minitopsim.plot import plot
from minitopsim.surface import Shadow_Error
from time import process_time

import sys
import os

def minitopsim():
    par.load_parameters(sys.argv[1])

    time = 0
    tend = par.TOTAL_TIME
    dt = timestep(par.TIME_STEP, time, tend)
    filename = sys.argv[1].replace('.cfg', '')

    # Initialize the surface
    surface = init_surface()

    # Write and plot initial surface
    if not write_surface(surface, time, filename + '.srf'):
        exit()

    t_start = process_time()   

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
        t_stop = process_time()
        print("Calculation time:", t_stop - t_start, "s")
        
        if par.PLOT_SURFACE:
            # Check if .srf_save is in directory
            if os.path.isfile(filename + '.srf_save'):
                print(f".srf_save file is found and used")
                plot(filename + '.srf', filename + '.srf_save')
            # Check if other .srf is specified
            elif len(sys.argv) >= 3:
                plot(filename + '.srf', sys.argv[2])
            else:
                print('No .srf_save file found / Please provide a .srf file as additional argument')

    return True