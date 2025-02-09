def format_term(coefficient, index, is_integer=False):
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
