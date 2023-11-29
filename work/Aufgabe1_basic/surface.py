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

        dx = np.diff(x)
        dy = np.diff(y)
    
        # Calculate the normal vectors between the points
        normal_vecs = np.vstack((-dy, dx))

        # Normalize the normal vectors
        normal_vecs = normal_vecs/np.linalg.norm(normal_vecs, axis=0)

        return normal_vecs

def plot(self):
    """
    A 2D plot of the surface.

    The points are connected by line segments.
    The x- and y-axes both only show integers wih distance of 20.

    """
    plt.plot(self.x, self.y, 'k')
    plt.axis('equal')
    plt.xticks(np.arange(int(min(self.x)), int(max(self.x))+1, 20))
    plt.yticks(np.arange(int(min(self.y)), int(max(self.y))+1, 20))
    plt.grid()
    plt.show()




