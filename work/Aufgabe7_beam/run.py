"""
Template for calling miniTopSim.

Feel free to copy, but do not modify the original!
"""
import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..')
sys.path.insert(0, codedir)
#sys.path.insert(0,"C:\\Users\\ACIN-Laimer\\Documents\\miniTopSim")
from minitopsim.main import minitopsim
import minitopsim.parameters as par
from minitopsim.beam import init
from plot_beam import plot_beam

plotting = True

if(plotting):
    par.load_parameters('const.cfg')
    beam_const = init(par)

    par.load_parameters('gauss.cfg')
    beam_gauss = init(par)

    par.load_parameters('erf.cfg')
    beam_erf = init(par)
    
    plot_beam(beam_const, beam_gauss, beam_erf)
    a = 1
else:
    sys.argv.append('erf.cfg')
    success = minitopsim()

