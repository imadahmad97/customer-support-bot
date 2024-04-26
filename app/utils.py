from flask import current_app
from flask_mail import Message, Mail

mail = Mail()


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.init_app(current_app)  # Ensure Mail uses the current app's context
    mail.send(msg)
