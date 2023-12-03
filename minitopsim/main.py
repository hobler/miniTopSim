"""
Main script and function to run miniTopSim.
"""
import parameters as par
from advance import advance, timestep
from io_surface import init_surface, write_surface

import sys
import matplotlib.pyplot as plt


def minitopsim():
    time = 0
    tend = float(sys.argv[1])
    dt = timestep(float(sys.argv[2]), time, tend)
    filename = f'basic_{tend}_{dt}'

    # Initialize the surface
    surface = init_surface()

    # Write and plot initial surface
    if not write_surface(surface, 0, filename + '.srf'):
        exit()
    surface.plot("Initial Surface")

    # Move surface over time until tend is reached
    while dt > 0:
        surface = advance(surface, dt)
        if not write_surface(surface, time + dt, filename + '.srf'):
            exit()
        time += dt
        dt = timestep(dt, time, tend)
        print("time = ", time, "dt = ", dt)

    # Plot final surface and save plot
    surface.plot("Final Surface")
    plt.legend()
    plt.title("Sputtering yield simulation, tend = " + str(tend) +
              "s, dt = " + sys.argv[2] + "s")

    plt.savefig(filename + '.png')
    plt.show()

    return True
