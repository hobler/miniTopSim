"""
Template for calling miniTopSim.

Feel free to copy, but do not modify the original!
"""

import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'minitopsim')
sys.path.insert(0, codedir)

sys.argv.append('work/Aufgabe9_initial/cosine_dt0_5.cfg')
sys.argv.append('work/Aufgabe9_initial/cosine.srf')

from minitopsim.main import minitopsim
import minitopsim.parameters as par
import init_surface
from minitopsim.io_surface import read_surface

success = minitopsim()


 