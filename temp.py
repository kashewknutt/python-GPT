from flask import Flask, request, jsonify
from configparser import ConfigParser
from app import ChatBot

app = Flask(__name__)

# Load API key from configuration file
config = ConfigParser()
config.read('credentials.ini')
api_key = config['gemini_ai']['API_KEY']

# Create an instance of ChatBot
chatbot = ChatBot(api_key=api_key)

@app.route('/chat', methods=['POST'])
def chat():
    # Get user input from request
    user_input = request.json.get('user_input')

    if user_input:
        try:
            # Send user input to chatbot and get response
            response = chatbot.send_prompt(user_input)
            return jsonify({'response': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    else:
        return jsonify({'error': 'Missing user_input parameter'}), 400

if __name__ == '__main__':
    app.run(debug=True)
