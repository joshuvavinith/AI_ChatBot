"""
web_demo.py — Streamlit web interface for AI ChatBot.

Run with:
    streamlit run web_demo.py

Environment variables:
    OPENAI_API_KEY   Set this to enable the LLM backend (optional).
"""

import streamlit as st

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from ai_chatbot import ChatBot

# ---------------------------------------------------------------------------
# Page configuration
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="AI ChatBot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 AI ChatBot")
st.caption(
    "Powered by **OpenAI GPT** (LLM mode) when `OPENAI_API_KEY` is set, "
    "otherwise uses offline **pattern-matching**."
)

# ---------------------------------------------------------------------------
# Session-level chatbot instance
# ---------------------------------------------------------------------------

# Per-session bot stored in session_state so each browser tab/user gets its own history
if "bot" not in st.session_state:
    st.session_state.bot = ChatBot()

bot: ChatBot = st.session_state.bot

# Initialise message history in session state
if "messages" not in st.session_state:
    st.session_state.messages: list[dict] = []
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": "Hello! I'm your AI chatbot. How can I help you today?",
        }
    )

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.header("⚙️ Settings")
    st.info(f"**Backend:** {'🤖 LLM (OpenAI)' if bot.mode == 'llm' else '📋 Pattern Matching'}")

    if st.button("🗑️ Clear conversation"):
        st.session_state.messages = [
            {
                "role": "assistant",
                "content": "Conversation cleared. How can I help you?",
            }
        ]
        bot.reset_history()
        st.rerun()

    st.markdown("---")
    st.markdown("### About")
    st.markdown(
        "This chatbot supports two backends:\n"
        "- **LLM mode**: uses OpenAI's API for intelligent, context-aware replies.\n"
        "- **Pattern mode**: offline fallback using a dialog dataset.\n\n"
        "Set `OPENAI_API_KEY` in your environment or a `.env` file to enable LLM mode."
    )

# ---------------------------------------------------------------------------
# Chat history display
# ---------------------------------------------------------------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------------------------------------------------------------------------
# Chat input
# ---------------------------------------------------------------------------
if prompt := st.chat_input("Type a message…"):
    # Show user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate and stream the assistant reply
    with st.chat_message("assistant"):
        if bot.mode == "llm":
            # Streaming response
            response_placeholder = st.empty()
            full_response = ""
            for token in bot.stream_chat(prompt):
                full_response += token
                response_placeholder.markdown(full_response + "▌")
            response_placeholder.markdown(full_response)
            reply = full_response
        else:
            reply = bot.chat(prompt)
            st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
