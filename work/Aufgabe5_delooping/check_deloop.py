"""tests the deloop() method of the surface class"""

import numpy as np
import matplotlib.pyplot as plt
from minitopsim.surface import Surface

if __name__ == '__main__':
    # surfaces with loops
    x_loops_1 = np.array([0, 3, 2, 2, 7, 7, 6, 9])
    y_loops_1 = np.array([2, 1, 3, 0, 0, 3, 1, 2])

    x_loops_2 = np.array([0, 5, 3, 2, 6, 8])
    y_loops_2 = np.array([1, 1, 3, 0, 3, 1])

    # surfaces without loops
    surface1 = Surface(x_loops_1, y_loops_1)
    x_delooped_1, y_delooped_1 = surface1.deloop(x_loops_1, y_loops_1)

    surface2 = Surface(x_loops_2, y_loops_2)
    x_delooped_2, y_delooped_2 = surface2.deloop(x_loops_2, y_loops_2)

    # plotting surfaces
    fig, axs = plt.subplots(2, 2, sharey=True)
    fig.suptitle("Delooping Surfaces")

    axs[0, 0].plot(x_loops_1, y_loops_1, "b*-")
    axs[0, 1].plot(x_delooped_1, y_delooped_1, "b*-")
    axs[1, 0].plot(x_loops_2, y_loops_2, "g*-")
    axs[1, 1].plot(x_delooped_2, y_delooped_2, "g*-")

    # plt.savefig("check_deloop.png")
    plt.show()
