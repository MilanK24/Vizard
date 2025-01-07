import streamlit as st
from file_handler.file_handler import data_exploration

def home_page():
    st.title("Welcome to the Data Explorer! 📊")
    st.markdown('<p class="tagline">Your gateway to insightful data analysis and visualization.</p>', unsafe_allow_html=True)
    st.markdown("""
    ### Unlock the Power of Your Data
    Upload your dataset and explore its insights through interactive visualizations and manipulations.
    - **Visualize** your data with various chart types.
    - **Manipulate** your dataset with easy-to-use tools.
    - **Download** your modified data effortlessly.
    """)
    if st.button("Start Exploring Your Data"):
        st.session_state.page = 'data_exploration'

def data_exploration_page():
    st.sidebar.title("Navigation")
    st.sidebar.subheader("Upload & Explore")
    data_exploration()