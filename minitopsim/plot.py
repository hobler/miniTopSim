import matplotlib.pyplot as plt
import matplotlib as mpl
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
    mpl.rcParams['keymap.fullscreen'] = "ß"
    mpl.rcParams['keymap.yscale'] = "#"

    # Connect with with event handling
    cid = fig.canvas.mpl_connect('key_press_event',lambda event: Surface_Plotter.onkey(event,fname,srf_fobj))
    plt.plot(srf_obj[0].x,srf_obj[0].y,"b")
    plt.show()


class Surface_Plotter:
    def onkey(event,fname,srf_fobj):
        if event.key.isdigit():
            print(event.key)
            fig.canvas.draw()
            number=int(event.key)
            srf_fobj=io.read_surface(srf_fobj,pow(2,number))
            ax.clear()
            ax.plot(srf_fobj[0].x, srf_fobj[0].y, "b")
            fig.canvas.draw()
        elif event.key == 'Space':
            print("lol")
        elif event.key == 'f':
            srf_fobj=io.read_surface(srf_fobj,1)
            ax.clear()
            ax.plot(srf_fobj[0].x, srf_fobj[0].y, "b")
            fig.canvas.draw()
            print(event.key)
        elif event.key == 'l':
            srf_fobj=io.read_surface(srf_fobj,10)
            ax.clear()
            ax.plot(srf_fobj[0].x,srf_fobj[0].y,"b")
            fig.canvas.draw()
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
