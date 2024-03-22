import tkinter as tk
from app import ChatBot
from configparser import ConfigParser

def send_message(chatbot, entry, chat_area):
    user_input = entry.get()
    if user_input.lower() == 'exit':
        chat_area.insert(tk.END, 'Goodbye!\n')
        chat_area.yview(tk.END)
        return
    try:
        response = chatbot.send_prompt(user_input)
        chat_area.config(state=tk.NORMAL)  # Enable editing temporarily
        chat_area.insert(tk.END, f'Rajat-AI: {response}\n')
        chat_area.config(state=tk.DISABLED)  # Disable editing again
        chat_area.yview(tk.END)
    except Exception as e:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f'Error: {e}\n')
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)
    entry.delete(0, tk.END)


def main():
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['gemini_ai']['API_KEY']

    chatbot = ChatBot(api_key=api_key)
    chatbot.start_conversation()

    root = tk.Tk()
    root.title("Rajat-AI Chatbot")

    chat_area = tk.Text(root, bd=1, bg="white", width=50, height=8, font=("Arial", 12))
    chat_area.insert(tk.END, "Welcome to the Rajat-AI!\n")
    chat_area.config(state=tk.DISABLED)
    chat_area.pack(pady=10)

    entry = tk.Entry(root, font=("Arial", 12))
    entry.pack(pady=10)

    send_button = tk.Button(root, text="Send", width=10, height=2, bg='blue', fg='white', command=lambda: send_message(chatbot, entry, chat_area))
    send_button.pack()

    root.mainloop()

main()
