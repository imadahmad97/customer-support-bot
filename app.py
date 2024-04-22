from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
app = Flask(__name__)

def configure_model():
    print("Configuring model with API Key:", GOOGLE_API_KEY)
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    return model

model = configure_model()

global_context = """
This is a customer service bot designed to assist with inquiries about products and services offered by [Your Company Name].
"""

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    print("Received data:", request.json)
    user_input = request.json.get('msg')
    if not user_input:
        return jsonify({'error': 'No user input provided'}), 400
    return get_Chat_response(user_input)

def get_Chat_response(text):
    prompt = global_context + "\nCustomer: " + text + "\nBot:"
    response_object = model.generate_content(prompt)
    response_text = response_object.result['candidates'][0]['content']['parts'][0]['text']
    return jsonify({'response': response_text})


if __name__ == '__main__':
    app.run(debug=True)
