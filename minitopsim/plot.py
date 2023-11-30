import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import os

"import work/Aufgabe3_plot/io_surface.py"
import minitopsim.io_surface as io
import minitopsim.surface as su


count = 0
fig, ax = plt.subplots()

def plot(fname):
    srf_fobj = su.Surface(0,0)
    srf_obj=io.read_surface(srf_fobj)
    # Überschreiben der default keymap Werte
    mpl.rcParams['keymap.save']="ü"
    mpl.rcParams['keymap.quit'] = "ä"
    # Connect with with event handling
    cid = fig.canvas.mpl_connect('key_press_event',lambda event: Surface_Plotter.onkey(event,fname))
    plt.plot(srf_obj.x,srf_obj.y)
    "plt.ion()"
    plt.show()
    "print('plot: Not yet implemented')"


class Surface_Plotter:
    def onkey(event,fname):
        if event.key == 'x':
            if event.xdata is not None and event.ydata is not None:
                ax.plot(event.xdata, event.ydata, 'bo-')
                fig.canvas.draw()
        elif event.key.isdigit():
            print(event.key)
            if event.xdata is not None and event.ydata is not None:
                ax.plot(event.xdata, event.ydata, 'bo-')
                fig.canvas.draw()
            number=int(event.key)
            "io.read_surface()"
        elif event.key == 'Space':
            print("lol")
        elif event.key == 'f':
            io.read_surface()
            print(event.key)
        elif event.key == 'l':
            io.read_surface()
            print(event.key)
        elif event.key == 'a':
            global count
            if count==0:
                ax.set_aspect('auto')
                count=count+1
            elif count==1:
                ax.set_aspect('equal')
                count=0
            fig.canvas.draw()
            print(event.key)
        elif event.key == 'd':
            print(event.key)
        elif event.key == 's':

            plt.savefig(os.path.join("work/Aufgabe3_plot",fname.split(".")[0]+".png"))
            print(event.key)
        elif event.key == 'b':
            print(event.key)
        elif event.key == 'q':
            plt.close()
            print(event.key)
