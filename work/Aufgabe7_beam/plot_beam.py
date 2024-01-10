import numpy as np
import matplotlib.pyplot as plt

def plot_beam(beam_const, beam_gauss, beam_erf):
    x = np.linspace(-1000, 1000, 10000) * 1e-7 # in cm
    F_const = np.full(len(x), beam_const(x))
    F_gauss = beam_gauss(x)
    F_erf = beam_erf(x)

    plt.plot(x, F_const, label='constant')
    plt.plot(x, F_gauss, label='gaussian')
    plt.plot(x, F_erf, label='error function')
    plt.legend()
    plt.show()

