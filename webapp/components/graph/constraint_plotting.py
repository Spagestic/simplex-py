import numpy as np
import streamlit as st
import plotly.graph_objects as go

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

        # Constructing the constraint string with '=' or '<='
        constraint_str = ""
        if constraint_x != 0:
            if constraint_x == 1:
                constraint_str += "x"
            elif constraint_x == -1:
                constraint_str += "-x"
            else:
                constraint_str += f"{constraint_x}x"
        if constraint_y != 0:
            if constraint_str != "":
                constraint_str += " + " if constraint_y > 0 else " - "
                if abs(constraint_y) != 1:
                    constraint_str += f"{abs(constraint_y)}"
            constraint_str += "y"

        if constraint_str == "":
            constraint_str = "0"

        if sense == '<=':
            constraint_str += " ≤ " + str(rhs_value)
        elif sense == '>=':
            constraint_str += " ≥ " + str(rhs_value)
        else:
            constraint_str += " = " + str(rhs_value)

        if constraint[1] != 0:
            y_values = (rhs_value - constraint[0] * x) / constraint[1]
            if sense == '<=':
                fig.add_trace(go.Scatter(x=x, y=y_values, mode='lines', name=constraint_str, fill='tonexty', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))
            elif sense == '>=':
                fig.add_trace(go.Scatter(x=x, y=y_values, mode='lines', name=constraint_str, fill='tozeroy', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))
            else:
                 fig.add_trace(go.Scatter(x=x, y=y_values, mode='lines', name=constraint_str))
        elif constraint[0] !=0: # Vertical Line
            if sense == '<=':
                fig.add_trace(go.Scatter(x=[rhs_value / constraint[0]] * len(y), y=y, mode='lines', name=constraint_str, fill='tonexty', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))
            elif sense == '>=':
                fig.add_trace(go.Scatter(x=[rhs_value / constraint[0]] * len(y), y=y, mode='lines', name=constraint_str, fill='tozeroy', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))
            else:
                fig.add_trace(go.Scatter(x=[rhs_value / constraint[0]] * len(y), y=y, mode='lines', name=constraint_str))
        else: # Constant constraint. Check feasibility and display message
            if sense == '<=' and rhs_value < 0:
                st.error("Infeasible problem detected. Constant constraint violation.")
                return
            elif sense == '>=' and rhs_value > 0:
                st.error("Infeasible problem detected. Constant constraint violation.")
                return
