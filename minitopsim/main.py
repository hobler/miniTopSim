"""
Main script and function to run miniTopSim.
"""
import parameters as par
import sys

sys.path.append("..")
from work.Aufgabe1_basic.advance import advance, timestep
from work.Aufgabe1_basic.io_surface import init_surface, write_surface
from work.Aufgabe1_basic.surface import Surface

def minitopsim():
   print('Running miniTopSim ...')
   print(f'TestParameter={par.TestParameter}')
   return True



