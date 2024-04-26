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
from .token import confirm_token, generate_token
from datetime import datetime
from .utils import send_email


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
                created_on=datetime.now(),
                is_admin=True,  # Ensure logical values are properly set; use True instead of 1 for clarity
                is_confirmed=False,  # Set as False initially, or True if you're confirming immediately
                confirmed_on=None,  # Set to None if not confirmed; change only when confirmed
            )

            db.session.add(new_user)
            db.session.commit()

            token = generate_token(new_user.email)
            confirm_url = url_for("confirm_email", token=token, _external=True)
            html = render_template("confirm_email.html", confirm_url=confirm_url)
            subject = "Please confirm your email"
            send_email(new_user.email, subject, html)

            flash("Registration successful! Please log in.")
            return redirect(url_for("login"))

        return render_template("register.html")

    @app.route("/confirm/<token>")
    def confirm_email(token):
        email = confirm_token(token)
        if not email:
            flash("The confirmation link is invalid or has expired.", "danger")
            return redirect(
                url_for("login")
            )  # Redirect to login instead of register to avoid confusion.

        user = User.query.filter_by(email=email).first()
        if user is None:
            flash("No account found for this email.", "danger")
            return redirect(url_for("register"))

        if user.is_confirmed:
            flash("Account already confirmed.", "success")
            return redirect(url_for("login"))

        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
        return redirect(url_for("login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        if request.method == "POST":
            username = request.form["username"]
            password = request.form["password"]
            user = User.query.filter_by(username=username).first()
            if (
                user
                and check_password_hash(user.password_hash, password)
                and user.is_confirmed
            ):
                login_user(user)
                return redirect(url_for("bots"))
            elif user and check_password_hash(user.password_hash, password):
                flash("Please verify your email")
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
