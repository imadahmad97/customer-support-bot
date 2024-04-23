from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    current_app,
)
from werkzeug.security import generate_password_hash
import google.generativeai as genai
from .models import User
from .extensions import db


def init_routes(app):

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            roles = request.form.get("roles", "")
            description = request.form.get("description", "")

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Username already exists. Please choose a different one.")
                return redirect(url_for("register"))

            new_user = User(
                username=username,
                password_hash=generate_password_hash(password),
                roles=roles,
                description=description,
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Please log in.")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        return render_template("login.html")

    def configure_model():
        with app.app_context():  # Ensures this is called within an app context
            genai.configure(api_key=current_app.config["GOOGLE_API_KEY"])
            model = genai.GenerativeModel("gemini-pro")
        return model

    # Instantiate the model when needed, ideally in a route or background task
    @app.route("/model")
    def load_model():
        model = configure_model()
        return jsonify({"message": "Model configured"})

    @app.route("/")
    def index():
        return render_template("chat.html")

    @app.route("/get", methods=["POST"])
    def get_Chat_response():
        user_input = request.json.get("msg")
        if not user_input:
            return jsonify({"error": "No user input provided"}), 400

        try:
            model = configure_model()  # Ensure model is configured correctly
            prompt = "Customer: " + user_input + "\nBot:"
            response = model.generate_content(prompt)
            response_text = response._result.candidates[0].content.parts[0].text
            return jsonify({"response": response_text})
        except Exception as e:
            print("Failed to generate or parse response:", str(e))
            return jsonify({"error": "Failed to generate response"}), 500

    def chat():
        print("Received data:", request.json)
        user_input = request.json.get("msg")
        if not user_input:
            return jsonify({"error": "No user input provided"}), 400
        model = configure_model()
        return get_Chat_response(user_input)

    @app.route("/setContext", methods=["POST"])
    def set_context():
        data = request.get_json()
        global_context = "Info about the bot and its context..."
        return jsonify({"message": "Context updated successfully"})
