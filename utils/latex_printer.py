import numpy as np
from typing import List
import logging

# Set up logging
logger = logging.getLogger(__name__)

def print_latex_problem(
    objective_coeffs: np.ndarray,
    constraint_matrix: np.ndarray,
    rhs_values: np.ndarray,
    senses: List[str],
    problem_type: str = 'max'
) -> None:
    """
    Prints the linear programming problem in LaTeX format.

    Args:
        objective_coeffs (np.ndarray): Objective function coefficients.
        constraint_matrix (np.ndarray): Constraint coefficient matrix.
        rhs_values (np.ndarray): Right-hand side values.
        senses (List[str]): List of strings for each constraint ('<=', '>=', '=').
        problem_type (str): 'max' for maximization, 'min' for minimization.
    """
    logger.info("Printing the linear programming problem in LaTeX format")
    
    num_vars = len(objective_coeffs)  # Number of variables

    # Objective function
    if problem_type == 'max':
        print(r'\begin{align*}')
        print(r'\max \quad &', end='')
    elif problem_type == 'min':
        print(r'\begin{align*}')
        print(r'\min \quad &', end='')
    else:
        raise ValueError("Invalid problem_type. Must be 'max' or 'min'.")
    
    obj_str = ' + '.join([f'{objective_coeffs[i]}x_{i+1}' for i in range(num_vars)])
    print(obj_str, r'\\')

    # Constraints
    print(r'\text{subject to} \quad &')
    for i in range(constraint_matrix.shape[0]):
        constraint_str = ' + '.join([f'{constraint_matrix[i, j]}x_{j+1}' for j in range(num_vars)])
        if senses[i] == '<=':
            sense_str = r'\leq'
        elif senses[i] == '>=':
            sense_str = r'\geq'
        elif senses[i] == '=':
            sense_str = '='
        else:
            raise ValueError("Invalid sense. Must be '<=', '>=', or '='.")
        print(constraint_str, sense_str, rhs_values[i], r'\\')

    # Non-negativity constraints
    non_neg_str = ', '.join([f'x_{i+1}' for i in range(num_vars)])
    print(non_neg_str, r'\geq 0')
    print(r'\end{align*}')
    
    logger.info("LaTeX output complete")
