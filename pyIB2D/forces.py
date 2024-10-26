import numpy as np


class ForceCalculator:
    """
    Calculates forces acting on the boundary markers.
    """

    def __init__(self, config, markers):
        self.config = config
        self.markers = markers

    def compute_elastic_forces(self, current_step):
        """
        Compute elastic forces based on marker positions.

        Elastic force \( F_{\text{elastic}} \) is calculated as:
        \[
        F_{\text{elastic}} = K \frac{X_{k+1} + X_{k-1} - 2X_k}{\Delta \theta^2}
        \]
        """
        dtheta = self.config.dtheta
        kp = self.config.kp
        km = self.config.km
        K = self.config.K
        positions = self.markers.positions
        
        elastic_force = K * (positions[kp, :] + positions[km, :] - 2 * positions) / (dtheta ** 2)
    
        if current_step >= self.config.cut_step >= 0:
            cut_marker = self.config.cut_marker
            elastic_force[cut_marker, :] = 0
            elastic_force[self.config.kp[cut_marker], :] = 0

        return elastic_force

    def compute_bending_forces(self, current_step):
        """
        Compute bending forces based on marker positions.

        Bending force \( F_{\text{bending}} \) is calculated as:
        \[
        F_{\text{bending}} = K_b \frac{X_{k+1} - 2X_k + X_{k-1}}{\Delta \theta^4}
        \]
        """
        dtheta = self.config.dtheta
        kp = self.config.kp
        km = self.config.km
        Kb = self.config.Kb
        positions = self.markers.positions
        curvature_term = positions[kp, :] - 2 * positions + positions[km, :]
        
        bending_force = Kb * curvature_term / (dtheta ** 4)

        if current_step >= self.config.cut_step >= 0:
            cut_marker = self.config.cut_marker
            bending_force[cut_marker, :] = 0

        return bending_force

    def total_forces(self, current_step):
        """
        Compute total forces acting on the markers.
        """
        elastic = self.compute_elastic_forces(current_step)
        bending = self.compute_bending_forces(current_step)
        
        return elastic + bending