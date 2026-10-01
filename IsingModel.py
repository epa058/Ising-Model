import random
import math
import matplotlib.pyplot as plt

# ---Some constants---
N = 25 # Size of grid (N x N grid in 2D; chain of N spins in 1D)
J = 1 # Coupling strength
kBT = 2.5 * J
dim = 2 # 1 or 2
diagonal = False # 2D only, additionally couples each spin to its 4 diagonal neighbours
warmup = 200 # Sweeps discarded so the system can reach equilibrium first
recorded_sweeps = 500 # Sweeps averaged over when measuring the magnetization
find_crit_temp = True # Plots <|m|> against kBT to locate the critical temperature

# The exact critical temperature in 2D without diagonals is 2 / ln(1 + sqrt(2)) ≈ 2.269 J (Onsager)
# In 1D, there is no phase transition at any kBT > 0, so the chain only looks noisier as kBT grows.

rows = 1 if dim == 1 else N  # A 1D chain is stored as a single row
spins = rows * N 

def random_grid():
    # Fill the grid with spins of -1 and +1 chosen randomly
    return [[random.choice([-1, 1]) for _ in range(N)] for _ in range(rows)]

def ordered_grid():
    # All spins +1; starting here can avoid long-lived stripe domains that a random start can freeze into at low kBT
    return [[1] * N for _ in range(rows)]

def neighbour_sum(grid, x, y):
    # Periodic boundary conditions
    left, right = (y - 1) % N, (y + 1) % N
    total = grid[x][left] + grid[x][right]
    if dim == 2:
        down, up = (x - 1) % N, (x + 1) % N
        total += grid[down][y] + grid[up][y]
        if diagonal:
            total += grid[down][left] + grid[down][right] + grid[up][left] + grid[up][right]
    return total

def metropolis_step(grid, kBT):
    # Pick a random spin
    x = random.randrange(rows)
    y = random.randrange(N)
    s = grid[x][y]

    # If the spin flips, only the bonds touching it change, so the energy change is
    # DeltaE = Ef - Ei = (-J * (-s) * neighbours) - (-J * s * neighbours) = 2 * J * s * neighbours
    DeltaE = 2 * J * s * neighbour_sum(grid, x, y)

    # Flip condition
    if DeltaE <= 0:
        grid[x][y] = -s  # Energy goes down (or stays the same): always flip
    else:
        P = math.exp(-DeltaE / kBT)  # Probability of flipping
        if random.random() < P:
            grid[x][y] = -s

def sweep(grid, kBT):
    # One sweep = as many attempted flips as there are spins
    for _ in range(spins):
        metropolis_step(grid, kBT)

def magnetization(grid):
    # Magnetization per spin, between -1 and +1
    total = 0
    for row in grid:
        for spin in row:
            total += spin
    return total / spins

def simulate(kBT, ordered_start=False):
    if ordered_start:
        grid = ordered_grid()
    else:
        grid = random_grid()

    # Warm-up
    for _ in range(warmup):
        sweep(grid, kBT)

    # Measurement: after each further sweep, record |m|, then take the average
    magnetization_sum = 0
    for _ in range(recorded_sweeps):
        sweep(grid, kBT)
        magnetization_sum += abs(magnetization(grid))
    average_magnetization = magnetization_sum / recorded_sweeps

    # grid is the final configuration
    return grid, average_magnetization

# ---Final configuration plot (I like blue)---
grid, m = simulate(kBT)
print(f"kBT = {kBT:.2f} J: <|m|> = {m:.3f}")
print()

fig1, ax1 = plt.subplots()
ax1.matshow(grid, cmap='Blues_r')  # _r reverses the colormap spectrum
ax1.set_title(f"kBT = {kBT:.2f} J")
if dim == 1:
    ax1.get_yaxis().set_visible(False)

# ---Critical temperature plot---
if find_crit_temp:
    T_max = 8 * J if diagonal else 4 * J
    temperatures = [T_max * i / 25 for i in range(1, 26)]
    magnetizations = []
    for T in temperatures:
        _, m = simulate(T, ordered_start=True)
        magnetizations.append(m)
        print(f"kBT = {T:.2f} J: <|m|> = {m:.3f}")

    fig2, ax2 = plt.subplots()
    ax2.plot(temperatures, magnetizations, 'o-')
    if dim == 2 and not diagonal:
        ax2.axvline(2 / math.log(1 + math.sqrt(2)) * J, color='gray', linestyle='--', label='Onsager $T_c$')
        ax2.legend()
    ax2.set_xlabel('kBT / J')
    ax2.set_ylabel('<|m|>')
    ax2.set_title(f"N = {N}, {dim}D" + (", with diagonals" if diagonal else ""))

plt.show()
