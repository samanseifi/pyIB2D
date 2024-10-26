# tests/test_config.py

import unittest
from pyIB2D.config import SimulationConfig


class TestSimulationConfig(unittest.TestCase):
    def test_default_config(self):
        config = SimulationConfig()
        self.assertEqual(config.length, 1.0)
        self.assertEqual(config.grid_size, 64)
        self.assertAlmostEqual(config.h, 1.0 / 64)
        self.assertEqual(config.rho, 1.0)
        self.assertEqual(config.mu, 0.01)
        self.assertEqual(config.tmax, 4.0)
        self.assertEqual(config.dt, 0.01)
        self.assertEqual(config.cut_marker, -1)
        self.assertEqual(config.cut_step, -1)

    def test_custom_config(self):
        config = SimulationConfig(length=2.0, grid_size=128, mu=0.05)
        self.assertEqual(config.length, 2.0)
        self.assertEqual(config.grid_size, 128)
        self.assertAlmostEqual(config.h, 2.0 / 128)
        self.assertEqual(config.mu, 0.05)


if __name__ == '__main__':
    unittest.main()
