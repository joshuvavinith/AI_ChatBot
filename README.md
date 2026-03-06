
# 🤖 AI ChatBot

![CI](https://github.com/joshuvavinith/AI_ChatBot/actions/workflows/ci.yml/badge.svg)
![Python](https://img.shields.io/badge/python-3.12-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A modern, extensible Python chatbot with two backends:

| Mode | When active | What it uses |
|------|-------------|--------------|
| **LLM** | `OPENAI_API_KEY` is set | OpenAI Chat Completions (GPT-3.5 / GPT-4o) |
| **Pattern Matching** | No API key present | Offline CSV dialog dataset |

Three interfaces are available: a **Tkinter desktop GUI**, a **Streamlit web app**, and a **FastAPI REST backend**.

---

## 📚 Table of Contents

- [Key Features](#-key-features)
- [Quick Start](#-quick-start)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Running the Chatbot](#-running-the-chatbot)
  - [Desktop GUI (Tkinter)](#-desktop-gui-tkinter)
  - [Web UI (Streamlit)](#-web-ui-streamlit)
  - [REST API (FastAPI)](#-rest-api-fastapi)
- [Docker](#-docker)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [CI/CD](#-cicd)
- [Architecture](#-architecture)
- [Contributing](#-contributing)

---

## ✨ Key Features

- 🤖 **LLM backend** — connects to OpenAI's API for intelligent, context-aware responses
- 📋 **Offline fallback** — pattern matching on a dialog dataset; works without internet/API key
- 🌐 **Streamlit web UI** — chat from any browser with streaming token output (LLM mode)
- 🔌 **FastAPI REST API** — `/chat` and `/train` endpoints; per-session conversation memory
- 🖥️ **Tkinter desktop GUI** — original GUI updated to show backend mode
- 🧠 **Conversation memory** — recent exchanges are passed to the LLM for follow-up questions
- 🐳 **Docker support** — single image supports both web and API modes via `MODE` build arg
- ✅ **Tests** — pytest suite covering core logic and API endpoints
- 🔄 **CI/CD** — GitHub Actions workflow: lint → test → Docker build

---

## 🚀 Quick Start

```bash
git clone https://github.com/joshuvavinith/AI_ChatBot.git
cd AI_ChatBot
pip install -r requirements.txt

# (optional) enable LLM mode
echo "OPENAI_API_KEY=sk-..." > .env

# Start the web UI
streamlit run web_demo.py
```

---

## 🔧 Installation

### 1. Clone & set up environment

```bash
git clone https://github.com/joshuvavinith/AI_ChatBot.git
cd AI_ChatBot
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. (Optional) Configure API key

Create a `.env` file in the project root:

```dotenv
OPENAI_API_KEY=sk-your-key-here
```

Or export it as an environment variable:

```bash
export OPENAI_API_KEY=sk-your-key-here
```

Without an API key the bot automatically falls back to offline pattern matching.

---

## ⚙️ Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENAI_API_KEY` | *(unset)* | Enables LLM mode when present |

### Kaggle Dataset (optional)

The pattern-matching bot can use a richer Kaggle dialog dataset.
To enable it, place `kaggle.json` in `~/.kaggle/` (or set `KAGGLE_USERNAME` / `KAGGLE_KEY`).
If unavailable, the bot falls back to `dialog.csv`.

---

## 💬 Running the Chatbot

### 🖥️ Desktop GUI (Tkinter)

```bash
python ai_chatbot.py
```

### 🌐 Web UI (Streamlit)

```bash
streamlit run web_demo.py
```

Open your browser at `http://localhost:8501`.

Features:
- Full conversation history
- Streaming token output in LLM mode (looks like ChatGPT)
- "Clear conversation" button in the sidebar

### 🔌 REST API (FastAPI)

```bash
uvicorn api:app --reload
```

Interactive docs available at `http://localhost:8000/docs`.

---

## 🐳 Docker

### Build

```bash
# Web UI (default)
docker build -t ai-chatbot:web .

# API mode
docker build --build-arg MODE=api -t ai-chatbot:api .
```

### Run

```bash
# Web UI — visit http://localhost:8501
docker run -p 8501:8501 -e OPENAI_API_KEY=sk-... ai-chatbot:web

# REST API — visit http://localhost:8000/docs
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... ai-chatbot:api
```

---

## 📡 API Reference

### `POST /chat`

Send a message and get a reply. Omit `session_id` to start a new session.

```json
// Request
{ "message": "Hello!", "session_id": "optional-uuid" }

// Response
{
  "reply": "Hi there! How can I help you?",
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "mode": "pattern"
}
```

### `DELETE /sessions/{session_id}`

Reset (delete) a conversation session.

### `POST /train`

Reload pattern-matching data from a CSV file on the server.

```json
// Request
{ "dialog_file": "/path/to/dialog.csv" }

// Response
{ "status": "retrained", "patterns_loaded": 42 }
```

### `GET /health`

```json
{ "status": "ok" }
```

---

## 🧪 Testing

```bash
pytest test_chatbot.py -v
```

The test suite covers:
- `SimpleBot` — training, exact/partial matching, defaults, missing file
- `ChatBot` — offline mode, history management, streaming, history cap, retraining
- FastAPI — all endpoints (health, chat, delete session, train)

---

## 🔄 CI/CD

GitHub Actions runs on every push and pull request to `main`:

1. **Lint** — `flake8` for syntax errors and undefined names
2. **Test** — `pytest` full suite
3. **Docker build** — both `web` and `api` images

---

## 📐 Architecture

```
+------------------+     +------------------+     +------------------+
|  Streamlit Web   |     |  FastAPI REST     |     |  Tkinter Desktop |
|  (web_demo.py)   |     |  (api.py)         |     |  (ai_chatbot.py) |
+--------+---------+     +--------+---------+     +--------+---------+
         |                        |                         |
         +------------------------+-------------------------+
                                  |
                         +--------v---------+
                         |    ChatBot       |  ← ai_chatbot.py
                         |  (facade)        |
                         +--+----------+----+
                            |          |
               +------------+          +------------+
               |                                    |
      +--------v---------+              +-----------v------+
      |   LLMBot         |              |   SimpleBot      |
      |  (OpenAI API)    |              |  (CSV patterns)  |
      +------------------+              +------------------+
```

---

## 🤝 Contributing

1. Fork this repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes and run `pytest test_chatbot.py -v`
4. Commit and push: `git push origin feature/my-feature`
5. Open a pull request

Please follow PEP 8 and include tests for any new logic.

---

## 📄 License

[MIT License](./LICENSE)

---

## 🔗 Connect

- 📧 [joshuvavinith.g@care.ac.in](mailto:joshuvavinith.g@care.ac.in)
- 🐙 [@joshuvavinith](https://github.com/joshuvavinith)
