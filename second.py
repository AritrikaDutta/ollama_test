import streamlit as st
import ollama

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="AI Assistant",
    layout="wide"
)

st.title("🧠 AI Assistant (Chat + Tasks)")

# -------------------------------
# Initialize conversation memory
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
st.sidebar.header("Task Selection")

task = st.sidebar.selectbox(
    "Choose a mode",
    [
        "Free Chat",
        "Summarize Text",
        "Explain Code",
        "Resume / SOP Review"
    ]
)

if st.sidebar.button("🔄 Reset Conversation"):
    st.session_state.messages = [
        {
            "role": "system",
            "content": "You are a helpful, clear, and professional AI assistant."
        }
    ]
    st.experimental_rerun()

# -------------------------------
# Input area
# -------------------------------
st.subheader("Your Input")

user_input = st.text_area(
    "Enter your text or query",
    height=200,
    placeholder="Type here..."
)

# -------------------------------
# Prompt routing logic
# -------------------------------
def build_prompt(selected_task, text):
    if selected_task == "Summarize Text":
        return (
            "Summarize the following text in 5 concise bullet points:\n\n"
            f"{text}"
        )

    elif selected_task == "Explain Code":
        return (
            "Explain the following code step by step in simple terms:\n\n"
            f"{text}"
        )

    elif selected_task == "Resume / SOP Review":
        return (
            "You are a professional resume and SOP reviewer.\n"
            "Analyze the following content and suggest clear improvements:\n\n"
            f"{text}"
        )

    else:  # Free Chat
        return text

# -------------------------------
# Send button
# -------------------------------
if st.button("Send"):
    if user_input.strip():

        final_prompt = build_prompt(task, user_input)

        # Add user message
        st.session_state.messages.append(
            {"role": "user", "content": final_prompt}
        )

        # Call Ollama chat API
        response = ollama.chat(
            model="llama3.2:1b",
            messages=st.session_state.messages,
            options={
                "temperature": 0.7
            }
        )

        assistant_reply = response["message"]["content"]

        # Add assistant response
        st.session_state.messages.append(
            {"role": "assistant", "content": assistant_reply}
        )

# -------------------------------
# Display conversation
# -------------------------------
st.divider()
st.subheader("Conversation")

for msg in st.session_state.messages[1:]:  # skip system message
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    else:
        st.markdown(f"**Assistant:** {msg['content']}")
