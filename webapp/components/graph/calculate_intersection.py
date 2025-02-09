import numpy as np

def calculate_intersection(constraint1, constraint2, rhs1, rhs2):
    a1, b1 = constraint1
    a2, b2 = constraint2
    det = a1 * b2 - a2 * b1
    if np.isclose(det, 0):
        return None  # Lines are parallel

    x = (b2 * rhs1 - b1 * rhs2) / det
    y = (a1 * rhs2 - a2 * rhs1) / det
    return x, y