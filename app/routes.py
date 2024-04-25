from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    current_app,
)
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
from .models import User, Chatbot
from .extensions import db


def init_routes(app):
    @app.route("/")
    def land():
        return redirect(url_for("login"))

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

    @app.route("/bots")
    @login_required
    def bots():
        chatbots = Chatbot.query.filter_by(user_id=current_user.get_id()).all()
        return render_template("bots.html", chatbots=chatbots)

    def configure_model():
        with app.app_context():
            genai.configure(api_key=current_app.config["GOOGLE_API_KEY"])
            model = genai.GenerativeModel("gemini-pro")
        return model

    @app.route("/questions", methods=["GET", "POST"])
    @login_required
    def questions():
        if request.method == "POST":
            data = request.get_json()
            companyContext = data.get("companyContext")
            botInfo = data.get("botInfo")
            botGoals = data.get("botGoals")
            issues = data.get("issues")
            botLang = data.get("botLang")
            print(issues)

            new_chatbot = Chatbot(
                user_id=current_user.id,
                context=companyContext + botInfo,
            )

            db.session.add(new_chatbot)
            db.session.commit()

            print("Chatbot created successfully!")
            return redirect(url_for("bots"))

        return render_template("questions.html")

    @app.route("/chat/<int:bot_id>")
    @login_required
    def chat_with_bot(bot_id):
        bot = Chatbot.query.get_or_404(bot_id)
        if bot.user_id != current_user.id:
            return redirect(url_for("bots"))
        initial_context = bot.context
        return render_template("chat.html", bot=bot, initial_context=initial_context)

    @app.route("/get/<int:bot_id>", methods=["POST"])
    @login_required
    def get_Chat_response(bot_id):
        bot = Chatbot.query.get_or_404(bot_id)
        if bot.user_id != current_user.id:
            return jsonify({"error": "Unauthorized access to bot"}), 403

        user_input = request.json.get("msg")
        if not user_input:
            return jsonify({"error": "No user input provided"}), 400

        try:
            model = configure_model()
            prompt = user_input
            print(prompt)
            response = model.generate_content(prompt)
            response_text = response._result.candidates[0].content.parts[0].text
            return jsonify({"response": response_text})
        except Exception as e:
            print("Failed to generate or parse response:", str(e))
            return jsonify({"error": "Failed to generate response"}), 500

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("login"))
