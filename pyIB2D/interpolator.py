import numpy as np


class Interpolator:
    """
    Handles interpolation between markers and grid.
    """

    def __init__(self, config, grid, markers):
        self.config = config
        self.grid = grid
        self.markers = markers

    def phi1(self, r):
        """
        Compute the interpolation function φ.

        The interpolation function is based on the 4-point delta function.
        """
        w = np.zeros(4)
        q = np.sqrt(1 + 4 * r * (1 - r))
        w[3] = (1 + 2 * r - q) / 8
        w[2] = (1 + 2 * r + q) / 8
        w[1] = (3 - 2 * r + q) / 8
        w[0] = (3 - 2 * r - q) / 8
        return w

    def phi2(self, r):
        """
        Compute the interpolation function φ (same as phi1).
        """
        return self.phi1(r)

    def interpolate_velocity_to_markers(self):
        """
        Interpolate the grid velocity to the marker positions.
        """
        h = self.config.h
        num_markers = self.config.num_boundary_markers
        marker_velocity = np.zeros((num_markers, 2))
        grid_size = self.config.grid_size

        for k in range(num_markers):
            s = self.markers.positions[k, :] / h
            i = np.floor(s).astype(int)
            r = s - i
            i1 = (i[0] - 1 + np.arange(4)) % grid_size
            i2 = (i[1] - 1 + np.arange(4)) % grid_size
            w = np.outer(self.phi1(r[0]), self.phi2(r[1]))
            marker_velocity[k, 0] = np.sum(
                w * self.grid.velocity_field[i1[:, None], i2, 0]
            )
            marker_velocity[k, 1] = np.sum(
                w * self.grid.velocity_field[i1[:, None], i2, 1]
            )

        return marker_velocity

    def spread_forces_to_grid(self, forces):
        """
        Spread the marker forces onto the fluid grid.
        """
        f = np.zeros_like(self.grid.velocity_field)
        h = self.config.h
        dtheta = self.config.dtheta
        c = dtheta / (h ** 2)
        grid_size = self.config.grid_size

        for k in range(self.config.num_boundary_markers):
            s = self.markers.positions[k, :] / h
            i = np.floor(s).astype(int)
            r = s - i
            i1 = (i[0] - 1 + np.arange(4)) % grid_size
            i2 = (i[1] - 1 + np.arange(4)) % grid_size
            w = np.outer(self.phi1(r[0]), self.phi2(r[1]))
            f[i1[:, None], i2, 0] += (c * forces[k, 0]) * w
            f[i1[:, None], i2, 1] += (c * forces[k, 1]) * w

        return f