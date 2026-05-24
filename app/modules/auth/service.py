from flask import jsonify
import time
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
        return error_response("Email already registered", code=400)

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
        verification_token=token
    )

    db.session.add(user)
    db.session.commit()

    send_verification_email(user.email, token)

    return success_response("Register success, please verify email", code=201)

def verify_user_email(token):
    user = User.query.filter_by(verification_token=token).first()

    if not user:
        return error_response("Invalid token", code=400)

    user.is_verified = True
    user.verification_token = None

    db.session.commit()

    return success_response("Email verified successfully", code=200)

def login_user(data):
    user = User.query.filter_by(email=data['email']).first()

    if not user:
        return error_response("Email or password incorrect", code=401)

    if not check_password_hash(user.password, data['password']):
        return error_response("Email or password incorrect", code=401)

    if not user.is_verified:
        return error_response("Please verify your email first", code=403)
    
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
        return success_response("Link reset has been sent", code=200)

    token = secrets.token_urlsafe(32)

    user.reset_token = token
    db.session.commit()

    send_reset_password_email(user.email, token)

    return success_response("Link reset has been sent", code=200)

def reset_password_service(data):
    user = User.query.filter_by(reset_token=data['token']).first()

    if not user:
        return error_response("Token is invalid or expired", code=400)

    user.password = generate_password_hash(data['password'])
    user.reset_token = None

    db.session.commit()

    return success_response("Password has been reset successfully", code=200)