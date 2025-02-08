import numpy as np
from typing import List
import logging

# Set up logging
logger = logging.getLogger(__name__)

def setup_tableau(
    objective_coeffs: np.ndarray,
    constraint_matrix: np.ndarray,
    rhs_values: np.ndarray,
    senses: List[str],
    problem_type: str = 'max'
) -> np.ndarray:
    """
    Sets up the initial tableau for the simplex method.

    Args:
        objective_coeffs (np.ndarray): Objective function coefficients.
        constraint_matrix (np.ndarray): Constraint coefficient matrix.
        rhs_values (np.ndarray): Right-hand side values.
        senses (List[str]): List of strings for each constraint ('<=', '>=', '=').
        problem_type (str): 'max' for maximization, 'min' for minimization.

    Returns:
        np.ndarray: The initial tableau as a numpy array.
    """
    logger.info("Setting up the initial tableau")
    
    num_constraints, num_original_vars = constraint_matrix.shape
    
    # If minimization, negate the objective function coefficients
    if problem_type == 'min':
        objective_coeffs = -objective_coeffs
        logger.debug("Negating objective coefficients for minimization problem")

    # Calculate the number of slack, surplus, and artificial variables
    num_slack_vars = senses.count('<=')
    num_surplus_vars = senses.count('>=')
    num_artificial_vars = senses.count('=') + num_surplus_vars

    # Calculate the total number of variables in the tableau
    num_total_vars = num_original_vars + num_slack_vars + num_artificial_vars

    # Initialize the tableau with zeros
    tableau = np.zeros((num_constraints + 1, num_total_vars + 1))

    # Objective function row
    tableau[0, :num_original_vars] = objective_coeffs
    tableau[0, -1] = 0  # Objective value

    # Constraint rows
    slack_surplus_index = num_original_vars
    artificial_index = num_original_vars + num_slack_vars
    for i in range(num_constraints):
        tableau[i + 1, :num_original_vars] = constraint_matrix[i, :]
        tableau[i + 1, -1] = rhs_values[i]

        if senses[i] == '<=':
            tableau[i + 1, slack_surplus_index] = 1
            slack_surplus_index += 1
        elif senses[i] == '>=' or senses[i] == '=':
            tableau[i + 1, artificial_index] = 1
            artificial_index += 1
            if senses[i] == '>=':
                tableau[i + 1, slack_surplus_index] = -1
                slack_surplus_index += 1
    
    logger.info("Initial tableau setup complete")
    return tableau
