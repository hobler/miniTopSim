"""
Main script and function to run miniTopSim.
"""
from minitopsim import parameters as par
import sys
import matplotlib.pyplot as plt

sys.path.append("..")
from work.Aufgabe1_basic.advance import advance, timestep
from work.Aufgabe1_basic.io_surface import init_surface, write_surface

def minitopsim():
   print('Running miniTopSim ...')
   print(f'TestParameter={par.TestParameter}')

   time = 0
   tend = float(sys.argv[1])
   dt = timestep(float(sys.argv[2]), time, tend)  
   filename = f'basic_{tend}_{dt}'

   # Initialize the surface
   surface = init_surface()
   print(surface.normal_vector()[0])
   print("Das ist NV")
   # Write and plot initial surface 
   if (write_surface(surface, 0, filename + '.srf')==False):
      exit()
   surface.plot("Initial Surface")

   # Move surface over time until tend is reached
   while dt > 0:
      surface = advance(surface, dt)
      if(write_surface(surface, time + dt, filename + '.srf')==False):
         exit()
      time += dt
      dt = timestep(dt, time, tend)
      print("time = ", time, "dt = ", dt)

   # Plot final surface and save plot
   surface.plot("Final Surface")
   plt.legend()
   plt.title("Sputtering yield simulation, tend = " + str(tend) + 
             "s, dt = " + sys.argv[2] +"s")

   plt.savefig(filename + '.png')
   plt.show()

   return True 



