import h5py


class ResultSaver:
    """
    Saves simulation results to an HDF5 file.
    """

    def __init__(self, config, grid, markers):
        self.config = config
        self.grid = grid
        self.markers = markers
        self.results_file = h5py.File("immersed_boundary_simulation_results.h5", "w")
        self.create_datasets()

    def create_datasets(self):
        """
        Create datasets for storing velocity fields and marker positions.
        """
        grid_size = self.config.grid_size
        num_markers = self.config.num_boundary_markers
        num_steps = self.config.clock_max

        self.results_file.create_dataset(
            "velocity_field", (num_steps, grid_size, grid_size, 2), dtype="f"
        )
        self.results_file.create_dataset(
            "marker_positions", (num_steps, num_markers, 2), dtype="f"
        )
        self.results_file.create_dataset("time", (num_steps,), dtype="f")

    def save_results(self, clock):
        """
        Save the current state of the simulation.
        """
        self.results_file["velocity_field"][clock] = self.grid.velocity_field
        self.results_file["marker_positions"][clock] = self.markers.positions
        self.results_file["time"][clock] = clock * self.config.dt

    def close(self):
        """
        Close the HDF5 results file.
        """
        self.results_file.close()

    @staticmethod
    def load_results(file_name="immersed_boundary_simulation_results.h5"):
        """
        Load simulation results from an HDF5 file.
        """
        return h5py.File(file_name, "r")

    @staticmethod
    def get_velocity_at_time(h5file, t):
        """
        Retrieve the velocity field at a specific time.
        """
        time_steps = h5file["time"][:]
        closest_index = (np.abs(time_steps - t)).argmin()
        return h5file["velocity_field"][closest_index]

    @staticmethod
    def get_marker_positions_at_time(h5file, t):
        """
        Retrieve the marker positions at a specific time.
        """
        time_steps = h5file["time"][:]
        closest_index = (np.abs(time_steps - t)).argmin()
        return h5file["marker_positions"][closest_index]