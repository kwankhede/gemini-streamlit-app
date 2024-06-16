from dotenv import load_dotenv

load_dotenv()  # Load environment variables

import streamlit as st
import os
import google.generativeai as genai

# Set page configuration
st.set_page_config(page_title="Let's-Chit-Chat")

# Adding favicon
st.markdown(
    """
    <link rel="icon" href="favicon.ico" type="image/x-icon">
    """,
    unsafe_allow_html=True,
)

# Custom CSS for styling and animations
st.markdown(
    """
    <style>
        body {
            margin: 0;
            font-family: Arial, sans-serif;
        }
        .sidebar-container {
            position: relative;
            overflow: hidden;
        }
        .sidebar-content {
            padding: 20px;
            background-color: #ffffff;
            border-radius: 10px;
            margin-bottom: 20px;
            z-index: 2;
            position: relative;
        }
        .funny-text {
            font-style: italic;
            color: #6a0dad;  /* Purple color for fun */
        }
        .created-by {
            font-size: 12px;
            color: #888888;
            margin-top: 10px;
        }
        .avatar {
            border-radius: 50%;
            width: 80px;
            height: 80px;
            margin-bottom: 10px;
        }
        .balloon {
            position: absolute;
            bottom: -150px;
            width: 30px;
            height: 40px;
            border-radius: 50%;
            background-color: var(--color);
            animation: rise 8s infinite;
            z-index: 1;
        }
        .balloon::before {
            content: "";
            position: absolute;
            bottom: -10px;
            left: 50%;
            width: 2px;
            height: 20px;
            background: #FDFD96;
        }
        @keyframes rise {
            0% {
                transform: translateY(0);
                opacity: 1;
            }
            100% {
                transform: translateY(-1200px);
                opacity: 0;
            }
        }
        .user-message {
            background-color: #d1e7ff;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            max-width: 80%;
        }
        .bot-message {
            background-color: #f1f1f1;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 10px;
            max-width: 80%;
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
    <div class="sidebar-content">
        <h3>Meet Kabir, Your Chatbot!</h3>
        <p>Hey there! I'm Kabir, your witty companion. Ask me anything and brace yourself for some fun!</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.sidebar.image("kabir.png", use_column_width=True)
st.sidebar.title("Chatbot Info")
st.sidebar.markdown(
    """
    **Name:** Let's-Chit-Chat
    """
)


# Funny messages about Kabir and creator
st.sidebar.markdown(
    """
    <div class='funny-text'>
    **Funny Facts About Me (Kabir):**
    - I know where you left your socks.
    - I once beat Google in a search contest (they cheated).
    - My favorite food is binary code.
    </div>
    <div class='created-by'>
    Created by Kabir's cool dad Kapil... for Kabuuuuuuuuuuu!
    </div>
""",
    unsafe_allow_html=True,
)


# Function to create balloons dynamically
def create_balloons(num):
    import random

    colors = [
        "#FF69B4",
        "#FF6347",
        "#FFD700",
        "#ADFF2F",
        "#87CEFA",
        "#8A2BE2",
        "#FFA07A",
        "#98FB98",
        "#DB7093",
        "#4682B4",
    ]
    for _ in range(num):
        color = random.choice(colors)
        balloon = f"""
        <div class="balloon" style="--color: {color}; left: {random.randint(0, 90)}%; animation-delay: {random.random()}s;"></div>
        """
        st.sidebar.markdown(balloon, unsafe_allow_html=True)


# Check if it's the first visit and trigger balloon creation
if "first_visit" not in st.session_state:
    st.session_state["first_visit"] = True

if st.session_state["first_visit"]:
    create_balloons(500)  # Increase number of balloons
    st.session_state["first_visit"] = False

# Main chat header and message
st.header("Let's-Chit-Chat")
st.markdown(
    "Hey there! I'm Kabir. Welcome to Let's-Chit-Chat, where you can ask me anything and I'll try to respond with my infinite wisdom!"
)

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
