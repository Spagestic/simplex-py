import logging
import numpy as np

logger = logging.getLogger(__name__)

def solve_simplex(objective_coeffs, constraint_matrix, rhs_values, senses, problem_type):
    """
    Solves the linear programming problem using the tabular simplex method.

    Args:
        objective_coeffs (np.array): The coefficients of the objective function.
        constraint_matrix (np.array): The matrix of constraint coefficients.
        rhs_values (np.array): The right-hand side values of the constraints.
        senses (list): The senses of the constraints ("<=", ">=", "=").
        problem_type (str): The type of the problem ("max" or "min").

    Returns:
        tuple: A tuple containing the solution status, the optimal solution, the optimal objective value, and the tableau history.
    """
    try:
        # Call the tabular simplex method
        from webapp.simplex import tabular_simplex
        status, solution, objective_value, tableau_history = tabular_simplex(
            objective_coeffs, constraint_matrix, rhs_values, senses, problem_type
        )
        return status, solution, objective_value, tableau_history
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
        return "error", None, None, None
