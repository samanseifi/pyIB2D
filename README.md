# Immersed Boundary Simulation

A Python code for simulating 2D immersed boundary problems using the semi-implicit solver for fluid solver

![Vorticity Evolution](vorticity_evolution.gif)

## Features

- Modular design with classes for configuration, grid management, marker handling, force calculation, fluid solving, interpolation, visualization, and result saving.
- Supports elastic and bending forces on immersed boundaries.
- Uses Fast Fourier Transforms for efficient fluid dynamics computations.
- Saves simulation results in HDF5 format.

## Installation

```bash
pip install -e .
