import os
import tkinter as tk
from tkinter import scrolledtext
import csv
import random
import kagglehub

# Simple chatbot class using pattern matching
class SimpleBot:
    def __init__(self):
        self.responses = {}
        self.default_responses = [
            "I'm not sure I understand. Could you rephrase that?",
            "Interesting question! I'm still learning.",
            "I don't have an answer for that yet.",
            "Could you tell me more about that?"
        ]
    
    def train(self, dialog_file):
        try:
            with open(dialog_file, encoding="utf-8") as file:
                reader = csv.reader(file)
                next(reader)  # Skip header row
                current_dialog = None
                question = None
                
                for row in reader:
                    if len(row) >= 3:  # dialog_id, line_id, text
                        dialog_id = row[0]
                        line_id = row[1]
                        text = row[2]
                        
                        if line_id == '1':  # This is a question/prompt
                            question = text.lower()
                        elif line_id == '2' and question:  # This is a response
                            if question not in self.responses:
                                self.responses[question] = []
                            self.responses[question].append(text)
                            question = None
            print(f"Trained with {len(self.responses)} dialog patterns")
        except Exception as e:
            print(f"Error loading training data: {e}")
    
    def get_response(self, message):
        message = message.lower()
        
        # Check for exact matches
        if message in self.responses:
            return random.choice(self.responses[message])
        
        # Check for partial matches
        for pattern, responses in self.responses.items():
            if pattern in message or message in pattern:
                return random.choice(responses)
        
        # Return default response if no match
        return random.choice(self.default_responses)

# Initialize chatbot
chatbot = SimpleBot()

# Add method to parse Kaggle's dialogs.txt format
def parse_kaggle_dialogs(file_path):
    try:
        print(f"Parsing Kaggle dialogs from {file_path}...")
        dialog_pairs = []
        current_dialog_id = 0
        
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            
        # Create a temporary CSV file in the expected format
        temp_csv_path = os.path.join(os.path.dirname(file_path), "converted_dialog.csv")
        with open(temp_csv_path, 'w', encoding='utf-8') as f:
            f.write("dialog_id,line_id,text\n")
            
            for i in range(0, len(lines)-1, 2):
                if i+1 < len(lines):
                    question = lines[i].strip()
                    answer = lines[i+1].strip()
                    
                    if question and answer:
                        current_dialog_id += 1
                        f.write(f"{current_dialog_id},1,{question}\n")
                        f.write(f"{current_dialog_id},2,{answer}\n")
        
        print(f"Converted {current_dialog_id} dialog pairs to CSV format")
        return temp_csv_path
    except Exception as e:
        print(f"Error parsing Kaggle dialogs: {e}")
        return None

# Try to download the dataset from Kaggle using kagglehub
try:
    print("Attempting to download chatbot data from Kaggle...")
    data_path = kagglehub.dataset_download("grafstor/simple-dialogs-for-chatbot")
    
    # Look for dialogs.txt (the actual file in the dataset)
    for root, dirs, files in os.walk(data_path):
        for file in files:
            if file.lower() == "dialogs.txt":
                kaggle_dialog_file = os.path.join(root, file)
                print(f"Found Kaggle dialog file: {kaggle_dialog_file}")
                
                # Convert the Kaggle format to our expected CSV format
                converted_file = parse_kaggle_dialogs(kaggle_dialog_file)
                if converted_file:
                    print("Training chatbot with Kaggle data...")
                    chatbot.train(converted_file)
                    break
        else:
            continue
        break
    else:
        raise FileNotFoundError("Dialog file not found in Kaggle dataset")
        
except Exception as e:
    print(f"Error with Kaggle dataset: {e}")
    print("Falling back to local dialog data...")
    
    # Fallback to local dialog.csv file
    local_dialog_file = "dialog.csv"
    try:
        print("Training chatbot with local dialog data...")
        chatbot.train(local_dialog_file)
    except Exception as e:
        print(f"Error loading local training data: {e}")

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

# Add a welcome message
chat_log.config(state=tk.NORMAL)
chat_log.insert(tk.END, "Bot: Hello! I'm your simple chatbot. How can I help you today?\n\n")
chat_log.config(state=tk.DISABLED)

print("Starting GUI chatbot...")
root.mainloop()
