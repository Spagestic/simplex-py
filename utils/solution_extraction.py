import numpy as np
from typing import Tuple
import logging

# Set up logging
logger = logging.getLogger(__name__)

def extract_solution(
    tableau: np.ndarray,
    num_original_vars: int,
    num_constraints: int,
    problem_type: str = 'max'
) -> Tuple[np.ndarray, float]:
    logger.info("Extracting solution from the tableau")
    
    optimal_solution = np.zeros(num_original_vars)
    
    # Iterate through each of the original variables
    for i in range(num_original_vars):
        # Check if the column corresponds to a basic variable (i.e., it has a 1 and the rest are 0)
        column = tableau[:, i]
        
        # Check if the column is a unit vector
        if np.sum(np.abs(column)) == 1 and np.sum(column == np.abs(column)) == 1:
            # If it is a unit vector, find the row where the 1 is located
            basic_variable_row = np.where(column == 1)[0][0]
            
            # The value of the basic variable is the value in the right-hand side of the tableau
            optimal_solution[i] = tableau[basic_variable_row, -1]
            logger.debug(f"Variable x_{i+1} is basic with value {optimal_solution[i]}")
            
    # Extract the optimal objective value from the tableau
    optimal_objective_value = tableau[0, -1]
    
    # If the problem was a minimization problem, negate the objective value
    if problem_type == 'min':
        optimal_objective_value = -optimal_objective_value
        logger.debug("Negating objective value for minimization problem")
        
    logger.info(f"Optimal solution: {optimal_solution}")
    logger.info(f"Optimal objective value: {optimal_objective_value}")
    
    return optimal_solution, optimal_objective_value
