import logging
import numpy as np

logger = logging.getLogger(__name__)

def solve_simplex(
        objective_coeffs, 
        constraint_matrix, 
        rhs_values, 
        senses, 
        problem_type,
        verbose=True
        ):
    try:
        # Call the tabular simplex method
        from webapp.simplex import tabular_simplex
        from webapp.logic.dual_simplex import dual_simplex # Import dual_simplex
        if problem_type == 'min':
            status, solution, objective_value, tableau_history = dual_simplex(objective_coeffs, constraint_matrix, rhs_values, senses, verbose)
        else:
            status, solution, objective_value, tableau_history = tabular_simplex(
                objective_coeffs, constraint_matrix, rhs_values, senses, problem_type, verbose
            )
        return status, solution, objective_value, tableau_history
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        return "error", None, None, None
