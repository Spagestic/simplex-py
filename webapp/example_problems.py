example_problems = {
    "Example 1: Maximization": {
        "objective_coeffs": [3, 5],
        "constraint_matrix": [[1, 0], [0, 2], [3, 2]],
        "rhs_values": [4, 12, 18],
        "senses": ['<=', '<=', '<='],
        "problem_type": "max"
    },
    "Example 2: Minimization": {
        "objective_coeffs": [-1, -1],
        "constraint_matrix": [[1, 2], [2, 1]],
        "rhs_values": [3, 3],
        "senses": ['<=', '<='],
        "problem_type": "min"
    },
    "Example 3: Maximization with Mixed Constraints": {
        "objective_coeffs": [1, 2],
        "constraint_matrix": [[1, 1], [1, 0]],
        "rhs_values": [4, 1],
        "senses": ['<=', '>='],  # Feasible region: x ≥ 1 and x + y ≤ 4
        "problem_type": "max"
    },
    "Example 4: Unbounded Maximization": {
        "objective_coeffs": [1, 1],
        "constraint_matrix": [[1, -1], [1, 0]],
        "rhs_values": [1, 0],
        "senses": ['<=', '>='],  # Unbounded: x ≥ 0 and x - y ≤ 1
        "problem_type": "max"
    },
    "Example 5: Infeasible Minimization": {
        "objective_coeffs": [3, 2],
        "constraint_matrix": [[1, 1], [1, 1]],
        "rhs_values": [5, 10],  # Contradiction: x + y ≤ 5 and x + y ≥ 10
        "senses": ['<=', '>='],
        "problem_type": "min"
    },
    "Example 6: Maximization with Equality": {
        "objective_coeffs": [4, 3],
        "constraint_matrix": [[1, 1], [2, 1]],
        "rhs_values": [5, 8],  # Equality x + y = 5 and inequality 2x + y ≤ 8
        "senses": ['=', '<='],
        "problem_type": "max"
    },
    "Example 7: Maximization with Three Variables": {
        "objective_coeffs": [3, 4, 1],
        "constraint_matrix": [[3, 10, 5], [5, 2, 8], [8, 10, 3]],
        "rhs_values": [120, 6, 105],
        "senses": ['<=', '<=', '<='],
        "problem_type": "max"
    },
    "Example 8: Minimization with Three Variables": {
        "objective_coeffs": [1, 1, 3],
        "constraint_matrix": [[2, 1, 3], [1, 2, 4], [3, 1, -2]],
        "rhs_values": [6, 8, 4],
        "senses": ['>=', '>=', '>='],
        "problem_type": "min"
    }
}