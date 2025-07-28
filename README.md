
# 🤖 Simple Python Chatbot with GUI (Tkinter)

## 🚀 Project Description  
Welcome to the **Simple Python Chatbot Project with GUI**! This repository provides an interactive chatbot built with **Python**, using pattern matching on a dialog dataset from Kaggle, and running inside a friendly **Tkinter-based desktop GUI**.

The chatbot uses a simple but effective pattern matching approach to respond to user queries based on a dataset of over 1,700 dialog patterns. It automatically downloads a rich conversation dataset from Kaggle to provide more natural and varied responses. If Kaggle is unavailable, it falls back to a local dataset. It's perfect for beginners, students, or hobby projects.

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

- 🔍 **Pattern matching chatbot** using simple but effective techniques
- 💬 **Interactive GUI** built with Tkinter
- 📥 **Kaggle dataset integration** with automatic download
- 📝 **Fallback to local dialog dataset** if Kaggle is unavailable
- 🔁 Supports exact and partial matching for better responses
- ⚡ Lightweight with minimal external dependencies
- 🧩 Easily extensible by adding more dialog patterns

---

## 🛠️ Technologies Used

- **Python 3.x** – Works with any modern Python version
- **Tkinter** – Built-in GUI framework
- **KaggleHub** – For downloading Kaggle datasets
- **CSV** – For reading dialog data
- **Random** – For selecting varied responses
- **Git** – For version control

> ✅ This implementation uses minimal external dependencies, with KaggleHub being the only non-standard library required. The core functionality works even without internet access by falling back to local data.

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

This project uses the [Simple Dialogs for Chatbot](https://www.kaggle.com/datasets/grafstor/simple-dialogs-for-chatbot) dataset via **KaggleHub**. The dataset contains over 1,800 conversation pairs that significantly enhance the chatbot's response capabilities.

### Dataset Features:

- 1,800+ question-answer pairs
- Covers a wide range of casual conversation topics
- Automatically downloaded and processed at runtime
- Converted from TXT to CSV format for compatibility

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

> ✅ If the dataset can't be downloaded, the chatbot will automatically fall back to the local dialog.csv file with basic conversation patterns.

---

## 💬 Usage Example

### ▶️ To Run the GUI Chatbot:

```bash
python ai_chatbot.py
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
