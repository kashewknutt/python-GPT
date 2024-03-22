import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

# Define some sample conversational data
conversations = [
    ("Hi", "Hello!"),
    ("How are you?", "I'm good, thank you."),
    ("What's your name?", "I'm a chatbot."),
    ("Bye", "Goodbye!"),
    # Add more conversations here
]

# Prepare data
questions = [pair[0] for pair in conversations]
answers = [pair[1] for pair in conversations]

# Tokenize input and output sequences
tokenizer = Tokenizer()
tokenizer.fit_on_texts(questions + answers)
vocab_size = len(tokenizer.word_index) + 1

# Convert text to sequences
question_sequences = tokenizer.texts_to_sequences(questions)
answer_sequences = tokenizer.texts_to_sequences(answers)

# Pad sequences to the same length for encoder and decoder inputs
max_sequence_length = max(len(seq) for seq in question_sequences + answer_sequences)
question_sequences = pad_sequences(question_sequences, maxlen=max_sequence_length, padding='post')
answer_sequences = pad_sequences(answer_sequences, maxlen=max_sequence_length, padding='post')

# Define the model
embedding_dim = 64
hidden_units = 128

# Define encoder model
encoder_inputs = tf.keras.layers.Input(shape=(max_sequence_length,))
encoder_embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim, mask_zero=True)(encoder_inputs)
encoder_outputs, state_h, state_c = tf.keras.layers.LSTM(hidden_units, return_state=True)(encoder_embedding)
encoder_states = [state_h, state_c]

# Define decoder model
decoder_inputs = tf.keras.layers.Input(shape=(max_sequence_length,))
decoder_embedding = tf.keras.layers.Embedding(vocab_size, embedding_dim, mask_zero=True)(decoder_inputs)
decoder_lstm = tf.keras.layers.LSTM(hidden_units, return_sequences=True, return_state=True)
decoder_outputs, _, _ = decoder_lstm(decoder_embedding, initial_state=encoder_states)
decoder_dense = tf.keras.layers.Dense(vocab_size, activation='softmax')
decoder_outputs = decoder_dense(decoder_outputs)

# Compile the model
model = tf.keras.models.Model([encoder_inputs, decoder_inputs], decoder_outputs)
model.compile(optimizer='adam', loss='sparse_categorical_crossentropy')

# Train the model
model.fit([question_sequences, answer_sequences[:, :-1]], answer_sequences[:, 1:], epochs=50, batch_size=32)

# Define encoder model for inference
encoder_model = tf.keras.models.Model(encoder_inputs, encoder_states)

# Define decoder model for inference
decoder_state_input_h = tf.keras.layers.Input(shape=(hidden_units,))
decoder_state_input_c = tf.keras.layers.Input(shape=(hidden_units,))
decoder_states_input = [decoder_state_input_h, decoder_state_input_c]
decoder_outputs, state_h, state_c = decoder_lstm(decoder_embedding, initial_state=decoder_states_input)
decoder_states = [state_h, state_c]
decoder_outputs = decoder_dense(decoder_outputs)
decoder_model = tf.keras.models.Model([decoder_inputs] + decoder_states_input, [decoder_outputs] + decoder_states)

# Define functions for inference
def preprocess_input(text):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=max_sequence_length, padding='post')
    return padded_sequence

def generate_response(input_text):
    input_sequence = preprocess_input(input_text)
    initial_states = encoder_model.predict(input_sequence)
    target_sequence = np.zeros((1, 1))
    target_sequence[0, 0] = tokenizer.word_index['<start>']
    stop_condition = False
    generated_sequence = ''
    while not stop_condition:
        output_tokens, h, c = decoder_model.predict([target_sequence] + initial_states)
        generated_token_index = np.argmax(output_tokens[0, -1, :])
        generated_word = tokenizer.index_word[generated_token_index]
        if generated_word == '<end>' or len(generated_sequence.split()) > max_sequence_length:
            stop_condition = True
        else:
            generated_sequence += generated_word + ' '
            target_sequence = np.zeros((1, 1))
            target_sequence[0, 0] = generated_token_index
            initial_states = [h, c]
    return generated_sequence.strip()

# Test the chatbot
print("Chatbot: Hi! How can I assist you today?")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Chatbot: Goodbye!")
        break
    response = generate_response(user_input)
    print("Chatbot:", response)
