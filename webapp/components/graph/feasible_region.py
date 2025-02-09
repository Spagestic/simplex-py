import numpy as np
import streamlit as st
import plotly.graph_objects as go
from scipy.optimize import linprog
from scipy.spatial import ConvexHull
import itertools

def calculate_feasible_region(fig, constraint_matrix, rhs):
    # Feasible Region Calculation
    A = np.vstack([constraint_matrix, [-1, 0], [0, -1]])
    b = np.hstack([rhs, 0, 0])
    c = [0, 0]  # Dummy objective for feasibility check

    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))

    if res.status != 0:  # Check for infeasibility or unboundedness
        st.warning(f"No feasible region found.  Scipy linprog status: {res.message}")
        return None

    # Find vertices of the feasible region (intersection points)
    vertices = []
    for i, j in itertools.combinations(range(A.shape[0]), 2):
        A_intersect = A[[i, j]]
        if np.linalg.matrix_rank(A_intersect) == 2:
            b_intersect = b[[i, j]]
            try:
                point = np.linalg.solve(A_intersect, b_intersect)
                if np.all(A @ point <= b + 1e-6):  # Tolerance for numerical stability
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
            # Fallback to displaying vertices as scatter plot with lines
            vertices = np.concatenate((vertices, [vertices[0]]))
            fig.add_trace(go.Scatter(x=vertices[:, 0], y=vertices[:, 1], mode='markers+lines', name='Feasible Region', marker=dict(size=8, color='green')))

    return vertices
