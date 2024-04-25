from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    current_app,
)
from flask_login import login_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
from .models import User
from .extensions import db


def init_routes(app):

    @app.route("/register", methods=["GET", "POST"])
    def register():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            email = request.form["email"]

            existing_user = User.query.filter_by(username=username).first()
            if existing_user:
                flash("Username already exists. Please choose a different one.")
                return redirect(url_for("register"))

            new_user = User(
                username=username,
                password_hash=generate_password_hash(password),
                email=email,
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Registration successful! Please log in.")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                return redirect(url_for("chat"))
            else:
                flash("Invalid username or password. Please try again.")
                return redirect(url_for("login"))
        return render_template("login.html")

    def configure_model():
        with app.app_context():
            genai.configure(api_key=current_app.config["GOOGLE_API_KEY"])
            model = genai.GenerativeModel("gemini-pro")
        return model

    @app.route("/model")
    def load_model():
        model = configure_model()
        return jsonify({"message": "Model configured"})

    @app.route("/questions")
    def questions():
        return render_template("questions.html")

    @app.route("/chat")
    @login_required
    def chat():
        return render_template("chat.html")

    @app.route("/get", methods=["POST"])
    def get_Chat_response():
        user_input = request.json.get("msg")
        global global_context
        if not user_input:
            return jsonify({"error": "No user input provided"}), 400

        try:
            model = configure_model()
            prompt = global_context + "Customer: " + user_input + "\nBot:"
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
        print(data)
        companyContext = data.get("companyContext")
        botInfo = data.get("botInfo")
        global global_context
        global_context = f"""
        This is a customer service bot designed to assist with inquiries about products and services offered by {companyContext}. It's name is {botInfo}
        """
        print(global_context)
        return global_context

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("login"))
