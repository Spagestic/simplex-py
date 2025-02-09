import numpy as np
import plotly.graph_objects as go

def plot_objective_function(fig, objective_coeffs, solution):
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
