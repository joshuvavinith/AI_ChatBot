
# 🤖 Python Chatbot with GUI (Tkinter + Kaggle Data)

## 🚀 Project Description  
Welcome to the **Python Chatbot Project with GUI**! This repository provides an interactive, intelligent chatbot built with **Python**, powered by **machine learning**, trained on **real dialog data from Kaggle**, and running inside a friendly **Tkinter-based desktop GUI**.

The chatbot learns from real conversations and responds contextually using machine learning. It’s perfect for beginners, students, or hobby projects.

---

## 📚 Table of Contents

- [Key Features](#-key-features)
- [Technologies Used](#-technologies-used)
- [Installation Instructions](#-installation-instructions)
- [Kaggle Dataset Setup](#-kaggle-dataset-setup)
- [Usage Example](#-usage-example)
- [Development Process](#-development-process)
- [Contributing Guidelines](#-contributing-guidelines)
- [Evaluation Metrics](#-evaluation-metrics)
- [Future Work](#-future-work)
- [Architecture Diagram](#-architecture-diagram)
- [Interaction with the Chatbot](#-interaction-with-the-chatbot)
- [Additional Information](#-additional-information)
- [Connect with Us](#-connect-with-us)

---

## ✨ Key Features

- 🧠 **ML-based chatbot** using ChatterBot and NLTK
- 💬 **Interactive GUI** built with Tkinter
- 📥 **Automatically downloads Kaggle dataset**
- 🔁 Trains on real conversation data at runtime
- ⚡ Lightweight, no external GUI dependencies required
- 🧩 Fallback to sample data if dataset isn't found

---

## 🛠️ Technologies Used

- **Python 3.6–3.8** (recommended for ChatterBot)
- **Tkinter** – Built-in GUI framework
- **ChatterBot** – Conversational AI library  
- **NLTK** – Natural language processing  
- **KaggleHub** – For downloading Kaggle datasets  
- **Git** – For version control  

> ⚠️ ChatterBot may not work properly with Python ≥3.9. Stick to Python 3.6–3.8 for stability.

---

## 🔧 Installation Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/joshuvavinith/AI_ChatBot.git
cd AI_ChatBot
```

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🔑 Kaggle Dataset Setup

This project uses the [Simple Dialogs for Chatbot](https://www.kaggle.com/datasets/grafstor/simple-dialogs-for-chatbot) dataset via **KaggleHub**.

### To enable Kaggle downloads:

1. Go to [kaggle.com/account](https://www.kaggle.com/account) and create an API token.
2. Download the `kaggle.json` file.
3. Place it in:

   - Linux/macOS: `~/.kaggle/kaggle.json`
   - Windows: `C:\Users\<YourUsername>\.kaggle\kaggle.json`

Alternatively, set environment variables:

```bash
export KAGGLE_USERNAME=your_username
export KAGGLE_KEY=your_key
```

> ✅ If the dataset can’t be downloaded, the chatbot will use fallback training data.

---

## 💬 Usage Example

### ▶️ To Run the GUI Chatbot:

```bash
python gui_chatbot.py
```

### 🖥️ GUI Features:

- Type your message in the input box
- Hit **Enter** or click **Send**
- The chatbot responds immediately
- Say `"bye"` or `"exit"` to end the chat

---

## 🧠 Development Process

1. **Dataset Retrieval**: Uses `kagglehub` to fetch dialog data from Kaggle
2. **Training**: Trains ChatterBot using NLTK preprocessed dialogs
3. **Interface**: Built with Tkinter for easy interaction
4. **Fallback**: Uses hardcoded sample training data if download fails

---

## 🤝 Contributing Guidelines

We welcome contributions! 🙌

### How to Contribute:

1. **Fork this repository**
2. Create a branch:

   ```bash
   git checkout -b feature-branch
   ```

3. Make your changes and commit:

   ```bash
   git commit -m "Add new feature"
   ```

4. Push and create a PR:

   ```bash
   git push origin feature-branch
   ```

> 💡 Follow Python best practices and test before submitting.

---

## 📈 Evaluation Metrics

- **BLEU Score** – Quality of generated response
- **Accuracy** – Expected vs actual answers
- **Responsiveness** – Time between input and output
- **User Feedback** – Manual quality testing

---

## 🌱 Future Work

- 🌐 Add API/web support for Flask or FastAPI
- 🧠 Switch to GPT/BERT for smarter conversations
- 🗣️ Voice integration with `speech_recognition`
- 💾 Save and reload previous conversation history
- 🖥️ Package as a desktop app using `pyinstaller`

---

## 📊 Architecture Diagram

```
+-------------+        +----------------------+        +-------------+
| User Input  +------->+    ChatBot Engine     +------->+ Bot Reply   |
+------+------+        +----------------------+        +-------------+
       |
       v
  [ Tkinter GUI ]
       |
       v
[ Kaggle Dataset Trainer ]
```

---

## 💬 Interaction with the Chatbot

The chatbot can be integrated or extended with:

- 📚 Custom datasets (CSV/TXT)
- ☁️ Cloud API support
- 🔊 Voice UI
- 💡 Smart context-based conversations

---

## 📱 Additional Information

- **Live Demo**: Coming soon!
- **License**: [MIT License](./LICENSE)

---

## 🔗 Connect with Us

- 📧 Email: [joshuvavinith.g@care.ac.in](mailto:joshuvavinith.g@care.ac.in)
- 🐙 GitHub: [@joshuvavinith](https://github.com/joshuvavinith)
