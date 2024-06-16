from dotenv import load_dotenv

load_dotenv()  # Load environment variables

import streamlit as st
import os
import google.generativeai as genai

# Set page configuration
st.set_page_config(page_title="Q&A Demo")

# Custom CSS for styling
st.markdown(
    """
    <style>
        body {
            background-color: #f0f0f0;
        }
        .main {
            background-color: #ffffff;
            padding: 10px;
            border-radius: 10px;
        }
        .stTextInput, .stButton {
            padding: 10px;
        }
        .user-message {
            background-color: #d1e7ff;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 5px;
        }
        .bot-message {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 5px;
        }
        .sidebar-content {
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            margin-bottom: 20px;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# Configure the generative AI model with the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Function to load Gemini Pro model and get responses
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])


def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response


# Initialize the Streamlit app
st.sidebar.title("About Me")
st.sidebar.markdown(
    """
    Hi! I'm your Gemini LLM Assistant. Feel free to ask me anything!
    """
)

st.sidebar.title("Chatbot Info")
st.sidebar.markdown(
    """
    **Name:** Gemini LLM Chatbot
    """
)

# Add image to sidebar
st.sidebar.image("kabir.png", use_column_width=True)

st.header("Gemini LLM Application")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Chat container to display the chat history
chat_container = st.container()

# Input field and submit button at the bottom
with st.form(key="chat_form", clear_on_submit=True):
    input = st.text_input("Type your message:", key="input")
    submit = st.form_submit_button("Send")

if submit and input:
    response = get_gemini_response(input)
    # Add user query and response to session state chat history
    st.session_state["chat_history"].append(("You", input))
    bot_response = ""
    for chunk in response:
        bot_response += chunk.text
    st.session_state["chat_history"].append(("Bot", bot_response))

# Display the chat history
with chat_container:
    for role, text in st.session_state["chat_history"]:
        if role == "You":
            st.markdown(
                f"<div class='user-message'><strong>{role}:</strong> {text}</div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='bot-message'><strong>{role}:</strong> {text}</div>",
                unsafe_allow_html=True,
            )
