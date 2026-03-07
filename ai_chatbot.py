"""
AI ChatBot — core module.

Supports two backends, selected automatically:
  1. LLM backend  – uses the OpenAI Chat Completions API when an
                    OPENAI_API_KEY environment variable (or .env file) is present.
  2. Pattern-matching backend – offline fallback using a CSV dialog dataset.

The public surface area is intentionally small so that web_demo.py and
api.py can both import from this module without pulling in Tkinter.
"""

import csv
import os
import random
from typing import Optional

# Load .env variables if python-dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# ---------------------------------------------------------------------------
# Pattern-matching backend
# ---------------------------------------------------------------------------


class SimpleBot:
    """Offline chatbot backed by a CSV dialog dataset."""

    def __init__(self) -> None:
        self.responses: dict[str, list[str]] = {}
        self.default_responses: list[str] = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting question! I'm still learning.",
            "I don't have an answer for that yet.",
            "Could you tell me more about that?",
        ]

    def train(self, dialog_file: str) -> None:
        try:
            with open(dialog_file, encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # skip header
                question: Optional[str] = None

                for row in reader:
                    if len(row) >= 3:
                        line_id = row[1]
                        text = row[2]

                        if line_id == "1":
                            question = text.lower()
                        elif line_id == "2" and question:
                            self.responses.setdefault(question, []).append(text)
                            question = None

            print(f"Trained with {len(self.responses)} dialog patterns")
        except Exception as exc:
            print(f"Error loading training data: {exc}")

    def get_response(self, message: str, history: Optional[list] = None) -> str:
        """Return a pattern-matched reply.  *history* is accepted but unused."""
        key = message.lower()

        if key in self.responses:
            return random.choice(self.responses[key])

        for pattern, replies in self.responses.items():
            if pattern in key or key in pattern:
                return random.choice(replies)

        return random.choice(self.default_responses)


# ---------------------------------------------------------------------------
# LLM backend (OpenAI)
# ---------------------------------------------------------------------------

class LLMBot:
    """Chatbot backed by the OpenAI Chat Completions API."""

    SYSTEM_PROMPT = (
        "You are a helpful, friendly, and concise AI assistant. "
        "Answer clearly and stay on topic."
    )

    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo") -> None:
        from openai import OpenAI  # deferred import so SimpleBot works without openai
        self.model = model
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def get_response(self, message: str, history: Optional[list] = None) -> str:
        """Call the OpenAI API and return the assistant reply.

        *history* is a list of ``{"role": ..., "content": ...}`` dicts
        representing the conversation so far (not including the current message).
        """
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": message})

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=512,
            temperature=0.7,
        )
        return completion.choices[0].message.content.strip()

    def stream_response(self, message: str, history: Optional[list] = None):
        """Yield response tokens one by one (for streaming UIs)."""
        messages = [{"role": "system", "content": self.SYSTEM_PROMPT}]
        if history:
            messages.extend(history)
        messages.append({"role": "user", "content": message})

        stream = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=512,
            temperature=0.7,
            stream=True,
        )
        for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta


# ---------------------------------------------------------------------------
# Unified ChatBot facade
# ---------------------------------------------------------------------------

class ChatBot:
    """High-level chatbot that auto-selects LLM or pattern-matching backend.

    Priority:
      1. Use LLMBot if ``OPENAI_API_KEY`` is set.
      2. Fall back to SimpleBot otherwise.

    Conversation history is maintained internally so callers only need to
    pass the current user message.
    """

    MAX_HISTORY = 20  # keep last N turns in context

    def __init__(self, dialog_file: Optional[str] = None, force_offline: bool = False) -> None:
        self.history: list[dict] = []
        self._llm: Optional[LLMBot] = None
        self._simple: Optional[SimpleBot] = None

        if not force_offline and os.environ.get("OPENAI_API_KEY"):
            try:
                self._llm = LLMBot()
                print("Using LLM backend (OpenAI).")
            except Exception as exc:
                print(f"LLM init failed ({exc}), falling back to pattern-matching.")

        if self._llm is None:
            self._simple = SimpleBot()
            self._load_training_data(dialog_file)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    @property
    def mode(self) -> str:
        return "llm" if self._llm else "pattern"

    def chat(self, message: str) -> str:
        """Process *message* and return a reply; history is updated automatically."""
        if self._llm:
            reply = self._llm.get_response(message, self.history)
        else:
            reply = self._simple.get_response(message, self.history)  # type: ignore[union-attr]

        self._update_history(message, reply)
        return reply

    def stream_chat(self, message: str):
        """Yield response tokens (LLM mode) or yield the full reply at once."""
        if self._llm:
            tokens: list[str] = []
            for token in self._llm.stream_response(message, self.history):
                tokens.append(token)
                yield token
            reply = "".join(tokens)
        else:
            reply = self._simple.get_response(message, self.history)  # type: ignore[union-attr]
            yield reply

        self._update_history(message, reply)

    @property
    def pattern_count(self) -> int:
        """Number of dialog patterns loaded (0 in LLM mode)."""
        return len(self._simple.responses) if self._simple else 0

    def reset_history(self) -> None:
        self.history.clear()

    def train(self, dialog_file: str) -> None:
        """Retrain the pattern-matching bot from a CSV file."""
        if self._simple:
            self._simple.train(dialog_file)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    def _update_history(self, user_msg: str, bot_reply: str) -> None:
        self.history.append({"role": "user", "content": user_msg})
        self.history.append({"role": "assistant", "content": bot_reply})
        # Trim to avoid unbounded growth
        if len(self.history) > self.MAX_HISTORY * 2:
            self.history = self.history[-(self.MAX_HISTORY * 2):]

    def _load_training_data(self, dialog_file: Optional[str]) -> None:
        if dialog_file and os.path.exists(dialog_file):
            self._simple.train(dialog_file)  # type: ignore[union-attr]
            return

        # Try Kaggle dataset first, fall back to local dialog.csv
        try:
            import kagglehub
            print("Attempting to download chatbot data from Kaggle...")
            data_path = kagglehub.dataset_download("grafstor/simple-dialogs-for-chatbot")

            for root_dir, _, files in os.walk(data_path):
                for fname in files:
                    if fname.lower() == "dialogs.txt":
                        kaggle_file = os.path.join(root_dir, fname)
                        converted = _parse_kaggle_dialogs(kaggle_file)
                        if converted:
                            print("Training chatbot with Kaggle data...")
                            self._simple.train(converted)  # type: ignore[union-attr]
                            return
            raise FileNotFoundError("dialogs.txt not found in Kaggle dataset")

        except Exception as exc:
            print(f"Kaggle dataset unavailable ({exc}), using local data.")

        local = os.path.join(os.path.dirname(__file__), "dialog.csv")
        if os.path.exists(local):
            print("Training chatbot with local dialog data...")
            self._simple.train(local)  # type: ignore[union-attr]
        else:
            print("No training data found; bot will use default responses only.")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _parse_kaggle_dialogs(file_path: str) -> Optional[str]:
    """Convert Kaggle's dialogs.txt into the CSV format expected by SimpleBot."""
    try:
        print(f"Parsing Kaggle dialogs from {file_path}...")
        with open(file_path, "r", encoding="utf-8") as fh:
            lines = fh.readlines()

        temp_csv_path = os.path.join(os.path.dirname(file_path), "converted_dialog.csv")
        dialog_id = 0
        with open(temp_csv_path, "w", encoding="utf-8", newline="") as fh:
            writer = csv.writer(fh)
            writer.writerow(["dialog_id", "line_id", "text"])
            for i in range(0, len(lines) - 1, 2):
                q, a = lines[i].strip(), lines[i + 1].strip()
                if q and a:
                    dialog_id += 1
                    writer.writerow([dialog_id, 1, q])
                    writer.writerow([dialog_id, 2, a])

        print(f"Converted {dialog_id} dialog pairs to CSV format")
        return temp_csv_path
    except Exception as exc:
        print(f"Error parsing Kaggle dialogs: {exc}")
        return None


# ---------------------------------------------------------------------------
# Tkinter GUI  (only runs when this file is executed directly)
# ---------------------------------------------------------------------------

def _run_gui() -> None:
    import tkinter as tk
    from tkinter import scrolledtext

    bot = ChatBot()

    gui_root = tk.Tk()
    gui_root.title("Chat with AI Bot")
    gui_root.geometry("500x580")

    # ── mode badge ──────────────────────────────────────────────────────────
    mode_label = tk.Label(
        gui_root,
        text=f"Mode: {'🤖 LLM (OpenAI)' if bot.mode == 'llm' else '📋 Pattern Matching'}",
        font=("Arial", 10),
        fg="#555",
    )
    mode_label.pack(anchor="w", padx=12, pady=(6, 0))

    # ── chat log ────────────────────────────────────────────────────────────
    chat_log = scrolledtext.ScrolledText(gui_root, wrap=tk.WORD)
    chat_log.config(state=tk.DISABLED)
    chat_log.pack(padx=10, pady=6, fill=tk.BOTH, expand=True)

    # ── input row ───────────────────────────────────────────────────────────
    entry_frame = tk.Frame(gui_root)
    entry_frame.pack(padx=10, pady=10, fill=tk.X)

    user_input = tk.Entry(entry_frame, font=("Arial", 14))
    user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

    def send_message() -> None:
        message = user_input.get().strip()
        if not message:
            return
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, f"You: {message}\n")
        user_input.delete(0, tk.END)

        response = bot.chat(message)
        chat_log.insert(tk.END, f"Bot: {response}\n\n")
        chat_log.config(state=tk.DISABLED)
        chat_log.yview(tk.END)

    send_btn = tk.Button(entry_frame, text="Send", command=send_message)
    send_btn.pack(side=tk.RIGHT)

    user_input.bind("<Return>", lambda _: send_message())

    # ── welcome message ─────────────────────────────────────────────────────
    chat_log.config(state=tk.NORMAL)
    chat_log.insert(tk.END, "Bot: Hello! I'm your AI chatbot. How can I help you today?\n\n")
    chat_log.config(state=tk.DISABLED)

    print("Starting GUI chatbot...")
    gui_root.mainloop()


if __name__ == "__main__":
    _run_gui()
