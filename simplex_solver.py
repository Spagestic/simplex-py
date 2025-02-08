import numpy as np
from typing import List, Tuple
from utils.transform_constraints import transform_constraints
from utils.setup_tableau import setup_tableau
from utils.pivot import select_entering_variable, select_leaving_variable, pivot
from utils.solution_extraction import extract_solution
from utils.input_validation import validate_inputs
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def simplex_solver(
    objective_coeffs: np.ndarray,
    constraint_matrix: np.ndarray,
    rhs_values: np.ndarray,
    senses: List[str],
    problem_type: str = 'max',
    max_iterations: int = 100
) -> Tuple[np.ndarray, float]:
    """
    Solves a linear programming problem using the simplex method.

    Args:
        objective_coeffs (np.ndarray): Objective function coefficients.
        constraint_matrix (np.ndarray): Constraint coefficient matrix.
        rhs_values (np.ndarray): Right-hand side values.
        senses (List[str]): List of strings for each constraint ('<=', '>=', '=').
        problem_type (str): 'max' for maximization, 'min' for minimization.
        max_iterations (int): Maximum number of iterations to perform.

    Returns:
        Tuple[np.ndarray, float]: A tuple containing the optimal solution and the optimal objective value.
    """
    logger.info("Starting simplex solver")
    
    # Validate inputs
    validate_inputs(objective_coeffs, constraint_matrix, rhs_values, senses, problem_type)
    
    # Transform constraints to standard form
    transformed_matrix, transformed_rhs = transform_constraints(constraint_matrix, rhs_values, senses)
    
    # Set up the initial tableau
    tableau = setup_tableau(objective_coeffs, transformed_matrix, transformed_rhs, senses, problem_type)
    logger.info(f"Initial Tableau:\n{tableau}")
    
    num_original_vars = len(objective_coeffs)
    num_constraints = len(senses)
    
    # Iterate until optimal solution is found or max iterations reached
    iteration = 0
    while iteration < max_iterations:
        logger.info(f"Iteration: {iteration + 1}")
        
        # Select entering variable
        entering_col = select_entering_variable(tableau)
        logger.info(f"Entering column: {entering_col}")
        
        # Check if all coefficients in the objective row are non-negative
        if tableau[0, entering_col] >= 0:
            logger.info("Optimal solution found")
            break
            
        # Select leaving variable
        leaving_row = select_leaving_variable(tableau, entering_col)
        logger.info(f"Leaving row: {leaving_row}")
        
        # Check if the problem is unbounded
        if leaving_row is None:
            logger.warning("Problem is unbounded")
            return None, float('inf')
        
        # Pivot
        tableau = pivot(tableau, entering_col, leaving_row)
        logger.info(f"Tableau after pivoting:\n{tableau}")
        
        iteration += 1
    
    # Extract solution
    optimal_solution, optimal_objective_value = extract_solution(tableau, num_original_vars, num_constraints, problem_type)
    
    logger.info(f"Optimal solution: {optimal_solution}")
    logger.info(f"Optimal objective value: {optimal_objective_value}")
    
    return optimal_solution, optimal_objective_value

if __name__ == '__main__':
    # Example usage
    objective_coeffs = np.array([3, 5])
    constraint_matrix = np.array([[1, 2], [3, 4]])
    rhs_values = np.array([5, 6])
    senses = ['<=', '<=']
    problem_type = 'max'
    
    optimal_solution, optimal_objective_value = simplex_solver(objective_coeffs, constraint_matrix, rhs_values, senses, problem_type)
    
    if optimal_solution is not None:
        print("Optimal Solution:", optimal_solution)
        print("Optimal Objective Value:", optimal_objective_value)
    else:
        print("Problem is unbounded")
