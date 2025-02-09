# Example problems
example_problems = {
    "Example 1: Maximization": {
        "objective_coeffs": [3, 5],
        "constraint_matrix": [[1, 0], [0, 2], [3, 2]],
        "rhs_values": [4, 12, 18],
        "senses": ['<=', '<=', '<='],
        "problem_type": "max"
    },
    "Example 2: Minimization": {
        "objective_coeffs": [2, 3],
        "constraint_matrix": [[1, 1], [2, 1]],
        "rhs_values": [10, 16],
        "senses": ['>=', '='],
        "problem_type": "min"
    },
    "Example 3: Maximization with mixed constraints": {
        "objective_coeffs": [1, 2],
        "constraint_matrix": [[1, 1], [1, 1]],
        "rhs_values": [4, 6],
        "senses": ['<=', '>='],
        "problem_type": "max"
    }
}
