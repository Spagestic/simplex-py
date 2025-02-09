import numpy as np
from utils.setup_tableau import setup_tableau
from utils.transform_constraints import transform_constraints
from utils.pivot import select_entering_variable, select_leaving_variable, pivot
from utils.solution_extraction import extract_solution
from utils.latex_printer import print_latex_problem
from utils.infeasibility_check import check_infeasibility
from utils.input_validation import validate_inputs
import logging
from utils.ratio_analysis import calculate_ratios  # Import the calculate_ratios function

# Set up logging
logger = logging.getLogger(__name__)

def tabular_simplex(
    objective_coeffs: np.ndarray,
    constraint_matrix: np.ndarray,
    rhs_values: np.ndarray,
    senses: list[str],
    problem_type: str = 'max'
) -> tuple[str, np.ndarray | None, float | None, list[np.ndarray]]:
    logger.info("Starting tabular simplex method")
    
    tableau_history = []  # Initialize list to store tableau history
    
    try:
        # Validate inputs to ensure the data is suitable for the simplex method
        validate_inputs(objective_coeffs, constraint_matrix, rhs_values, senses, problem_type)
        logger.debug("Inputs validated successfully")
        
        num_constraints, num_original_vars = constraint_matrix.shape
        logger.debug(f"Number of constraints: {num_constraints}")
        logger.debug(f"Number of original variables: {num_original_vars}")

        # Print the problem in LaTeX format for better readability and educational purposes
        print("\nProblem in LaTeX format:")
        print_latex_problem(objective_coeffs, constraint_matrix, rhs_values, senses, problem_type)

        # Transform constraints with '>=' to '<=' by multiplying the row and rhs_values by -1.
        transformed_constraint_matrix, transformed_rhs_values = transform_constraints(constraint_matrix, rhs_values, senses)
        logger.debug("Constraints transformed successfully")
        
        # Set up the initial tableau for the simplex method
        tableau = setup_tableau(objective_coeffs, transformed_constraint_matrix, transformed_rhs_values, senses, problem_type)
        logger.debug("Tableau setup complete")
        
        print("\nInitial Problem Setup:")
        print(f"Number of constraints (m): {num_constraints}")
        print(f"Number of variables (n): {num_original_vars}")
        print(f"Objective function coefficients (c): {objective_coeffs}")
        
        # Check for infeasibility: look for artificial variables in the basis with non-zero values
        status = check_infeasibility(tableau, num_original_vars, senses, num_constraints)
        if status == 'infeasible':
            return status, None, None, tableau_history
        
        iteration = 0
        while True:
            iteration += 1
            print(f"\n{'='*50}")
            print(f"Iteration {iteration}:")
            print("Current tableau:")
            print(tableau)
            
            # Display detailed current information
            print("\n[Step] Displaying current basic variables and RHS values:")
            for i in range(1, tableau.shape[0]):
                print(f"Row {i} (Basis): {tableau[i, :-1]} | RHS: {tableau[i, -1]}")
            
            # Store the current tableau in the history
            tableau_history.append(tableau.copy())

            # Check for optimality
            if np.all(tableau[0, :-1] >= 0):
                status = 'optimal'
                optimal_solution, optimal_objective_value = extract_solution(tableau, num_original_vars, num_constraints, problem_type)
                tol = 1e-6
                if np.any(np.dot(transformed_constraint_matrix, optimal_solution) > transformed_rhs_values + tol):
                    print("\nProblem is infeasible!")
                    logger.warning("Optimal solution violates at least one constraint")
                    return 'infeasible', None, None, tableau_history
                print("\nOptimal solution found!")
                logger.info(f"Optimal solution found: {optimal_solution}, Objective value: {optimal_objective_value}")
                return status, optimal_solution, optimal_objective_value, tableau_history

            # Display detailed optimality test status
            print("\n[Step] Checking objective row for negative coefficients:")
            print(tableau[0, :-1])
            
            # Select entering variable
            entering_col_index = select_entering_variable(tableau)
            print(f"\nEntering variable chosen: x_{entering_col_index+1} with coefficient {tableau[0, entering_col_index]:.4f}")
            logger.debug(f"Selected entering variable: column {entering_col_index}")

            # Compute and display ratios with detailed explanation
            ratios = calculate_ratios(tableau, entering_col_index)
            print("\n[Step] Computing ratios for leaving variable:")
            for i, ratio in enumerate(ratios[1:], start=1):
                print(f"Row {i} ratio: {ratio}")
            leaving_row = select_leaving_variable(tableau, entering_col_index)

            if leaving_row is None:
                status = 'unbounded'
                print("\nProblem is unbounded!")
                logger.warning("Problem is unbounded")
                return status, None, None, tableau_history
            
            print(f"\nLeaving variable chosen: row {leaving_row} with pivot element {tableau[leaving_row, entering_col_index]:.4f}")
            logger.debug("About to perform pivot operation")
            
            # Perform pivot and display normalized pivot row
            tableau = pivot(tableau, entering_col_index, leaving_row)
            print("\n[Step] After pivot operation, new tableau:")
            print(tableau)
            print("\n[Step] Normalized pivot row details:")
            print(tableau[leaving_row, :])
            
    except ValueError as e:
        logger.error(f"ValueError: {e}")
        return 'infeasible', None, None, tableau_history
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return 'infeasible', None, None, tableau_history