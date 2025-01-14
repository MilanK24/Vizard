import streamlit as st
import pandas as pd
from visualizations.visualizations import data_visualization
from chats.chat_utils import verify_state_df


def data_exploration():
    try:
        result, message = verify_state_df()
        if not result:
            st.error(message)
            st.stop()
        try:
            uploaded_file = st.sidebar.file_uploader("📁 Upload your dataset (CSV format)", type="csv")
        except FileNotFoundError:
            st.error("🚨 File not found!")
            st.stop()
        except ValueError:
            st.error("🚨 Invalid file format!")
            st.stop()
        except TypeError:
            st.error("🚨 Invalid file type!")
            st.stop()
        except Exception as e:
            st.error("Some Error has occured!!")
            st.stop()

        if uploaded_file:
            try:
                if uploaded_file.type != "text/csv":
                    st.error("🚨 Please upload a CSV file.")
                    st.stop()
                try:
                    st.session_state.df = pd.read_csv(uploaded_file)  
                except pd.errors.ParserError:
                    st.error("🚨 Error parsing the CSV file. It might be improperly formatted.")
                    st.stop()
                except UnicodeDecodeError:
                    st.error("🚨 Error reading the file. It might have an unsupported encoding.")

                st.sidebar.success("File uploaded successfully!")

                df = st.session_state.df
                st.sidebar.success("File uploaded successfully!")

                st.expander("🔍 Uploaded Dataset Preview", expanded=True)
                st.dataframe(df.head())
                st.markdown(f"**Rows:** {df.shape[0]}, **Columns:** {df.shape[1]}")
                st.markdown("---")
                st.markdown("### Full Dataset Summary")
                st.write(df.describe())
                try:
                    data_visualization(df)
                except Exception as e:
                    st.error(f"🚨 Error generating visualizations: {e}")
                    st.stop()
                if st.button("Chat with Your Dataset"):
                    if "page" not in st.session_state:
                        st.session_state.page = "chat"  
                    else:
                        st.session_state.page = 'chat'
            except Exception as e:
                st.error("🚨 Error reading the uploaded file. Please ensure it is a valid CSV file.")
    except Exception as e:
        st.error(f"🚨 An unexpected error occurred: {e}")
        st.stop()