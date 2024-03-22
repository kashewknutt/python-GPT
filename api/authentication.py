from flask import Flask, request, jsonify
from pymongo import MongoClient
import json

app = Flask(__name__)

import bcrypt

# Connect to MongoDB
client = MongoClient('mongodb+srv://2022sanketdhuri:WKm6WEKmHe80Mgql@cluster0.91iy5uo.mongodb.net/python')
db = client['user_data']
user_collection = db['users']

# Function to hash passwords
def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

# Function to verify passwords
def verify_password(stored_password, provided_password):
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_password)

# API endpoint for user signup
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    if data:
        # Check if email/phone already exists
        existing_user = user_collection.find_one({"$or": [{"email": data['email']}, {"phone": data['phone']}]})
        if existing_user:
            return jsonify({"error": "Email/Phone already exists"}), 400
        else:
            # Hash the password before storing
            data['password'] = hash_password(data['password'])
            # Inserting user data into MongoDB
            user_id = user_collection.insert_one(data).inserted_id
            return jsonify({"message": "User registered successfully", "user_id": str(user_id)}), 201
    else:
        return jsonify({"error": "No data provided"}), 400

# API endpoint for user login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    if data:
        # Check if email/phone exists
        existing_user = user_collection.find_one({"$or": [{"email": data['email']}, {"phone": data['phone']}]})
        if existing_user:
            # Verify password
            if verify_password(existing_user['password'], data['password']):
                return jsonify({"message": "Login successful"}), 200
            else:
                return jsonify({"error": "Invalid password"}), 401
        else:
            return jsonify({"error": "User not found"}), 404
    else:
        return jsonify({"error": "No data provided"}), 400

if __name__ == '__main__':
    app.run(debug=True)
