# tests/test_interpolator.py

import unittest
import numpy as np
from pyIB2D.config import SimulationConfig
from pyIB2D.grid import Grid
from pyIB2D.markers import BoundaryMarkers
from pyIB2D.interpolator import Interpolator


class TestInterpolator(unittest.TestCase):
    def setUp(self):
        self.config = SimulationConfig()
        self.grid = Grid(self.config)
        self.markers = BoundaryMarkers(self.config)
        self.interpolator = Interpolator(self.config, self.grid, self.markers)
        self.forces = np.zeros((self.config.num_boundary_markers, 2))

    def test_phi_functions(self):
        r = 0.5
        w1 = self.interpolator.phi1(r)
        w2 = self.interpolator.phi2(r)
        self.assertEqual(w1.shape, (4,))
        self.assertEqual(w2.shape, (4,))

    def test_interpolate_velocity_to_markers(self):
        velocities = self.interpolator.interpolate_velocity_to_markers()
        self.assertEqual(
            velocities.shape,
            (self.config.num_boundary_markers, 2),
        )

    def test_spread_forces_to_grid(self):
        f_grid = self.interpolator.spread_forces_to_grid(self.forces)
        self.assertEqual(
            f_grid.shape,
            self.grid.velocity_field.shape,
        )


if __name__ == '__main__':
    unittest.main()
