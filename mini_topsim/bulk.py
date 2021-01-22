'''
Description: Implementation of the Bulk class with methods for writing and plotting the dopant distribution.

Classes:
		Bulk: provides plotting and writing functions for the object of this class
		
Functions:
	write_bulk(): Writes the dopant distribution for the corresponding node coordinates to an .out file.
	plot_bulk():  Plots dopant concentration on the nodes of a regular lattice

Author: Omerasevic Armin (01325962)
Part of the miniTopSim Project: https://github.com/hobler/miniTopSim 
'''
import os
import matplotlib.pyplot as plt
import numpy as np
import mini_topsim.parameters as par


filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', 'work', 'Aufgabe16_implant/')


class Bulk:
	'''
	Provides the functions for plotting a dopant distribution of a corresponding surface
	as well as saving a class Bulk data to an .out file.
	'''
	def __init__(self, xvals, yvals, conc=False):
		'''
		Initializes all class parameters.
		'''
		self.xvals = xvals
		self.yvals = yvals
		self.x_grid = np.arange(par.XMIN, par.XMAX , par.BULK_DX)
		self.y_grid = np.arange(np.amin(self.yvals) - par.RP - 3*par.DRP, 0+5 , par.BULK_DY)	
		self.conc = conc 
		self.save_data_form = codedir + f"{par.INITIAL_SURFACE_TYPE.lower()}"			
	
	def write_bulk(self):
		'''
		Writes the dopant distribution for the corresponding node coordinates to an .out file.
		'''
		with open(codedir + f"/Bulk_{par.INITIAL_SURFACE_TYPE}.out", 'w') as bulk_out_file:
			bulk_out_file.write("Dopant distribution\n\tX\t\tY\t\tconc\n")
			for i, x_koor in enumerate(self.x_grid):  
				for j, y_koor in enumerate(self.y_grid):
					bulk_out_file.write(f"{x_koor:7.2f}\t{y_koor:7.2f}\t\t{self.conc[i][j]:.3E}\n")
					

	def plot_bulk(self, save_fig=False):
		'''
		Plots dopant concentration on the nodes of a regular lattice with contour lines at concentrations 
		0.1, 0.2, ... 1.0 of the maximum occurring concentration.
	
		Arg: 
			save_fig: Decides between plotting the concentration of the nodes and saving of the plot as .jpg image
		'''	
		norm_conc = np.transpose(self.conc)/np.amax(self.conc)
		print("Max concentration: " ,np.amax(self.conc)) 
		doping_conc = np.arange(0.1, 1.1, 0.1)
		plt.contourf(self.x_grid, self.y_grid, norm_conc, doping_conc, cmap='jet')
		plt.colorbar()
		plt.title('Dopant distribution for "{}" function'.format(par.INITIAL_SURFACE_TYPE))
		plt.xlabel("x coordinate of a lattice node")
		plt.ylabel("y coordinate of a lattice node")
		plt.plot(self.xvals, self.yvals, "-r") #Showing the surface itself
		plt.xlim([np.amin(self.x_grid),np.amax(self.x_grid)])
		plt.ylim([np.amin(self.y_grid),np.amax(self.y_grid)])
		if save_fig:
			plt.savefig(f"{self.save_data_form}.png")
		else:
			plt.show()		
		