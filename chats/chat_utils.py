import requests
import streamlit as st
from pandasai import Agent
from pandasai.llm.google_gemini import GoogleGemini
import os
from pandasai import SmartDataframe

def verify_gemini_api_key(api_key):
    if not api_key:
        return False, "No Attribute value provided"
    
    API_VERSION = 'v1'
    api_url = f'https://generativelanguage.googleapis.com/{API_VERSION}/models?key={api_key}'
    
    try:
        response = requests.get(api_url, headers={'Content-Type': 'application/json'}, timeout=10)
        response.raise_for_status()  

    except requests.exceptions.ConnectionError:
        return False, "Connection error occurred"
        
    except requests.exceptions.Timeout:
        return False, "The request timed out"
        
    except requests.exceptions.HTTPError as err:
        return False, f"HTTP error occurred: {err}"
        
    except ValueError:
        return False, "Invalid response format."

    if response.status_code != 200:
        error_message = response.json().get('error', {}).get('message', 'Invalid API Key')
        return False, f"Error: {error_message}"
    
    return True, "Valid API Key"

def verify_state_df():
    if "df" not in st.session_state:
        return False, "Please upload and explore a dataset before using this feature!"
    
    try:
        df = st.session_state.df

    except KeyError as e:
        return False, f"KeyError: {str(e)} The DataFrame is not initialized in session state"
    
    except AttributeError as e:
        return False, f"AttributeError: {str(e)} - There was an issue with the DataFrame structure"
    
    except TypeError as e:
        return False, f"TypeError: {str(e)} - The operation on the DataFrame failed due to type mismatch"
    
    except Exception as e:
        return False, f"An unexpected error occurred: {str(e)}"
    
    return True, f"Everything Working Fine!!"

def verify_chat(ch):
    if not isinstance(ch, str):
        return False, "Input must be a string."
    
    if not ch.strip():
        return False, "Please enter a prompt before submitting!!"
    
    return True, "Input is valid."
    
def verify_module_config_smartdataframe(gen_api):
    try:
        if gen_api is None:
            # raise ValueError("Environment variable 'GEMINI_API_KEY' is missing")
            return False ,"Environment variable 'GEMINI_API_KEY' is missing"
        df = st.session_state.df
        llm = GoogleGemini(api_key=gen_api)
        updated_df = SmartDataframe(df, config={"llm": llm})
        return True, "Everything working Fine!!"

    except NameError as e:
        return False, "NameError: name 'llm' is not defined"
    except ModuleNotFoundError as e:
        return False, "ModuleNotFoundError: No module named 'pandas_ai'"
    except TypeError as e:
        return False, "TypeError: Object of type 'DataFrame' is not JSON serializable"
    except AttributeError as e:
        return False, "AttributeError: 'NoneType' object has no attribute 'chat'"
    except Exception as e:
        return False, "Exception as occured!!"
    
def verify_module_config_agent():
    try: 
        df = st.session_state.df
        agent = Agent(df)
        return True, "Everything working Fine!!"
    except NameError as e:
        return False, "NameError: name 'llm' is not defined"
    except ModuleNotFoundError as e:
        return False, "ModuleNotFoundError: No module named 'pandas_ai'"
    except TypeError as e:
        return False, "TypeError: __init__() missing required positional argument"
    except AttributeError as e:
        return False, "AttributeError: 'NoneType' object has no attribute 'chat'"
    except Exception as e:
        return False, "Exception as occured!!"




