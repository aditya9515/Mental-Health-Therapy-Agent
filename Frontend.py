# Setup-Streamlit
import streamlit as st
import requests


URL = "http://localhost:8000/ask"

st.set_page_config(page_title="AI Mental Health Therapist", layout="wide")
st.title("AI Mental Health Therapist")

# intialize chat history in session state
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# User input
user_input = st.chat_input("How can I assist you today with your mental health?")

if user_input:
    #append user message to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_input})


    # fixed dummy response for demonstration
    # ai_response = "I'm here to help you. Can you tell me more about how you're feeling?"
    ai_reponse = requests.post(URL, json={"message": user_input})
    # print("ADA",ai_reponse.json())
    data = ai_reponse.json()
    print(data)
    st.session_state.chat_history.append({"role": "assistant", "content": data})
    

# Display chat history
for message in st.session_state.chat_history:
    if message["role"] == "user":
        st.chat_message("user").write(message["content"])
    else:
        st.chat_message("assistant").write(message["content"])