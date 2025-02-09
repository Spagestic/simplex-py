import numpy as np

def find_primal_solution(dual_solution, constraint_matrix, objective_coeffs):
    """
    Finds the primal solution using complementary slackness.

    Args:
        dual_solution (np.array): Optimal solution of the dual problem.
        constraint_matrix (np.array): Constraint matrix of the primal problem.
        objective_coeffs (np.array): Objective coefficients of the primal problem.

    Returns:
        np.array: Primal solution.
    """
    num_original_vars = len(objective_coeffs)
    num_constraints = constraint_matrix.shape[0]
    primal_solution = np.zeros(num_original_vars)

    # Identify binding constraints in the dual
    binding_constraints_dual = np.where(dual_solution > 1e-6)[0]  # Use a small tolerance

    # Set corresponding primal variables to zero
    non_binding_constraints_dual = np.setdiff1d(np.arange(num_constraints), binding_constraints_dual)
    for i in non_binding_constraints_dual:
        # Find columns in constraint matrix corresponding to non-binding constraints
        # and set corresponding primal variables to zero
        primal_solution[i] = 0

    # For binding constraints, solve a reduced system of equations
    A_reduced = constraint_matrix[binding_constraints_dual, :]
    b_reduced = objective_coeffs[binding_constraints_dual]

    # Check if the reduced system is solvable
    if A_reduced.shape[1] >= A_reduced.shape[0]:
        try:
            # Solve the reduced system using least squares
            primal_solution, _, _, _ = np.linalg.lstsq(A_reduced, b_reduced, rcond=None)
        except np.linalg.LinAlgError:
            print("Singular matrix encountered. Cannot solve for primal variables.")
            return None
    else:
        print("Underdetermined system. Cannot uniquely solve for primal variables.")
        return None

    return primal_solution