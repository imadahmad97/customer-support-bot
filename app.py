from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=GOOGLE_API_KEY)
app = Flask(__name__)
CORS(app)

model = genai.GenerativeModel('gemini-pro')

global_context = """
This is a customer service bot designed to assist with inquiries about products and services offered by [Your Company Name]. It should provide accurate information, demonstrate patience, and maintain a polite and professional tone at all times. The bot should escalate issues it cannot resolve to human agents.
"""

@app.route('/chatbot', methods=['POST'])
def chatbot():
    user_input = request.json.get('user_input')
    if not user_input:
        return jsonify({'error': 'No user input provided'}), 400

    prompt = global_context + "\nCustomer: " + user_input + "\nBot:"
    response = model.generate_content(prompt)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)
