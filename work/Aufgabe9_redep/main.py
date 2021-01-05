import os, sys
filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', '..', 'mini_topsim')
sys.path.insert(0, codedir)

from surface import Surface
import parameters as par
import time

import matplotlib.pyplot as plt

config_filename="yamamura.cfg"
config_file = os.path.join(os.path.dirname(__file__), config_filename)

if not config_file.endswith('.cfg'):
    print('Error: Incorrect config.')
    sys.exit()

filename = os.path.splitext(config_file)[0] + '.srf'

if os.path.exists(filename):
    os.remove(filename)

par.load_parameters(config_file)

# my stuff

my_surface = Surface()

my_surface.plot(10)  # 10 ist nur ein Dummy
my_surface.write(10, filename)
start = time.time()
my_surface.view_factor()
stop = time.time()
print('Computation time for view_factor: ', (stop-start)*1000, 'ms')
# plt.show()


