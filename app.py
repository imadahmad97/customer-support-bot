import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
app = Flask(__name__)

def configure_model():
    """
    Configures and returns a Generative AI model with the specified API key.

    Returns:
        object: A GenerativeModel instance ready to generate content.
    """
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    return model

model = configure_model()

@app.route("/")
def index():
    """
    Render the main chat interface page.

    Returns:
        str: HTML content of the chat interface.
    """
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    """
    Endpoint to process incoming messages from the user and generate responses.

    Returns:
        json: JSON object containing the generated response or error message.
    """
    print("Received data:", request.json)
    user_input = request.json.get('msg')
    if not user_input:
        return jsonify({'error': 'No user input provided'}), 400
    return get_Chat_response(user_input)

def get_Chat_response(text):
    """
    Generates a response to the user's input using the global context and the configured model.

    Args:
        text (str): User's input text to which the bot should respond.

    Returns:
        json: JSON object containing the bot's text response or an error message.
    """
    global global_context
    prompt = global_context + "\nCustomer: " + text + "\nBot:"
    try:
        response = model.generate_content(prompt)
        response_text = response._result.candidates[0].content.parts[0].text
        return jsonify({'response': response_text})
    except Exception as e:
        print("Failed to generate or parse response:", str(e))
        return jsonify({'error': 'Failed to generate response'}), 500

@app.route("/setContext", methods=["POST"])
def set_context():
    """
    Updates the global context used by the chatbot based on user-provided 
    company name and bot introduction.

    Returns:
        json: JSON object confirming the context update or an error message.
    """
    data = request.get_json()
    company_context = data.get('companyContext')
    bot_info = data.get('botInfo')
    botGoals = data.get('botGoals')
    botLang = data.get('botLang')
    global global_context
    global_context = f"""
    This is a customer service bot designed to assist with inquiries about products and services offered by a company. Here is some company context: {company_context}. 
    Here's some info about how you should act: {bot_info}. And here are is a summary for your purpose and goals: {botGoals}.
    """
    return jsonify({'message': 'Context updated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
