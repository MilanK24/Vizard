import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from chats.chat_utils import verify_state_df

def data_visualization(df):
    try:
        result, message = verify_state_df()
        if not result:
            st.error(message)
            st.stop()

        if st.sidebar.checkbox("Show Data Visualization"):
            column_to_plot = st.sidebar.selectbox("Select Column for Visualization", df.columns)
            plot_type = st.sidebar.selectbox("Select Plot Type", ["Bar", "Line", "Histogram"])

            if column_to_plot not in df.columns:
                st.error(f"Column '{column_to_plot}' does not exist in the dataframe.")
                st.stop()
            if plot_type not in ["Bar", "Line", "Histogram"]:
                st.error("Invalid plot type selected.")
                st.stop()
            if not column_to_plot :
                st.warning("Please Choose Column Plot") 
            if not plot_type :
                st.warning("Please Choose Plot Type") 

            plt.figure(figsize=(10, 5))
            if plot_type == "Bar":
                sns.countplot(data=df, x=column_to_plot)
            elif plot_type == "Line":
                df[column_to_plot].value_counts().sort_index().plot(kind='line')
            elif plot_type == "Histogram":
                plt.hist(df[column_to_plot], bins=20)

            plt.title(f"{plot_type} of {column_to_plot}")
            plt.xlabel(column_to_plot)
            plt.ylabel("Count")
            st.pyplot(plt)

        st.subheader("Data Manipulation")
        if st.sidebar.checkbox("Perform Data Manipulation"):
            operation = st.sidebar.selectbox("Select Operation", ["Filter Rows", "Add New Column", "Drop Column"])
            if operation == "Filter Rows":

                filter_column = st.sidebar.selectbox("Select Column to Filter", df.columns)
                if filter_column not in df.columns:
                    st.error(f"Column '{filter_column}' does not exist.")
                    st.stop()
                filter_value = st.sidebar.text_input("Filter Value (exact match)")
                if filter_value:
                    df = df[df[filter_column] == filter_value]
                    st.success(f"Filtered rows where {filter_column} is {filter_value}.")
                    st.dataframe(df)
            elif operation == "Add New Column":
                new_col_name = st.sidebar.text_input("New Column Name")
                new_col_value = st.sidebar.text_input("Value for New Column (can be static or expression)")
                if new_col_name and new_col_value:
                    try:
                        try:
                            df[new_col_name] = eval(new_col_value) if new_col_value.isnumeric() else new_col_value
                        except Exception as e:
                            st.error(f"Error evaluating expression: {e}")
                        st.success(f"Added column '{new_col_name}'.")
                        st.dataframe(df)
                    except Exception as e:
                        st.error(f"Error adding new column: {e}")

            elif operation == "Drop Column":
                drop_column = st.sidebar.selectbox("Select Column to Drop", df.columns)
                if drop_column not in df.columns:
                    st.error(f"Column '{drop_column}' does not exist.")
                    st.stop()
                if drop_column:
                    df.drop(columns=[drop_column], inplace=True)
                    st.success(f"Dropped column '{drop_column}'.")
                    st.dataframe(df)

        try:
            csv = df.to_csv(index=False).encode('utf-8')
        except Exception as e:
            st.error(f"Error generating CSV file: {e}")
        st.download_button(
            label="Download Modified Data as CSV",
            data=csv,
            file_name='modified_data.csv',
            mime='text/csv',
            key='download-csv'
        )
    except Exception as e:
        st.error(f"An unexpected error occurred: {e}")


