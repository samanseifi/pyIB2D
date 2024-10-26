# tests/test_forces.py

import unittest
from pyIB2D.config import SimulationConfig
from pyIB2D.markers import BoundaryMarkers
from pyIB2D.forces import ForceCalculator


class TestForceCalculator(unittest.TestCase):
    def setUp(self):
        self.config = SimulationConfig()
        self.markers = BoundaryMarkers(self.config)
        self.force_calculator = ForceCalculator(self.config, self.markers)

    def test_compute_elastic_forces(self):
        forces = self.force_calculator.compute_elastic_forces(0)
        self.assertEqual(
            forces.shape,
            (self.config.num_boundary_markers, 2),
        )

    def test_compute_bending_forces(self):
        forces = self.force_calculator.compute_bending_forces(0)
        self.assertEqual(
            forces.shape,
            (self.config.num_boundary_markers, 2),
        )

    def test_total_forces(self):
        forces = self.force_calculator.total_forces(0)
        self.assertEqual(
            forces.shape,
            (self.config.num_boundary_markers, 2),
        )


if __name__ == '__main__':
    unittest.main()
