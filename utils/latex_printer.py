import numpy as np

def print_latex_problem(c, A, b, senses, prob_type='max'):
    """
    Prints the linear programming problem in LaTeX format.

    Args:
        c: Objective function coefficients (numpy array).
        A: Constraint coefficient matrix (numpy array).
        b: Right-hand side values (numpy array).
        senses: List of strings for each constraint ('<=', '>=', '=').
        prob_type: 'max' for maximization, 'min' for minimization.
    """
    n = len(c)  # Number of variables

    # Objective function
    if prob_type == 'max':
        print(r'\begin{align*}')
        print(r'\max \quad &', end='')
    elif prob_type == 'min':
        print(r'\begin{align*}')
        print(r'\min \quad &', end='')
    
    obj_str = ' + '.join([f'{c[i]}x_{i+1}' for i in range(n)])
    print(obj_str, r'\\')

    # Constraints
    print(r'\text{subject to} \quad &')
    for i in range(A.shape[0]):
        constraint_str = ' + '.join([f'{A[i, j]}x_{j+1}' for j in range(n)])
        if senses[i] == '<=':
            sense_str = r'\leq'
        elif senses[i] == '>=':
            sense_str = r'\geq'
        elif senses[i] == '=':
            sense_str = '='
        print(constraint_str, sense_str, b[i], r'\\')

    # Non-negativity constraints
    non_neg_str = ', '.join([f'x_{i+1}' for i in range(n)])
    print(non_neg_str, r'\geq 0')
    print(r'\end{align*}')
