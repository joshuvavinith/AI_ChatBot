
# 🤖 Python Chatbot with GUI (Tkinter)

## 🚀 Project Description  
Welcome to the **Python Chatbot Project with GUI**! This repository provides a simple but intelligent chatbot built with **Python**, powered by **machine learning**, and integrated into a **Tkinter-based desktop GUI**. The chatbot learns from interactions and provides context-aware responses.

---

## 📚 Table of Contents

- [Key Features](#-key-features)
- [Technologies Used](#-technologies-used)
- [Installation Instructions](#-installation-instructions)
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
- 🗣️ Responds with context-aware answers from trained conversations
- 🔁 Extendable and adaptable for various domains
- ⚡ Lightweight, no external GUI dependencies required

---

## 🛠️ Technologies Used

- **Python**  
- **Tkinter** – GUI library (built-in)
- **ChatterBot** – Conversational engine  
- **NLTK** – Natural Language Toolkit for tokenization  
- **Git** – Version control and collaboration  

> ⚠️ **Note**: ChatterBot may have compatibility issues on Python 3.9+. Use Python 3.6–3.8 for the best experience.

---

## 🔧 Installation Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/joshuvavinith/AI_ChatBot.git
cd AI_ChatBot
````

### 2. Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

> ✅ `nltk` data is downloaded automatically the first time the app runs.

---

## 💬 Usage Example

### ▶️ To Run the Chatbot GUI:

```bash
python gui_chatbot.py
```

### 🖥️ GUI Features:

* Type your message and press **Enter** or click **Send**
* Chatbot responds instantly
* Say `"bye"` or `"exit"` to end the chat

---

## 🧠 Development Process

1. **Data Preprocessing**: Tokenization using NLTK.
2. **Training**: The chatbot is trained using `ListTrainer` on a simple conversation list.
3. **Interface**: Tkinter GUI handles user input and bot responses.

---

## 🤝 Contributing Guidelines

We welcome contributions! 🚀

### To Contribute:

1. **Fork this repo**
2. **Create a new branch** for your feature:

   ```bash
   git checkout -b feature-name
   ```
3. **Make changes** and commit:

   ```bash
   git commit -m "Add new feature or fix bug"
   ```
4. **Push your branch** and create a pull request:

   ```bash
   git push origin feature-name
   ```

> 💡 Please follow code conventions and test your contributions.

---

## 📈 Evaluation Metrics

* **Responsiveness**: Delay between input and response
* **Accuracy**: Quality of response compared to expected output
* **User Experience**: Manual testing for usability and flow

---

## 🌱 Future Work

Planned enhancements:

* 🎨 Add themes and styling with `ttk` or `ttkbootstrap`
* 🧠 Switch to GPT/transformer-based model for more realistic replies
* 🗣️ Add voice input/output integration
* ☁️ Package as a standalone `.exe` or Mac app

---

## 📊 Architecture Diagram

```
+-------------+        +-----------------+        +-------------+
| User Input  +------->+   ChatBot Core  +------->+ Bot Response|
+------+------+        +-----------------+        +-------------+
       |
       v
  [Tkinter GUI]
```

> 🧠 This project combines ChatterBot's NLP engine with a live Tkinter interface.

---

## 💬 Interaction with the Chatbot

This chatbot can be integrated into other apps or enhanced with:

* 🧠 Custom datasets for domain-specific training
* 🔌 API wrappers for web integration
* 🖼️ Voice UI or advanced GUI frameworks

---

## 📱 Additional Information

* **Demo**: Coming soon!
* **License**: This project is licensed under the [MIT License](./LICENSE).

---

## 🔗 Connect with Us

* 📧 Email: [joshuvavinith@pm.me](mailto:joshuvavinith.g@care.ac.in)
* 🐱 GitHub: [joshuvavinith](https://github.com/joshuvavinith)

---


