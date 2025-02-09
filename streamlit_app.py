import streamlit as st
import logging
from webapp.components.example_selection import example_selection
from webapp.components.input_form import input_form
from webapp.components.display_results import display_results
from webapp.logic.solve_simplex import solve_simplex
from webapp.logic.load_example import load_example
from webapp.logic.problem_latex import problem_latex

from webapp.example_problems import example_problems

# Configure logging
logging.basicConfig(level=logging.INFO)

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

    # Example selection
    example_name = example_selection(example_problems)

    # Load example values if an example is selected
    objective_coeffs, constraint_matrix, rhs_values, senses, problem_type = load_example(example_name, example_problems)

    # Update the number of constraints based on the selected example
    if example_name != "None":
        st.session_state.num_constraints = len(example_problems[example_name]["constraint_matrix"])

    # Input form
    problem_type, objective_coeffs, constraint_matrix, rhs_values, senses, submitted = input_form(example_name, example_problems, problem_type)

    if submitted:
        if objective_coeffs is not None and constraint_matrix is not None and rhs_values is not None:
            # Call the tabular simplex method
            status, solution, objective_value, tableau_history = solve_simplex(
                objective_coeffs, constraint_matrix, rhs_values, senses, problem_type
            )

            # Display results
            if status == 'optimal':
                # Display the problem in LaTeX format
                st.subheader("Problem Formulation (LaTeX)")
                latex_str = problem_latex(objective_coeffs, constraint_matrix, rhs_values, senses)
                st.latex(latex_str)

            display_results(status, solution, objective_value, tableau_history, objective_coeffs, constraint_matrix, rhs_values)
        else:
            st.error("Please provide valid inputs for all parameters.")

if __name__ == "__main__":
    main()
