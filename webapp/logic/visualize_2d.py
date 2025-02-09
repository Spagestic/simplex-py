import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
import itertools

def visualize_2d(objective_coeffs, constraint_matrix, rhs, solution, senses):
    x = np.linspace(0, 10, 400)
    y = np.linspace(0, 10, 400)
    X, Y = np.meshgrid(x, y)

    fig = go.Figure()

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

    # Feasible Region Calculation
    A = np.vstack([constraint_matrix, [-1, 0], [0, -1]])
    b = np.hstack([rhs, 0, 0])
    c = [0, 0]  # Dummy objective for feasibility check

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

    if res.status != 0:  # Check for infeasibility or unboundedness
        st.warning(f"No feasible region found.  Scipy linprog status: {res.message}")
        return

    # Find vertices of the feasible region (intersection points)
    vertices = []
    for i, j in itertools.combinations(range(A.shape[0]), 2):
        A_intersect = A[[i, j]]
        if np.linalg.matrix_rank(A_intersect) == 2:
            b_intersect = b[[i, j]]
            try:
                point = np.linalg.solve(A_intersect, b_intersect)
                if np.all(A @ point <= b + 1e-8):  # Tolerance for numerical stability
                    vertices.append(point)
            except np.linalg.LinAlgError:
                pass  # Parallel lines


    if vertices:
        vertices = np.array(vertices)
        try:
            hull = ConvexHull(vertices)
            hull_vertices = vertices[hull.vertices]
            fig.add_trace(go.Scatter(x=hull_vertices[:, 0], y=hull_vertices[:, 1], fill='toself', mode='lines', name='Feasible Region', fillcolor='rgba(0,255,0,0.2)'))
        except Exception as e: # scipy.spatial.qhull.QhullError
            st.warning(f"Error during ConvexHull calculation: {e}")
            fig.add_trace(go.Scatter(x=vertices[:, 0], y=vertices[:, 1], mode='markers+lines', name='Feasible Region', marker=dict(size=8, color='green')))



    # Objective Function and Optimal Solution
    if solution is not None:
        objective_value = np.dot(objective_coeffs, solution)
        fig.add_trace(go.Scatter(x=[solution[0]], y=[solution[1]], mode='markers', marker=dict(size=10, color='red'), name=f'Optimal Solution: ({solution[0]:.2f}, {solution[1]:.2f})'))
    else:
        objective_value = 0 # or handle appropriately if no solution

    x_vals = np.array([0, 10])
    if objective_coeffs[1] != 0:
        y_vals = (objective_value - objective_coeffs[0] * x_vals) / objective_coeffs[1]
    elif objective_coeffs[0] != 0: # Handle vertical objective function
        y_vals = [0,10] # Arbitrary vertical line within the plot range
        x_vals = np.array([objective_value / objective_coeffs[0]] * 2) # Adjust x_vals
    else: # Objective function is a constant
        y_vals = [0,10] # Arbitrary vertical line within the plot range

    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Objective Function', line=dict(color='red')))


    fig.update_layout(title='Feasible Region and Optimal Solution', xaxis_title='x', yaxis_title='y', showlegend=True, width=800, height=600)
    st.plotly_chart(fig, use_container_width=True)