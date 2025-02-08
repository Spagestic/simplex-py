import numpy as np
from typing import List, Union
import logging

# Set up logging
logger = logging.getLogger(__name__)

def validate_inputs(
    objective_coeffs: np.ndarray,
    constraint_matrix: np.ndarray,
    rhs_values: np.ndarray,
    senses: List[str],
    problem_type: str = 'max'
) -> None:
    """
    Validates the inputs for the simplex method.

    Args:
        objective_coeffs (np.ndarray): Objective function coefficients.
        constraint_matrix (np.ndarray): Constraint coefficient matrix.
        rhs_values (np.ndarray): Right-hand side values.
        senses (List[str]): List of strings for each constraint ('<=', '>=', '=').
        problem_type (str): 'max' for maximization, 'min' for minimization.

    Raises:
        ValueError: If any of the inputs are invalid.
    """
    logger.info("Validating inputs")
    
    # Check if the objective coefficients are a 1D numpy array
    if not isinstance(objective_coeffs, np.ndarray) or objective_coeffs.ndim != 1:
        logger.error("Objective coefficients must be a 1D numpy array.")
        raise ValueError("Objective coefficients must be a 1D numpy array.")
    
    # Check if the constraint matrix is a 2D numpy array
    if not isinstance(constraint_matrix, np.ndarray) or constraint_matrix.ndim != 2:
        logger.error("Constraint matrix must be a 2D numpy array.")
        raise ValueError("Constraint matrix must be a 2D numpy array.")
    
    # Check if the right-hand side values are a 1D numpy array
    if not isinstance(rhs_values, np.ndarray) or rhs_values.ndim != 1:
        logger.error("Right-hand side values must be a 1D numpy array.")
        raise ValueError("Right-hand side values must be a 1D numpy array.")
    
    # Check if the senses are a list of strings
    if not isinstance(senses, list) or not all(isinstance(sense, str) for sense in senses):
        logger.error("Senses must be a list of strings.")
        raise ValueError("Senses must be a list of strings.")
    
    # Check if the problem type is valid
    if problem_type not in ['max', 'min']:
        logger.error("Problem type must be 'max' or 'min'.")
        raise ValueError("Problem type must be 'max' or 'min'.")
    
    # Check if the dimensions of the inputs are consistent
    num_constraints = constraint_matrix.shape[0]
    num_variables = constraint_matrix.shape[1]
    
    if len(rhs_values) != num_constraints:
        logger.error("The number of right-hand side values must be equal to the number of constraints.")
        raise ValueError("The number of right-hand side values must be equal to the number of constraints.")
    
    if len(objective_coeffs) != num_variables:
        logger.error("The number of objective coefficients must be equal to the number of variables.")
        raise ValueError("The number of objective coefficients must be equal to the number of variables.")
    
    if len(senses) != num_constraints:
        logger.error("The number of senses must be equal to the number of constraints.")
        raise ValueError("The number of senses must be equal to the number of constraints.")
    
    logger.info("Inputs validated successfully.")
