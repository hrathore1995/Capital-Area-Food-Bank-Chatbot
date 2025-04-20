# 🤖 Capital Area Food Bank Droid Assistant

This is a smart, AI-powered chatbot built using Streamlit and OpenAI to help Capital Area Food Bank partners and clients get quick and helpful responses to common support queries. It uses GPT-4o-mini to understand the context of questions, classify their urgency, and provide polite, concise, and actionable replies.

---

## 🚀 Features

- ✅ Classifies queries into: **Very Urgent**, **Urgent**, **Medium**, or **Low Priority**
- 💬 Responds with clear, polite replies tailored to the urgency level
- 🔐 Secure integration with OpenAI using `secrets.toml`
- 🧠 Logs all queries, responses, and priority to `chat_log.csv` for review and future training
- 🖥️ Simple Streamlit interface for fast deployment and demo

---

## 🗂 Project Structure

```
ticket-triage-ai/
├── app.py                      # Streamlit chat interface
├── ai_utils.py                # Core LLM logic + logging
├── requirements.txt           # Python dependencies
├── .gitignore                 # Files to ignore in Git
├── .streamlit/
│   └── secrets.toml           # Secure location for API key
└── chat_log.csv               # Auto-generated chat log (not committed)
```

---

## 🛠 Requirements

- Python 3.8+
- Streamlit
- OpenAI Python SDK
- Git (for deployment via GitHub)

---

## 📦 Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ticket-triage-ai.git
cd ticket-triage-ai

# Create virtual environment and install dependencies
pip install -r requirements.txt
```

---

## 🔐 Setup Your OpenAI Key

Create the file: `.streamlit/secrets.toml`

Paste the following (replace with your actual key):

```toml
OPENAI_API_KEY = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

Do NOT commit this file to GitHub — it's already in `.gitignore`.

---

## ▶️ Run the App Locally

```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## ☁️ Deploy to Streamlit Cloud

1. Push your project to a **private GitHub repository**
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud)
3. Click **New app**
4. Choose your GitHub repo
5. Set `app.py` as the entry file
6. Add your OpenAI key in the Streamlit **Secrets Manager**
7. Click **Deploy**

---

## 🧠 How It Works

1. User enters a support query
2. The app sends it to OpenAI with instructions to:
   - Classify the urgency level
   - Generate a helpful, short reply
3. The reply is formatted with a custom greeting + closing
4. The full interaction is logged to `chat_log.csv`

---

## 🧾 Example Log Entry

```csv
timestamp,query,priority,ai_response
2025-04-20T22:40:01,"Can I change my delivery slot?",Medium,"This is Capital Area Food Bank Droid Assist... Thank you for reaching out."
```

---

## 🤝 Acknowledgments

Built with ❤️ by Harshwardhan using:
- [Streamlit](https://streamlit.io/)
- [OpenAI](https://platform.openai.com/)
- [Pandas](https://pandas.pydata.org/)