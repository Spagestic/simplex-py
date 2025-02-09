import streamlit as st
import pandas as pd
from webapp.logic.visualize_2d import visualize_2d
import numpy as np  # Import numpy

def display_results(status, solution, objective_value, tableau_history, objective_coeffs, constraint_matrix, rhs_values, senses):
    st.header("Results")
    st.write(f"Status: {status}")
    if status == 'optimal':
        st.write(f"Optimal Solution: {solution}")
        st.write(f"Optimal Objective Value: {objective_value}")

        # Display tableau history
        st.header("Tableau History")
        if tableau_history is not None:
            for i, tableau in enumerate(tableau_history):
                st.subheader(f"Iteration {i + 1}")
                st.dataframe(pd.DataFrame(tableau))  # Display tableau as a dataframe

                # Calculate and display ratios
                if i < len(tableau_history) - 1:
                    entering_col_index = np.argmin(tableau_history[i][0, :-1])
                    ratios = calculate_ratios_from_tableau(tableau_history[i], entering_col_index)
                    st.write(f"Ratios for Iteration {i + 1}: {ratios}")

        # Display 2D graph if the problem has two variables
        if len(objective_coeffs) == 2:
            visualize_2d(objective_coeffs, constraint_matrix, rhs_values, solution, senses)
    elif status == 'unbounded':
        st.write("The problem is unbounded.")
        if len(objective_coeffs) == 2:
            visualize_2d(objective_coeffs, constraint_matrix, rhs_values, solution, senses)
    elif status == 'infeasible':
        st.write("The problem is infeasible.")
        if len(objective_coeffs) == 2:
            visualize_2d(objective_coeffs, constraint_matrix, rhs_values, solution, senses)

def calculate_ratios_from_tableau(tableau: np.ndarray, entering_col_index: int) -> np.ndarray:
    ratios = []
    for i in range(1, tableau.shape[0]):
        if tableau[i, entering_col_index] > 0:
            ratio = tableau[i, -1] / tableau[i, entering_col_index]
            ratios.append(ratio)
        else:
            ratios.append(np.inf)
    return np.array(ratios)
