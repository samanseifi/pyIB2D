import numpy as np


class BoundaryMarkers:
    """
    Represents the immersed boundary markers.
    """

    def __init__(self, config):
        self.config = config
        self.positions = np.zeros((config.num_boundary_markers, 2))
        self.initialize_boundary_markers()

    def initialize_boundary_markers(self):
        """
        Initialize the boundary markers in a circular shape.
        """
        for k in range(self.config.num_boundary_markers):
            theta = k * self.config.dtheta
            self.positions[k, 0] = (self.config.length / 2) + (
                self.config.length / 4
            ) * np.cos(theta)
            self.positions[k, 1] = (self.config.length / 2) + (
                self.config.length / 4
            ) * np.sin(theta)