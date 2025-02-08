import numpy as np
from utils.setup_tableau import setup_tableau
from utils.transform_constraints import transform_constraints
from utils.pivot import select_entering_variable, select_leaving_variable, pivot
from utils.solution_extraction import extract_solution
from utils.latex_printer import print_latex_problem
from utils.input_validation import validate_inputs
import logging

# Set up logging
logger = logging.getLogger(__name__)

def tabular_simplex(
    objective_coeffs: np.ndarray,
    constraint_matrix: np.ndarray,
    rhs_values: np.ndarray,
    senses: list[str],
    problem_type: str = 'max'
) -> tuple[str, np.ndarray | None, float | None]:
    """
    Solves a linear programming problem using the tabular simplex method,
    printing the major steps for educational purposes. This version allows
    different types of constraints.

    Args:
        objective_coeffs (np.ndarray): Objective function coefficients. For maximization, these are 
           the coefficients in the form z = c1*x1 + c2*x2 + ... + cn*xn. For minimization, the
           coefficients are negated at the beginning.
        constraint_matrix (np.ndarray): Constraint coefficient matrix, where each row is a constraint.
        rhs_values (np.ndarray): Right-hand side values.
        senses (list[str]): List of strings for each constraint where each entry is one of:
                '<=' : less-than-or-equal-to constraint,
                '>=' : greater-than-or-equal-to constraint (will be converted to <=),
                 '=' : equality constraint.
        problem_type (str): 'max' for maximization, 'min' for minimization.

    Returns:
        tuple[str, np.ndarray | None, float | None]: A tuple containing:
            - status: 'optimal', 'unbounded', or 'infeasible'
            - x: The optimal solution (numpy array) or None if the problem is unbounded/infeasible.
            - z: The optimal objective value or None if the problem is unbounded/infeasible.
    """
    logger.info("Starting tabular simplex method")
    
    try:
        # Validate inputs
        validate_inputs(objective_coeffs, constraint_matrix, rhs_values, senses, problem_type)
        logger.debug("Inputs validated successfully")
        
        num_constraints, num_original_vars = constraint_matrix.shape
        logger.debug(f"Number of constraints: {num_constraints}")
        logger.debug(f"Number of original variables: {num_original_vars}")

        # Print the problem in LaTeX format
        print("\nProblem in LaTeX format:")
        print_latex_problem(objective_coeffs, constraint_matrix, rhs_values, senses, problem_type)

        # Transform constraints with '>=' to '<=' by multiplying the row and rhs_values by -1.
        transformed_constraint_matrix, transformed_rhs_values = transform_constraints(constraint_matrix, rhs_values, senses)
        logger.debug("Constraints transformed successfully")
        
        # Set up the tableau
        tableau = setup_tableau(objective_coeffs, transformed_constraint_matrix, transformed_rhs_values, senses, problem_type)
        logger.debug("Tableau setup complete")
        
        print("\nInitial Problem Setup:")
        print(f"Number of constraints (m): {num_constraints}")
        print(f"Number of variables (n): {num_original_vars}")
        print(f"Objective function coefficients (c): {objective_coeffs}")
        
        iteration = 0
        while True:
            iteration += 1
            print(f"\n{'='*50}")
            print(f"Iteration {iteration}:")
            print("Current tableau:")
            print(tableau)

            # Optimality test: if all coefficients (except RHS) are non-negative.
            if np.all(tableau[0, :-1] >= 0):
                status = 'optimal'
                optimal_solution, optimal_objective_value = extract_solution(tableau, num_original_vars, num_constraints, problem_type)
                print("\nOptimal solution found!")
                logger.info(f"Optimal solution found: {optimal_solution}, Objective value: {optimal_objective_value}")
                return status, optimal_solution, optimal_objective_value

            # Select entering variable: choose most negative coefficient in objective row.
            entering_col_index = select_entering_variable(tableau)
            print(f"\nSelecting entering variable:")
            print(f"Most negative coefficient in objective row: {tableau[0, entering_col_index]:.4f}")
            print(f"Entering variable: x_{entering_col_index+1}")

            # Leaving variable selection: compute ratios.
            leaving_row = select_leaving_variable(tableau, entering_col_index)
            
            # Check for unboundedness.
            if leaving_row is None:
                status = 'unbounded'
                print("\nProblem is unbounded!")
                logger.warning("Problem is unbounded")
                return status, None, None
            
            print(f"\nLeaving variable: row {leaving_row}")
            print(f"Pivot element: {tableau[leaving_row, entering_col_index]:.4f}")

            # Pivot operation.
            tableau = pivot(tableau, entering_col_index, leaving_row)
            logger.debug(f"Tableau after pivot:\n{tableau}")

    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return 'infeasible', None, None
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return 'infeasible', None, None