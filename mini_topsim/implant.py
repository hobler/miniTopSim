'''
Description: Initialization of the corresponding surface. There is defined a class Gauss, 
which provides a callable object for calculating the Gaussian function.

Classes:
		Gauss: provides a callable object for calculating the Gaussian function.

Functions:
		__call__(self): Calculates the Gaussian function.

Additionally this module can be used as a script:
	USAGE: $ python3 implant.py [name of .cfg file]
	where: .cfg file defines the implantation for the corresponding surface

Author: Omerasevic Armin (01325962)
Part of the miniTopSim Project: https://github.com/hobler/miniTopSim 
'''
from init_surface import init_surface
from bulk import Bulk
from surface import Surface

import sys
import numpy as np
import mini_topsim.parameters as par
from scipy.interpolate import interp1d


class Gauss:
	'''
	Provides a callable object for calculating the Gaussian function.
	'''			
		
	def __call__(self, bulk):	
		'''
		Calculates the Gaussian function.
		We use it since the probability distribution for the end point of the ion trajectories 
		can be approximately described by a Gaussian function.			
		'''
		f_interp = interp1d(bulk.xvals, bulk.yvals, kind = 'cubic',bounds_error=False) 
		
		prefactor = par.DOSE*(1e-14)/(2*np.pi*par.DRP*par.DRLAT)
		Delta_R_p_pow = 2*par.DRP**2
		Delta_R_lat_pow = 2*par.DRLAT**2				
			
		conc = np.zeros(shape=(len(bulk.x_grid),len(bulk.y_grid)))
		for i, x_koor in enumerate(bulk.x_grid):  
			for j, y_koor in enumerate(bulk.y_grid):
				conc[i][j]=0.0			
				if y_koor <= f_interp(x_koor):  #inside material
					for psi_i in np.arange(x_koor - 3*par.DRLAT, x_koor + 3*par.DRLAT , par.BULK_DX): 
						if psi_i >= par.XMIN and psi_i <= par.XMAX:                     
							conc[i][j]+=np.exp(-(((np.absolute(np.absolute(y_koor)-np.absolute(f_interp(psi_i))-par.RP)) ** 2)/Delta_R_p_pow)- \
							((np.absolute(x_koor-psi_i) ** 2)/Delta_R_lat_pow))*par.BULK_DX
					conc[i][j]*=prefactor
				#print(x_koor , y_koor, conc[i][j])	
		bulk.conc = conc	

		
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
			s = Surface()
			b = Bulk(s.xvals,s.yvals)
			g = Gauss()
			g(b)
			b.write_bulk()
			b.plot_bulk()
		else:
			sys.exit("Wrong config file format .cfg!")
	else:
		sys.exit("No Config file passed!")