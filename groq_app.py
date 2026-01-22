import streamlit as st
from groq import Groq
import os

# -------------------------------
# Setup Groq client
# -------------------------------
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(page_title="AI Assistant", layout="wide")
st.title("🧠 AI Assistant (Groq)")

# -------------------------------
# Conversation memory
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful, clear, and professional AI assistant."
        }
    ]

# -------------------------------
# Sidebar: task selection
# -------------------------------
st.sidebar.header("Task Mode")

task = st.sidebar.selectbox(
    "Choose a mode",
    ["Free Chat", "Summarize Text", "Explain Code", "Resume / SOP Review"]
)

if st.sidebar.button("🔄 Reset Conversation"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful, clear, and professional AI assistant."
        }
    ]
    st.rerun()

# -------------------------------
# Prompt router
# -------------------------------
def build_prompt(mode, text):
    if mode == "Summarize Text":
        return f"Summarize the following text in 5 concise bullet points:\n\n{text}"
    elif mode == "Explain Code":
        return f"Explain the following code step by step in simple terms:\n\n{text}"
    elif mode == "Resume / SOP Review":
        return (
            "You are a professional resume and SOP reviewer.\n"
            "Analyze the following content and suggest clear improvements:\n\n"
            f"{text}"
        )
    return text

# -------------------------------
# Input form
# -------------------------------
with st.form("chat_form", clear_on_submit=True):
    user_input = st.text_area("Enter your text", height=200)
    submitted = st.form_submit_button("Send")

# -------------------------------
# Handle submission
# -------------------------------
if submitted and user_input.strip():
    final_prompt = build_prompt(task, user_input)

    st.session_state.messages.append(
        {"role": "user", "content": final_prompt}
    )

    with st.spinner("Thinking..."):
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.messages,
            temperature=0.7
        )

    assistant_reply = response.choices[0].message.content

    st.session_state.messages.append(
        {"role": "assistant", "content": assistant_reply}
    )

# -------------------------------
# Display conversation
# -------------------------------
st.divider()
st.subheader("Conversation")

for msg in st.session_state.messages[1:]:
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")







