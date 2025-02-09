import numpy as np
from typing import Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

def select_entering_variable(tableau: np.ndarray) -> int:
    logger.debug("Selecting entering variable")
    entering_col_index = np.argmin(tableau[0, :-1])
    logger.debug(f"Entering variable selected: column {entering_col_index}")
    return entering_col_index


def calculate_ratios(tableau: np.ndarray, entering_col_index: int) -> np.ndarray:
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
    logger.info(f"Performing pivot operation: entering column {entering_col_index}, leaving row {leaving_row}")
    pivot_element = tableau[leaving_row, entering_col_index]
    
    # Divide the leaving row by the pivot element
    print(f"\n[Pivot Step] Normalizing pivot row {leaving_row} by dividing by pivot element {pivot_element:.4f}:")
    tableau[leaving_row, :] /= pivot_element
    print(tableau)
    logger.debug(f"Leaving row normalized by pivot element")
    
    # Subtract multiples of the leaving row from all other rows to make the
    # entering column zero in those rows
    for i in range(tableau.shape[0]):
        if i != leaving_row:
            factor = tableau[i, entering_col_index]
            print(f"\n[Pivot Step] Eliminating variable in row {i} using row {leaving_row}, factor = {factor:.4f}:")
            tableau[i, :] -= factor * tableau[leaving_row, :]
            print(tableau)
            logger.debug(f"Row {i} updated to make entering column zero")
            
    logger.info("Pivot operation complete")
    return tableau
