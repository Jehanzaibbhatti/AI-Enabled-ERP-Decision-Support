"""
AI-Enabled ERP Decision Support
MSIT 5910 Capstone Project
"""

import streamlit as st


st.set_page_config(
    page_title="AI-Enabled ERP Decision Support",
    page_icon="📊",
    layout="wide"
)

st.title("AI-Enabled ERP Decision Support")

st.write(
    "A proof-of-concept decision-support framework for analyzing "
    "ERP-style data using analytics and machine learning."
)

st.info(
    "Prototype status: The application interface is being developed. "
    "AI-generated outputs will remain subject to human review and validation."
)

st.subheader("Planned Use Cases")

st.markdown(
    """
    1. **Financial and Project Trend Analysis**
    2. **ERP Exception and Risk Detection**
    3. **Project Cost-Overrun Prediction**
    """
)

st.subheader("Data Source")

st.write(
    "The proof of concept will use synthetic or appropriately "
    "de-identified ERP-style data."
)
