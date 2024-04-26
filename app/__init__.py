from flask import Flask
from .config import Config
from .extensions import db, login_manager, bcrypt
from .models import User
from flask_mail import Mail


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.reflect()
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = "login"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.config.update(
        MAIL_SERVER="smtp.mail.yahoo.com",
        MAIL_PORT=587,
        MAIL_USE_TLS=True,
        MAIL_USERNAME="imadahmad97@yahoo.ca",
        MAIL_PASSWORD="umjznypifyortcqr",
        MAIL_DEFAULT_SENDER="imadahmad97@yahoo.ca",
    )
    bcrypt.init_app(app)

    from .routes import init_routes

    init_routes(app)

    return app
