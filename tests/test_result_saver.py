# tests/test_result_saver.py

import numpy as np
import unittest
import os
from pyIB2D.config import SimulationConfig
from pyIB2D.grid import Grid
from pyIB2D.markers import BoundaryMarkers
from pyIB2D.result_saver import ResultSaver


class TestResultSaver(unittest.TestCase):
    def setUp(self):
        self.config = SimulationConfig(tmax=0.01, dt=0.01)
        self.grid = Grid(self.config)
        self.markers = BoundaryMarkers(self.config)
        self.result_saver = ResultSaver(self.config, self.grid, self.markers)

    def test_create_datasets(self):
        self.assertIn('velocity_field', self.result_saver.results_file)
        self.assertIn('marker_positions', self.result_saver.results_file)
        self.assertIn('time', self.result_saver.results_file)

    # def test_save_and_load_results(self):
    #     self.result_saver.save_results(0)
    #     self.result_saver.close()
    #     with ResultSaver.load_results() as h5file:
    #         velocity = ResultSaver.get_velocity_at_time(h5file, 0)
    #         positions = ResultSaver.get_marker_positions_at_time(h5file, 0)
    #         self.assertEqual(velocity.shape, (self.config.grid_size, self.config.grid_size, 2))
    #         self.assertEqual(positions.shape, (self.config.num_boundary_markers, 2))
    #     # Clean up the test file
    #     os.remove('immersed_boundary_simulation_results.h5')


if __name__ == '__main__':
    unittest.main()
