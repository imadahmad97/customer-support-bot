from flask import current_app
from flask_mail import Message, Mail
import os
from werkzeug.utils import secure_filename
import boto3, botocore
from .config import Config


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


def upload_file_to_s3(file, acl="public-read"):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=Config.AWS_ACCESS_KEY,
        aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
    )
    try:
        s3.upload_fileobj(
            file,
            "chativate-avatars",
            file.filename,
            ExtraArgs={"ACL": acl, "ContentType": file.content_type},
        )

    except Exception as e:
        print("Something Happened: ", e)
        return e

    return Config.S3_DB_URL + file.filename
