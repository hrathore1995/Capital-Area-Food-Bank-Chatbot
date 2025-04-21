from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Securely load API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# Map categories to keywords (context)
topic_map = {
    "Order or Delivery Change Requests": "order, delivery, items, change, item",
    "Food Availability or Selection Issues": "available, out of stock, food types, substitutions",
    "Training or New Partner Setup Questions": "partner registration, onboarding, training, support",
    "General Delivery and Food Support": "support, delay, food box, feedback",
    "Adding/Modifying Orders or Cases": "add item, modify order, cases, quantity",
    "Other": "miscellaneous or unspecified issue"
}

def generate_reply(user_query, issue_category):
    category_keywords = topic_map.get(issue_category, "")

    system_prompt = f"""
You are a helpful AI assistant for Capital Area Food Bank.

Your task:
1. Understand the user's query in the context of the selected issue category.
2. Classify the urgency level as one of: Very Urgent, Urgent, Medium, or Low Priority.
3. Generate a short, polite, and helpful response (under 60 words) in context to selected issue category. Always begin your first response with a friendly greeting.

Issue Category: {issue_category}
Relevant Context: {category_keywords}

Return your reply in this format:
Priority: <One of the 4 levels>
Response: <Helpful response only>
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_query}
        ],
        temperature=0.3
    )

    output = response.choices[0].message.content.strip()

    if "Priority:" in output and "Response:" in output:
        priority = output.split("Priority:")[1].split("Response:")[0].strip()
        core_reply = output.split("Response:")[1].strip()
    else:
        priority = "Unknown"
        core_reply = output

    # Final message with footer
    full_reply = (
        f"{core_reply}\n\n"
        "Capital Area Food Bank Droid Assist Chat Support"
    )

    # Log query + category + response
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": user_query,
        "category": issue_category,
        "priority": priority,
        "ai_response": full_reply
    }
    log_df = pd.DataFrame([log_entry])
    if os.path.exists("chat_log.csv"):
        log_df.to_csv("chat_log.csv", mode="a", header=False, index=False)
    else:
        log_df.to_csv("chat_log.csv", index=False)

    return full_reply
