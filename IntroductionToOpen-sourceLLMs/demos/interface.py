import streamlit as st
import requests

st.set_page_config(page_title="GloboAssist", page_icon="🤖")
st.title("GloboAssist Support Bot")

OLLAMA_URL = "http://localhost:11434/api/generate"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("How can I help you today?"):
    st.chat_message("user").markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    request_data = {
        "model": "globo-assist",
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=request_data)
        response.raise_for_status()
        full_response = response.json()
        assistant_msg = full_response['response']

    except Exception as e:
        assistant_msg = f"Sorry, I'm experiencing a technical issue: {e}"

    with st.chat_message("assistant"):
        st.markdown(assistant_msg)
    st.session_state.messages.append({"role": "assistant", "content": assistant_msg})