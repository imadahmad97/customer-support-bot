from flask_login import UserMixin
from .extensions import db
import random


class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)

    def get_id(self):
        return self.id


def random_six_digit_number():
    return random.randint(100000, 999999)


class Chatbot(db.Model):
    __tablename__ = "chatbots"
    id = db.Column(db.Integer, primary_key=True, default=random_six_digit_number)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    context = db.Column(db.String)

    def __repr__(self):
        return f"<Chatbot {self.id} owned by user {self.user_id}>"
