import numpy as np
import logging

# Set up logging
logger = logging.getLogger(__name__)

def check_infeasibility(tableau: np.ndarray, num_original_vars: int, senses: list[str], num_constraints: int) -> str | None:
    logger.info("Checking for infeasibility")
    
    num_slack_vars = senses.count('<=')
    artificial_vars_start = num_original_vars + num_slack_vars
    
    for i in range(num_constraints):
        basic_variable_col = np.where(tableau[i+1, :num_original_vars + num_slack_vars + num_constraints] == 1)[0]
        if len(basic_variable_col) > 0:
            basic_variable_col = basic_variable_col[0]
            if basic_variable_col >= artificial_vars_start:
                if tableau[i+1, -1] != 0:  # Check if the artificial variable has a non-zero value
                    status = 'infeasible'
                    print("\nProblem is infeasible!")
                    logger.warning("Problem is infeasible: artificial variable in basis with non-zero value")
                    return status
    
    logger.info("Problem is feasible")
    return None
