import streamlit as st

def example_selection(example_problems):
    """
    Creates a Streamlit selectbox for example problems.

    Args:
        example_problems (dict): A dictionary containing example problems.

    Returns:
        str: The name of the selected example problem.
    """
    example_name = st.selectbox("Select an Example Problem", ["None"] + list(example_problems.keys()))
    return example_name