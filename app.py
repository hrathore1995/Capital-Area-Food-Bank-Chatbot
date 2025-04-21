import streamlit as st
from ai_utils import generate_reply

st.set_page_config(page_title="CAFB Droid Assistant", page_icon="🤖")
st.title("🤖 CAFB Droid Chat Support")

# Initialize chat state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "category" not in st.session_state:
    st.session_state.category = None

# Category options
categories = [
    "Order or Delivery Change Requests",
    "Food Availability or Selection Issues",
    "Training or New Partner Setup Questions",
    "General Delivery and Food Support",
    "Adding/Modifying Orders or Cases",
    "Other"
]

# Reset both category and messages if button clicked
def reset_conversation():
    st.session_state.pop("category", None)
    st.session_state.messages = []

# Category selection screen
if st.session_state.category is None:
    st.subheader("What type of issue are you facing?")
    st.session_state.category = st.selectbox("Choose a category:", categories)
    st.stop()

# Chat history display
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Enter your ticket/query here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        reply = generate_reply(user_input, st.session_state.category)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# Sidebar option to change category and reset chat
st.sidebar.button("🔄 Change Issue Category", on_click=reset_conversation)
