import streamlit as st

def render():
    st.title("Car Insights Dashboard")
    st.write("Welcome to the Car Insights Dashboard!")
    
    st.header("Home")
    st.write("This dashboard provides insights into car listings and helps identify potential deals.")
    
    # Add some introductory content
    st.subheader("Features")
    st.markdown("""
    - **Data Analysis**: Explore car data with interactive visualizations
    - **Price Prediction**: Get AI-powered price predictions for cars
    - **Opportunities**: Discover potential deals and opportunities
    """)
    
    # Add a call to action
    st.info("Use the sidebar to navigate between different sections of the dashboard.") 