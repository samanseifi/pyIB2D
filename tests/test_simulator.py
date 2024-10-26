# tests/test_simulator.py

import unittest
import os
from pyIB2D.config import SimulationConfig
from pyIB2D.simulator import ImmersedBoundarySimulator


class TestImmersedBoundarySimulator(unittest.TestCase):
    def test_run_simulation(self):
        config = SimulationConfig(tmax=0.01, dt=0.01)
        simulator = ImmersedBoundarySimulator(config)
        simulator.run_simulation()
        # Check if results file exists
        self.assertTrue(os.path.exists('immersed_boundary_simulation_results.h5'))
        # Clean up the test file
        os.remove('immersed_boundary_simulation_results.h5')


if __name__ == '__main__':
    unittest.main()
