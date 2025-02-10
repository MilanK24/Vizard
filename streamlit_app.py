import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

import streamlit as st
from pandasai import SmartDataframe
from pandasai.llm.google_gemini import GoogleGemini
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import seaborn as sns
from pandasai import Agent
from pandasai.helpers.cache import Cache
from pandasai.connectors.pandas import PandasConnector

import os
os.environ["MPLCONFIGDIR"] = "/app/matplotlib"
import matplotlib

import streamlit as st
from pymongo import MongoClient
import bcrypt
st.set_page_config(page_title="VIZARD", page_icon="⚔️")
MONGO_URI = "mongodb+srv://milan:milan@daytona.2kcr9.mongodb.net/"
client = MongoClient(MONGO_URI)
db = client["user_database"]  
users_collection = db["users"]  


def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

def authenticate_user(username, password):
    user = users_collection.find_one({"username": username})
    if user and verify_password(password, user["password"]):
        return True
    return False

def register_user(username, password):
    if users_collection.find_one({"username": username}):
        return "Username already exists!"
    
    hashed_pw = hash_password(password)
    users_collection.insert_one({"username": username, "password": hashed_pw})
    return "User registered successfully!"

st.title("🔐 User Authentication ")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["username"] = ""

menu = st.sidebar.radio("Navigation", ["Login", "Register"])

if menu == "Login":
    if not st.session_state.get("logged_in", True):
        # st.warning("🚨 You need to log in first!")
        # st.stop()
        st.subheader("🔑 Login")
        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if authenticate_user(username, password):
                st.session_state["logged_in"] = True
                st.session_state["username"] = username
                st.markdown(f"✅ Welcome, {username}!")
                
            else:
                st.error("❌ Invalid username or password.")

elif menu == "Register":
    st.subheader("📝 Register")
    new_username = st.text_input("Choose a Username", key="reg_user")
    new_password = st.text_input("Choose a Password", type="password", key="reg_pass")
    
    if st.button("Register"):
        msg = register_user(new_username, new_password)
        if "successfully" in msg:
            st.success(msg)
        else:
            st.error(msg)

if st.session_state["logged_in"]:
    st.sidebar.success(f"Logged in as: {st.session_state['username']}")
    # st.subheader("🎉 Welcome to the Dashboard!")
    st.write("This is a protected page that only logged-in users can see.")
    

    if st.button("Logout"):
        st.session_state["logged_in"] = False
        st.session_state["username"] = ""
        st.experimental_rerun()


llm = GoogleGemini(api_key='AIzaSyA9dAYUonF8mY1qve2omBtckh9mJegaMso')
os.environ["PANDASAI_API_KEY"] = "$2a$10$/LzDcQcjhdGX1srHprphU.ua8Q071KVmFYJjPJxH0flOG2ETr03sm"



st.markdown(
    """
    <style>
    body {
        background: linear-gradient(135deg, #f0f0f0, #d9d9d9);
        color: #333;
        font-family: 'Helvetica Neue', sans-serif;
    }
    .main {
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        background-color: black;
        transition: all 0.5s ease; /* Smooth transition */
    }
    h1 {
        text-align: center;
        font-size: 3rem;
        color: #007aff;
        text-shadow: 1px 1px #e3e3e3;
    }
    h2 {
        text-align: center;
        font-size: 2rem;
        color: #333;
    }
    .tagline {
        text-align: center;
        font-size: 1.5rem;
        margin-bottom: 20px;
    }
    .stButton button {
        background-color: #007aff;
        color: white;
        border: none;
        padding: 12px 30px;
        border-radius: 5px;
        transition: background-color 0.3s ease-in-out, transform 0.2s ease-in-out;
    }
    .stButton button:hover {
        background-color: #005bb5;
        transform: scale(1.05);
    }
    .footer {
        text-align: center;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

if 'page' not in st.session_state:
    st.session_state.page = 'home'

def go_to_chat():
    st.session_state.page = 'chat'

def go_to_data_exploration():
    st.session_state.page = 'data_exploration'


if "df" not in st.session_state:
    st.session_state.df = None
if st.session_state.page == 'home':
    if not st.session_state.get("logged_in", False):
        st.warning("🚨 You need to log in first!")
        st.stop()
    else:
        st.title("Welcome to the Data Explorer! 📊")
        st.markdown('<p class="tagline">Your gateway to insightful data analysis and visualization.</p>', unsafe_allow_html=True)
        st.markdown("""
        ### Unlock the Power of Your Data
        Upload your dataset and explore its insights through interactive visualizations and manipulations.
        - *Visualize* your data with various chart types.
        - *Manipulate* your dataset with easy-to-use tools.
        - *Download* your modified data effortlessly.
        """)

    if st.button("Start Exploring Your Data"):
        go_to_data_exploration()

elif st.session_state.page == 'data_exploration':
    if not st.session_state.get("logged_in", False):
        st.warning("🚨 You need to log in first!")
        st.stop()
    else:


        st.sidebar.title("Navigation")
        st.sidebar.subheader("Upload & Explore")

        uploaded_file = st.sidebar.file_uploader("📁 Upload your dataset (CSV format)", type="csv")

        if uploaded_file:
            try:
                st.session_state.df = pd.read_csv(uploaded_file)  
                st.sidebar.success("File uploaded successfully!")

                df = st.session_state.df
                st.sidebar.success("File uploaded successfully!")

                with st.expander("🔍 Uploaded Dataset Preview", expanded=True):
                    st.dataframe(df.head())
                    st.markdown(f"*Rows:* {df.shape[0]}, *Columns:* {df.shape[1]}")
                    st.markdown("---")
                    st.markdown("### Full Dataset Summary")
                    st.write(df.describe())

                    if st.sidebar.checkbox("Show Data Visualization"):
                        column_to_plot = st.sidebar.selectbox("Select Column for Visualization", df.columns)
                        plot_type = st.sidebar.selectbox("Select Plot Type", ["Bar", "Line", "Histogram"])

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
                                    df[new_col_name] = eval(new_col_value) if new_col_value.isnumeric() else new_col_value
                                    st.success(f"Added column '{new_col_name}'.")
                                    st.dataframe(df)
                                except Exception as e:
                                    st.error(f"Error adding new column: {e}")

                        elif operation == "Drop Column":
                            drop_column = st.sidebar.selectbox("Select Column to Drop", df.columns)
                            if drop_column:
                                df.drop(columns=[drop_column], inplace=True)
                                st.success(f"Dropped column '{drop_column}'.")
                                st.dataframe(df)

                    csv = df.to_csv(index=False).encode('utf-8')
                    st.download_button(
                        label="Download Modified Data as CSV",
                        data=csv,
                        file_name='modified_data.csv',
                        mime='text/csv',
                        key='download-csv'
                    )

                if st.button("Chat with Your Dataset"):
                    go_to_chat()

            except Exception as e:
                st.error("🚨 Error reading the uploaded file. Please ensure it is a valid CSV file.")

if st.session_state.page == 'chat':
    if not st.session_state.get("logged_in", False):
        st.warning("🚨 You need to log in first!")
        st.stop()
    else:

        st.header("💬 Chat with Your Dataset")

        if st.session_state.df is None:
            st.error("Please upload and explore a dataset before using this feature!")
            st.stop()

        df = st.session_state.df
        # custom_cache = Cache(filepath="/app/cache/cache_db_0.11.db")

        # df_connector = PandasConnector(df)
        updated_df = SmartDataframe(df, config={"llm": llm})


        suggested_prompts = [
            "What is the average value of column X?",
            "Show me the distribution of column Y.",
            "Filter rows where column Z is greater than A.",
            "What insights can you provide about this dataset?",
        ]
        agent = Agent(df)

        with st.form("chat_form"):
            chat_prompt = st.text_area(
                "Type your prompt here...",
                placeholder="e.g., What are the trends in this dataset?",
                key="chat_prompt",
            )

            st.markdown("### Suggested Prompts:")
            selected_prompt = st.radio(
                "Choose a suggested prompt:",
                options=["None"] + suggested_prompts,
                key="selected_prompt",
            )

            if selected_prompt != "None":
                chat_prompt = selected_prompt

            submitted = st.form_submit_button("Submit")
            if submitted:
                if not chat_prompt.strip():
                    st.error("Please enter a prompt before submitting!")
                else:
                    try:
                        response2 = agent.chat(chat_prompt)
                        st.markdown("### Response:")

                        if "exports" in response2:
                            img = Image.open(response2)

                            fig, ax = plt.subplots()
                            ax.imshow(img)
                            ax.axis('off')

                            st.pyplot(fig)
                        else:
                            if "Potential security risk" in response2:
                                st.warning("⚠️ **The entered prompt is not relevant to the dataset.**")

                                st.markdown("""
                                    The provided input does not match the dataset structure.  
                                    Please refine your query by ensuring the following:
                                """)

                                st.info("💡 **How to improve your prompt:**")
                                st.markdown("""
                                - **Use correct column names**: Ensure you reference actual columns from the dataset.
                                - **Be specific**: Provide a clear and structured question.
                                - **Stay relevant**: Avoid unrelated queries that do not match the dataset's context.
                                - **Check for typos**: Misspelled words may lead to an invalid query.
                                """)
                            else:
                                st.text_area(value=response2, height=200, key="response2")
                    except Exception as ValueError:
                        st.warning("⚠️ The provided value does not match the expected format or data type.")
                        st.markdown("""
                            **Possible reasons for this issue:**
                            - The input value may be incorrectly formatted.
                            - You might be using an invalid column name.
                            - The requested operation might not be applicable to this dataset.

                            **Suggested Actions:**
                            - Double-check the column names in the dataset.
                            - Ensure you're using the correct data type (e.g., numerical values for calculations).
                            - Try rephrasing your query for better clarity.
                        """)
                    except Exception as e:
                        st.error(f"An error occurred while processing your prompt: {e}")
                        st.text_area("Second Response: ", value=response2, height=200, key="response2")

    if st.button("Back to Data Exploration"):
        go_to_data_exploration()



st.markdown(
    """
    <hr>
    <div class="footer">
        <p>Designed for dynamic dataset querying.</p>
        <p><i>Tip: Make your queries specific for better results!</i></p>
    </div>
    """,
   unsafe_allow_html=True,
)