"""tests the has_shadows/get_shadows methods of the surface class"""

import numpy as np
import matplotlib.pyplot as plt
from minitopsim.surface import Surface

if __name__ == '__main__':
    #surface with no shadows, since xvals only increase
    x_no_shadows = np.arange(21)
    y_no_shadows = np.ones_like(x_no_shadows)

    #surface with shadows, since xvals don't only increase
    x_shadows_1 = np.array([0, 1, 2, 2, 1, 3, 5, 4, 4, 5, 6])
    y_shadows_1 = np.array([0, 0, 0, -1, -2, -2, -2, -1, 0, 0, 0])

    x_shadows_2 = np.array([0, 1, 2, 3, 4, 3, 5, 4, 3, 5, 6])
    y_shadows_2 = np.array([0, -0.5, 0.5, 0, 0, 1, 1, -1, -2, -2, -1])

    srf_no_shadows = Surface(x_no_shadows, y_no_shadows)
    srf_shadows_1 = Surface(x_shadows_1, y_shadows_1)
    srf_shadows_2 = Surface(x_shadows_2, y_shadows_2)

    assert(srf_no_shadows.has_shadows() == False)
    assert(srf_shadows_1.has_shadows() == True)
    assert(srf_shadows_2.has_shadows() == True)

    msk_1 = srf_shadows_1.get_shadows()
    msk_2 = srf_shadows_2.get_shadows()

    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Shadowed Surfaces")

    ax1.plot(srf_shadows_1.x, srf_shadows_1.y, "b*--", label="Surface")
    ax1.plot(srf_shadows_1.x[msk_1], srf_shadows_1.y[msk_1],
             "rx", label="Shadows", markersize=12)

    ax2.plot(srf_shadows_2.x, srf_shadows_2.y, "g*--", label="Surface")
    ax2.plot(srf_shadows_2.x[msk_2], srf_shadows_2.y[msk_2],
             "rx", label="Shadows", markersize=12)

    ax1.legend(loc="lower left")
    ax2.legend(loc="lower left")

    #plt.savefig("check_shadows.png")
    plt.show()