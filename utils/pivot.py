import numpy as np

def select_entering_variable(tableau):
    """
    Selects the entering variable by choosing the column with the most negative
    coefficient in the objective row (first row).

    Args:
        tableau: The simplex tableau (numpy array).

    Returns:
        The index of the entering variable (column index).
    """
    return np.argmin(tableau[0, :-1])


def calculate_ratios(tableau, entering_col):
     """
     Calculates the ratios for the leaving variable selection.
     Ignores rows where the element in the entering column is zero or negative.

     Args:
          tableau: The simplex tableau (numpy array).
          entering_col: The index of the entering variable (column index).

     Returns:
          An array of ratios (b_i / a_ij) for each row, or None if the element
          in the entering column is zero or negative.
     """
     ratios = []
     for i in range(1, tableau.shape[0]):
          if tableau[i, entering_col] > 0:
               ratios.append(tableau[i, -1] / tableau[i, entering_col])
          else:
               ratios.append(np.inf)  # Use np.inf to represent that the ratio is not valid
     return np.array(ratios)


def select_leaving_variable(tableau, entering_col):
    """
    Selects the leaving variable by choosing the row with the minimum ratio
    (b_i / a_ij) where a_ij is the element in the entering column.

    Args:
        tableau: The simplex tableau (numpy array).
        entering_col: The index of the entering variable (column index).

    Returns:
        The index of the leaving variable (row index), or None if the problem is unbounded.
    """
    ratios = calculate_ratios(tableau, entering_col)
    
    # If all ratios are np.inf, the problem is unbounded
    if np.all(ratios == np.inf):
        return None

    # Find the index of the minimum ratio (excluding infinities)
    leaving_row_index = np.argmin(ratios)
    
    # The leaving row index is relative to the ratios array, so add 1 to get the actual row index in the tableau
    leaving_row = leaving_row_index + 1
    
    return leaving_row


def pivot(tableau, entering_col, leaving_row):
    """
    Performs the pivot operation on the tableau.

    Args:
        tableau: The simplex tableau (numpy array).
        entering_col: The index of the entering variable (column index).
        leaving_row: The index of the leaving variable (row index).

    Returns:
        The updated tableau after the pivot operation.
    """
    pivot_element = tableau[leaving_row, entering_col]
    
    # Divide the leaving row by the pivot element
    tableau[leaving_row, :] /= pivot_element
    
    # Subtract multiples of the leaving row from all other rows to make the
    # entering column zero in those rows
    for i in range(tableau.shape[0]):
        if i != leaving_row:
            factor = tableau[i, entering_col]
            tableau[i, :] -= factor * tableau[leaving_row, :]
            
    return tableau
