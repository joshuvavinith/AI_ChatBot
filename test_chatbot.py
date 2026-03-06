"""
test_chatbot.py — Unit tests for AI ChatBot.

Run with:
    pytest test_chatbot.py -v
"""

import os
import tempfile
import pytest
from fastapi.testclient import TestClient

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

DIALOG_CSV = """\
dialog_id,line_id,text
1,1,hello
1,2,Hi there! How can I help?
2,1,what is your name
2,2,I'm a chatbot built with Python!
3,1,bye
3,2,Goodbye! Have a great day.
"""


@pytest.fixture
def dialog_file(tmp_path):
    """Write a small dialog CSV and return its path."""
    path = tmp_path / "test_dialog.csv"
    path.write_text(DIALOG_CSV, encoding="utf-8")
    return str(path)


# ---------------------------------------------------------------------------
# SimpleBot tests
# ---------------------------------------------------------------------------

class TestSimpleBot:
    def test_train_loads_patterns(self, dialog_file):
        from ai_chatbot import SimpleBot

        bot = SimpleBot()
        bot.train(dialog_file)
        assert len(bot.responses) == 3

    def test_exact_match(self, dialog_file):
        from ai_chatbot import SimpleBot

        bot = SimpleBot()
        bot.train(dialog_file)
        assert bot.get_response("hello") == "Hi there! How can I help?"

    def test_partial_match(self, dialog_file):
        from ai_chatbot import SimpleBot

        bot = SimpleBot()
        bot.train(dialog_file)
        reply = bot.get_response("hey, hello there")
        assert reply == "Hi there! How can I help?"

    def test_default_response_on_unknown(self, dialog_file):
        from ai_chatbot import SimpleBot

        bot = SimpleBot()
        bot.train(dialog_file)
        reply = bot.get_response("zxqwerty unknown phrase 12345")
        assert isinstance(reply, str)
        assert len(reply) > 0

    def test_train_missing_file(self):
        from ai_chatbot import SimpleBot

        bot = SimpleBot()
        bot.train("/nonexistent/path/dialog.csv")
        assert bot.responses == {}


# ---------------------------------------------------------------------------
# ChatBot (facade) tests — forced offline mode
# ---------------------------------------------------------------------------

class TestChatBot:
    def test_offline_mode(self, dialog_file):
        from ai_chatbot import ChatBot

        bot = ChatBot(dialog_file=dialog_file, force_offline=True)
        assert bot.mode == "pattern"

    def test_chat_returns_string(self, dialog_file):
        from ai_chatbot import ChatBot

        bot = ChatBot(dialog_file=dialog_file, force_offline=True)
        reply = bot.chat("hello")
        assert isinstance(reply, str)
        assert len(reply) > 0

    def test_history_grows_with_turns(self, dialog_file):
        from ai_chatbot import ChatBot

        bot = ChatBot(dialog_file=dialog_file, force_offline=True)
        assert bot.history == []
        bot.chat("hello")
        assert len(bot.history) == 2  # one user + one assistant

    def test_reset_history(self, dialog_file):
        from ai_chatbot import ChatBot

        bot = ChatBot(dialog_file=dialog_file, force_offline=True)
        bot.chat("hello")
        bot.reset_history()
        assert bot.history == []

    def test_stream_chat_yields_text(self, dialog_file):
        from ai_chatbot import ChatBot

        bot = ChatBot(dialog_file=dialog_file, force_offline=True)
        tokens = list(bot.stream_chat("hello"))
        assert len(tokens) >= 1
        assert "".join(tokens) == "Hi there! How can I help?"

    def test_history_capped(self, dialog_file):
        from ai_chatbot import ChatBot

        bot = ChatBot(dialog_file=dialog_file, force_offline=True)
        # Drive history past MAX_HISTORY * 2
        for _ in range(bot.MAX_HISTORY + 5):
            bot.chat("hello")
        assert len(bot.history) <= bot.MAX_HISTORY * 2

    def test_retrain(self, dialog_file, tmp_path):
        from ai_chatbot import ChatBot

        bot = ChatBot(dialog_file=dialog_file, force_offline=True)

        new_csv = tmp_path / "new_dialog.csv"
        new_csv.write_text(
            "dialog_id,line_id,text\n1,1,howdy\n1,2,Howdy partner!\n",
            encoding="utf-8",
        )
        bot.train(str(new_csv))
        assert bot.chat("howdy") == "Howdy partner!"


# ---------------------------------------------------------------------------
# FastAPI tests
# ---------------------------------------------------------------------------

@pytest.fixture
def api_client(dialog_file, monkeypatch):
    """Return a TestClient with the FastAPI app; force offline mode."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    # Reset module-level state between tests
    import api as api_module
    api_module.clear_all_sessions()

    # Pre-populate a session backed by test data
    from ai_chatbot import ChatBot
    bot = ChatBot(dialog_file=dialog_file, force_offline=True)
    sid = "test-session"
    api_module._sessions[sid] = bot

    from fastapi.testclient import TestClient
    return TestClient(api_module.app), sid


class TestAPI:
    def test_health(self, api_client):
        client, _ = api_client
        resp = client.get("/health")
        assert resp.status_code == 200
        assert resp.json()["status"] == "ok"

    def test_chat_creates_session(self, api_client):
        client, _ = api_client
        resp = client.post("/chat", json={"message": "hello"})
        assert resp.status_code == 200
        data = resp.json()
        assert "reply" in data
        assert "session_id" in data
        assert data["mode"] in ("llm", "pattern")

    def test_chat_with_session(self, api_client):
        client, sid = api_client
        resp = client.post("/chat", json={"message": "hello", "session_id": sid})
        assert resp.status_code == 200
        data = resp.json()
        assert data["session_id"] == sid
        assert isinstance(data["reply"], str)

    def test_chat_empty_message(self, api_client):
        client, _ = api_client
        resp = client.post("/chat", json={"message": "   "})
        assert resp.status_code == 400

    def test_delete_session(self, api_client):
        client, sid = api_client
        resp = client.delete(f"/sessions/{sid}")
        assert resp.status_code == 200

        # Session should be gone now
        resp2 = client.delete(f"/sessions/{sid}")
        assert resp2.status_code == 404

    def test_train_valid_file(self, api_client, dialog_file):
        client, _ = api_client
        resp = client.post("/train", json={"dialog_file": dialog_file})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "retrained"
        assert data["patterns_loaded"] > 0

    def test_train_missing_file(self, api_client):
        client, _ = api_client
        resp = client.post("/train", json={"dialog_file": "/nonexistent/file.csv"})
        assert resp.status_code == 404
