import numpy as np
from utils.setup_tableau import setup_tableau
from utils.transform_constraints import transform_constraints
from utils.pivot import select_entering_variable, select_leaving_variable, pivot
from utils.solution_extraction import extract_solution
from utils.latex_printer import print_latex_problem


def tabular_simplex(c, A, b, senses, prob_type='max'):
    """
    Solves a linear programming problem using the tabular simplex method,
    printing the major steps for educational purposes. This version allows
    different types of constraints.

    Args:
        c: Objective function coefficients (numpy array). For maximization, these are 
           the coefficients in the form z = c1*x1 + c2*x2 + ... + cn*xn. For minimization, the
           coefficients are negated at the beginning.
        A: Constraint coefficient matrix (numpy array), where each row is a constraint.
        b: Right-hand side values (numpy array).
        senses: List of strings for each constraint where each entry is one of:
                '<=' : less-than-or-equal-to constraint,
                '>=' : greater-than-or-equal-to constraint (will be converted to <=),
                 '=' : equality constraint.
        prob_type: 'max' for maximization, 'min' for minimization.

    Returns:
        A tuple containing:
            - status: 'optimal', 'unbounded', or 'infeasible'
            - x: The optimal solution (numpy array) or None if the problem is unbounded/infeasible.
            - z: The optimal objective value or None if the problem is unbounded/infeasible.
    """
    m, n = A.shape  # m = number of constraints, n = number of variables

    # Print the problem in LaTeX format
    print("\nProblem in LaTeX format:")
    print_latex_problem(c, A, b, senses, prob_type)

    # Transform constraints with '>=' to '<=' by multiplying the row and b by -1.
    A_trans, b_trans = transform_constraints(A, b, senses)
    
    # Set up the tableau
    tableau = setup_tableau(c, A_trans, b_trans, senses, prob_type)
    
    print("\nInitial Problem Setup:")
    print(f"Number of constraints (m): {m}")
    print(f"Number of variables (n): {n}")
    print(f"Objective function coefficients (c): {c}")
    
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
            x, z = extract_solution(tableau, n, m, prob_type)
            print("\nOptimal solution found!")
            return status, x, z

        # Select entering variable: choose most negative coefficient in objective row.
        entering_col = select_entering_variable(tableau)
        print(f"\nSelecting entering variable:")
        print(f"Most negative coefficient in objective row: {tableau[0, entering_col]:.4f}")
        print(f"Entering variable: x_{entering_col+1}")

        # Leaving variable selection: compute ratios.
        leaving_row = select_leaving_variable(tableau, entering_col)
        
        # Check for unboundedness.
        if leaving_row is None:
            status = 'unbounded'
            print("\nProblem is unbounded!")
            return status, None, None
        
        print(f"\nLeaving variable: row {leaving_row}")
        print(f"Pivot element: {tableau[leaving_row, entering_col]:.4f}")

        # Pivot operation.
        tableau = pivot(tableau, entering_col, leaving_row)