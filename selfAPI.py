import tkinter as tk
import requests

class ChatBotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("ChatBot")
        self.root.geometry("400x500")

        self.message_list = tk.Listbox(root, height=20, width=50, bg="lightgray")
        self.message_list.pack(pady=10)

        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.message_list.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.message_list.config(yscrollcommand=self.scrollbar.set)

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        self.input_box = tk.Entry(self.input_frame, width=40)
        self.input_box.pack(side="left", padx=10)

        self.send_button = tk.Button(self.input_frame, text="Send", command=self.send_message)
        self.send_button.pack(side="left")

        self.api_endpoint = 'https://python-backend-three.vercel.app/api/chat'

    def send_message(self):
        user_input = self.input_box.get()
        self.display_message(user_input, "You")
        self.input_box.delete(0, tk.END)
        
        bot_response = self.get_bot_response(user_input)
        self.display_message(bot_response, "Bot")

    def display_message(self, message, sender):
        self.message_list.insert(tk.END, f"{sender}: {message}")

    def get_bot_response(self, user_input):
        try:
            # Send user input to your API
            payload = {'content': user_input}  # Provide user input under the key 'content'
            response = requests.post(self.api_endpoint, json=payload)
            response.raise_for_status()  # Raise HTTPError for bad responses
            
            if response.status_code == 200:
                return response.json()["responseChat"]  # Extract response from JSON data
            else:
                return f"Error: Unexpected response {response.status_code}"
        except requests.exceptions.RequestException as e:
            return f"Error: Unable to connect to the chatbot service. {e}"


if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatBotGUI(root)
    root.mainloop()
