import numpy as np
from .format_term import format_term

def problem_latex(objective_coeffs, constraint_matrix, rhs_values, senses):
    """
    Formats the problem as a LaTeX string.

    Args:
        objective_coeffs (np.array): The coefficients of the objective function.
        constraint_matrix (np.array): The matrix of constraint coefficients.
        rhs_values (np.array): The right-hand side values of the constraints.
        senses (list): The senses of the constraints ("<=", ">=", "=").

    Returns:
        str: A LaTeX string representing the problem.
    """
    # Begin LaTeX string
    latex_str = r"\begin{array}{rl}" + "\n"
    
    # Objective function
    objective_terms = [format_term(c, i) for i, c in enumerate(objective_coeffs)]
    objective_str = " ".join(term for term in objective_terms if term)
    if objective_str.startswith("+"):
        objective_str = objective_str[1:]  # Remove leading "+" sign
    latex_str += r"    \text{max} & " + objective_str + r" \\" + "\n"
    
    # Constraints
    latex_str += r"    \text{s.t.} & \begin{aligned}" + "\n"
    for i in range(len(constraint_matrix)):
        constraint_terms = [format_term(a, j) for j, a in enumerate(constraint_matrix[i])]
        constraint_str = " ".join(term for term in constraint_terms if term)
        if constraint_str.startswith("+"):
            constraint_str = constraint_str[1:]
        
        latex_str += constraint_str + f" {senses[i]} {rhs_values[i]:.2f}"

        
        if i < len(constraint_matrix) - 1:
            latex_str += r" \\" + "\n"
        else:
            latex_str += r" \\" + "\n"
    latex_str += r"\end{aligned}" + r" \\" + "\n"
    
    # Non-negativity constraints
    non_negativity_str = r"    & 0 \leq " + ", \quad 0 \leq ".join([f"x_{i+1}" for i in range(len(objective_coeffs))]) + "."
    latex_str += non_negativity_str + "\n"
    
    # End LaTeX string
    latex_str += r"\end{array}"
    
    return latex_str
