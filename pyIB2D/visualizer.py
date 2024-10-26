import matplotlib.pyplot as plt


class Visualizer:
    """
    Handles visualization of the simulation.
    """

    def __init__(self, config, grid, markers):
        self.config = config
        self.grid = grid
        self.markers = markers

    def visualize(self, clock):
        """
        Visualize the vorticity field and marker positions at each time step.
        """
        vorticity = self.grid.compute_vorticity()
        plt.contourf(self.grid.x_grid, self.grid.y_grid, vorticity, levels=20, vmin=-5, vmax=5,)
        plt.plot(self.markers.positions[:, 0], self.markers.positions[:, 1], "ko", markersize=1)
        plt.axis([0, self.config.length, 0, self.config.length])
        plt.gca().set_aspect("equal", adjustable="box")
        plt.title(f"Time step: {clock}, Time: {clock * self.config.dt:.2f}")
        plt.draw()
        plt.pause(0.01)
        plt.clf()