import numpy as np
from typing import Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

def select_entering_variable(tableau: np.ndarray) -> int:
    """
    Selects the entering variable by choosing the column with the most negative
    coefficient in the objective row (first row).

    Args:
        tableau (np.ndarray): The simplex tableau.

    Returns:
        int: The index of the entering variable (column index).
    """
    logger.debug("Selecting entering variable")
    entering_col_index = np.argmin(tableau[0, :-1])
    logger.debug(f"Entering variable selected: column {entering_col_index}")
    return entering_col_index


def calculate_ratios(tableau: np.ndarray, entering_col_index: int) -> np.ndarray:
    """
    Calculates the ratios for the leaving variable selection.
    Ignores rows where the element in the entering column is zero or negative.

    Args:
        tableau (np.ndarray): The simplex tableau.
        entering_col_index (int): The index of the entering variable (column index).

    Returns:
        np.ndarray: An array of ratios (b_i / a_ij) for each row, or None if the element
        in the entering column is zero or negative.
    """
    logger.debug(f"Calculating ratios for entering column {entering_col_index}")
    ratios = []
    for i in range(1, tableau.shape[0]):
        if tableau[i, entering_col_index] > 0:
            ratio = tableau[i, -1] / tableau[i, entering_col_index]
            ratios.append(ratio)
            logger.debug(f"Ratio for row {i}: {ratio}")
        else:
            ratios.append(np.inf)  # Use np.inf to represent that the ratio is not valid
            logger.debug(f"Ratio for row {i}: infinity (element in entering column <= 0)")
    return np.array(ratios)


def select_leaving_variable(tableau: np.ndarray, entering_col_index: int) -> Optional[int]:
    """
    Selects the leaving variable by choosing the row with the minimum ratio
    (b_i / a_ij) where a_ij is the element in the entering column.

    Args:
        tableau (np.ndarray): The simplex tableau.
        entering_col_index (int): The index of the entering variable (column index).

    Returns:
        Optional[int]: The index of the leaving variable (row index), or None if the problem is unbounded.
    """
    logger.debug("Selecting leaving variable")
    ratios = calculate_ratios(tableau, entering_col_index)
    
    # If all ratios are np.inf, the problem is unbounded
    if np.all(ratios == np.inf):
        logger.warning("Problem is unbounded: all ratios are infinite")
        return None

    # Find the index of the minimum ratio (excluding infinities)
    leaving_row_index = np.argmin(ratios)
    
    # The leaving row index is relative to the ratios array, so add 1 to get the actual row index in the tableau
    leaving_row = leaving_row_index + 1
    
    logger.debug(f"Leaving variable selected: row {leaving_row}")
    return leaving_row


def pivot(tableau: np.ndarray, entering_col_index: int, leaving_row: int) -> np.ndarray:
    """
    Performs the pivot operation on the tableau.

    Args:
        tableau (np.ndarray): The simplex tableau.
        entering_col_index (int): The index of the entering variable (column index).
        leaving_row (int): The index of the leaving variable (row index).

    Returns:
        np.ndarray: The updated tableau after the pivot operation.
    """
    logger.info(f"Performing pivot operation: entering column {entering_col_index}, leaving row {leaving_row}")
    pivot_element = tableau[leaving_row, entering_col_index]
    
    # Divide the leaving row by the pivot element
    tableau[leaving_row, :] /= pivot_element
    logger.debug(f"Leaving row normalized by pivot element")
    
    # Subtract multiples of the leaving row from all other rows to make the
    # entering column zero in those rows
    for i in range(tableau.shape[0]):
        if i != leaving_row:
            factor = tableau[i, entering_col_index]
            tableau[i, :] -= factor * tableau[leaving_row, :]
            logger.debug(f"Row {i} updated to make entering column zero")
            
    logger.info("Pivot operation complete")
    return tableau
