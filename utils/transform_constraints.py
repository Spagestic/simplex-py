import numpy as np

def transform_constraints(A, b, senses):
    """
    Transforms '>=' constraints to '<=' by multiplying the row and b by -1.

    Args:
        A: Constraint coefficient matrix (numpy array).
        b: Right-hand side values (numpy array).
        senses: List of strings for each constraint ('<=', '>=', '=').

    Returns:
        A_trans: transformed constraint matrix
        b_trans: transformed right-hand side values
    """
    A_trans = A.copy()
    b_trans = b.copy()
    for i in range(len(senses)):
        if senses[i] == '>=':
            A_trans[i, :] = -A[i, :]
            b_trans[i] = -b[i]
            senses[i] = '<='  # Update sense to '<='
    return A_trans, b_trans
