import streamlit as st
from ui.page_manager import render_sidebar, render_current_page

def main():
    # Set page configuration
    st.set_page_config(
        page_title="Car Insights Dashboard",
        page_icon="🚗",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Render the sidebar with navigation
    render_sidebar()
    
    # Render the current page
    render_current_page()

if __name__ == "__main__":
    main() 