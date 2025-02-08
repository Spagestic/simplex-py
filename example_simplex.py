import numpy as np
from simplex import tabular_simplex

# Example 1: Maximization problem with all <= constraints
c1 = np.array([3, 5])
A1 = np.array([[1, 0], [0, 2], [3, 2]])
b1 = np.array([4, 12, 18])
senses1 = ['<=', '<=', '<=']

print("Example 1: Maximization")
status1, x1, z1 = tabular_simplex(c1, A1, b1, senses1, prob_type='max')

print(f"\nFinal Status: {status1}")
if x1 is not None:
    print(f"Optimal solution: x = {x1}")
    print(f"Optimal objective value: z = {z1}")

# Example 2: Minimization problem with mixed constraints
c2 = np.array([2, 3])
A2 = np.array([[1, 1], [2, 1]])
b2 = np.array([10, 16])
senses2 = ['>=', '=']

print("\nExample 2: Minimization")
status2, x2, z2 = tabular_simplex(c2, A2, b2, senses2, prob_type='min')

print(f"\nFinal Status: {status2}")
if x2 is not None:
    print(f"Optimal solution: x = {x2}")
    print(f"Optimal objective value: z = {z2}")

# Example 3: Another Maximization problem with mixed constraints
c3 = np.array([1, 2])
A3 = np.array([[1, 1], [1, 1]])
b3 = np.array([4, 6])
senses3 = ['<=', '>=']

print("\nExample 3: Maximization with mixed constraints")
status3, x3, z3 = tabular_simplex(c3, A3, b3, senses3, prob_type='max')

print(f"\nFinal Status: {status3}")
if x3 is not None:
    print(f"Optimal solution: x = {x3}")
    print(f"Optimal objective value: z = {z3}")
