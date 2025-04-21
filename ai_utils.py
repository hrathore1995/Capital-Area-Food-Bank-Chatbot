from openai import OpenAI
import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Securely load API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

def generate_reply(user_query):
    system_prompt = """
You are a helpful AI assistant for Capital Area Food Bank.

Your task:
1. Analyze the user's query.
2. Classify it as one of: Very Urgent, Urgent, Medium, or Low Priority.
3. Generate a short, polite, helpful reply (under 60 words) — but do include any greeting or closing. Just the helpful core content.

If anything not related to food,order,delivery,time, query resolution etc ask politely to type related queries to CAFB. Allow for greeting to be typed by the users.
Return format:
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

    # Wrap the reply with greeting and closing
    full_reply = (
        
        f"{core_reply}\n\n"
        "Capital Area Food Bank Droid Assist Chat Support"
    )

    # Log to CSV
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "query": user_query,
        "priority": priority,
        "ai_response": full_reply
    }
    log_df = pd.DataFrame([log_entry])
    if os.path.exists("chat_log.csv"):
        log_df.to_csv("chat_log.csv", mode="a", header=False, index=False)
    else:
        log_df.to_csv("chat_log.csv", index=False)

    return full_reply
