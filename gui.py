import tkinter as tk
from app import ChatBot
from configparser import ConfigParser

def send_message(event=None):
    user_input = entry.get()
    if user_input.lower() == 'exit':
        chat_area.insert(tk.END, 'Goodbye!\n')
        chat_area.yview(tk.END)
        return
    # Display user question
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, f'You: {user_input}\n', 'user_question')
    chat_area.config(state=tk.DISABLED)
    chat_area.yview(tk.END)
    # Get bot response
    try:
        response = chatbot.send_prompt(user_input)
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f'Rajat-AI: {response}\n', 'bot_response')
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)
    except Exception as e:
        chat_area.config(state=tk.NORMAL)
        chat_area.insert(tk.END, f'Error: {e}\n', 'error_message')
        chat_area.config(state=tk.DISABLED)
        chat_area.yview(tk.END)
    entry.delete(0, tk.END)

def main():
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['gemini_ai']['API_KEY']

    global chatbot
    chatbot = ChatBot(api_key=api_key)
    chatbot.start_conversation()

    root = tk.Tk()
    root.title("Rajat-AI Chatbot")

    # Make the window full-screen
    root.attributes('-fullscreen', True)

    # Set background color
    root.configure(bg='lightgrey')

    # Configure font styles
    entry_font = ('Arial', 12)
    chat_font = ('Arial', 12)

    # Configure colors
    bg_color = 'lightgrey'
    text_color = 'black'
    user_question_color = 'green'
    bot_response_color = 'blue'
    error_message_color = 'red'

    global entry, chat_area
    chat_area = tk.Text(root, bd=1, bg=bg_color, fg=text_color, font=chat_font, wrap=tk.WORD)
    chat_area.tag_config('user_question', foreground=user_question_color)
    chat_area.tag_config('bot_response', foreground=bot_response_color)
    chat_area.tag_config('error_message', foreground=error_message_color)
    chat_area.config(state=tk.DISABLED)
    chat_area.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

    # Insert initial welcome message
    chat_area.config(state=tk.NORMAL)
    chat_area.insert(tk.END, "Welcome to the Rajat-AI!\n", 'bot_response')
    chat_area.config(state=tk.DISABLED)

    entry = tk.Entry(root, font=entry_font)
    entry.pack(fill=tk.X, padx=20, pady=10)
    entry.bind("<Return>", send_message)  # Bind Enter key to send_message function

    send_button = tk.Button(root, text="Send", font=entry_font, bg='blue', fg='white', command=send_message)
    send_button.pack(side=tk.BOTTOM, padx=20, pady=10)

    root.mainloop()

main()
