import numpy as np
import streamlit as st
import plotly.graph_objects as go
from .create_constraint_string import create_constraint_string

def plot_constraints(fig, constraint_matrix, rhs, senses):
    x_range = np.linspace(-10, 20, 400)
    y_range = np.linspace(-10, 20, 400)

    # Plot each constraint
    for i in range(constraint_matrix.shape[0]):
        constraint = constraint_matrix[i]
        rhs_value = rhs[i]
        constraint_x = constraint[0]
        constraint_y = constraint[1]
        sense = senses[i]

        constraint_str = create_constraint_string(constraint_x, constraint_y, rhs_value, sense)

        if constraint_y != 0:
            y_values = (rhs_value - constraint_x * x_range) / constraint_y
            fig.add_trace(go.Scatter(x=x_range, y=y_values, mode='lines', name=constraint_str, line=dict(width=2, dash='dash')))
        elif constraint_x !=0: # Vertical Line
            x_value = rhs_value / constraint_x
            fig.add_trace(go.Scatter(x=[x_value] * len(y_range), y=y_range, mode='lines', name=constraint_str, line=dict(width=2, dash='dash')))
        else: # Constant constraint. Check feasibility and display message
            if sense == '<=' and rhs_value < 0:
                st.error("Infeasible problem detected. Constant constraint violation.")
                return
            elif sense == '>=' and rhs_value < 0:
                st.error("Infeasible problem detected. Constant constraint violation.")
                return

    # Create a grid of x and y values
    x_grid, y_grid = np.meshgrid(x_range, y_range)

    # Evaluate feasibility for each point in the grid
    feasible_region = np.ones_like(x_grid, dtype=bool)
    for i in range(constraint_matrix.shape[0]):
        constraint = constraint_matrix[i]
        rhs_value = rhs[i]
        sense = senses[i]

        if constraint[1] != 0:
            constraint_values = constraint[0] * x_grid + constraint[1] * y_grid
        else:
            constraint_values = constraint[0] * x_grid  # Vertical line case

        if sense == '<=':
            feasible_region &= (constraint_values <= rhs_value)
        elif sense == '>=':
            feasible_region &= (constraint_values >= rhs_value)

    # Shade the feasible region
    fig.add_trace(go.Contour(
        x=x_range,
        y=y_range,
        z=feasible_region.astype(int),
        colorscale=[[0, 'rgba(0,0,0,0)'], [1, 'rgba(0,100,80,0.2)']],
        showscale=False,
        contours_coloring='fill',
        name='Feasible Region'
    ))

    fig.update_layout(
        xaxis_title='x',
        yaxis_title='y',
        showlegend=True
    )
