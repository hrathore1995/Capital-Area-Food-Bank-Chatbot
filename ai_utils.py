from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Load OpenAI client securely
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Map categories to keyword context
topic_map = {
    "Order or Delivery Change Requests": "order, delivery, items, change, item",
    "Food Availability or Selection Issues": "available, out of stock, food types, substitutions",
    "Training or New Partner Setup Questions": "partner registration, onboarding, training, support",
    "General Delivery and Food Support": "support, delay, food box, feedback",
    "Adding/Modifying Orders or Cases": "add item, modify order, cases, quantity",
    "Other": "miscellaneous or unspecified issue"
}

def generate_reply(chat_history, issue_category):
    category_keywords = topic_map.get(issue_category, "")

    system_prompt = f"""
You are a helpful AI assistant for Capital Area Food Bank.

Context:
- Issue Category: {issue_category}
- Keywords: {category_keywords}

Instructions:
- Consider the full chat history before generating your response.
- Classify the urgency level as one of: Very Urgent, Urgent, Medium, Low Priority.
- Respond with a polite, helpful message under 60 words.
- Begin with a greeting and end with a helpful tone.

Return your reply in this format:
Priority: <One of the 4 levels>
Response: <Helpful response only>
"""

    # Construct chat for OpenAI
    messages = [{"role": "system", "content": system_prompt}]
    for msg in chat_history:
        messages.append({"role": msg["role"], "content": msg["content"]})

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        temperature=0.3
    )

    output = response.choices[0].message.content.strip()

    if "Priority:" in output and "Response:" in output:
        priority = output.split("Priority:")[1].split("Response:")[0].strip()
        core_reply = output.split("Response:")[1].strip()
    else:
        priority = "Unknown"
        core_reply = output

    full_reply = f"{core_reply}\n\nCapital Area Food Bank Droid Assist Chat Support"

    # Log query
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "category": issue_category,
        "priority": priority,
        "query": chat_history[-1]['content'],
        "ai_response": full_reply
    }
    log_df = pd.DataFrame([log_entry])
    if os.path.exists("chat_log.csv"):
        log_df.to_csv("chat_log.csv", mode="a", header=False, index=False)
    else:
        log_df.to_csv("chat_log.csv", index=False)

    return full_reply
