import streamlit as st
import numpy as np
from webapp.logic.problem_latex import problem_latex

def input_form(example_name, example_problems, problem_type="max"):
    with st.sidebar.form("input_form"):
        st.header("Input Parameters")

        # Problem type selection
        if 'problem_type' not in st.session_state:
            st.session_state.problem_type = "max" if problem_type == "max" else "min"
        problem_type = st.selectbox("Problem Type", ["max", "min"], index=0 if st.session_state.problem_type == "max" else 1)
        st.session_state.problem_type = problem_type

        # Objective coefficients input
        if example_name != "None":
            objective_coeffs_str = ", ".join(map(str, example_problems[example_name]["objective_coeffs"]))
        else:
            objective_coeffs_str = "5, 4"
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

        if 'num_constraints' not in st.session_state:
            st.session_state.num_constraints = 2

        # Dynamic constraint input rows
        constraint_matrix = []
        rhs_values = []
        senses = []

        for i in range(st.session_state.num_constraints):
            cols = st.columns([3, 1, 1])  # Adjust column widths as needed
            with cols[0]:
                if example_name != "None":
                    constraint_coeffs_str = ", ".join(map(str, example_problems[example_name]["constraint_matrix"][i]))
                else:
                    constraint_coeffs_str = "3, 5" if i == 0 else "4, 1" if i == 1 else "0, 0"
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
                    sense = example_problems[example_name]["senses"][i]
                else:
                    sense = "<="
                sense = st.selectbox(f"Sense {i+1}", ["<=", ">=", "="], index = ["<=", ">=", "="].index(sense), key=f"sense_{i}")
            with cols[2]:
                if example_name != "None":
                    rhs_value = float(example_problems[example_name]["rhs_values"][i])
                else:
                    rhs_value = 78.0 if i == 0 else 36.0 if i == 1 else 0.0
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

        # Display the problem in LaTeX format
        st.subheader("Problem Formulation (LaTeX)")
        if objective_coeffs is not None:
            latex_str = problem_latex(objective_coeffs, constraint_matrix, rhs_values, senses, st.session_state.problem_type)
            st.latex(latex_str)
        else:
            st.write("Please input the problem parameters.")

        # Solve button
        submitted = st.form_submit_button("Solve")

    return problem_type, objective_coeffs, constraint_matrix, rhs_values, senses, submitted