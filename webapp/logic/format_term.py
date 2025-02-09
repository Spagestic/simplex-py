def format_term(coeff, index):
    """Format a term in the objective function or constraint."""
    if coeff == 0:
        return ""
    term = ""
    if coeff > 0:
        term += "+ "
    else:
        term += "- "
        coeff = abs(coeff)  # Use absolute value for negative coefficients
    if coeff != 1:
        term += f"{coeff}"
    term += f"x_{index+1}"
    return term
