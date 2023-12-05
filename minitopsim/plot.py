"""Plotting and event handling

Variables:
    fig and ax are for updating the plot with key press events

Functions:
   plot(fname): is responsible for plotting and connecting the event handler

Classes:
    Surface_Plotter: Contains the event handling functionality for
        controlling the plot.

"""

import matplotlib.pyplot as plt
import matplotlib as mpl
import os
import numpy
import numpy as np

import minitopsim.io_surface as io

fig, ax = plt.subplots()


def plot(fname):
    """Calls read_surface function to create a surface object which is then plotted

        Args:
            fname(file): the file to be plotted
        """
    x=np.linspace(0,1000,100)
    y=np.linspace(0,2000,100)

    srf_fobj = open(os.path.join("work/Aufgabe3_plot", fname), "r")
    srf_obj = io.read_surface(srf_fobj)

    # Overwriting the default keymap values to use them for our purposes
    mpl.rcParams['keymap.save'] = "ü"
    mpl.rcParams['keymap.quit'] = "ä"
    mpl.rcParams['keymap.fullscreen'] = "ß"
    mpl.rcParams['keymap.yscale'] = "#"
    mpl.rcParams["keymap.back"] = "~"

    # Connect with the event handling
    plot1=Surface_Plotter(fname)

    "cid = fig.canvas.mpl_connect('key_press_event', lambda event: Surface_Plotter.on_key_press(plot1,event))"
    plot1.run()
    "cid = fig.canvas.mpl_connect('key_press_event', Surface_Plotter.on_key_press)"
    fig.canvas.manager.set_window_title(fname)
    plt.plot(x, y, "b")
    plt.xlabel('x in nm')
    plt.ylabel('y in nm')    
    plt.show()

class Surface_Plotter:
    def __init__(self, srf_file):
        self.srf_file=srf_file
    def on_key_press(self,event):
        print(event.key)
        if event.key=="q":
            "self.srf_file.close()"
            plt.close()
        elif event.key=="a":
            "if Surface_Plotter.count == 0:"
            ax.set_aspect('auto')
            self.update_plot()
            "Surface_Plotter.count += 1"
            "elif Surface_Plotter.count == 1:"
            ax.set_aspect('equal')
            self.update_plot()
            "Surface_Plotter.count = 0"
        elif event.key=="b":
            ax.set_ylim(-100, 5)
            ax.set_xlim(-150, 150)
            self.update_plot()
            ax.autoscale()
        elif event.key=="s":
            plt.savefig(os.path.join("work/Aufgabe3_plot", self.srf_file.split(".")[0] + ".png"))
        elif event.key=="r":
            pass
        elif event.key=="d":
            pass
        elif event.key=="f":
            pass
        elif event.key=="l":
            pass
        elif event.key.isdigit():
            pass
        elif event.key==" ":
            pass
    def update_plot(self):
        "ax.plot(srf_obj[0].x, srf_obj[0].y, b)"
        fig.canvas.draw()
    def run(self):
        fig.canvas.mpl_connect('key_press_event', lambda event: Surface_Plotter.on_key_press(self,event))
"""class Surface_Plotter:
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
