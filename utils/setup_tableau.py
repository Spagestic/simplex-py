import numpy as np

def setup_tableau(c, A, b, senses, prob_type='max'):
    """
    Sets up the initial tableau for the simplex method.

    Args:
        c: Objective function coefficients (numpy array).
        A: Constraint coefficient matrix (numpy array).
        b: Right-hand side values (numpy array).
        senses: List of strings for each constraint ('<=', '>=', '=').
        prob_type: 'max' for maximization, 'min' for minimization.

    Returns:
        The initial tableau as a numpy array.
    """
    m, n = A.shape  # m = number of constraints, n = number of variables

    # If minimization, negate the objective function coefficients
    if prob_type == 'min':
        c = -c

    # Create an augmented matrix [A | I] where I is an identity matrix
    num_slack_vars = senses.count('<=')
    num_surplus_vars = senses.count('>=')
    num_artificial_vars = senses.count('=') + num_surplus_vars

    num_total_vars = n + num_slack_vars + num_artificial_vars

    tableau = np.zeros((m + 1, num_total_vars + 1))

    # Objective function row
    tableau[0, :n] = c
    tableau[0, -1] = 0  # Objective value

    # Constraint rows
    slack_surplus_index = n
    artificial_index = n + num_slack_vars
    for i in range(m):
        tableau[i + 1, :n] = A[i, :]
        tableau[i + 1, -1] = b[i]

        if senses[i] == '<=':
            tableau[i + 1, slack_surplus_index] = 1
            slack_surplus_index += 1
        elif senses[i] == '>=' or senses[i] == '=':
            tableau[i + 1, artificial_index] = 1
            artificial_index += 1
            if senses[i] == '>=':
                tableau[i + 1, slack_surplus_index] = -1
                slack_surplus_index += 1
    return tableau
