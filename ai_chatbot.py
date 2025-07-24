import os
import tkinter as tk
from tkinter import scrolledtext
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import kagglehub
import csv

# Download the dataset from Kaggle using kagglehub
print("Downloading chatbot data from Kaggle...")
data_path = kagglehub.dataset_download("grafstor/simple-dialogs-for-chatbot")

# Locate the conversation file (assuming 'questions.csv' and 'answers.csv')
dialog_file = os.path.join(data_path, "dialog.csv")

# Initialize chatbot
chatbot = ChatBot("GUIBot")
trainer = ListTrainer(chatbot)

# Load and train chatbot with Kaggle dataset
dialog_pairs = []
try:
    with open(dialog_file, encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 2:
                dialog_pairs.append(row[0])
                dialog_pairs.append(row[1])

    if dialog_pairs:
        print("Training chatbot with Kaggle data...")
        trainer.train(dialog_pairs)
except Exception as e:
    print(f"Error loading training data: {e}")

# Create GUI
root = tk.Tk()
root.title("Chat with GUIBot")
root.geometry("500x550")

chat_log = scrolledtext.ScrolledText(root, wrap=tk.WORD)
chat_log.config(state=tk.DISABLED)
chat_log.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

entry_frame = tk.Frame(root)
entry_frame.pack(padx=10, pady=10, fill=tk.X)

user_input = tk.Entry(entry_frame, font=("Arial", 14))
user_input.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))


def send_message():
    message = user_input.get()
    if message.strip():
        chat_log.config(state=tk.NORMAL)
        chat_log.insert(tk.END, "You: " + message + "\n")
        response = chatbot.get_response(message)
        chat_log.insert(tk.END, "Bot: " + str(response) + "\n\n")
        chat_log.config(state=tk.DISABLED)
        chat_log.yview(tk.END)
        user_input.delete(0, tk.END)

send_btn = tk.Button(entry_frame, text="Send", command=send_message)
send_btn.pack(side=tk.RIGHT)

user_input.bind("<Return>", lambda event=None: send_message())

root.mainloop()
