import numpy as np
from scipy.fft import fftn, ifftn


class FluidSolver:
    """
    Solves the fluid dynamics equations.
    """

    def __init__(self, config, grid):
        self.config = config
        self.grid = grid
        self.a_matrix = self.compute_a_matrix()

    def compute_a_matrix(self):
        """
        Precompute the A matrix for solving the fluid equations in Fourier space.
        """
        N = self.config.grid_size
        dt = self.config.dt
        mu = self.config.mu
        rho = self.config.rho
        h = self.config.h

        a_matrix = np.zeros((N, N, 2, 2), dtype=complex)
        for m1 in range(N):
            for m2 in range(N):
                if not (
                    (m1 == 0 or m1 == N // 2) and (m2 == 0 or m2 == N // 2)
                ):
                    t = (2 * np.pi / N) * np.array([m1, m2])
                    s = np.sin(t)
                    ss = np.outer(s, s) / np.dot(s, s)
                    a_matrix[m1, m2, :, :] = np.eye(2) - ss

        for m1 in range(N):
            for m2 in range(N):
                t = (np.pi / N) * np.array([m1, m2])
                s = np.sin(t)
                denom = 1 + (dt / 2) * (mu / rho) * (4 / (h ** 2)) * np.dot(s, s)
                a_matrix[m1, m2, :, :] /= denom

        return a_matrix

    def skew_symmetric(self, velocity):
        """
        Compute the skew-symmetric part of the nonlinear term.

        The skew-symmetric form helps in conserving kinetic energy.
        """
        skew = np.zeros_like(velocity)
        skew[:, :, 0] = self.skew_term(velocity, velocity[:, :, 0])
        skew[:, :, 1] = self.skew_term(velocity, velocity[:, :, 1])
        return skew

    def skew_term(self, velocity, component):
        """
        Compute a component of the skew-symmetric term.
        """
        ip = self.config.ip
        im = self.config.im
        h = self.config.h
        term1 = (
            (velocity[ip, :, 0] + velocity[:, :, 0]) * component[ip, :]
            - (velocity[im, :, 0] + velocity[:, :, 0]) * component[im, :]
        )
        term2 = (
            (velocity[:, ip, 1] + velocity[:, :, 1]) * component[:, ip]
            - (velocity[:, im, 1] + velocity[:, :, 1]) * component[:, im]
        )
        return (term1 + term2) / (4 * h)

    def fluid_dynamics_step(self, forces):
        """
        Update the fluid velocity field based on the forces.

        The fluid velocity \( \mathbf{u} \) is updated in Fourier space.
        """
        dt = self.config.dt
        rho = self.config.rho
        velocity_field = self.grid.velocity_field

        w = (
            velocity_field
            - (dt / 2) * self.skew_symmetric(velocity_field)
            + (dt / (2 * rho)) * forces
        )

        w_hat = fftn(w, axes=(0, 1))
        updated_velocity_hat = np.zeros_like(w_hat, dtype=complex)

        updated_velocity_hat[:, :, 0] = (
            self.a_matrix[:, :, 0, 0] * w_hat[:, :, 0]
            + self.a_matrix[:, :, 0, 1] * w_hat[:, :, 1]
        )
        updated_velocity_hat[:, :, 1] = (
            self.a_matrix[:, :, 1, 0] * w_hat[:, :, 0]
            + self.a_matrix[:, :, 1, 1] * w_hat[:, :, 1]
        )

        updated_velocity = np.real(ifftn(updated_velocity_hat, axes=(0, 1)))
        self.grid.velocity_field = updated_velocity