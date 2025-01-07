import streamlit as st
from pandasai import SmartDataframe
from pandasai.llm.google_gemini import GoogleGemini
import streamlit as st
import matplotlib.pyplot as plt
from pandasai.helpers.cache import Cache
import streamlit as st
from pandasai import SmartDataframe
from pandasai.llm.google_gemini import GoogleGemini
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import os
from pandasai import Agent

llm = GoogleGemini(api_key='AIzaSyA9dAYUonF8mY1qve2omBtckh9mJegaMso')
os.environ["PANDASAI_API_KEY"] = "$2a$10$/LzDcQcjhdGX1srHprphU.ua8Q071KVmFYJjPJxH0flOG2ETr03sm"

def chat_page():
    if st.session_state.df is None:
            st.error("Please upload and explore a dataset before using this feature!")
            st.stop()

    df = st.session_state.df
    # custom_cache = Cache(filepath="/app/cache/cache_db_0.11.db")
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
                    response = updated_df.chat(chat_prompt)
                    response2 = agent.chat(chat_prompt)

                    st.markdown("### Response:")
                    if "exports" in response:
                        img = Image.open(response)

                        fig, ax = plt.subplots()
                        ax.imshow(img)
                        ax.axis('off')

                        st.pyplot(fig)

                    elif isinstance(response, str):
                        st.text_area("Response:", value=response, height=200, key="response")
                    else:
                        st.warning("Unexpected response format. Please refine your query!")  
                    if "exports" in response2:
                        img = Image.open(response2)

                        fig, ax = plt.subplots()
                        ax.imshow(img)
                        ax.axis('off')

                        st.pyplot(fig)
                    else:
                        st.text_area("Second Response: ", value=response2, height=200, key="response2")
                except Exception as e:
                    st.error(f"An error occurred while processing your prompt: {e}")
                    st.text_area("Second Response: ", value=response2, height=200, key="response2")

