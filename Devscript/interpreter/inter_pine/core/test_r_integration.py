import rpy2.robjects as robjects

# Create an R vector
r_vector = robjects.FloatVector([1.1, 2.2, 3.3, 4.4, 5.5])

# Calculate mean using R
mean_result = robjects.r['mean'](r_vector)

print(f"Mean calculated in R: {mean_result[0]}")
