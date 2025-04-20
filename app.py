import streamlit as st
from ai_utils import generate_reply

st.set_page_config(page_title="CAFB Droid Assistant", page_icon="🤖")
st.title("🤖 CAFB Droid Chat Support")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display message history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
user_input = st.chat_input("Enter your ticket/query here...")

if user_input:
    # User message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # AI response
    with st.spinner("Thinking..."):
        reply = generate_reply(user_input)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)
