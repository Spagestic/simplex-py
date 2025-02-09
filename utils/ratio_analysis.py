import numpy as np
import logging

# Set up logging
logger = logging.getLogger(__name__)

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
