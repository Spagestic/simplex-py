import numpy as np
from utils.find_primal_solution import find_primal_solution

def dual_simplex(objective_coeffs, constraint_matrix, rhs_values, senses, verbose=True):
    # 1. Convert to Standard Form (all constraints as <= for the dual)
    A = np.array(constraint_matrix)
    b = np.array(rhs_values)
    c = np.array(objective_coeffs)

    # 2. Create the Dual Problem
    # Dual objective: maximize b^T y
    dual_objective_coeffs = b
    # Dual constraints: A^T y <= c
    dual_constraint_matrix = A.T
    dual_rhs_values = c
    dual_senses = ['<='] * len(c)  # All dual constraints are <=

    # 3. Solve the Dual using tabular_simplex (which handles maximization)
    from webapp.simplex import tabular_simplex
    status, dual_solution, dual_optimal, tableau_history = tabular_simplex(dual_objective_coeffs, dual_constraint_matrix, dual_rhs_values, dual_senses, problem_type='max', verbose=verbose)

    if status == 'optimal':
        # Strong duality: dual optimal = primal optimal
        primal_optimal = dual_optimal

        # Find primal solution using complementary slackness
        primal_solution = find_primal_solution(dual_solution, constraint_matrix, objective_coeffs)

        return status, primal_solution, primal_optimal, tableau_history # Return primal optimal value
    else:  # Dual is infeasible or unbounded, meaning primal is infeasible or unbounded.
        return status, None, None, tableau_history
