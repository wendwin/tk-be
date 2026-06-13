from flask import jsonify
import time
from datetime import datetime, timedelta
from app.models.auth.user import User
from app.models.auth.role import Role
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from flask_jwt_extended import create_access_token, create_refresh_token, set_access_cookies, set_refresh_cookies, get_csrf_token
from app.utils.email import send_verification_email, send_reset_password_email
from app.utils.responses import success_response, error_response

def register_user(data):
    if User.query.filter_by(email=data['email']).first():
        return error_response("Email sudah terdaftar", code=400)

    role = Role.query.filter_by(name='orang_tua').first()

    if not role:
        return error_response("Role orang tua tidak ditemukan", code=500)

    token = secrets.token_urlsafe(32)

    user = User(
        first_name=data["first_name"],
        last_name=data.get("last_name"),
        email=data['email'],
        password=generate_password_hash(data['password']),
        role=role,
        verification_token=token,
        verification_token_expires_at=datetime.utcnow() + timedelta(minutes=30)
    )

    db.session.add(user)
    db.session.commit()

    send_verification_email(user.email, token)

    return success_response("Registrasi berhasil, silahkan verifikasi email", code=201)

def verify_user_email(token):
    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return error_response("Token verifikasi tidak valid", code=400)

    if (
        not user.verification_token_expires_at
        or user.verification_token_expires_at < datetime.utcnow()
    ):
        user.verification_token = None
        user.verification_token_expires_at = None
        db.session.commit()

        return error_response("Token verifikasi sudah kedaluwarsa", code=400)

    user.is_verified = True
    user.verification_token = None
    user.verification_token_expires_at = None

    db.session.commit()

    return success_response("Email berhasil diverifikasi", code=200)

def login_user(data):
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return error_response("Email atau password salah", code=401)

    if not check_password_hash(user.password, data['password']):
        return error_response("Email atau password salah", code=401)

    if not user.is_verified:
        return error_response("Email belum diverifikasi", code=403)
    
    if not user.is_active:
        raise ValueError("Akun sudah dinonaktifkan")

    token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role.name}
    )

    refresh_token = create_refresh_token(identity=str(user.id))

    response, code = success_response(
        "Login success", 
        data={
            "user": {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role.name,
            }
        },
        code=200
    )

    set_access_cookies(response, token)
    set_refresh_cookies(response, refresh_token)

    csrf_token = get_csrf_token(token)
    response.headers["X-CSRF-TOKEN"] = csrf_token

    return response, code

def forgot_password_service(data):
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        time.sleep(1)
        return success_response("Jika email terdaftar, link reset password akan dikirim ke email Anda", code=200)

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    user.reset_token_expires_at = datetime.utcnow() + timedelta(minutes=30)

    db.session.commit()

    send_reset_password_email(user.email, token)

    return success_response("Jika email terdaftar, link reset password akan dikirim ke email Anda", code=200)

def reset_password_service(data):
    user = User.query.filter_by(reset_token=data['token']).first()

    if not user:
        return error_response("Token reset password tidak valid", code=400)

    if (
        not user.reset_token_expires_at
        or user.reset_token_expires_at < datetime.utcnow()
    ):
        user.reset_token = None
        user.reset_token_expires_at = None
        db.session.commit()

        return error_response("Token reset password sudah kedaluwarsa", code=400)

    user.password = generate_password_hash(data['password'])
    user.reset_token = None
    user.reset_token_expires_at = None

    db.session.commit()

    return success_response("Password berhasil direset", code=200)