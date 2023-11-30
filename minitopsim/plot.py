import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

"import work/Aufgabe3_plot/io_surface.py"
import minitopsim.io_surface as io
import minitopsim.surface as su

fig, ax = plt.subplots()
ax.plot(np.random.rand(10))


def plot(fname):
    x = np.linspace(0, 90, 100)
    y=np.linspace(500,1000,100)
    srf_fobj = su.Surface(x, y)
    "io.read_surface(srf_fobj)"
    # Überschreiben der default keymap Werte
    mpl.rcParams['keymap.save']="ü"
    #connect with with event handling
    cid = fig.canvas.mpl_connect('key_press_event',Surface_Plotter.onkey)
    plt.plot(srf_fobj.x,srf_fobj.y)
    "plt.ion()"
    plt.show()
    "print('plot: Not yet implemented')"


class Surface_Plotter:
    def onkey(event):
        "print(event.key)"
        if event.key == 'x':
            if event.xdata is not None and event.ydata is not None:
                ax.plot(event.xdata, event.ydata, 'bo-')
                fig.canvas.draw()
        elif event.key.isdigit():
            print(event.key)
            if event.xdata is not None and event.ydata is not None:
                ax.plot(event.xdata, event.ydata, 'bo-')
                fig.canvas.draw()
        elif event.key == 'f':
            print(event.key)
        elif event.key == 'l':
            print(event.key)
        elif event.key == 'a':
            ax.set_aspect('auto')
            fig.canvas.draw()
            print(event.key)
        elif event.key == 'd':
            print(event.key)
        elif event.key == 's':
            plt.savefig("trench.png")
            print(event.key)
        elif event.key == 'b':
            print(event.key)
        elif event.key == 'q':
            print(event.key)
