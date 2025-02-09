import streamlit as st

def example_selection(example_problems):
    example_name = st.selectbox("Select an Example Problem", ["None"] + list(example_problems.keys()))
    return example_name