import streamlit as st
from . import home, data_analysis, price_prediction, opportunities

# Dictionary mapping page names to their render functions
PAGES = {
    "Home": home.render,
    "Data Analysis": data_analysis.render,
    "Price Prediction": price_prediction.render,
    "Opportunities": opportunities.render
}

def render_sidebar():
    """Render the sidebar with navigation buttons."""
    st.sidebar.title("Navigation")
    
    # Get the current page from session state or default to Home
    if "current_page" not in st.session_state:
        st.session_state.current_page = "Home"
    
    # Create buttons for each page
    for page_name in PAGES.keys():
        if st.sidebar.button(page_name, key=f"btn_{page_name}"):
            st.session_state.current_page = page_name
    
    # Display current page in sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("Current Page")
    st.sidebar.write(st.session_state.current_page)

def render_current_page():
    """Render the current page based on session state."""
    current_page = st.session_state.current_page
    PAGES[current_page]() 