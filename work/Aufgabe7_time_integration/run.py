"""
Template for calling miniTopSim.

Feel free to copy, but do not modify the original!
"""
import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

from mini_topsim.main import mini_topsim

success = mini_topsim()

