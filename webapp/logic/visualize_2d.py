import numpy as np
import streamlit as st
import pandas as pd

def visualize_2d(objective_coeffs, constraint_matrix, rhs, solution):
    # Define the range for x values
    x = np.linspace(0, 10, 100)

    # Create a dictionary to store the data for the chart
    chart_data = {}

    # Plot each constraint
    for i in range(constraint_matrix.shape[0]):
        constraint = constraint_matrix[i]
        rhs_value = rhs[i]

        if constraint[1] != 0:  # y is not zero
            y_values = (rhs_value - constraint[0] * x) / constraint[1]
            chart_data[f'Constraint {i+1}'] = y_values
        else:  # y is zero, plot a vertical line (as a horizontal line on the chart)
            # For vertical lines, we'll create a constant y value for the range of x
            chart_data[f'Constraint {i+1}'] = np.full_like(x, rhs_value / constraint[0])

    # Plot the objective function (as a line)
    # To plot the objective function, we need to express y in terms of x: y = (z - ax) / b
    # Since 'z' (objective value) is not fixed for the line, we'll plot a line for a specific objective value
    if solution is not None:
        objective_value = np.dot(objective_coeffs, solution)  # Use the optimal objective value
    else:
        objective_value = 0  # Default value when no solution is available
        solution = [0,0]
    y_values_objective = (objective_value - objective_coeffs[0] * x) / objective_coeffs[1]
    chart_data['Objective Function'] = y_values_objective

    # Create a DataFrame from the chart data
    df = pd.DataFrame(chart_data, index=x)
    df.index.name = 'x'  # Set x-axis label

    # Display the line chart in Streamlit
    st.line_chart(df)

    # Display the optimal solution as text
    st.write(f'Optimal Solution: x = {solution[0]:.2f}, y = {solution[1]:.2f}')
