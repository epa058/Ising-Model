import random
import matplotlib.pyplot as plt
import math

# ---Some constants---
N = 25 # Size of grid
J = 1 # Coupling strength
kBT = 2.5 * J # Critical temperature occurs at approximately 2.25~2.27 * J without diagonal contributions and at approximately 5.5 * J with diagonal contributions

# ---2D case---

# ---Initiate a grid of zeros---
grid = []

for i in range(N):
    row = []
    for j in range(N):
        row.append(0)
    grid.append(row)
    
# ---Fill the grid with spins of -1 and +1 chosen randomly---
for i in range(N):
    for j in range(N):
        spin = random.choice([-1, 1])
        grid[i][j] = spin
        
print(grid)

# ---Actual Metropolis algorithm implementation---
for i in range (N * 10000): # Iteration count
    # Pick a random spin
    x = random.randrange(0, N)
    y = random.randrange(0, N)

    # Neighbouring spins
    x_left = x - 1
    x_right = x + 1
    y_down = y - 1
    y_up = y + 1

    # Periodic boundary conditions
    if x_left < 0:
        x_left = x_left + N
    if x_right >= N:
        x_right = x_right - N
    if y_down < 0:
        y_down = y_down + N
    if y_up >= N:
        y_up = y_up - N

    '''
    If the spin at (x, y) flips, the only affected terms in the sum of the total energy
    will be the terms that contain the flipped spin.

    Instead of calculating the total initial and final energies of the system
    if the flip occurs, we only need to calculate the initial and final energies
    of the neighbouring pairs to the flipped spin.
    '''

    # No diagonal contributions
    Ei = -J * ((grid[x][y]) * (grid[x_left][y] + grid[x_right][y] + grid[x][y_down] + grid[x][y_up]))
    Ef = -J * ((-grid[x][y]) * (grid[x_left][y] + grid[x_right][y] + grid[x][y_down] + grid[x][y_up]))

    # With diagonal contributions (uncomment to include diagonal neighbours)
    # Ei = -J * ((grid[x][y]) * (grid[x_left][y] + grid[x_right][y] + grid[x][y_down] + grid[x][y_up] + grid[x_left][y_up] + grid[x_right][y_up] + grid[x_left][y_down] + grid[x_right][y_down]))
    # Ef = -J * ((-grid[x][y]) * (grid[x_left][y] + grid[x_right][y] + grid[x][y_down] + grid[x][y_up] +  grid[x_left][y_up] + grid[x_right][y_up] + grid[x_left][y_down] + grid[x_right][y_down]))

    # Calculate the change in energy of the system if the flip occurs
    DeltaE = Ef - Ei

    # Flip condition
    if DeltaE <= 0:
        grid[x][y] = -grid[x][y]
    else:
        P = math.exp(-DeltaE / kBT) # Probability
        p = random.uniform(0, 1) <= P

        if p == True: # Flip
            grid[x][y] = -grid[x][y]
        else: # No flip
            grid[x][y] = grid[x][y]
            
# ---Plotting (I like blue)---
fig, ax = plt.subplots()
ax.matshow(grid, cmap='Blues_r') # _r reverses the colormap spectrum
plt.show()

'''
# ---1D case---

# ---Initiate an array of zeros---
array = []

for i in range(N):
        array.append(0)

# ---Fill the array with spins of -1 and +1 chosen randomly---
for i in range(N):
    spin = random.choice([-1, 1])
    array[i] = spin

# ---Actual Metropolis algorithm implementation---
for i in range (N * 10000): # Iteration count
        # Pick a random spin
        x = random.randrange(0, N)

        # Neighbouring spins
        x_left = x - 1
        x_right = x + 1

        # Periodic boundary conditions
        if x_left < 0:
            x_left = x_left + N
        if x_right >= N:
            x_right = x_right - N

        # If the spin at (x, y) flips, the only affected terms in the sum of the total energy will be the terms that contain the flipped spin.
        # Instead of calculating the total initial and final energies of the system if the flip occurs, we only need to calculate the initial and final energies of the neighbouring pairs to the flipped spin.

        Ei = -J * ((array[x]) * (array[x_left] + array[x_right]))
        Ef = -J * ((-array[x]) * (array[x_left] + array[x_right]))

        # Calculate the change in energy of the system if the flip occurs
        DeltaE = Ef - Ei

        # Flip condition
        if DeltaE <= 0:
            array[x] = -array[x]
        else:
            P = math.exp(-DeltaE / kBT) # Probability
            p = random.uniform(0, 1) <= P
            
            if p == True: # Flip
                array[x]= -array[x]
            else: # No flip
                array[x] = array[x]

# ---Plotting (I like blue)---
grid = []
grid.append(array)

fig, ax = plt.subplots()
ax.get_yaxis().set_visible(False)
ax.matshow(grid, cmap='Blues_r') # _r reverses the colormap spectrum
plt.show()
'''
