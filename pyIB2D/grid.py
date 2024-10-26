import numpy as np


class Grid:
    """
    Represents the computational grid.
    """

    def __init__(self, config):
        self.config = config
        self.x_grid, self.y_grid = np.meshgrid(
            np.arange(config.grid_size) * config.h,
            np.arange(config.grid_size) * config.h,
            indexing="ij",
        )
        self.velocity_field = np.zeros((config.grid_size, config.grid_size, 2))
        self.initialize_velocity_field()

    def initialize_velocity_field(self):
        """
        Initialize the velocity field with a sinusoidal profile.
        """
        for j1 in range(self.config.grid_size):
            x = j1 * self.config.h
            self.velocity_field[j1, :, 1] = np.sin(
                2 * np.pi * x / self.config.length
            )

    def compute_vorticity(self):
        """
        Compute the vorticity field.

        Vorticity ω is calculated as:
        \[
        \omega = \frac{\partial v}{\partial x} - \frac{\partial u}{\partial y}
        \]
        """
        ip = self.config.ip
        im = self.config.im
        h = self.config.h
        vorticity = (
            self.velocity_field[ip, :, 1]
            - self.velocity_field[im, :, 1]
            - self.velocity_field[:, ip, 0]
            + self.velocity_field[:, im, 0]
        ) / (2 * h)
        return vorticity
