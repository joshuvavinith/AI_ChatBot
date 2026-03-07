"""
api.py — FastAPI REST backend for AI ChatBot.

Run with:
    uvicorn api:app --reload

Endpoints:
    POST /chat           Send a message and receive a reply.
    POST /train          Reload the pattern-matching bot from a CSV file.
    GET  /health         Health check.
    DELETE /sessions/{id} Reset a conversation session.

Environment variables:
    OPENAI_API_KEY   Optional – enables the LLM backend.
"""

import os
import uuid
from typing import Optional

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from ai_chatbot import ChatBot

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="AI ChatBot API",
    description=(
        "REST API for the AI ChatBot. Supports LLM (OpenAI) and offline "
        "pattern-matching backends. Maintains per-session conversation history."
    ),
    version="1.0.0",
)

# Per-session bots (keyed by session_id string)
_sessions: dict[str, ChatBot] = {}

# Dialog file used when creating new sessions (updated by /train)
_default_dialog_file: Optional[str] = None


def clear_all_sessions() -> None:
    """Remove all active sessions and reset the default dialog file. Intended for use in tests."""
    global _default_dialog_file
    _sessions.clear()
    _default_dialog_file = None


def _get_or_create_session(session_id: Optional[str]) -> tuple[str, ChatBot]:
    """Return (session_id, ChatBot) for the given session; create if missing."""
    if session_id is None:
        # Create a new session
        session_id = str(uuid.uuid4())

    if session_id not in _sessions:
        _sessions[session_id] = ChatBot(dialog_file=_default_dialog_file)

    return session_id, _sessions[session_id]


# ---------------------------------------------------------------------------
# Request / Response schemas
# ---------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    reply: str
    session_id: str
    mode: str


class TrainRequest(BaseModel):
    dialog_file: str


class TrainResponse(BaseModel):
    status: str
    patterns_loaded: int


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/health")
def health_check():
    """Simple health check."""
    return {"status": "ok"}


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    """Send a message and receive a reply.

    If *session_id* is omitted, a new session is created and its ID is
    returned so the client can continue the conversation.
    """
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message must not be empty.")

    session_id, bot = _get_or_create_session(request.session_id)
    reply = bot.chat(request.message)

    return ChatResponse(reply=reply, session_id=session_id, mode=bot.mode)


@app.delete("/sessions/{session_id}")
def reset_session(session_id: str):
    """Delete a conversation session (clears history)."""
    if session_id in _sessions:
        del _sessions[session_id]
        return {"status": "session deleted", "session_id": session_id}
    raise HTTPException(status_code=404, detail="Session not found.")


@app.post("/train", response_model=TrainResponse)
def train(request: TrainRequest):
    """Reload pattern-matching data from a CSV file on the server.

    The file must exist on the server filesystem.  All existing sessions are
    cleared so that subsequent requests create new sessions using the updated
    training data.
    """
    if not os.path.exists(request.dialog_file):
        raise HTTPException(
            status_code=404,
            detail="Training file not found on server.",
        )

    # Retrain a fresh bot to validate and count the patterns
    fresh_bot = ChatBot(dialog_file=request.dialog_file, force_offline=True)
    patterns = fresh_bot.pattern_count

    # Persist the dialog file so new sessions created after this point use it,
    # then clear existing sessions so they pick up the new data on next request.
    global _default_dialog_file
    _default_dialog_file = request.dialog_file
    _sessions.clear()

    return TrainResponse(status="retrained", patterns_loaded=patterns)
