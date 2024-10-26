from pyIB2D.grid import Grid
from pyIB2D.markers import BoundaryMarkers
from pyIB2D.forces import ForceCalculator
from pyIB2D.fluid_solver import FluidSolver
from pyIB2D.interpolator import Interpolator
from pyIB2D.visualizer import Visualizer
from pyIB2D.result_saver import ResultSaver

class ImmersedBoundarySimulator:
    """
    Main simulation class orchestrating all components.
    """

    def __init__(self, config):
        self.config = config
        self.grid = Grid(config)
        self.markers = BoundaryMarkers(config)
        self.force_calculator = ForceCalculator(config, self.markers)
        self.fluid_solver = FluidSolver(config, self.grid)
        self.interpolator = Interpolator(config, self.grid, self.markers)
        self.visualizer = Visualizer(config, self.grid, self.markers)
        self.result_saver = ResultSaver(config, self.grid, self.markers)

    def run_simulation(self):
        """
        Run the immersed boundary simulation.
        """
        for clock in range(self.config.clock_max):
            # Interpolate velocity to markers
            marker_velocity = self.interpolator.interpolate_velocity_to_markers()

            # Update marker positions (midpoint method)
            marker_intermediate = (
                self.markers.positions + (self.config.dt / 2) * marker_velocity
            )

            # Compute forces at the intermediate marker positions
            self.markers.positions = marker_intermediate  # Temporarily update positions
            forces = self.force_calculator.total_forces(clock)
            self.markers.positions -= (self.config.dt / 2) * marker_velocity  # Revert positions

            # Spread forces onto the grid
            forces_on_grid = self.interpolator.spread_forces_to_grid(forces)

            # Fluid dynamics step
            self.fluid_solver.fluid_dynamics_step(forces_on_grid)

            # Update marker positions with updated velocity field
            marker_velocity = self.interpolator.interpolate_velocity_to_markers()
            self.markers.positions += self.config.dt * marker_velocity

            # Visualization
            self.visualizer.visualize(clock)

            # Save results
            self.result_saver.save_results(clock)

        self.result_saver.close()