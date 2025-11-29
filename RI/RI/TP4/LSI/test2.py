import numpy as np

# Selected rows of S_k_inv @ U_k.T
rows = np.array([
    [-0.03593769,  0.04096726, -0.00129446],
    [-0.03177361,  0.00514632,  0.00225371],
    [-0.02323165, -0.00541501,  0.00365516],
    [-0.06120461, -0.00122591, -0.02025101],
    [-0.07901222, -0.11125016, -0.09663657],
    [-0.03797056, -0.0348305,   0.07169695]
])

# Sum column-wise
col_sums = np.sum(rows, axis=0)

print("Sum of first values:", col_sums[0])
print("Sum of second values:", col_sums[1])
print("Sum of third values:", col_sums[2])
