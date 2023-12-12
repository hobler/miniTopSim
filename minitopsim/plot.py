"""
File: surface_plotter.py

A script for plotting surfaces and providing interactive navigation using Matplotlib.

Classes:
    SurfacePlotter: A class for managing the plotting functionality.

Functions:
    plot(): Creates a Surface_Plotter object and starts the event loop.
"""

import matplotlib.pyplot as plt
import os
import matplotlib as mpl
from minitopsim.io_surface import read_surface


def plot(srf_file):
    mpl.rcParams['keymap.save'] = "ü"
    mpl.rcParams['keymap.quit'] = "ä"
    mpl.rcParams['keymap.fullscreen'] = "ß"
    mpl.rcParams['keymap.yscale'] = "#"
    mpl.rcParams["keymap.back"] = "~"

    plot1 = Surface_Plotter(srf_file)
    plot1.run()


class Surface_Plotter:
    """
    A class for plotting surfaces and providing interactive navigation.

    Attributes:
        srf_file (str): The name of the surface file to be plotted.
        surface_data (list): List containing tuples of surface data and corresponding times.
        index (int): Current index of the displayed surface in surface_data.
        show_every (int): Step size for showing surfaces during navigation.
        reverse (bool): Flag indicating whether to navigate in reverse.
        aspect_ratio_auto (bool): Flag indicating whether to automatically adjust aspect ratio.
        delete_previous (bool): Flag indicating whether to delete the previous plot before updating.
        save_plot (bool): Flag indicating whether to save the plot.
        adjust_boundaries (bool): Flag indicating whether to adjust plot boundaries.

    Methods:
        initialize_plot(): Initialize the Matplotlib plot.
        read_surfaces(): Read surface data from a file and populate surface_data.
        on_key_press(event): Handle key press events for navigation and other actions.
        update_plot(): Update the Matplotlib plot based on current settings.
        start_plotting(): Start the interactive plot.
    """

    def __init__(self, srf_file):
        """
        Initialize the SurfacePlotter object.

        Args:
            srf_file (str): The name of the surface file to be plotted.
        """
        self.srf_file = srf_file

        # Store the surface and time tuples in a list
        self.surface_data = []

        self.index = 0

        self.show_every = 0
        self.reverse = False
        self.aspect_ratio_auto = True
        self.delete_previous = False
        self.save_plot = False
        self.adjust_boundaries = True

        # read all surface files at initialization
        self.read_surfaces()

        # Weitere Initialisierungen können hier erfolgen

        # Erstelle den ersten Plot
        self.fig, self.ax = plt.subplots()
        self.update_plot()

    def read_surfaces(self):
        with open(self.srf_file, 'r') as file:
            self.surface_data = []  # Clear existing surface data
            while True:
                current_surface, current_time = read_surface(file)
                if current_surface is None or current_time is None:
                    break
                self.surface_data.append((current_surface, current_time))

    def on_key_press(self, event):
        """
        Handle key press events for navigation and other actions.

        Args:
            event (KeyEvent): The key press event.
        """
        key = event.key

        if key == ' ':
            """self.read_surfaces()"""
            self.index = (self.index + 1 + self.show_every) if not self.reverse else (self.index - 1 - self.show_every)
            self.update_plot()
        elif key.isdigit():
            n = int(key)
            self.show_every = (2 ** n) - 1
        elif key == 'f':
            self.index = 0
            self.update_plot()
        elif key == 'l':
            self.index = len(self.surface_data) - 1
            self.update_plot()
        elif key == 'r':
            self.reverse = not self.reverse
        elif key == 'a':
            self.aspect_ratio_auto = not self.aspect_ratio_auto
            self.update_plot()
        elif key == 'd':
            self.delete_previous = not self.delete_previous
        elif key == 's':
            file = os.path.split(self.srf_file)[1]
            plt.savefig(os.path.join(os.getcwd(), f"{os.path.splitext(file)[0]}.png"))
            print("file saved")
        elif key == 'b':
            self.adjust_boundaries = not self.adjust_boundaries
            self.update_plot()
        elif key == 'q':
            plt.close()

    def update_plot(self):
        """
        Update the Matplotlib plot based on current settings.
        """
        if self.delete_previous:
            self.ax.clear()

        if 0 <= self.index < len(self.surface_data):
            current_surface, current_time = self.surface_data[self.index]
            self.ax.plot(current_surface.x, current_surface.y, "b")
            self.ax.set_title(f"Time: {current_time}")
            self.ax.set_xlabel("X Position (nm)")
            self.ax.set_ylabel("Y Position (nm)")

            self.ax.set_aspect('auto' if self.aspect_ratio_auto else 'equal')

            if self.adjust_boundaries:
                self.ax.autoscale()
            else:
                self.ax.set_ylim(self.ax.get_ylim())
                self.ax.set_xlim(self.ax.get_xlim())

            self.fig.canvas.draw_idle()
        elif self.index >= len(self.surface_data):
            print("last surface already plotted")
            self.index = len(self.surface_data) - 1 - self.show_every
        elif self.index < 0:
            self.index = 0 + self.show_every
            print("first surface already plotted")

    def run(self):
        self.fig.canvas.manager.set_window_title(self.srf_file)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)
        plt.show()
