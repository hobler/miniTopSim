import matplotlib.pyplot as plt
import matplotlib as mpl
import os

"import work/Aufgabe3_plot/io_surface.py"
import minitopsim.io_surface as io
import minitopsim.surface as su



fig, ax = plt.subplots()

def plot(fname):
    srf_fobj = su.Surface(0,0)
    srf_obj=io.read_surface(srf_fobj)
    # Überschreiben der default keymap Werte
    mpl.rcParams['keymap.save']="ü"
    mpl.rcParams['keymap.quit'] = "ä"
    mpl.rcParams['keymap.fullscreen'] = "ß"
    mpl.rcParams['keymap.yscale'] = "#"
    mpl.rcParams["keymap.back"]="~"

    # Connect with with event handling
    cid = fig.canvas.mpl_connect('key_press_event',lambda event: Surface_Plotter.onkey(event,fname,srf_fobj))
    plt.plot(srf_obj[0].x,srf_obj[0].y,"b")
    plt.show()


class Surface_Plotter:
    count = 0
    count2 = 0
    count3 = 0
    count4 = 0
    d =1
    r=1

    def onkey(event,fname,srf_fobj):
        # white space is backspace
        if event.key==" ":
            pass
        elif event.key.isdigit():
            print(event.key)
            number=int(event.key)
            srf_fobj=io.read_surface(srf_fobj,pow(2,number))
            if Surface_Plotter.d==1:
                ax.clear()
            ax.plot(srf_fobj[0].x, srf_fobj[0].y, "b")
            fig.canvas.draw()
        elif event.key == 'Space':
            print("lol")
        elif event.key == 'f':
            srf_fobj=io.read_surface(srf_fobj,1)
            if Surface_Plotter.d==1:
                ax.clear()
            ax.plot(srf_fobj[0].x, srf_fobj[0].y, "b")
            fig.canvas.draw()
            print(event.key)
        elif event.key == 'l':
            srf_fobj=io.read_surface(srf_fobj,10)
            if Surface_Plotter.d==1:
                ax.clear()
            ax.plot(srf_fobj[0].x,srf_fobj[0].y,"b")
            fig.canvas.draw()
            print(event.key)
        elif event.key == 'r':
            global r
            if Surface_Plotter.count2==0:
                r=1
                Surface_Plotter.count2+=1
            elif Surface_Plotter.count2==1:
                r=2
                Surface_Plotter.count2=0
            print(r)
        elif event.key == 'a':
            if Surface_Plotter.count==0:
                ax.set_aspect('auto')
                Surface_Plotter.count+=1
            elif Surface_Plotter.count==1:
                ax.set_aspect('equal')
                Surface_Plotter.count=0
            fig.canvas.draw()
            print(event.key)
        elif event.key == 'd':
            if Surface_Plotter.count3==0:
                Surface_Plotter.d=1
                Surface_Plotter.count3+=1
            elif Surface_Plotter.count3==1:
                Surface_Plotter.d=2
                Surface_Plotter.count3=0
            print(event.key)
        elif event.key == 's':
            plt.savefig(os.path.join("work/Aufgabe3_plot",fname.split(".")[0]+".png"))
            print(event.key)
        elif event.key == 'b':
            if Surface_Plotter.count4==0:
                ax.set_ylim(-100, 5)
                ax.set_xlim(-150, 150)
                Surface_Plotter.count4 += 1
            elif Surface_Plotter.count4==1:
                ax.autoscale()
                Surface_Plotter.count4=0
            fig.canvas.draw()
            print(event.key)
        elif event.key == 'q':
            plt.close()
            print(event.key)
