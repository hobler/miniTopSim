import matplotlib.pyplot as plt
import matplotlib as mpl
import os

import minitopsim.io_surface as io

fig, ax = plt.subplots()


def plot(fname):
    srf_fobj = "trench.srf"
    srf_obj = io.read_surface(srf_fobj)

    # Overwriting the default keymap values to use them for our purposes
    mpl.rcParams['keymap.save'] = "ü"
    mpl.rcParams['keymap.quit'] = "ä"
    mpl.rcParams['keymap.fullscreen'] = "ß"
    mpl.rcParams['keymap.yscale'] = "#"
    mpl.rcParams["keymap.back"] = "~"

    # Connect with the event handling
    cid = fig.canvas.mpl_connect('key_press_event', lambda event: Surface_Plotter.onkey(event, srf_fobj))
    fig.canvas.manager.set_window_title(fname)
    plt.plot(srf_obj[0].x, srf_obj[0].y, "b")
    plt.xlabel('x in nm')
    plt.ylabel('y in nm')
    plt.show()


class Surface_Plotter:
    count = 0
    count2 = 0
    count3 = 0
    count4 = 0
    incdec=0

    d = 1
    r = 1

    def onkey(event, srf_fobj):
        # white space represents backspace
        if event.key == " ":
            if Surface_Plotter.r == 1:

                Surface_Plotter.incdec+=1
                print(Surface_Plotter.r)
            elif Surface_Plotter.r == 2:
                Surface_Plotter.incdec -= 1
                print(Surface_Plotter.r)
            if Surface_Plotter.d == 1:
                    ax.clear()
            srf_obj = io.read_surface(srf_fobj,Surface_Plotter.incdec)
            ax.plot(srf_obj[0].x, srf_obj[0].y, "b")
            fig.canvas.draw()

        elif event.key.isdigit():

            print(event.key)
            number = int(event.key)
            srf_obj = io.read_surface(srf_fobj, pow(2, number))
            if Surface_Plotter.d == 1:
                ax.clear()
            ax.plot(srf_obj[0].x, srf_obj[0].y, "b")
            fig.canvas.draw()

        elif event.key == 'f':

            srf_obj = io.read_surface(srf_fobj, 1)
            if Surface_Plotter.d == 1:
                ax.clear()
            ax.plot(srf_obj[0].x, srf_obj[0].y, "b")
            fig.canvas.draw()
            print(event.key)

        elif event.key == 'l':

            srf_obj = io.read_surface(srf_fobj, 10)
            if Surface_Plotter.d == 1:
                ax.clear()
            ax.plot(srf_obj[0].x, srf_obj[0].y, "b")
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
            print(event.key)
