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
                        interp_y = self.y[j]    # no interpolation needed
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
                # potentially shadowed point
                shadows_mask[i] = (y <= interp_y)

        for i, (x, y) in reversed(list(enumerate(zip(self.x[:-1],
                                                     self.y[:-1])))):
            if x >= np.min(self.x[i+1:]):
                if x > finalx:
                    msg = "Shadow is after the final point of Surface."
                    raise Shadow_Error(msg)
                for j in range(i+1, self.x.size):
                    if self.x[j] == x:
                        interp_y = self.y[j]    # no interpolation needed
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
                # potentially shadowed point
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

    def deloop(self):
        """
        Calculates a new sequence of point coordinates by eliminating loops.

        Returns:
            x_delooped (array(float)): The x-coordinates of the points without loops.
            y_delooped (array(float)): The y-coordinates of the points without loops.

        """
        x = self.x
        y = self.y
        x_local = x.tolist()
        y_local = y.tolist()
        k = 0
        x_delooped = []
        y_delooped = []
        dx = np.diff(x)
        dy = np.diff(y)

        for i in range(dx.size-2):
            for j in range(i+2, dx.size):
                a = [[dx[j], -dx[i]], [dy[j], -dy[i]]]
                b = [x[i] - x[j], y[i] - y[j]]              # create coefficient arrays
                try:
                    check_t, check_k = np.linalg.solve(a, b)      # trying to solve system of equations
                except np.linalg.LinAlgError:
                    check_t, check_k = [2, 2]
                if ((check_t >= 0) & (check_t < 1) &
                        (check_k >= 0) & (check_k < 1)):    # finding intersections
                    t = check_t
                    x_neu = x[j] + dx[j] * t
                    y_neu = y[j] + dy[j] * t
                    x_delooped = x_delooped + x_local[k: i + 1] + [x_neu]
                    y_delooped = y_delooped + y_local[k: i + 1] + [y_neu]
                    k = j + 1

        x_delooped = x_delooped + x_local[k:dx.size + 1]
        y_delooped = y_delooped + y_local[k:dy.size + 1]

        x_delooped = np.array(x_delooped)
        y_delooped = np.array(y_delooped)

        return x_delooped, y_delooped
    
    def view_factor(self):
       """Returns the view factor matrix of the surface.

       Args:
           none
       """
       n_nodes = len(self.x)
       
       # Calculate node distance matrix
       d_x = np.tile(self.x, (n_nodes, 1)) - np.tile(self.x, (n_nodes, 1)).T
       d_y = np.tile(self.y, (n_nodes, 1)) - np.tile(self.y, (n_nodes, 1)).T
       d = np.sqrt(d_x**2 + d_y**2)
           
       # Calculate cos_beta matrix
       cos_beta = np.zeros((n_nodes, n_nodes))
       normal_vecs = -self.normal_vector()
       for i in range(n_nodes):
                   d_ij_vecs = np.array([d_x[i,:], d_y[i,:]])
                   # Norm of normal vectors should be 1
                   normal_vec_norm = np.linalg.norm(normal_vecs[:,i])
                   cos_beta[i] = np.dot(normal_vecs[:,i], d_ij_vecs)/(d[i,:]*normal_vec_norm)          
       
       # Set the diagonal values to zero
       np.fill_diagonal(cos_beta, 0)                        
       
       # Create a binary mask for valid indices
       valid_mask = (cos_beta > 0) & (cos_beta.T > 0) & (~np.eye(n_nodes, dtype=bool))
       
       # transpose cos_beta_ji = cos_beta_ij
       cos_b_X_b_T = np.matmul(cos_beta, cos_beta.T)
       
       # Calculate node distances
       d_lj_1 =  np.roll(d, 1, axis=1)
       d_lj_2 =  np.roll(d, -1, axis=1)
       d_lj = d_lj_1 + d_lj_2/2
       
       # Calculate the view factor matrix f
       f = np.zeros((n_nodes, n_nodes))
       f = np.where(valid_mask, cos_b_X_b_T / (2 * d) * d_lj, 0)

       return f
