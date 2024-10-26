# tests/test_fluid_solver.py

import unittest
import numpy as np
from pyIB2D.config import SimulationConfig
from pyIB2D.grid import Grid
from pyIB2D.fluid_solver import FluidSolver


class TestFluidSolver(unittest.TestCase):
    def setUp(self):
        self.config = SimulationConfig()
        self.grid = Grid(self.config)
        self.fluid_solver = FluidSolver(self.config, self.grid)
        self.forces = np.zeros_like(self.grid.velocity_field)

    def test_compute_a_matrix(self):
        self.assertEqual(
            self.fluid_solver.a_matrix.shape,
            (self.config.grid_size, self.config.grid_size, 2, 2),
        )

    def test_fluid_dynamics_step(self):
        initial_velocity = self.grid.velocity_field.copy()
        self.fluid_solver.fluid_dynamics_step(self.forces)
        updated_velocity = self.grid.velocity_field
        self.assertEqual(
            updated_velocity.shape,
            initial_velocity.shape,
        )


if __name__ == '__main__':
    unittest.main()
