"""
Script to compare the three beam flux densities graphically

The function plot_beam_comparison allows user to graphically compare the three
different beam flux densities from the associated beam classes BeamConstant with
a broad beam, BeamGaussian with a Gaussian beam and BeamError with an error
function beam. Additionally, user can set the parameters J, I, fwhm, Wx, Wz and
xc according to their needs.
The output is an image stored in the working directory.

This file contains the following functions:
    * plot_beam_comparison - calculates the three different beam flux densities
"""

import os
import sys
import matplotlib.pyplot as plt
import numpy as np

# Adding the code directory to sys.path
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

import mini_topsim.beam as beam


def plot_beam_comparison():
    """
    Calculating and plotting the different beam flux densities

    :return:
    """
    xmin = -1000
    xmax = 1000
    step = 1
    xvals = np.arange(xmin, xmax + 1, step)

    # Initialize parameters
    beam.init_beam_profile(config='const.cfg')

    # Broad beam
    beam.init_beam_profile(beam_type='constant')
    fbeam_constant = beam.get_fbeam(x=xvals)

    # Gaussian beam
    beam.init_beam_profile(beam_type='Gaussian')
    fbeam_Gaussian = beam.get_fbeam(x=xvals, I=0.92e-13)

    # Error function beam
    beam.init_beam_profile(beam_type='error function')
    fbeam_error = beam.get_fbeam(x=xvals, I=1e-11)

    # Plotting the three different diagrams
    fig, ax = plt.subplots()
    ax.plot(xvals, fbeam_constant, 'b-', label=r'$Broad\ beam$')
    ax.plot(xvals, fbeam_Gaussian, 'r--', label=r'$Gaussian\ beam$')
    ax.plot(xvals, fbeam_error, 'g:', label=r'$Error\ function\ beam$')
    ax.set_title('Beam flux density')
    ax.set_xlabel(r'$x\ in\ nm$')
    ax.set_ylabel(r'$F_{beam}(x)\ in\ \frac{atoms}{cm^2s}$')
    ax.legend(loc='lower right')
    ax.grid(which='both')

    plt.show()
    fig.savefig('plot_beam.png')


if __name__ == '__main__':
    plot_beam_comparison()
