import numpy as np
import streamlit as st
import plotly.graph_objects as go
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
import itertools

from ..components.graph.constraint_plotting import plot_constraints
from ..components.graph.objective_function import plot_objective_function

def visualize_2d(objective_coeffs, constraint_matrix, rhs, solution, senses):
    """
    Visualizes a 2D linear programming problem, including constraints, feasible region,
    and the objective function.
    """
    fig = go.Figure()

    # Plot constraints
    plot_constraints(fig, constraint_matrix, rhs, senses)

    # Plot objective function and optimal solution
    if solution is not None:
        plot_objective_function(fig, objective_coeffs, solution)
    else:
        st.warning("No optimal solution to display.")

    fig.update_layout(title='Feasible Region and Optimal Solution', xaxis_title='x', yaxis_title='y', showlegend=True, width=800, height=600)
    st.plotly_chart(fig, use_container_width=True)