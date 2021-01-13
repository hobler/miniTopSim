"""
Script to run miniTopSim code from work directory Aufgabe8_beam

Usage: $python3 run.py <.cfg file>
"""

import os
import sys

# Adding the code directory to sys.path
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

from mini_topsim.main import mini_topsim

mini_topsim()
