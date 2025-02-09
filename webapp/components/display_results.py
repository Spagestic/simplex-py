import streamlit as st
import pandas as pd
from webapp.logic.visualize_2d import visualize_2d

def display_results(status, solution, objective_value, tableau_history, objective_coeffs, constraint_matrix, rhs):
    st.header("Results")
    st.write(f"Status: {status}")
    if status == 'optimal':
        st.write(f"Optimal Solution: {solution}")
        st.write(f"Optimal Objective Value: {objective_value}")

        # Display tableau history
        st.header("Tableau History")
        for i, tableau in enumerate(tableau_history):
            st.subheader(f"Iteration {i + 1}")
            st.dataframe(pd.DataFrame(tableau))  # Display tableau as a dataframe

        # Display 2D graph if the problem has two variables
        if len(objective_coeffs) == 2:
            visualize_2d(objective_coeffs, constraint_matrix, rhs, solution)
    elif status == 'unbounded':
        st.write("The problem is unbounded.")
        if len(objective_coeffs) == 2:
            visualize_2d(objective_coeffs, constraint_matrix, rhs, solution)
    elif status == 'infeasible':
        st.write("The problem is infeasible.")
        if len(objective_coeffs) == 2:
            visualize_2d(objective_coeffs, constraint_matrix, rhs, solution)
