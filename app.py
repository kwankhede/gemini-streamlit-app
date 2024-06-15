from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

# Ensure the API key is correctly retrieved from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")
if api_key is None:
    st.error("API key not found. Please set the GOOGLE_API_KEY environment variable.")
    st.stop()

genai.configure(api_key=api_key)

# Initialize our Streamlit app
st.set_page_config(page_title="Gemini LLM & Vision Demo")

st.header("Gemini LLM & Vision: Your AI Assistant for Text and Image")
st.markdown("###### Explore the capabilities of the Gemini LLM and Vision models.")
st.markdown("##### About this Project")
st.info(
    """
    This project demonstrates the integration of Google's Generative AI models with a Streamlit application.
    Users can input text prompts or upload images to generate responses from the Gemini models.
    """
)
st.write("Select the type of input and interact with the Gemini model:")

# Add radio buttons for user to select input type
input_type = st.radio("Choose input type:", ("Text only", "Text and Image"))


# Define function to get Gemini response for text input
def get_gemini_text_response(input_text):
    model = genai.GenerativeModel("gemini-pro")
    try:
        response = model.generate_content(input_text)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Define function to get Gemini response for text and image input
def get_gemini_image_response(input_text, image):
    model = genai.GenerativeModel("gemini-pro-vision")
    try:
        if input_text != "":
            response = model.generate_content([input_text, image])
        else:
            response = model.generate_content(image)
        return response.text
    except Exception as e:
        st.error(f"An error occurred: {e}")
        return None


# Input field for text prompt
input_text = st.text_input("Input Prompt: ", key="input")

# If the user selects "Text and Image", show file uploader
image = None
if input_type == "Text and Image":
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

# Submit button
submit = st.button("Submit")

# If submit button is clicked
if submit:
    if input_type == "Text only":
        response = get_gemini_text_response(input_text)
    else:
        response = get_gemini_image_response(input_text, image)

    if response:
        st.subheader("The Response is")
        st.write(response)
