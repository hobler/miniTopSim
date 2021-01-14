'''
Description: Initialization of the corresponding surface. There is definded a class Gaus, 
which provides a callable object for calculating the Gauss function.

Classes:
		 Gauss: BESCHREIBUNG_FEHLT

Functions:

naziv_1_funkcije(): BESCHREIBUNG_FEHLT
naziv_2_funkcije(): BESCHREIBUNG_FEHLT

Additionally this module can be used as a script:
	USAGE: $ python3 implant.py [Name of .cfg file]
	where: .cfg file defines the implantation for the corresponding surface

Author: Omerasevic Armin (01325962)
Part of the miniTopSim Project: https://github.com/hobler/miniTopSim 
'''
import os, sys
from init_surface import init_surface
import parameters as par
import matplotlib.pyplot as plt
import numpy as np
import math

# Test
from bulk import Bulk


class Gauss:
	def __init__(self):
		
		self.x_grid = np.arange(par.XMIN, par.XMAX + 1, par.BULK_DX)
		self.y_surface = init_surface(self.x_grid)
		
		gridline_nextTo_y_min_surface = int(np.amin(self.y_surface)/par.BULK_DY - 1) * par.BULK_DY
		self.y_grid = np.arange((gridline_nextTo_y_min_surface), 0 + 1, par.BULK_DY)
		
		
	def __call__(self):
		surface_dict = dict(zip(self.x_grid, self.y_surface))
		
		const = par.DOSE*(1e-14)/(2*np.pi*par.DRP*par.DRLAT)
		Delta_R_p_pow = 2*par.DRP**2
		Delta_R_lat_pow = 2*par.DRLAT**2
		
		triplets = []
		for x_koor in self.x_grid:  
			for y_koor in self.y_grid:
				C = 0
				if y_koor < surface_dict[x_koor]:
					for psi_i in np.arange(x_koor-3*par.DRLAT, x_koor+3*par.DRLAT + 1, par.BULK_DX):
						if psi_i >= par.XMIN and psi_i <= par.XMAX:                     
							C+=math.exp((-math.pow((y_koor-surface_dict[psi_i]-par.DRP), 2)/Delta_R_p_pow)-(math.pow((x_koor-psi_i), 2)/Delta_R_lat_pow))*par.BULK_DX
				triplets.append((x_koor, y_koor, C))
			
		dotierstoffkonz = [h[2] for h in triplets]	
		#print(len(dotierstoffkonz))
		#print(len(self.x_grid))
		#print(len(self.y_grid))
		return self.x_grid, self.y_grid, dotierstoffkonz

if __name__ == '__main__':
	if(len(sys.argv) == 2):
		config_file = sys.argv[1]
		if config_file.endswith(".cfg"):
			par.load_parameters(config_file)
			gauss = Gauss()
			x, y, c = gauss()
			new_b = Bulk(x, y, c)
			new_b.write_bulk()
			new_b.plot_bulk()
			print()
			
			# # Test plot
			# plt.plot(gaus.bulk_dx, gaus, "x-", label="C_arr")
			# plt.title('Surface')
			# plt.xlabel('x[nm]')
			# plt.ylabel('y[nm]')
			# plt.show()
		else:
			sys.exit("Wrong config file format .cfg!")
	else:
		sys.exit("No Config file passed!")