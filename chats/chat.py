import streamlit as st

from pandasai.llm.google_gemini import GoogleGemini

import matplotlib.pyplot as plt
from pandasai.helpers.cache import Cache

from pandasai import SmartDataframe
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image
import PIL
import os
from pandasai import Agent
from chats.chat_utils import verify_gemini_api_key, verify_state_df, verify_chat, verify_module_config_smartdataframe, verify_module_config_agent




os.environ["GEMINI_API_KEY"] = 'AIzaSyA9dAYUonF8mY1qve2omBtckh9mJegaMso'
gen_api = os.environ.get("GEMINI_API_KEY")

os.environ["PANDASAI_API_KEY"] = "$2a$10$/LzDcQcjhdGX1srHprphU.ua8Q071KVmFYJjPJxH0flOG2ETr03sm"

def chat_page():
    try:
        is_valid, message = verify_gemini_api_key(gen_api)  
        
        if not is_valid:
            st.error(message)  
            st.stop()

        llm = GoogleGemini(api_key=gen_api)

        result, message = verify_state_df()
        if not result:
            st.error(message)
            st.stop()

        df = st.session_state.df
        # custom_cache = Cache(filepath="/app/cache/cache_db_0.11.db")
        r1, msg1 = verify_module_config_smartdataframe(gen_api)
        r2, msg2 = verify_module_config_agent()
        if r1 or r2:
            st.warning(msg2 if msg1 == "Everything working Fine!!" else msg1)
        if not r1 and r2:
            st.error("The network connection is currently slow. Please check your internet connection")
            st.stop()
        
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
                result, msg = verify_chat(chat_prompt)
                if not result:
                    st.warning(msg)
                else:
                    try:
                        response = updated_df.chat(chat_prompt)
                        response2 = agent.chat(chat_prompt)

                        st.markdown("### Response:")
                        for resp in [response, response2]:
                            if "exports" in resp:
                                img = Image.open(resp)
                                st.image(img, use_column_width=True)
                                break
                        if isinstance(resp, str):
                            st.text_area("Response:", value=response, height=200, key="response")
                        elif isinstance(response2, str):
                            st.text_area("Second Response:", value=response2, height=200, key="response2")
                        else:
                            st.warning("Unexpected response format. Please refine your query!")
                    except (AttributeError, TypeError, ValueError) as e:
                        st.error(f"An error occurred while processing your prompt: {str(e)}")
                    except FileNotFoundError as e:
                        st.error(f"File not found: {str(e)}")
                    except PIL.UnidentifiedImageError as e:
                        st.error(f"Could not identify image file: {str(e)}")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")
    except Exception as e:
        st.error(f"An error occurred while processing your prompt: {e}")

