"""
Module containing the class Surface.
"""
import numpy as np

class Shadow_Error(Exception):
    """Error during Shadow calculation in Surface Class"""
    pass

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

    def has_shadows(self):
        """Returns True if the surface has any shadows."""
        return np.any(np.diff(self.x) <= 0)

    def get_shadows(self):
        """Returns a boolean mask of all the shadowed poits of the surface.

        Important only use mask if Surface.has_shadows().

        Typical Usage:
            mask = surface.get_shadows()
            surface.x[mask]     #shadowed x-values
            surface.y[mask]     #shadowed y-values

        Raises:
            Shadow_Error: Shadow before/after the first/final Surface point.
        """
        shadows_mask = np.full_like(self.x, False, dtype=bool)

        firstx = self.x[0]
        finalx = self.x[-1]

        for i, (x, y) in enumerate(zip(self.x[1:], self.y[1:]), 1):
            if x <= np.max(self.x[:i]):
                if x < firstx:
                    msg = "Shadow is before the first point of Surface."
                    raise Shadow_Error(msg)
                for j in range(i-1, -1, -1):
                    if self.x[j] == x:
                        interp_y = self.y[j]    #no interpolation needed
                        break
                    elif self.x[j] < x < self.x[j+1]:
                        xp = self.x[j:j+2]
                        yp = self.y[j:j+2]
                        interp_y = np.interp(x, xp, yp)
                        break
                    elif self.x[j] > x > self.x[j+1]:
                        xp = self.x[j+1:j-1:-1]
                        yp = self.y[j+1:j-1:-1]
                        interp_y = np.interp(x, xp, yp)
                        break
                #potentially shadowed point
                shadows_mask[i] = (y <= interp_y)

        for i, (x, y) in reversed(list(enumerate(zip(self.x[:-1],
                                                     self.y[:-1])))):
            if x >= np.min(self.x[i+1:]):
                if x > finalx:
                    msg = "Shadow is after the final point of Surface."
                    raise Shadow_Error(msg)
                for j in range(i+1, self.x.size):
                    if self.x[j] == x:
                        interp_y = self.y[j]    #no interpolation needed
                        break
                    elif self.x[j-1] < x < self.x[j]:
                        xp = self.x[j-1:j+1]
                        yp = self.y[j-1:j+1]
                        interp_y = np.interp(x, xp, yp)
                        break
                    elif self.x[j-1] > x > self.x[j]:
                        xp = self.x[j:j-2:-1]
                        yp = self.y[j:j-2:-1]
                        interp_y = np.interp(x, xp, yp)
                        break
                #potentially shadowed point
                shadows_mask[i] = shadows_mask[i] or (y <= interp_y)

        return shadows_mask

    def interpolate(self, xnew):
        """Interpolates the surface for new x-values.
        
        Important do not use if surface still has shadows.

        Args:
            xnew (array-like): x-values to interpolate
        """
        ynew = np.interp(xnew, self.x, self.y)
        self.x = xnew
        self.y = ynew
        
    def view_factor(self):
        """Returns the view factor matrix of the surface.

        Args:
            none
        """
        n_nodes = len(self.x)
        
        # Calculate node distance matrix
        d_x = np.zeros((n_nodes, n_nodes))
        d_y = np.zeros((n_nodes, n_nodes))
        for i in range(n_nodes):
            d_x[i] = self.x - self.x[i]
            d_y[i] = self.y - self.y[i]
        d = np.sqrt(d_x**2 + d_y**2)
        
        # Calculate cos_beta matrix
        cos_beta = np.zeros((n_nodes, n_nodes))
        normal_vecs = -self.normal_vector()
        for i in range(n_nodes):
            for j in range(n_nodes):
                # Avoid zero divison d_ii=0
                if i != j:
                    d_ij_vec = np.array([d_x[i,j], d_y[i,j]])
                    # Norm of normal vectors should be 1
                    cos_beta[i, j] = np.dot(normal_vecs[:,i], d_ij_vec)/d[i,j]

        # Calculate the view factor matrix f
        f = np.zeros((n_nodes, n_nodes))
        for i in range(n_nodes):
            for j in range(n_nodes):
                if i != j and cos_beta[i,j] > 0 and cos_beta[j,i] > 0:
                    # Calc d_lj and handle first and last node
                    if j == 0:
                        d_lj = d[i,j+1];
                    elif j == (n_nodes-1):
                        d_lj = d[i,j-1]
                    else:
                        d_lj = (d[i,j+1] + d[i,j-1])/2
                    
                    f[i,j] = cos_beta[i,j] * cos_beta[j,i] / (2 * d[i, j])*d_lj
        
        return f