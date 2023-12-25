# Ising-Model

![](https://github.com/epa058/Strange-Attractors/blob/main/Animations/Aizawa%20Attractor.gif)

This Python code simulates the two-dimensional Ising model using the Metropolis algorithm on a square lattice at a given temperature. 

It begins by initializing the spin grid, in which each magnetic spin is assigned a random initial state of -1 or +1. The Metropolis algorithm then evolves the spin system by randomly flipping spins based on changes in the system's energy, parametrized by $kB T$, the Boltzmann constant $k_B$ multiplied by the temperature $T$. The energy calculations take into account the nearest neighbours' spins, which may include diagonal interactions, under periodic boundary conditions. After a set number of iterations, the resulting spin configuration is visualized using a colour map. The script also includes a section for a one-dimensional model, which is currently commented out.

The results are displayed in the folders "2D noDiag," "2D withDiag," and "1D."
