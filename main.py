from pyIB2D.config import SimulationConfig
from pyIB2D.simulator import ImmersedBoundarySimulator
from pyIB2D.result_saver import ResultSaver


def run_immersed_boundary_simulation():
    config = SimulationConfig(
        length=1.0,
        grid_size=64,
        boundary_markers=None,
        rho=1.0,
        mu=0.1,
        tmax=4,
        dt=0.001,
        cut_marker=-1,
        cut_step=-1,
    )
    simulation = ImmersedBoundarySimulator(config)
    simulation.run_simulation()


if __name__ == "__main__":
    run_immersed_boundary_simulation()

    # Example usage of loading results:
    with ResultSaver.load_results() as h5file:
        t_query = 0.3
        velocity_field = ResultSaver.get_velocity_at_time(h5file, t_query)
        marker_positions = ResultSaver.get_marker_positions_at_time(h5file, t_query)
        print("Velocity at t=0.3:", velocity_field)
        print("Marker positions at t=0.3:", marker_positions)
