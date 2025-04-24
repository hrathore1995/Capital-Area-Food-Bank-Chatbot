import streamlit as st
from ai_utils import generate_reply

st.set_page_config(page_title="CAFB Droid Assistant", page_icon="🤖")
st.title("🤖 CAFB Droid Assist Chat Support")

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

# Manual reset function
def reset_conversation():
    st.session_state.pop("category", None)
    st.session_state.messages = []

# 🔁 Auto-reset if too many messages
if len(st.session_state.messages) >= 50:
    st.session_state.messages = []
    st.session_state.pop("category", None)
    st.info("🔄 Conversation reset after 50 messages to keep responses focused.")
    st.stop()

# If category not selected, show dropdown
if st.session_state.category is None:
    st.subheader("What type of issue are you facing?")
    st.session_state.category = st.selectbox("Choose a category:", categories)
    st.stop()

# ✅ Display current category above chat
st.markdown(f"**🗂️ Current Issue Category:** `{st.session_state.category}`")
st.divider()

# Show chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input box
user_input = st.chat_input("Enter your ticket/query here...")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        reply = generate_reply(st.session_state.messages, st.session_state.category)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    with st.chat_message("assistant"):
        st.markdown(reply)

# Manual category reset button
st.sidebar.button("🔄 Change Issue Category", on_click=reset_conversation)
