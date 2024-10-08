from flask import (
    render_template,
    request,
    redirect,
    url_for,
    flash,
    jsonify,
    current_app,
    session,
)
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import google.generativeai as genai
from .models import User, Chatbot
from .extensions import db
from .token import confirm_token, generate_token
from datetime import datetime
from .utils import send_email, upload_file_to_gcs
import json
from flask_dance.contrib.google import make_google_blueprint, google
import stripe


def init_routes(app):

    google_bp = make_google_blueprint(
        client_id=app.config["GOOGLE_CLIENT_ID"],
        client_secret=app.config["GOOGLE_CLIENT_SECRET"],
        redirect_to="google_login_callback",
        scope=[
            "https://www.googleapis.com/auth/userinfo.profile",
            "https://www.googleapis.com/auth/userinfo.email",
            "openid",
        ],
    )
    app.register_blueprint(google_bp, url_prefix="/login")

    @app.route("/")
    def land():
        return render_template("index.html")

    @app.route("/login/google_login_callback")
    def google_login_callback():
        if not google.authorized:
            return "Access Denied", 403

        resp = google.get("/oauth2/v2/userinfo")
        if resp.ok:
            user_info = resp.json()
            user = User.query.filter_by(email=user_info["email"]).first()
            if not user:
                email = user_info["email"]
                username = email.split("@")[0]
                user = User(
                    username=username,
                    password_hash="google_login_account",
                    email=user_info["email"],
                    created_on=datetime.now(),
                    is_admin=True,
                    is_confirmed=True,
                    confirmed_on=datetime.now(),
                )
                db.session.add(user)
                db.session.commit()

            login_user(user)

            # Check if the user is subscribed
            if not user.is_subscribed:
                # Redirect to the subscription page if not subscribed
                return redirect(url_for("create_checkout_session", email=user.email))

            return redirect(url_for("bots"))

        return "Failed to fetch user info", 500

    @app.route("/confirm_email")
    def post_registration():
        return render_template("post_registration.html")

    @app.route("/liveness_check")
    def liveness_check():
        return "OK", 200

    @app.route("/readiness_check")
    def readiness_check():
        return "OK", 201

    @app.route("/confirm/<token>")
    def confirm_email(token):
        email = confirm_token(token)
        if not email:
            print("The confirmation link is invalid or has expired.", "danger")
            return redirect(url_for("login_register"))

        user = User.query.filter_by(email=email).first()
        if user is None:
            print("No account found for this email.", "danger")
            return redirect(url_for("login_register"))

        if user.is_confirmed:
            print("Account already confirmed.", "success")
            return redirect(url_for("login_register"))

        print("Is confirmed before:", user.is_confirmed)
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        print("Is confirmed after:", user.is_confirmed)

        try:
            db.session.commit()
            print("You have confirmed your account. Thanks!", "success")
        except Exception as e:
            db.session.rollback()
            print(str(e), "error")
            return redirect(url_for("login_register"))

        return redirect(url_for("login_register"))

    @app.route("/login", methods=["GET", "POST"])
    def login_register():
        if request.method == "POST":
            action = request.form.get("action")
            if action == "Login with Google":
                return redirect(url_for("google.login"))
            elif action == "Register":
                username = request.form["username"]
                password = request.form["password"]
                email = request.form["email"]

                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    flash("Username already exists. Please choose a different one.")
                    return redirect(url_for("login_register"))

                new_user = User(
                    username=username,
                    password_hash=generate_password_hash(password),
                    email=email,
                    created_on=datetime.now(),
                    is_admin=True,
                    is_confirmed=False,
                    confirmed_on=None,
                )

                db.session.add(new_user)
                db.session.commit()

                token = generate_token(new_user.email)
                confirm_url = url_for("confirm_email", token=token, _external=True)
                html = render_template("confirm_email.html", confirm_url=confirm_url)
                subject = "Please confirm your email"
                send_email(new_user.email, subject, html)

                flash("Registration successful! Please proceed to the payment.")
                return redirect(url_for("create_checkout_session", email=email))

            elif action == "Login":
                username = request.form["username"]
                password = request.form["password"]
                user = User.query.filter_by(username=username).first()
                if user and check_password_hash(user.password_hash, password):
                    print("1")
                    if user.is_confirmed:
                        login_user(user)
                        return redirect(url_for("bots"))
                    else:
                        print("2")
                        flash("Please verify your email")
                else:
                    print("3")
                    flash("Invalid username or password. Please try again.")
                    return redirect(url_for("login_register"))
        return render_template("login.html")

    @app.route("/public-chat/<int:bot_id>")
    def public_chat(bot_id):
        bot = Chatbot.query.get_or_404(bot_id)
        bot = Chatbot.query.get_or_404(bot_id)
        if bot.user_id != current_user.id:
            return redirect(url_for("bots"))
        initial_context = json.loads(bot.context)
        chatbot_Name = bot.chatbotName
        cardBgColor = bot.cardBgColor
        avatar_url = bot.avatar_url
        return render_template(
            "public_chat.html",
            bot=bot,
            chatbot_intro_name=initial_context["chatbot_intro_name"],
            chatbot_name=chatbot_Name,
            company_name=initial_context["company_name"],
            company_description=initial_context["company_description"],
            products_services=initial_context["products_services"],
            customer_description=initial_context["customer_description"],
            greeting_phrase=initial_context["greeting_phrase"],
            issues=initial_context["issues"],
            card_bg_color=cardBgColor,
            avatar_url=avatar_url,
        )

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

    @app.route("/chat_preview")
    def chat_preview():
        bot = Chatbot.query.get_or_404(12)
        chatbotName = bot.chatbotName
        initial_context = bot.context
        cardBgColor = bot.cardBgColor
        avatar_url = bot.avatar_url
        return render_template(
            "chat_preview.html",
            bot=bot,
            chatbotName=chatbotName,
            initial_context=initial_context,
            card_bg_color=cardBgColor,
            avatar_url=avatar_url,
        )

    @app.route("/submit-initial-config", methods=["GET", "POST"])
    def submit_initial_config():
        if "avatar" in request.files:
            file = request.files["avatar"]
            if file.filename != "":
                output = upload_file_to_gcs(file)
                if output is not None:
                    session["initial_config"] = request.form.to_dict()
                    session["avatar_url"] = output
                else:
                    flash("Failed to upload avatar.", "error")
            else:
                session["initial_config"] = request.form.to_dict()

        return jsonify(status="success"), 200

    @app.route("/create-new-bot", methods=["GET", "POST"])
    def create_new_bot():
        if request.method == "POST":
            initial_config = session.pop("initial_config", {})
            default_avatar_url = "https://i.ibb.co/nbjZnHd/chatbot.png"
            avatar_url = session.pop("avatar_url", default_avatar_url)

            detailed_info = request.get_json()

            context_data = {
                "chatbot_intro_name": detailed_info.get(
                    "chatbot_intro_name", "default_chatbot_name"
                ),
                "company_name": detailed_info.get(
                    "company_name", "default_company_name"
                ),
                "company_description": detailed_info.get(
                    "company_description", "default_company_description"
                ),
                "products_services": detailed_info.get(
                    "products_services", "default_products_services"
                ),
                "customer_description": detailed_info.get(
                    "customer_description", "default_customer_description"
                ),
                "greeting_phrase": detailed_info.get(
                    "greeting_phrase", "default_greeting_phrase"
                ),
                "issues": detailed_info.get("issues", []),
            }

            context_json = json.dumps(context_data)

            new_chatbot = Chatbot(
                user_id=current_user.id,
                context=context_json,
                chatbotName=initial_config.get("chatbotName", "ChatBot"),
                cardBgColor=initial_config.get("cardBgColor", "#FFFFFF"),
                avatar_url=avatar_url,
            )

            db.session.add(new_chatbot)
            db.session.commit()

            return redirect(url_for("bots"))

        return render_template("create_chatbot.html")

    @app.route("/chat/<int:bot_id>")
    @login_required
    def chat_with_bot(bot_id):
        bot = Chatbot.query.get_or_404(bot_id)
        if bot.user_id != current_user.id:
            return redirect(url_for("bots"))
        initial_context = json.loads(bot.context)
        chatbot_Name = bot.chatbotName
        cardBgColor = bot.cardBgColor
        avatar_url = bot.avatar_url
        return render_template(
            "chat.html",
            bot=bot,
            chatbot_intro_name=initial_context["chatbot_intro_name"],
            chatbot_name=chatbot_Name,
            company_name=initial_context["company_name"],
            company_description=initial_context["company_description"],
            products_services=initial_context["products_services"],
            customer_description=initial_context["customer_description"],
            greeting_phrase=initial_context["greeting_phrase"],
            issues=initial_context["issues"],
            card_bg_color=cardBgColor,
            avatar_url=avatar_url,
        )

    @app.route("/get/<int:bot_id>", methods=["POST"])
    @login_required
    def get_Chat_response(bot_id):
        bot = Chatbot.query.get_or_404(bot_id)
        if bot.user_id != current_user.id:
            return jsonify({"error": "Unauthorized access to bot"}), 403

        user_input = request.json.get("msg")
        if not user_input:
            return jsonify({"error": "No user input provided"}), 400

        while True:
            try:
                model = configure_model()
                prompt = user_input
                response = model.generate_content(
                    prompt,
                    generation_config=genai.types.GenerationConfig(
                        max_output_tokens=400
                    ),
                )
                response_text = response._result.candidates[0].content.parts[0].text
                return jsonify({"response": response_text})
            except Exception as e:
                print("Failed to generate or parse response:", str(e))
                return jsonify({"error": "Failed to generate response"}), 500
            break

    @app.route("/logout")
    def logout():
        logout_user()
        return redirect(url_for("login_register"))

    @app.route("/create-checkout-session", methods=["GET", "POST"])
    def create_checkout_session():
        print("Creating checkout session.")
        email = request.args.get("email")
        print("Email:", email)
        stripe.api_key = app.config["STRIPE_SECRET_KEY"]
        # Find the user in the database
        user = User.query.filter_by(email=email).first()
        if not user:
            print("User not found.")
            flash("User not found")
            return redirect(url_for("login_register"))

        # Create a customer in Stripe if not already created
        if user.stripe_customer_id:
            customer_id = user.stripe_customer_id
            print("Existing customer ID:", customer_id)
        else:
            customer = stripe.Customer.create(email=email)
            customer_id = customer.id
            print("New customer ID:", customer_id)

            # Update the user's stripe_customer_id
            user.stripe_customer_id = customer.id
            db.session.commit()

        stripe_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": "price_1PqnDWKEwAs1n38cT4w37bp7",
                    "quantity": 1,
                },
            ],
            mode="subscription",
            customer=user.stripe_customer_id,
            success_url=url_for("subscription_success", _external=True),
            cancel_url=url_for("subscription_cancel", _external=True),
            subscription_data={
                "trial_settings": {
                    "end_behavior": {"missing_payment_method": "cancel"}
                },
                "trial_period_days": 30,
            },
        )
        return redirect(stripe_session.url, code=303)

    def handle_successful_subscription(stripe_session):
        customer_id = stripe_session["customer"]
        print("Customer ID:", customer_id)
        print(f"Type of customer_id: {type(customer_id)}")

        print("Session data:", stripe_session)

        all_users = User.query.all()
        for user in all_users:
            print(
                f"User ID: {user.id}, Stripe Customer ID: {user.stripe_customer_id}, Type: {type(user.stripe_customer_id)}"
            )

        if customer_id:
            # Fetch the user associated with this Stripe customer ID and update their subscription status
            user = User.query.filter_by(stripe_customer_id=customer_id).first()
            if user:
                user.is_subscribed = 1
                db.session.commit()
                print(f"User {user.id} subscription status updated to 1.")
            else:
                print(f"No user found with customer ID: {customer_id}")
        else:
            print("No customer ID found in the session.")

    @app.route("/webhook", methods=["POST"])
    def stripe_webhook():
        print("Received webhook.")
        stripe.api_key = app.config["STRIPE_SECRET_KEY"]
        payload = request.get_data(as_text=True)
        sig_header = request.headers.get("Stripe-Signature")
        event = None
        print(app.config["STRIPE_ENDPOINT_SECRET"])

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, app.config["STRIPE_ENDPOINT_SECRET"]
            )
            print("Event received:", event)
        except ValueError as e:
            print("Error parsing the webhook payload:", str(e))
            return "", 400
        except stripe.error.SignatureVerificationError as e:
            print("Error verifying the webhook signature:", str(e))
            return "", 400

        if event["type"] == "checkout.session.completed":
            stripe_session = event["data"]["object"]
            # Update the user’s subscription status in your database
            handle_successful_subscription(stripe_session)  # Implement this function
            print("Subscription handling completed.")
        else:
            print(event["type"])

        return "", 200

    @app.route("/subscription-success")
    def subscription_success():
        print("Subscription success.")
        return render_template("subscription_success.html")

    @app.route("/subscription-cancel")
    def subscription_cancel():
        print("Subscription cancelled.")
        return render_template("subscription_cancel.html")
