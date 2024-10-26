# tests/test_markers.py

import unittest
from pyIB2D.config import SimulationConfig
from pyIB2D.markers import BoundaryMarkers


class TestBoundaryMarkers(unittest.TestCase):
    def setUp(self):
        self.config = SimulationConfig()
        self.markers = BoundaryMarkers(self.config)

    def test_marker_initialization(self):
        num_markers = self.config.num_boundary_markers
        self.assertEqual(
            self.markers.positions.shape,
            (num_markers, 2),
        )


if __name__ == '__main__':
    unittest.main()
