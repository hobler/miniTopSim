"""
Module containing the class Surface.
"""
import numpy as np
import matplotlib.pyplot as plt


class Surface:
    """
    Class representing a surface in the xy-plane.

    Attributes:
            x (array(float)): The x-coordinates of the points.
            y (array(float)): The y-coordinates of the points.

    Between each two points a line segment is drawn. The surface is
    thus defined by the x and y coordinates of the points.
    At the first/last point segments are only drawn to the
    next/previous point.
    The x and y coordinates are stored in arrays of the same length.
    """
    def __init__(self, x, y):
        """
        Initializes the surface with the given x and y values.

        """
        self.x = x
        self.y = y

    def normal_vector(self):
        """
        Calculates the normal vectors of the surface pointing inwards.

        Returns:
            array(float): The normal vectors of the surface.

        """
        x = self.x
        y = self.y

        # calculate difference between points, append (1,0) for last
        # point
        dx = np.diff(x)
        dy = np.diff(y)

        # normalize dx and dy
        magnitude = np.sqrt(dx**2 + dy**2)
        dx /= magnitude
        dy /= magnitude

        dx = dx[:-1] + dx[1:]
        dy = dy[:-1] + dy[1:]

        dx = np.concatenate(((1,), dx, (1,)))
        dy = np.concatenate(((0,), dy, (0,)))

        # Calculate the normal vectors between the points
        normal_vecs = np.vstack((dy, -dx))

        # Normalize the normal vectors
        # Vektornorm stimmt nicht
        normal_vecs /= np.linalg.norm(normal_vecs, axis=0)

        return normal_vecs

    def plot(self, name):
        """
        A 2D plot of the surface.

        Args:
            filename (str): The name of the file to which the plot is
            saved.
        """
        plt.plot(self.x, self.y, 'o-', markersize=2, label=name)
        plt.xticks(np.arange(-60, 61, 20))
        plt.yticks(np.arange(-120, 21, 20))
        plt.xlabel('x [nm]')
        plt.ylabel('y [nm]')
        plt.grid()
