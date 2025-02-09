import numpy as np
import streamlit as st
import plotly.graph_objects as go
from .create_constraint_string import create_constraint_string

def plot_constraints(fig, constraint_matrix, rhs, senses):
    x = np.linspace(0, 10, 400)
    y = np.linspace(0, 10, 400)

    # Plot each constraint
    for i in range(constraint_matrix.shape[0]):
        constraint = constraint_matrix[i]
        rhs_value = rhs[i]
        constraint_x = constraint[0]
        constraint_y = constraint[1]
        sense = senses[i]

        constraint_str = create_constraint_string(constraint_x, constraint_y, rhs_value, sense)

        if constraint_y != 0:
            y_values = (rhs_value - constraint_x * x) / constraint_y
            if sense == '<=':
                fig.add_trace(go.Scatter(x=x, y=y_values, mode='lines', name=constraint_str, fill='tozeroy', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))
            elif sense == '>=':
                fig.add_trace(go.Scatter(x=x, y=y_values, mode='lines', name=constraint_str, fill='tozeroy', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))
            else:
                 fig.add_trace(go.Scatter(x=x, y=y_values, mode='lines', name=constraint_str))
        elif constraint_x !=0: # Vertical Line
            x_value = rhs_value / constraint_x
            if sense == '<=':
                fig.add_trace(go.Scatter(x=[x_value] * len(y), y=y, mode='lines', name=constraint_str, fill='tozeroy', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))
            elif sense == '>=':
                fig.add_trace(go.Scatter(x=[x_value] * len(y), y=y, mode='lines', name=constraint_str, fill='tozeroy', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))
            else:
                fig.add_trace(go.Scatter(x=[x_value] * len(y), y=y, mode='lines', name=constraint_str))
        else: # Constant constraint. Check feasibility and display message
            if sense == '<=' and rhs_value < 0:
                st.error("Infeasible problem detected. Constant constraint violation.")
                return
            elif sense == '>=' and rhs_value < 0:
                st.error("Infeasible problem detected. Constant constraint violation.")
                return
