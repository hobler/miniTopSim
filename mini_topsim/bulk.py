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
	def __init__(self, x, y, conc):
		'''
		Initializes all class parameters.
		'''
		self.x = x
		self.y = y
		self.conc = conc
		self.save_data_form = codedir + f"{par.INITIAL_SURFACE_TYPE.lower()}"

	def write_bulk(self):
		'''
		Writes the dopant distribution for the corresponding node coordinates to an .out file.
		'''
		with open(codedir + f"/Bulk_{par.INITIAL_SURFACE_TYPE}.out", 'w') as bulk_out_file:
			bulk_out_file.write("Dopant distribution\nX\t\tY\t\t\tconc\n")
			for x in self.x:
				for y, conc in zip(self.y, np.asarray(self.conc).reshape(-1)):
					bulk_out_file.write(f"{x}\t{y}\t{conc}\n")				
					
	# def plot_bulk(self, save_fig=False):
		# plt.contourf(self.x, self.y, self.conc)
		# plt.colorbar()
		# plt.title("Dopant distribution")
		# plt.xlabel("x coordinate of a lattice node")
		# plt.ylabel("y coordinate of a lattice node")
		# if save_fig:
			# plt.savefig(f"{self.save_data_form}.png")
		# else:
			# plt.show()

	def plot_bulk(self, save_fig=False):
		'''
		Plots dopant concentration on the nodes of a regular lattice with contour lines at concentrations 
		0.1, 0.2, ... 0.9 of the maximum occurring concentration.
	
		Arg: 
			save_fig: Decides between plotting the concentration of the nodes and saving of the plot as .jpg image
		'''	
		norm_conc = self.conc/np.amax(self.conc)
		doping_conc = np.arange(0.1, 1.0, 0.1)
		plt.contourf(self.x, self.y, norm_conc, doping_conc, cmap='jet')
		plt.colorbar()
		plt.title("Dopant distribution")
		plt.xlabel("x coordinate of a lattice node")
		plt.ylabel("y coordinate of a lattice node")
		if save_fig:
			plt.savefig(f"{self.save_data_form}.png")
		else:
			plt.show()		
		