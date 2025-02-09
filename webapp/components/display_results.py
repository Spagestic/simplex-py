import streamlit as st
import pandas as pd

def display_results(status, solution, objective_value, tableau_history):
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
    elif status == 'unbounded':
        st.write("The problem is unbounded.")
    elif status == 'infeasible':
        st.write("The problem is infeasible.")
