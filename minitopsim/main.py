"""
Main script and function to run miniTopSim.
"""
import minitopsim.parameters as par
from minitopsim.advance import advance, timestep
from minitopsim.io_surface import init_surface, write_surface
from minitopsim.plot import plot

import sys
import matplotlib.pyplot as plt


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


    while dt > 0:
        surface = advance(surface, dt, par.ETCH_RATE)
        if not write_surface(surface, time + dt, filename + '.srf'):
            exit()
        time += dt
        dt = timestep(dt, time, tend)
        print(f'time = {time}, dt = {dt}')

    if par.PLOT_SURFACE:
        plot(filename + '.srf')

    """        surface.plot("Initial Surface")

    # Move surface over time until tend is reached
    while dt > 0:
        surface = advance(surface, dt, par.ETCH_RATE)
        if not write_surface(surface, time + dt, filename + '.srf'):
            exit()
        time += dt
        dt = timestep(dt, time, tend)
        print(f'time = {time}, dt = {dt}')

    # Plot final surface and save plot
    if par.PLOT_SURFACE:
        surface.plot("Final Surface")
        plt.legend()
        plt.title(f'Sputtering yield simulation, tend = {tend}s, dt = '
                f'{par.TIME_STEP}s')

        plt.savefig(filename + '.png')
        plt.show()"""

    return True
