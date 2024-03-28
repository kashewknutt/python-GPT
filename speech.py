import tkinter as tk
import requests
import speech_recognition as sr
import pyttsx3

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

        self.speech_button = tk.Button(self.input_frame, text="Speech Input", command=self.get_speech_input)
        self.speech_button.pack(side="left", padx=10)
   
        self.speak_button = tk.Button(self.input_frame, text="Speak Response", command=self.speak_response)
        self.speak_button.pack(side="left")

        self.api_endpoint = 'https://python-backend-three.vercel.app/api/chat'
        self.recognizer = sr.Recognizer()
        self.speaker = pyttsx3.init()

    def send_message(self):
        user_input = self.input_box.get()
        self.display_message(user_input, "You")
        self.input_box.delete(0, tk.END)
        
        bot_response = self.get_bot_response(user_input)
        self.display_message(bot_response, "Python-GPT:")
        self.speak_response()

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

    def recognize_speech(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source)

        try:
            print("Recognizing...")
            user_input = self.recognizer.recognize_google(audio)
            return user_input
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand what you said."
        except sr.RequestError as e:
            return f"Error: {e}"

    def speak_response(self):
        bot_response = self.message_list.get(tk.END).split(":")[1].strip()
        self.speak(bot_response)

    def get_speech_input(self):
        user_input = self.recognize_speech()
        self.input_box.delete(0, tk.END)
        self.input_box.insert(tk.END, user_input)

    def speak(self, text):
        self.speaker.say(text)
        self.speaker.runAndWait()

if __name__ == "__main__":
    root = tk.Tk()
    chatbot_gui = ChatBotGUI(root)
    root.mainloop()
