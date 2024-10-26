# tests/test_grid.py

import unittest
from pyIB2D.config import SimulationConfig
from pyIB2D.grid import Grid


class TestGrid(unittest.TestCase):
    def setUp(self):
        self.config = SimulationConfig()
        self.grid = Grid(self.config)

    def test_grid_initialization(self):
        self.assertEqual(
            self.grid.velocity_field.shape, (self.config.grid_size, self.config.grid_size, 2)
        )
        self.assertEqual(
            self.grid.x_grid.shape, (self.config.grid_size, self.config.grid_size)
        )

    def test_compute_vorticity(self):
        vorticity = self.grid.compute_vorticity()
        self.assertEqual(vorticity.shape, (self.config.grid_size, self.config.grid_size))


if __name__ == '__main__':
    unittest.main()
