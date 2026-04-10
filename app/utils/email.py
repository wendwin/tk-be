from flask_mail import Message
from app.extensions import mail
from flask import current_app as app
from flask import render_template

def send_verification_email(email, token):
    base_url = app.config["BASE_URL"]
    verify_url =  f"{base_url}/api/auth/verify-email/{token}"

    msg = Message(
        subject="Verifikasi Email",
        recipients=[email],
        sender=app.config["MAIL_DEFAULT_SENDER"]
    )

    msg.body = f"""
                Halo,

                Silakan verifikasi email kamu melalui link berikut:
                {verify_url}

                Jika kamu tidak merasa mendaftar, abaikan email ini.
                """

    msg.html = render_template("email/verify.html", verify_url=verify_url)

    mail.send(msg)

def send_reset_password_email(email, token):
    fe_url = app.config["FRONTEND_URL"]
    reset_link_url = f"{fe_url}/reset-password?token={token}"

    msg = Message(
        subject="Reset Password",
        recipients=[email],
        sender=app.config["MAIL_DEFAULT_SENDER"]
    )

    msg.body = f"""
                Halo,

                Silakan reset password kamu melalui link berikut:
                {reset_link_url}

                Jika kamu tidak merasa mendaftar, abaikan email ini.
                """

    msg.html = render_template("email/reset.html", reset_link_url=reset_link_url)

    mail.send(msg)