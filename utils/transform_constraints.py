import numpy as np
from typing import List, Tuple
import logging

# Set up logging
logger = logging.getLogger(__name__)

def transform_constraints(
    constraint_matrix: np.ndarray,
    rhs_values: np.ndarray,
    senses: List[str]
) -> Tuple[np.ndarray, np.ndarray]:
    logger.info("Transforming constraints to standard form (<=)")
    
    transformed_constraint_matrix = constraint_matrix.copy()
    transformed_rhs_values = rhs_values.copy()
    
    for i, sense in enumerate(senses):
        if sense == '>=':
            logger.debug(f"Transforming constraint {i} from '>=' to '<='")
            transformed_constraint_matrix[i, :] = -constraint_matrix[i, :]
            transformed_rhs_values[i] = -rhs_values[i]
            senses[i] = '<='  # Update sense to '<='
            logger.debug(f"Constraint {i} transformed")
            
    logger.info("Constraints transformed successfully")
    return transformed_constraint_matrix, transformed_rhs_values
