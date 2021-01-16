'''
Description: Initialization of the corresponding surface. There is defined a class Gauss, 
which provides a callable object for calculating the Gaussian function.

Classes:
		Gauss: provides a callable object for calculating the Gaussian function.

Functions:

	__init__(self): Initializes all parameters of the class Gauss.
	__call__(self): Calculates the Gaussian function.

Additionally this module can be used as a script:
	USAGE: $ python3 implant.py [name of .cfg file]
	where: .cfg file defines the implantation for the corresponding surface

Author: Omerasevic Armin (01325962)
Part of the miniTopSim Project: https://github.com/hobler/miniTopSim 
'''
import sys
import matplotlib.pyplot as plt
import numpy as np
import mini_topsim.parameters as par
from init_surface import init_surface
from bulk import Bulk


class Gauss:
	'''
	Provides a callable object for calculating the Gaussian function.
	'''
	def __init__(self):
		'''
		Initializes all class parameters.
		'''
		self.x_grid = np.arange(par.XMIN, par.XMAX + 1, par.BULK_DX)
		self.y_surface = init_surface(self.x_grid)
		gridline_min_surface = int(np.amin(self.y_surface)/par.BULK_DY - 1) * par.BULK_DY
		self.y_grid = np.arange(gridline_min_surface - par.RP - 3*par.DRP, 0 + 1, par.BULK_DY)		
		
	def __call__(self):	
		'''
		Calculates the Gaussian function.
		We use it since the probability distribution for the end point of the ion trajectories 
		can be approximately described by a Gaussian function.
		
		Returns: nodes of a regular lattice for which the dopant concentration should be calculated and
		the dopant concentration for every node.
			
		'''
		surface_dict = dict(zip(self.x_grid, self.y_surface))
		prefactor = par.DOSE*(1e-14)/(2*np.pi*par.DRP*par.DRLAT)
		Delta_R_p_pow = 2*par.DRP**2
		Delta_R_lat_pow = 2*par.DRLAT**2
		
		conc = np.zeros(shape=(len(self.x_grid),len(self.y_grid)))
		for i, x_koor in enumerate(self.x_grid):  
			for j, y_koor in enumerate(self.y_grid):
				conc[i][j] = 0
				if y_koor < surface_dict[x_koor]:
					for psi_i in np.arange(x_koor - 3*par.DRLAT, x_koor + 3*par.DRLAT + 1, par.BULK_DX):  #Fehler in der Angabe?
						if psi_i >= par.XMIN and psi_i <= par.XMAX:                     
							conc[i][j]+=np.exp(((-(y_koor-surface_dict[psi_i]-par.RP) ** 2)/Delta_R_p_pow)- \
							(((x_koor-psi_i) ** 2)/Delta_R_lat_pow))*par.BULK_DX
				conc[i][j]*=prefactor*100
				
		conc = np.transpose(conc)	
		return self.x_grid, self.y_grid, conc

if __name__ == '__main__':
	'''
	This module can be used as a script to plot dopant concentration on the nodes of a regular lattice,
	to write the dopant distribution of the nodes to a file or to save the plot as .png file if needed.

	USAGE: $ python implant.py [name of .cfg file]
	'''
	if(len(sys.argv) == 2):
		config_file = sys.argv[1]
		if config_file.endswith(".cfg"):
			par.load_parameters(config_file)
			gauss = Gauss()
			x, y, conc = gauss()
			bulk_obj = Bulk(x, y, conc)
			bulk_obj.write_bulk()
			bulk_obj.plot_bulk()
		else:
			sys.exit("Wrong config file format .cfg!")
	else:
		sys.exit("No Config file passed!")