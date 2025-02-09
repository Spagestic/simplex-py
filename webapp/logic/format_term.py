def format_term(coefficient, index, is_integer=False):
    """
    Formats a single term in the linear programming problem.

    Args:
        coefficient (float): The coefficient of the term.
        index (int): The index of the variable (starting from 0).
        is_integer (bool): True if the coefficient is an integer, False otherwise.

    Returns:
        str: The formatted term as a string.
    """
    if coefficient == 0:
        return ""

    if is_integer:
        coeff_str = str(int(coefficient))
    else:
        coeff_str = f"{coefficient:.2f}"

    if coefficient > 0:
        sign = "+"
    else:
        sign = "-"
        coeff_str = coeff_str[1:]  # Remove the negative sign

    if coeff_str == "1":
        term = f"{sign} x_{index + 1}"
    else:
        term = f"{sign} {coeff_str}x_{index + 1}"

    return term
