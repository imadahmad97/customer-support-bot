from flask import Flask
from .config import Config
from .extensions import db, login_manager, bcrypt
from .models import User
from flask_googlestorage import GoogleStorage, Bucket
from datetime import timedelta


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.reflect()
        db.create_all()

    login_manager.init_app(app)
    login_manager.login_view = "login_register"
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.config.update(
        MAIL_SERVER=Config.MAIL_SERVER,
        MAIL_PORT=Config.MAIL_PORT,
        MAIL_USE_TLS=Config.MAIL_USE_TLS,
        MAIL_USERNAME=Config.MAIL_USERNAME,
        MAIL_PASSWORD=Config.MAIL_PASSWORD,
        MAIL_DEFAULT_SENDER=Config.MAIL_DEFAULT_SENDER,
    )
    bcrypt.init_app(app)
    files = Bucket(Config.GCP_BUCKET_NAME)
    storage = GoogleStorage(files)

    app.config.update(
        GOOGLE_STORAGE_LOCAL_DEST=app.instance_path,
        GOOGLE_STORAGE_SIGNATURE={"expiration": timedelta(minutes=5)},
        GOOGLE_STORAGE_FILES_BUCKET=Config.GCP_BUCKET_NAME,
    )
    storage.init_app(app)

    from .routes import init_routes

    init_routes(app)

    return app
