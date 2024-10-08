from flask import current_app
from flask_mail import Message, Mail
from google.cloud import storage
from functools import wraps
from flask import redirect, url_for
from .models import User


mail = Mail()


def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config["MAIL_DEFAULT_SENDER"],
    )
    mail.init_app(current_app)
    mail.send(msg)


def upload_file_to_gcs(file):
    """Uploads a file to Google Cloud Storage."""
    client = storage.Client(project=current_app.config["GCLOUD_PROJECT"])
    bucket = client.bucket(current_app.config["GCP_BUCKET_NAME"])
    blob = bucket.blob(file.filename)

    try:
        blob.upload_from_file(file, content_type=file.content_type)
    except Exception as e:
        print(f"Failed to upload file to GCS: {e}")
        return None

    return f"https://storage.googleapis.com/chativateavatars/{file.filename}"


def subscription_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not User.is_subscribed:
            return redirect(url_for("subscribe"))
        return f(*args, **kwargs)

    return decorated_function
