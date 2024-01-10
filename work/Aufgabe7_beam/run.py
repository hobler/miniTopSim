"""
This module handles the setup and execution of minitopsim simulations and 
beam plotting functionalities.

The script sets up the necessary file directories, adjusts the system path for 
module importing, and provides the option to either plot beam configurations 
or run the minitopsim simulation based on specified configuration files.

Usage:
    The module can be run directly, with the option to enable plotting by 
    setting the 'plotting' flag. If plotting is disabled, it runs the
    minitopsim simulation using the different configuration file.

Dependencies:
    Requires the minitopsim package, including its main, parameters, and 
    plot_beam modules. The configuration files for beam setups ('const.cfg', 
    'gauss.cfg', 'erf.cfg') should be present in the appropriate directory.
"""

import os, sys

# Get the directory of the current file.
filedir = os.path.dirname(__file__)

# Set the path to the parent directory of the current file's directory.
codedir = os.path.join(filedir, '..', '..')

# Insert the parent directory path to the system path for module importing.
sys.path.insert(0, codedir)

# Import minitopsim main module, parameters and plot_beam module.
from minitopsim.main import minitopsim
import minitopsim.parameters as par
import minitopsim.plot_beam as plotBeam

# Set a flag to control the execution of plotting functionality.
plotting = True

if(plotting):
    # Initialize beam configurations if plotting is enabled.
    beam_const, beam_gauss, beam_erf = plotBeam.init_beams('const.cfg', 'gauss.cfg', 'erf.cfg')

    # Plot the beams using the initialized configurations.
    plotBeam.plot_beam(beam_const, beam_gauss, beam_erf)
else:
    # Append the configuration file to system arguments for minitopsim processing.
    sys.argv.append('const.cfg')

    # Run the minitopsim simulation.
    success = minitopsim()