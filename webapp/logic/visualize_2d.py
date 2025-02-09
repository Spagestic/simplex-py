import numpy as np
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from scipy.optimize import linprog

def visualize_2d(objective_coeffs, constraint_matrix, rhs, solution):
    x = np.linspace(0, 10, 400)
    y = np.linspace(0, 10, 400)
    X, Y = np.meshgrid(x, y)

    fig = go.Figure()

    # Plot each constraint
    for i in range(constraint_matrix.shape[0]):
        constraint = constraint_matrix[i]
        rhs_value = rhs[i]

        constraint_x = int(constraint[0]) if constraint[0] == int(constraint[0]) else constraint[0]
        constraint_y = int(constraint[1]) if constraint[1] == int(constraint[1]) else constraint[1]

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
                constraint_str += " + "
            if constraint_y == 1:
                constraint_str += "y"
            elif constraint_y == -1:
                constraint_str += "-y"
            else:
                constraint_str += f"{constraint_y}y"

        if constraint_str == "":
            constraint_str = "0"

        if constraint[1] != 0:
            y_values = (rhs_value - constraint[0] * x) / constraint[1]
            fig.add_trace(go.Scatter(x=x, y=y_values, mode='lines', name=f'{constraint_str} <= {rhs_value}', fill='tonexty', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))
        else:
            fig.add_trace(go.Scatter(x=[rhs_value / constraint[0]] * len(y), y=y, mode='lines', name=f'{constraint_str} <= {rhs_value}', fill='tonexty', fillcolor=f'rgba({i*50 % 255},{i*30 % 255},{i*70 % 255},0.1)'))

    # Find intersection points to define the feasible region
    # This is a simplified approach and might not work for all cases
    A = constraint_matrix
    b = rhs
    
    # Add non-negativity constraints
    A = np.vstack([A, [-1, 0], [0, -1]])
    b = np.hstack([b, 0, 0])

    # Solve for the feasible region vertices
    from scipy.optimize import linprog
    
    # Define the objective function (doesn't matter for finding feasible points)
    c = [0, 0]  
    
    # Solve the linear program
    res = linprog(c, A_ub=A, b_ub=b, bounds=(0, None))
    
    # Extract the vertices of the feasible region
    if res.success:
        # Find corner points by iterating through all pairs of constraints
        import itertools
        
        # Indices of all constraints
        indices = range(A.shape[0])
        
        # Store intersection points
        intersections = []
        
        # Iterate through all pairs of constraints
        for i, j in itertools.combinations(indices, 2):
            A_intersect = A[[i, j]]
            
            # Check if the matrix is invertible
            if np.linalg.matrix_rank(A_intersect) == 2:
                b_intersect = b[[i, j]]
                
                # Solve for the intersection point
                try:
                    point = np.linalg.solve(A_intersect, b_intersect)
                    
                    # Check if the point satisfies all constraints
                    if np.all(A @ point <= b + 1e-6):  # Adding a small tolerance
                        intersections.append(point)
                except np.linalg.LinAlgError:
                    # The constraints are parallel, so there is no intersection point
                    pass
        
        # Convert the intersection points to a numpy array
        vertices = np.array(intersections)
        
        # Convex hull
        from scipy.spatial import ConvexHull
        
        if len(vertices) >= 3:
            try:
                hull = ConvexHull(vertices)
        
                # Extract the vertices of the convex hull
                hull_vertices = vertices[hull.vertices]
        
                # Plot the feasible region as a polygon
                fig.add_trace(go.Scatter(x=hull_vertices[:, 0], y=hull_vertices[:, 1], fill='toself', mode='lines', name='Feasible Region', fillcolor='rgba(0,255,0,0.2)'))
            except Exception as e:
                if "QhullError" in str(e) and "qh_maxsimplex" in str(e):
                    st.warning(f"QhullError encountered: {e}. Trying a higher tolerance.")
                    try:
                        hull = ConvexHull(vertices, qhull_options='Q12')  # Increase tolerance
                        hull_vertices = vertices[hull.vertices]
                        fig.add_trace(go.Scatter(x=hull_vertices[:, 0], y=hull_vertices[:, 1], fill='toself', mode='lines', name='Feasible Region', fillcolor='rgba(0,255,0,0.2)'))
                    except Exception as e2:
                        st.warning(f"Error creating convex hull even with higher tolerance: {e2}")
                else:
                    st.warning(f"Error creating convex hull: {e}")
        elif 0 < len(vertices) < 3:
            # Handle the case where the feasible region is a line or a point
            st.warning("The feasible region is a line or a point.")
            fig.add_trace(go.Scatter(x=vertices[:, 0], y=vertices[:, 1], mode='markers+lines', name='Feasible Region', marker=dict(size=8, color='green')))
        else:
            st.warning("No feasible region found.")
    else:
        print("No feasible region found.")
        st.warning("No feasible region found. The problem may be infeasible.")
        return  # Exit the function early if no feasible region is found

    # Plot the objective function
    if solution is not None:
        objective_value = np.dot(objective_coeffs, solution)
    else:
        objective_value = 0
        solution = [0, 0]
    
    # Choose two points to define the line
    x_vals = np.array([0, 10])
    y_vals = (objective_value - objective_coeffs[0] * x_vals) / objective_coeffs[1] if objective_coeffs[1] != 0 else np.array([objective_value / objective_coeffs[0]] * 2)
    
    # Plot the objective function line
    fig.add_trace(go.Scatter(x=x_vals, y=y_vals, mode='lines', name='Objective Function', line=dict(color='red')))

    # Plot the optimal solution
    fig.add_trace(go.Scatter(x=[solution[0]], y=[solution[1]], mode='markers', marker=dict(size=10, color='red'), name=f'Optimal Solution: ({solution[0]:.2f}, {solution[1]:.2f})'))

    # Set labels and title
    fig.update_layout(
        title='Feasible Region and Optimal Solution',
        xaxis_title='x',
        yaxis_title='y',
        showlegend=True,
        width=800,
        height=600
    )

    # Display the plot in Streamlit
    st.plotly_chart(fig, use_container_width=True)
