import numpy as np

def is_dual_feasible(tableau):
    # Check if all RHS values (excluding the objective row) are non-negative
    return np.all(tableau[1:, -1] >= 0)

def dual_simplex(objective_coeffs, constraint_matrix, rhs_values, senses, verbose=True):
    # 1. Convert to Standard Form (all constraints as <= for the dual)
    A = np.array(constraint_matrix)
    b = np.array(rhs_values)
    c = np.array(objective_coeffs)

    # 2. Create the Dual Problem
    # Dual objective: maximize b^T y
    dual_objective_coeffs = b
    # Dual constraints: A^T y <= c
    dual_constraint_matrix = A.T
    dual_rhs_values = c
    dual_senses = ['<='] * len(c)  # All dual constraints are <=

    # 3. Solve the Dual using tabular_simplex (which handles maximization)
    status, dual_solution, dual_optimal = tabular_simplex(dual_objective_coeffs, dual_constraint_matrix, dual_rhs_values, dual_senses, problem_type='max', verbose=verbose)

    if status == 'optimal':
        # Strong duality: dual optimal = primal optimal
        primal_optimal = dual_optimal

        # Find primal solution using complementary slackness
        primal_solution = find_primal_solution(dual_solution, constraint_matrix, objective_coeffs)

        return status, primal_solution, primal_optimal # Return primal optimal value
    else:  # Dual is infeasible or unbounded, meaning primal is infeasible or unbounded.
        return status, None, None

def find_primal_solution(dual_solution, constraint_matrix, objective_coeffs):
    """
    Finds the primal solution using complementary slackness.

    Args:
        dual_solution (np.array): Optimal solution of the dual problem.
        constraint_matrix (np.array): Constraint matrix of the primal problem.
        objective_coeffs (np.array): Objective coefficients of the primal problem.

    Returns:
        np.array: Primal solution.
    """
    num_original_vars = len(objective_coeffs)
    num_constraints = constraint_matrix.shape[0]
    primal_solution = np.zeros(num_original_vars)

    # Identify binding constraints in the dual
    binding_constraints_dual = np.where(dual_solution > 1e-6)[0]  # Use a small tolerance

    # Set corresponding primal variables to zero
    non_binding_constraints_dual = np.setdiff1d(np.arange(num_constraints), binding_constraints_dual)
    for i in non_binding_constraints_dual:
        # Find columns in constraint matrix corresponding to non-binding constraints
        # and set corresponding primal variables to zero
        primal_solution[i] = 0

    # For binding constraints, solve a reduced system of equations
    A_reduced = constraint_matrix[binding_constraints_dual, :]
    b_reduced = objective_coeffs[binding_constraints_dual]

    # Check if the reduced system is solvable
    if A_reduced.shape[1] >= A_reduced.shape[0]:
        try:
            # Solve the reduced system using least squares
            primal_solution, _, _, _ = np.linalg.lstsq(A_reduced, b_reduced, rcond=None)
        except np.linalg.LinAlgError:
            print("Singular matrix encountered. Cannot solve for primal variables.")
            return None
    else:
        print("Underdetermined system. Cannot uniquely solve for primal variables.")
        return None

    return primal_solution

def select_leaving_variable_dual(tableau):
    rhs = tableau[1:, -1]
    leaving_row = np.argmin(rhs) + 1  # +1 to offset the objective row
    if rhs[leaving_row -1] >= 0: # Check if the most negative RHS is non-negative. If so, the solution is dual feasible.
        return None
    return leaving_row

def select_entering_variable_dual(tableau, leaving_row):
    ratios = []
    for j in range(tableau.shape[1] - 1):
        if tableau[leaving_row, j] < 0:
            ratios.append(tableau[0, j] / abs(tableau[leaving_row, j]))
        else:
            ratios.append(np.inf)

    if np.all(np.isinf(ratios)):  # Check if all ratios are infinite
        return None
    return np.argmin(ratios)

def print_tableau(tableau, iteration=None):
    if iteration is not None:
        print(f"\n--- Iteration {iteration} ---")
    print("Current Tableau:")
    # Print a rounded copy of the tableau for easier reading
    print(np.array_str(tableau, precision=3, suppress_small=True))
    print("-" * 50)

def solve_dual_problem(objective_coeffs, constraint_matrix, rhs_values, senses, verbose=True):
    # Transform primal constraints
    tcm, trhs = transform_constraints(constraint_matrix, rhs_values, senses)
    # For a primal minimization problem:
    # Dual objective: maximize b^T y, so use transformed RHS as dual objective coefficients.
    dual_objective_coeffs = trhs.copy()
    # Dual constraints: A^T y <= c, where c is the original objective coefficients.
    dual_constraint_matrix = tcm.T
    dual_rhs_values = objective_coeffs.copy()
    dual_senses = ['<='] * len(objective_coeffs)  # assume all dual variables are nonnegative
    
    if verbose:
        print("Constructed dual problem from primal minimization problem.")
    # Solve the dual as a maximization problem using tabular_simplex.
    status, dual_solution, dual_optimal = tabular_simplex(dual_objective_coeffs, dual_constraint_matrix, dual_rhs_values, dual_senses, problem_type='max', verbose=verbose)
    if verbose and status == 'optimal':
        print("Dual problem solved optimally.")
        print("Dual solution:", np.round(dual_solution, 3))
        print("Dual optimal objective value:", round(dual_optimal, 3))
    # Under strong duality, the dual optimal value equals the primal optimal value.
    return status, dual_solution, dual_optimal

# Modify tabular_simplex to use the dual formulation for minimization problems.
def tabular_simplex(objective_coeffs, constraint_matrix, rhs_values, senses, problem_type='max', verbose=True):
    num_constraints, num_original_vars = constraint_matrix.shape

    # Transform constraints if needed
    transformed_constraint_matrix, transformed_rhs_values = transform_constraints(constraint_matrix, rhs_values, senses)
    tableau = setup_tableau(objective_coeffs, transformed_constraint_matrix, transformed_rhs_values, senses, problem_type)

    if verbose:
        print("\nInitial Tableau:")
        print_tableau(tableau)
        print("Explanation: We reach the solution when all coefficients in the objective row (first row) "
              "are nonnegative. This means that no further improvements can be achieved.")

    # If it's a minimization problem, create and solve the dual problem.
    if problem_type == 'min':
        if verbose:
            print("Converting minimization problem to its dual formulation for solution.")
        return solve_dual_problem(objective_coeffs, constraint_matrix, rhs_values, senses, verbose)

    # Initial infeasibility check (e.g., checking artificial variables)
    status = check_infeasibility(tableau, num_original_vars, senses, num_constraints)
    if status == 'infeasible':
        if verbose:
            print("The problem is infeasible at the initial tableau.")
        return status, None, None

    iteration = 0
    while True:
        iteration += 1

        if verbose:
            print_tableau(tableau, iteration)
        
        # Check the optimality condition: If all coefficients in the objective row (except RHS) are nonnegative,
        # then the current solution is optimal.
        if np.all(tableau[0, :-1] >= 0):
            if verbose:
                print("All coefficients in the objective row are now nonnegative.")
                print("Explanation: No further improvement is possible so the current solution is optimal.")
            optimal_solution, optimal_objective_value = extract_solution(tableau, num_original_vars, num_constraints, problem_type)
            if np.any(np.dot(transformed_constraint_matrix, optimal_solution) > transformed_rhs_values + 1e-6):
                if verbose:
                    print("After checking, there is a violation in the constraints (infeasible basic variable)!")
                return 'infeasible', None, None
            if verbose:
                print("Optimal solution reached!")
                print("Solution:", np.round(optimal_solution, 3))
                print("Objective value:", round(optimal_objective_value, 3))
            return 'optimal', optimal_solution, optimal_objective_value

        # Select entering variable: the variable with the most negative coefficient in the objective row.
        entering_col_index = select_entering_variable(tableau)
        if verbose:
            print(f"Entering variable (most negative coefficient) is at column index: {entering_col_index}")
            print(f"Coefficient value for entering variable: {tableau[0, entering_col_index]:.3f}")

        # Calculate ratios to determine the leaving variable.
        ratios = calculate_ratios(tableau, entering_col_index)
        if verbose:
            print("Calculating ratios for the pivot operation (RHS divided by pivot column coefficient):")
            for idx, ratio in enumerate(ratios, start=1):
                if tableau[idx, entering_col_index] > 0:
                    print(f"Row {idx}: RHS = {tableau[idx, -1]:.3f}, Coefficient = {tableau[idx, entering_col_index]:.3f}, Ratio = {tableau[idx, -1]:.3f} / {tableau[idx, entering_col_index]:.3f} = {ratio:.3f}")
                else:
                    print(f"Row {idx}: Coefficient = {tableau[idx, entering_col_index]:.3f} (Not eligible for pivot, ratio = inf)")
                    
        # Select leaving variable based on the minimum ratio rule.
        leaving_row = select_leaving_variable(tableau, entering_col_index)
        if leaving_row is None:
            if verbose:
                print("No valid leaving variable found (all ratios are infinite). The problem is unbounded!")
            return 'unbounded', None, None

        if verbose:
            print(f"Leaving variable (minimum ratio) is at row index: {leaving_row}")

        # Perform the pivot operation.
        tableau = pivot(tableau, entering_col_index, leaving_row)
        if verbose:
            print("After pivot operation, the tableau is updated as follows:")
            print_tableau(tableau, iteration)

def check_infeasibility(tableau, num_original_vars, senses, num_constraints):
    # This check looks for artificial basic variables with nonzero values.
    num_slack_vars = senses.count('<=')
    artificial_vars_start = num_original_vars + num_slack_vars

    for i in range(num_constraints):
        basic_variable_cols = np.where(tableau[i+1, :num_original_vars + num_slack_vars + num_constraints] == 1)[0]
        if len(basic_variable_cols) > 0:
            basic_var = basic_variable_cols[0]
            if basic_var >= artificial_vars_start and tableau[i+1, -1] != 0:
                return 'infeasible'
    return None

def select_entering_variable(tableau):
    # Identify the most negative coefficient in the objective row (excluding the RHS).
    return np.argmin(tableau[0, :-1])

def calculate_ratios(tableau, entering_col_index):
    ratios = []
    # Compute ratios for each constraint (row 1 and onward)
    for i in range(1, tableau.shape[0]):
        if tableau[i, entering_col_index] > 0:
            ratios.append(tableau[i, -1] / tableau[i, entering_col_index])
        else:
            ratios.append(np.inf)
    return np.array(ratios)

def select_leaving_variable(tableau, entering_col_index):
    ratios = calculate_ratios(tableau, entering_col_index)
    if np.all(ratios == np.inf):
        return None
    # Add one because the first row is the objective function
    return np.argmin(ratios) + 1

def pivot(tableau, entering_col_index, leaving_row):
    print("The pivot element is the element at the intersection of the leaving row and the entering column.")
    pivot_element = tableau[leaving_row, entering_col_index]
    print(f"Pivot Element: Tableau[{leaving_row}, {entering_col_index}] = {pivot_element:.3f}")

    print(f"Dividing row {leaving_row} by pivot element {pivot_element:.3f}")
    tableau[leaving_row, :] = tableau[leaving_row, :] / pivot_element

    print("Updated Tableau after dividing leaving row:")
    print(np.array_str(tableau, precision=3, suppress_small=True))


    for i in range(tableau.shape[0]):
        if i != leaving_row:
            factor = tableau[i, entering_col_index]
            print(f"Eliminating variable in row {i} using factor {factor:.3f}")
            tableau[i, :] -= factor * tableau[leaving_row, :]
            print(f"Updated Tableau after eliminating row {i}:")
            print(np.array_str(tableau, precision=3, suppress_small=True))

    return tableau

def setup_tableau(objective_coeffs, constraint_matrix, rhs_values, senses, problem_type='max'):
    num_constraints, num_original_vars = constraint_matrix.shape

    if problem_type == 'min':
        # Convert minimization to maximization by negating the objective coefficients.
        objective_coeffs = -objective_coeffs

    num_slack_vars = senses.count('<=')
    num_surplus_vars = senses.count('>=')
    num_artificial_vars = senses.count('=') + num_surplus_vars
    num_total_vars = num_original_vars + num_slack_vars + num_artificial_vars

    tableau = np.zeros((num_constraints + 1, num_total_vars + 1))
    tableau[0, :num_original_vars] = -objective_coeffs  # Negate objective coefficients here

    slack_surplus_index = num_original_vars
    artificial_index = num_original_vars + num_slack_vars + num_surplus_vars
    for i in range(num_constraints):
        tableau[i + 1, :num_original_vars] = constraint_matrix[i, :]
        tableau[i + 1, -1] = rhs_values[i]

        if senses[i] == '<=':
            tableau[i + 1, slack_surplus_index] = 1
            slack_surplus_index += 1
        elif senses[i] == '>=' or senses[i] == '=':
            # For '>=' or '=' constraints, add an artificial variable to help find a basic feasible solution.
            tableau[i + 1, artificial_index - num_surplus_vars] = 1
            artificial_index += 1
            if senses[i] == '>=':
                # Also add a surplus variable (which will have a negative sign)
                tableau[i + 1, slack_surplus_index] = -1
                slack_surplus_index += 1
    return tableau

def extract_solution(tableau, num_original_vars, num_constraints, problem_type='max'):
    optimal_solution = np.zeros(num_original_vars)
    # Look through each original variable column to see if it's a basic variable.
    for i in range(num_original_vars):
        column = tableau[:, i]
        if np.sum(np.abs(column)) == 1 and np.count_nonzero(column == 1) == 1:
            basic_variable_row = np.where(column == 1)[0][0]
            optimal_solution[i] = tableau[basic_variable_row, -1]

    optimal_objective_value = tableau[0, -1]
    if problem_type == 'min':
        optimal_objective_value = -optimal_objective_value
    return optimal_solution, optimal_objective_value

def transform_constraints(constraint_matrix, rhs_values, senses):
    transformed_constraint_matrix = constraint_matrix.copy()
    transformed_rhs_values = rhs_values.copy()
    for i, sense in enumerate(senses):
        if sense == '>=':
            # Multiply the constraint by -1 to convert '>=' into '<='.
            transformed_constraint_matrix[i, :] = -constraint_matrix[i, :]
            transformed_rhs_values[i] = -rhs_values[i]
    return transformed_constraint_matrix, transformed_rhs_values
