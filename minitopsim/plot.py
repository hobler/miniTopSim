
import matplotlib.pyplot as plt
import os
import matplotlib as mpl
from minitopsim.io_surface import read_surface
from minitopsim.surface import Surface

def plot(srf_file):

    mpl.rcParams['keymap.save'] = "ü"
    mpl.rcParams['keymap.quit'] = "ä"
    mpl.rcParams['keymap.fullscreen'] = "ß"
    mpl.rcParams['keymap.yscale'] = "#"
    mpl.rcParams["keymap.back"] = "~"

    plot1 = Surface_Plotter(srf_file)
    plot1.run()

class Surface_Plotter:
    def __init__(self, srf_file):
        self.srf_file = srf_file

        # we have to know which surface to use
        self.surface_data = []
        self.index = 0
        self.show_every = 1
        self.reverse = False
        self.aspect_ratio_auto = True
        self.delete_previous = False
        self.save_plot = False
        self.adjust_boundaries = True
        self.initial_index = 0

        self.read_surfaces()


        # Weitere Initialisierungen können hier erfolgen

        # Erstelle den ersten Plot
        self.fig, self.ax = plt.subplots()
        self.update_plot()

    def read_surfaces(self):
        with open(os.path.join("work/Aufgabe3_plot",self.srf_file), 'r') as file:
            self.surface_data = []  # Clear existing surface data
            while True:
                current_surface, current_time = read_surface(file)
                if current_surface is None or current_time is None:
                    break
                self.surface_data.append((current_surface, current_time))

    def on_key_press(self, event):
        key = event.key

        if key == ' ':
            self.index = (self.index + 1) if not self.reverse else (self.index - 1)
        elif key.isdigit():
            n = int(key)
            self.show_every = 2 ** n
        elif key == 'f':
            self.index = 0
        elif key == 'l':
            self.index = len(self.surface_data) - 1
        elif key == 'r':
            self.reverse = not self.reverse
        elif key == 'a':
            self.aspect_ratio_auto = not self.aspect_ratio_auto
        elif key == 'd':
            self.delete_previous = not self.delete_previous
        elif key == 's':
            plt.savefig(os.path.join(f"work/Aufgabe3_plot",f"{self.srf_file.split('.')[0]}.png"))
        elif key == 'b':
            self.adjust_boundaries = not self.adjust_boundaries
        elif key == 'q':
            plt.close()
        self.update_plot()

    def update_plot(self):
        if self.delete_previous:
            self.ax.clear()

        if 0 <= self.index < len(self.surface_data):
            current_surface, current_time =self.surface_data[self.index]
            self.ax.plot(current_surface.x,current_surface.y,"b", label=f"Time: {current_time}")
            self.ax.set_title("Surface Plot")
            self.ax.set_xlabel("X Position (nm)")
            self.ax.set_ylabel("Y Position (nm)")

            self.ax.set_aspect('auto' if self.aspect_ratio_auto else 'equal')

            if self.adjust_boundaries:
                self.ax.autoscale()
                """self.ax.set_ylim(-100, 100)
                self.ax.set_xlim(-150, 150)"""
            else:
                self.ax.set_ylim(-100,5)
                self.ax.set_xlim(-150, 150)
                """self.ax.set_xlim(min(current_surface.y), max(current_surface.y))
                self.ax.set_ylim(min(current_surface.x), max(current_surface.x))"""

            self.ax.legend()
            self.fig.canvas.draw_idle()
        else:
            self.index=0

        #else:
        """ current_time = self.times_and_surfaces[0]"""
        """self.ax.text(0.5, 0.5, f"Time: {current_time}", horizontalalignment='center',
        verticalalignment='center', fontsize=12)"""

    def run(self):
        self.fig.canvas.manager.set_window_title(self.srf_file)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

        # Halte die Anwendung geöffnet
        plt.show()



"""Plotting and event handling

Variables:
    fig and ax are for updating the plot with key press events

Functions:
   plot(fname): is responsible for plotting and connecting the event handler

Classes:
    Surface_Plotter: Contains the event handling functionality for
        controlling the plot.



import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import numpy
import numpy as np

import minitopsim.io_surface as io

fig, ax = plt.subplots()
ln, = ax.plot([], [])

def plot(fname):
    Calls read_surface function to create a surface object which is then plotted

        Args:
            fname(file): the file to be plotted
        
    x=np.linspace(0,1000,100)
    y=np.linspace(0,2000,100)



    # Overwriting the default keymap values to use them for our purposes
    mpl.rcParams['keymap.save'] = "ü"
    mpl.rcParams['keymap.quit'] = "ä"
    mpl.rcParams['keymap.fullscreen'] = "ß"
    mpl.rcParams['keymap.yscale'] = "#"
    mpl.rcParams["keymap.back"] = "~"

    # Connect with the event handling
    plot1=Surface_Plotter(fname)
    srf_fobj = open(os.path.join("work/Aufgabe3_plot", fname), "r")
    srf_obj = io.read_surface(plot1.srf_fobj)
    "cid = fig.canvas.mpl_connect('key_press_event', lambda event: Surface_Plotter.on_key_press(plot1,event))"
    plot1.run()
    "cid = fig.canvas.mpl_connect('key_press_event', Surface_Plotter.on_key_press)"

    plt.plot(x, y, "b")
    plt.xlabel('x in nm')
    plt.ylabel('y in nm')    
    plt.show()

class Surface_Plotter:
    def __init__(self, srf_file):
        self.srf_file=srf_file
        self.srf_fobj=open(os.path.join("work/Aufgabe3_plot", self.srf_file), "r")

        self.aspectratio=0
        self.boundary=0
        self.clear=0
        self.reverse=0


    def on_key_press(self,event):
        print(event.key)
        if event.key=="q":
            self.srf_fobj.close()
            plt.close()
        elif event.key=="a":
            if self.aspectratio==0:
                self.aspectratio+=1
                ax.set_aspect('equal')
            else:
                self.aspectratio = 0
                ax.set_aspect('auto')
            self.update_plot()
        elif event.key=="b":

            if self.boundary==0:
                self.boundary += 1
                ax.set_ylim(-100, 5)
                ax.set_xlim(-150, 150)
            else:
                self.boundary = 0
                ax.autoscale()

            self.update_plot()

        elif event.key=="s":
            plt.savefig(os.path.join("work/Aufgabe3_plot", self.srf_file.split(".")[0] + ".png"))
        elif event.key=="r":
            pass
        elif event.key=="d":
            if self.clear==0:
                self.clear+=1
                ax.clear()
            else:
                self.clear=0

            self.update_plot()
        elif event.key=="f":
            io.read_surface(self.srf_fobj)
            self.update_plot()
        elif event.key=="l":
            io.read_surface(self.srf_fobj)
            self.update_plot()
        elif event.key.isdigit():
            io.read_surface(self.srf_fobj)
        elif event.key==" ":
            io.read_surface(self.srf_fobj)
            self.update_plot()
    def update_plot(self):
        "ax.plot(srf_obj[0].x, srf_obj[0].y, b)"
        fig.canvas.draw()
    def run(self):
        fig.canvas.manager.set_window_title(self.srf_file)
        fig.canvas.mpl_connect('key_press_event', self.on_key_press)
class Surface_Plotter:
    Check if new attributes meet conditions and set variables if so.

        Variables: count,count2,count3,count4,d,r state variables to switch between modes

        Functions:
            onkey(eventm,srf_fobj)
        
    count = 0
    count2 = 0
    count3 = 0
    count4 = 0
    incdec=0
    number=0

    d = 1
    r = 1
    k = 1

    # add class method decorator (cls)
    def onkey(event, srf_fobj):
        Callback Function responsible for key events

            Args:
                event: controlls which
                srf_fobj (file): file to be read

        
        # white space represents backspace
        if event.key == " ":
            if Surface_Plotter.r == 1:

                if Surface_Plotter.k==0:
                    Surface_Plotter.incdec=-3-Surface_Plotter.number-1
                elif Surface_Plotter.k==1:
                    Surface_Plotter.incdec=-3-Surface_Plotter.incdec-1
                elif Surface_Plotter.k==2:
                    print("last surface already plotted")

            elif Surface_Plotter.r == 2:

                if Surface_Plotter.k==0:
                    Surface_Plotter.incdec=-3+Surface_Plotter.number+1
                elif Surface_Plotter.k==1:
                    print("first surface already plotted")
                elif Surface_Plotter.k==2:
                    Surface_Plotter.incdec=-3-Surface_Plotter.incdec+1

            if Surface_Plotter.d == 1:
                    ax.clear()
            "print(Surface_Plotter.incdec)"
            srf_obj = io.read_surface(srf_fobj,Surface_Plotter.incdec)
            ax.plot(srf_obj[0].x, srf_obj[0].y, "b")
            fig.canvas.draw()

        elif event.key.isdigit():

            print(event.key)
            number = int(event.key)
            srf_obj = io.read_surface(srf_fobj, pow(2, number))
            Surface_Plotter.incdec=number
            if Surface_Plotter.d == 1:
                ax.clear()
            ax.plot(srf_obj[0].x, srf_obj[0].y, "b")
            Surface_Plotter.k = 0
            fig.canvas.draw()

        elif event.key == 'f':

            srf_obj = io.read_surface(srf_fobj,-1)
            if Surface_Plotter.d == 1:
                ax.clear()
            ax.plot(srf_obj[0].x, srf_obj[0].y, "b")
            Surface_Plotter.k=1
            fig.canvas.draw()
            print(event.key)

        elif event.key == 'l':

            srf_obj = io.read_surface(srf_fobj, -2)
            if Surface_Plotter.d == 1:
                ax.clear()
            ax.plot(srf_obj[0].x, srf_obj[0].y, "b")
            Surface_Plotter.k=2
            fig.canvas.draw()
            print(event.key)

        elif event.key == 'r':

            if Surface_Plotter.count2 == 0:
                Surface_Plotter.r = 1
                Surface_Plotter.count2 += 1
            elif Surface_Plotter.count2 == 1:
                Surface_Plotter.r = 2
                Surface_Plotter.count2 = 0
            print(Surface_Plotter.r)

        elif event.key == 'a':

            if Surface_Plotter.count == 0:
                ax.set_aspect('auto')
                Surface_Plotter.count += 1
            elif Surface_Plotter.count == 1:
                ax.set_aspect('equal')
                Surface_Plotter.count = 0
            fig.canvas.draw()
            print(event.key)

        elif event.key == 'd':

            if Surface_Plotter.count3 == 0:
                Surface_Plotter.d = 1
                Surface_Plotter.count3 += 1
            elif Surface_Plotter.count3 == 1:
                Surface_Plotter.d = 2
                Surface_Plotter.count3 = 0
            print(event.key)

        elif event.key == 's':

            plt.savefig(os.path.join("work/Aufgabe3_plot", srf_fobj.split(".")[0] + ".png"))
            print(event.key)

        elif event.key == 'b':

            if Surface_Plotter.count4 == 0:
                ax.set_ylim(-100, 5)
                ax.set_xlim(-150, 150)
                Surface_Plotter.count4 += 1
            elif Surface_Plotter.count4 == 1:
                ax.autoscale()
                Surface_Plotter.count4 = 0
            fig.canvas.draw()
            print(event.key)

        elif event.key == 'q':

            plt.close()
            print(event.key)"""
