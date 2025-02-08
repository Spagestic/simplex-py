import numpy as np

def extract_solution(tableau, n, m, prob_type='max'):
    """
    Extracts the solution from the final tableau.

    Args:
        tableau: The final simplex tableau (numpy array).
        n: The number of original variables.
        m: The number of constraints.
        prob_type: 'max' for maximization, 'min' for minimization.

    Returns:
        A tuple containing:
            - x: The optimal solution (numpy array).
            - z: The optimal objective value.
    """
    x = np.zeros(n)
    
    # Iterate through each of the original variables
    for i in range(n):
        # Check if the column corresponds to a basic variable (i.e., it has a 1 and the rest are 0)
        col = tableau[:, i]
        
        # Check if the column is a unit vector
        if np.sum(np.abs(col)) == 1 and np.sum(col == np.abs(col)) == 1:
            # If it is a unit vector, find the row where the 1 is located
            basic_var_row = np.where(col == 1)[0][0]
            
            # The value of the basic variable is the value in the right-hand side of the tableau
            x[i] = tableau[basic_var_row, -1]
            
    # Extract the optimal objective value from the tableau
    z = tableau[0, -1]
    
    # If the problem was a minimization problem, negate the objective value
    if prob_type == 'min':
        z = -z
        
    return x, z
