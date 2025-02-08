import streamlit as st
import numpy as np
import pandas as pd
import logging
from simplex import tabular_simplex

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    st.title("Tabular Simplex Method Solver")

    # Initialize session state for constraints
    if 'num_constraints' not in st.session_state:
        st.session_state.num_constraints = 1
    if 'constraint_inputs' not in st.session_state:
        st.session_state.constraint_inputs = []

    # Add constraint button (outside the form)
    if st.button("Add Constraint"):
        st.session_state.num_constraints += 1

    # Remove constraint button (but keep at least one) (outside the form)
    if st.session_state.num_constraints > 1:
        if st.button("Remove Constraint"):
            st.session_state.num_constraints -= 1

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

    # Example selection
    example_name = st.selectbox("Select an Example Problem", ["None"] + list(example_problems.keys()))

    # Load example values if an example is selected
    if example_name != "None":
        example = example_problems[example_name]
        objective_coeffs = example["objective_coeffs"]
        constraint_matrix = example["constraint_matrix"]
        rhs_values = example["rhs_values"]
        senses = example["senses"]
        problem_type = example["problem_type"]

        # Set default values for input fields
        objective_coeffs_str = ", ".join(map(str, objective_coeffs))
        num_vars = len(objective_coeffs)

        # Set number of constraints based on the example
        st.session_state.num_constraints = len(constraint_matrix)

        # Initialize constraint inputs in session state
        st.session_state.constraint_inputs = []
        for i in range(st.session_state.num_constraints):
            st.session_state.constraint_inputs.append({
                "coeffs": ", ".join(map(str, constraint_matrix[i])),
                "sense": senses[i],
                "rhs": rhs_values[i]
            })
    else:
        objective_coeffs_str = "1, 2"
        objective_coeffs = None
        num_vars = 2
        constraint_matrix = None
        rhs_values = None
        senses = None
        problem_type = "max"

    # Input form
    with st.sidebar.form("input_form"):
        st.header("Input Parameters")

        # Problem type selection
        problem_type = st.selectbox("Problem Type", ["max", "min"], index = 0 if problem_type == "max" else 1)

        # Objective coefficients input
        objective_coeffs_str = st.text_input("Objective Function Coefficients (comma-separated)", objective_coeffs_str)
        try:
            objective_coeffs = np.array([float(x) for x in objective_coeffs_str.split(',')])
        except ValueError:
            st.error("Invalid input for objective coefficients. Please enter comma-separated numbers.")
            objective_coeffs = None

        # Number of variables (inferred from objective coefficients)
        num_vars = len(objective_coeffs) if objective_coeffs is not None else 0

        # Constraint inputs
        st.subheader("Constraints")

        # Dynamic constraint input rows
        constraint_matrix = []
        rhs_values = []
        senses = []

        for i in range(st.session_state.num_constraints):
            cols = st.columns([3, 1, 1])  # Adjust column widths as needed
            with cols[0]:
                if example_name != "None":
                    constraint_coeffs_str = ", ".join(map(str, example["constraint_matrix"][i]))
                else:
                    constraint_coeffs_str = "1, 1"
                constraint_coeffs_str = st.text_input(f"Constraint {i+1} Coefficients (comma-separated)", constraint_coeffs_str, key=f"constraint_{i}")
                try:
                    constraint_coeffs = np.array([float(x) for x in constraint_coeffs_str.split(',')])
                    if len(constraint_coeffs) != num_vars:
                        st.error(f"Number of coefficients in constraint {i+1} must match the number of variables ({num_vars}).")
                        constraint_coeffs = None
                except ValueError:
                    st.error(f"Invalid input for constraint {i+1} coefficients. Please enter comma-separated numbers.")
                    constraint_coeffs = None
            with cols[1]:
                if example_name != "None":
                    sense = example["senses"][i]
                else:
                    sense = "<="
                sense = st.selectbox(f"Sense {i+1}", ["<=", ">=", "="], index = ["<=", ">=", "="].index(sense), key=f"sense_{i}")
            with cols[2]:
                if example_name != "None":
                    rhs_value = float(example["rhs_values"][i])
                else:
                    rhs_value = 0.0
                try:
                    rhs_value = st.number_input(f"RHS {i+1}", value=rhs_value, format="%.2f", key=f"rhs_{i}")
                except ValueError:
                    st.error(f"Invalid input for RHS value in constraint {i+1}. Please enter a number.")
                    rhs_value = None

            if constraint_coeffs is not None and rhs_value is not None:
                constraint_matrix.append(constraint_coeffs)
                rhs_values.append(rhs_value)
                senses.append(sense)

        # Convert to numpy arrays
        if constraint_matrix:
            constraint_matrix = np.array(constraint_matrix)
            rhs_values = np.array(rhs_values)

        # Solve button
        submitted = st.form_submit_button("Solve")

    if submitted:
        if objective_coeffs is not None and constraint_matrix is not None and rhs_values is not None:
            try:
                # Call the tabular simplex method
                status, solution, objective_value, tableau_history = tabular_simplex(
                    objective_coeffs, constraint_matrix, rhs_values, senses, problem_type
                )

                # Display results
                st.header("Results")
                st.write(f"Status: {status}")
                if status == 'optimal':
                    st.write(f"Optimal Solution: {solution}")
                    st.write(f"Optimal Objective Value: {objective_value}")

                    # Display the problem in LaTeX format
                    st.subheader("Problem Formulation (LaTeX)")
                    latex_str = f"\\text{{Maximize }} z = {', '.join([f'{int(c) if c.is_integer() else c}x_{i+1}' for i, c in enumerate(objective_coeffs)])} \\\\\n"
                    latex_str += "\\text{Subject to:} \\\\\n"
                    for i in range(len(constraint_matrix)):
                        latex_str += f"{', '.join([f'{int(a) if a.is_integer() else a}x_{j+1}' for j, a in enumerate(constraint_matrix[i])])} {senses[i]} {int(rhs_values[i]) if isinstance(rhs_values[i], float) and rhs_values[i].is_integer() else rhs_values[i]} \\\\\n"
                    st.latex(latex_str)

                elif status == 'unbounded':
                    st.write("The problem is unbounded.")
                elif status == 'infeasible':
                    st.write("The problem is infeasible.")

                # Display tableau history
                st.header("Tableau History")
                for i, tableau in enumerate(tableau_history):
                    st.subheader(f"Iteration {i + 1}")
                    st.dataframe(pd.DataFrame(tableau))  # Display tableau as a dataframe

            except Exception as e:
                st.error(f"An error occurred: {e}")
                logger.exception(f"An error occurred: {e}")
        else:
            st.error("Please provide valid inputs for all parameters.")


if __name__ == "__main__":
    main()
