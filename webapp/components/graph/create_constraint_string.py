def create_constraint_string(constraint_x, constraint_y, rhs_value, sense):
    """
    Constructs a constraint string for display purposes.
    """
    constraint_str = ""
    if constraint_x != 0:
        if constraint_x == 1:
            constraint_str += "x"
        elif constraint_x == -1:
            constraint_str += "-x"
        else:
            constraint_str += f"{constraint_x}x"
    if constraint_y != 0:
        if constraint_str != "":
            constraint_str += " + " if constraint_y > 0 else " - "
            if abs(constraint_y) != 1:
                constraint_str += f"{abs(constraint_y)}"
        constraint_str += "y"

    if constraint_str == "":
        constraint_str = "0"

    if sense == '<=':
        constraint_str += " ≤ " + str(rhs_value)
    elif sense == '>=':
        constraint_str += " ≥ " + str(rhs_value)
    else:
        constraint_str += " = " + str(rhs_value)
    
    return constraint_str
