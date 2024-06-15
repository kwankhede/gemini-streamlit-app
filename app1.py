from dotenv import load_dotenv

load_dotenv()  # loading all the environmental variables

import streamlit as st
import os
import google.generativeai as genai

# Ensure the API key is correctly retrieved from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)

# Function to load Gemini and gemini pro models
model = genai.GenerativeModel("gemini-pro")


def get_gemini_response(question):
    try:
        response = model.generate_content(question)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


st.set_page_config(page_title="Q and A Demo")

st.header("Gemini LLM Application")
input = st.text_input("Input: ", key="input")
submit = st.button("Ask the Question")

# When submit button is clicked
if submit:
    response = get_gemini_response(input)
    if response:
        st.subheader("Response")
        st.write(response)
