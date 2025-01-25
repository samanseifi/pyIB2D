import matplotlib.pyplot as plt
import imageio
import os

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
        and save it in a gif file.
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

    def visualize_create_gif(self, clock, save_gif=True, gif_filename="vorticity_evolution.gif"):
        """
        Visualize the vorticity field and marker positions at each time step
        and save it as a gif file.
        """
        # Create a temporary folder to store images
        temp_dir = "temp_images"
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)

        # Compute vorticity
        vorticity = self.grid.compute_vorticity()
        
        # Plot the vorticity field and marker positions
        plt.contourf(self.grid.x_grid, self.grid.y_grid, vorticity, levels=20, vmin=-5, vmax=5)
        plt.plot(self.markers.positions[:, 0], self.markers.positions[:, 1], "ko", markersize=1)
        plt.axis([0, self.config.length, 0, self.config.length])
        plt.gca().set_aspect("equal", adjustable="box")
        plt.title(f"Time step: {clock}, Time: {clock * self.config.dt:.2f}")
        
        # Save each frame as an image
        img_filename = os.path.join(temp_dir, f"frame_{clock:04d}.png")
        plt.savefig(img_filename)
        plt.clf()

        # After all time steps, create GIF
        if clock == self.config.clock_max - 1 and save_gif:
            images = []
            for i in range(self.config.clock_max):
                img_file = os.path.join(temp_dir, f"frame_{i:04d}.png")
                images.append(imageio.imread(img_file))

            imageio.mimsave(gif_filename, images, duration=0.1)
            print(f"Saved GIF as {gif_filename}")

            # Clean up temporary images
            for img_file in images:
                os.remove(img_file)
            os.rmdir(temp_dir)
