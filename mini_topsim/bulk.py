'''
Description: Implementation of the Bulk class with methods for writing and plotting the dopant distribution.

Classes:
         Bulk: opis_klase

Functions:

naziv_1_funkcije(): BESCHREIBUNG_FEHLT
naziv_2_funkcije(): BESCHREIBUNG_FEHLT

Author: Omerasevic Armin (01325962)
Part of the miniTopSim Project: https://github.com/hobler/miniTopSim 
'''
import os
# import sys
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import parameters as par
import numpy as np

filedir = os.path.dirname(__file__)
codedir = os.path.join(filedir, '..', 'work', 'Aufgabe16_implant')
# sys.path.insert(0, codedir)

class Bulk:
	def __init__(self, x, y, c):
		# self.triplets = np.array(triplets, dtype=object)
		self.x = x
		self.y = y
		self.c = c

	def write_bulk(self):
		with open(codedir + f"/Bulk_{par.INITIAL_SURFACE_TYPE}.out", 'w') as bulk_out_file:
			bulk_out_file.write("Dotierstoffverteilung\nX\t\tY\t\t\tC\n")
			for x in self.x:
				for y, C in zip(self.y, np.asarray(self.c).reshape(-1)):
					bulk_out_file.write(f"{x}\t{y}\t{C}\n")
				
					
	# def plot_bulk(self):
		# X,Y = np.meshgrid(self.x,self.y)
		# c_array=np.array(self.c)
		# C = np.transpose(c_array.reshape(len(self.x), len(self.y)))
		
		# fig = plt.figure()
		# plt.contourf(X,Y,C)
		# plt.title("Dotierstoffverteilung")
		# plt.xlabel("X")
		# plt.ylabel("Y")
		# plt.show()
	

	def plot_bulk(self, save_fig=False):
		X, Y = np.meshgrid(self.x, self.y)
		c_array=np.array(self.c)
		C = np.transpose(c_array.reshape(len(self.x), len(self.y)))		
		
		fig = plt.figure()
		doping_conc = np.arange(0.1, 1, 0.1)
		plt.contourf(X, Y, C, doping_conc, cmap='jet')
		plt.colorbar()
		if save_fig:
			plt.savefig(f"{self.save_data_form}.png")
		else:
			plt.show()		
		