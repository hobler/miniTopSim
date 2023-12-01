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
        
        dx = np.append(np.diff(x), 1)
        dy = np.append(np.diff(y), 0)
        
        # Calculate the normal vectors between the points
        normal_vecs = np.vstack((dy, -dx))

        # Normalize the normal vectors
        normal_vecs = normal_vecs/np.linalg.norm(normal_vecs)

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





