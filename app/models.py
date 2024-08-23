from flask_login import UserMixin
from .extensions import db
import random


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=True)
    password_hash = db.Column(db.String, nullable=True)
    email = db.Column(db.String, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    is_subscribed = db.Column(db.Boolean, default=False)
    stripe_customer_id = db.Column(db.String(255), unique=True, nullable=True)

    def get_id(self):
        return self.id


def random_six_digit_number():
    return random.randint(100000, 999999)


class Chatbot(db.Model):
    __tablename__ = "chatbots"
    id = db.Column(db.Integer, primary_key=True, default=random_six_digit_number)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    context = db.Column(db.String, default="default context")
    chatbotName = db.Column(db.String(255), default="ChatBot")
    cardBgColor = db.Column(db.String(10), default="#FFFFFF")
    avatar_url = db.Column(db.String(255), default="default_image_url")

    def __repr__(self):
        return f"<Chatbot {self.id} owned by user {self.user_id}>"
