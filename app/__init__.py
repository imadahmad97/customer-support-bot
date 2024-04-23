from flask import Flask
from .config import Config
from .extensions import db, login_manager, bcrypt
from .models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    with app.app_context():
        db.reflect()
        db.create_all()

    login_manager.init_app(app)

    bcrypt.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes import init_routes

    init_routes(app)

    return app
