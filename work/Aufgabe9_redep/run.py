import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)
import mini_topsim.main as mtp
import numpy as np
import mini_topsim.sputtering as sputter
import mini_topsim.beam as beam
import scipy.constants as sciconst
import mini_topsim.parameters as par

#Run minitopsim
mtp.mini_topsim()
