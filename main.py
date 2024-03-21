from configparser import ConfigParser
from app import ChatBot

def main():
    config = ConfigParser()
    config.read('credentials.ini')
    api_key = config['gemini_ai']['API_KEY']

    chatbot = ChatBot(api_key=api_key)
    chatbot.start_conversation()
    #chatbot.clear_conversation()

    print('Welcome to the Rajat-AI!')

    while True:
        user_input = input('You: ')
        if user_input.lower() == 'exit':
            print('Goodbye!')
            break

        try:
            response = chatbot.send_prompt(user_input)
            print(f'{chatbot.CHATBOT_NAME}: {response}')
        except Exception as e:
            print(f'Error: {e}')
main()