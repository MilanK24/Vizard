import streamlit as st
import pandas as pd
from visualizations.visualizations import data_visualization
from chat.chat import chat_page

def data_exploration():
    uploaded_file = st.sidebar.file_uploader("📁 Upload your dataset (CSV format)", type="csv")
    if uploaded_file:
        try:
            st.session_state.df = pd.read_csv(uploaded_file)  
            st.sidebar.success("File uploaded successfully!")

            df = st.session_state.df
            st.sidebar.success("File uploaded successfully!")

            st.expander("🔍 Uploaded Dataset Preview", expanded=True)
            st.dataframe(df.head())
            st.markdown(f"**Rows:** {df.shape[0]}, **Columns:** {df.shape[1]}")
            st.markdown("---")
            st.markdown("### Full Dataset Summary")
            st.write(df.describe())
            data_visualization(df)
            if st.button("Chat with Your Dataset"):
                st.session_state.page = 'chat'
        except Exception as e:
            st.error("🚨 Error reading the uploaded file. Please ensure it is a valid CSV file.")
