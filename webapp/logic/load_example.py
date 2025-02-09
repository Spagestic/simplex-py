def load_example(example_name, example_problems):
    if example_name != "None":
        example = example_problems[example_name]
        objective_coeffs = example["objective_coeffs"]
        constraint_matrix = example["constraint_matrix"]
        rhs_values = example["rhs_values"]
        senses = example["senses"]
        problem_type = example["problem_type"]
        return objective_coeffs, constraint_matrix, rhs_values, senses, problem_type
    else:
        return None, None, None, None, "max"
