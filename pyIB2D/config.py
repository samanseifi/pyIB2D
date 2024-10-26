import numpy as np


class SimulationConfig:
    """
    Configuration parameters for the simulation.
    """

    def __init__(self, length=1.0, grid_size=64, boundary_markers=None, rho=1.0, mu=0.01, tmax=4.0, dt=0.01, cut_marker=-1, cut_step=-1,):
        self.length = length
        self.grid_size = grid_size
        self.h = length / grid_size
        self.ip = (np.arange(grid_size) + 1) % grid_size
        self.im = (np.arange(grid_size) - 1) % grid_size
        self.rho = rho
        self.mu = mu
        self.tmax = tmax
        self.dt = dt
        self.clock_max = int(np.ceil(tmax / dt))
        self.cut_marker = cut_marker
        self.cut_step = cut_step

        self.num_boundary_markers = (
            boundary_markers
            if boundary_markers
            else int(np.ceil(np.pi * (length / 2) / (self.h / 2)))
        )
        self.dtheta = 2 * np.pi / self.num_boundary_markers
        self.kp = (np.arange(self.num_boundary_markers) + 1) % self.num_boundary_markers
        self.km = (np.arange(self.num_boundary_markers) - 1) % self.num_boundary_markers

        self.K = 1.0  # Elastic stiffness coefficient
        self.Kb = 0.01  # Bending stiffness coefficient
