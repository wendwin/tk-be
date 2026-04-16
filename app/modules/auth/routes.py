from flask import Blueprint, request, redirect, current_app as app
from .service import register_user, login_user, verify_user_email, forgot_password_service, reset_password_service
from .schema import RegisterSchema, LoginSchema, ForgotPasswordSchema, ResetPasswordSchema
from marshmallow import ValidationError
from app.extensions import limiter
from flask_jwt_extended import unset_jwt_cookies, jwt_required, get_jwt_identity, get_jwt, create_access_token, set_access_cookies, get_csrf_token
from app.models import User
from app.utils.responses import success_response, error_response

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['POST'])
@limiter.limit("5 per minute; 20 per hour")
def register():
    data = RegisterSchema().load(request.json)
    return register_user(data)

@auth_bp.route('/verify-email/<token>', methods=['GET'])
@limiter.limit("10 per minute")
def verify_email(token):
    url = app.config["FRONTEND_URL"]
    result, status = verify_user_email(token)

    if status == 200:
        return redirect(f"{url}/login?verified=true") 

    return result, status

@auth_bp.route('/login', methods=['POST'])
@limiter.limit("10 per minute; 50 per hour")
def login():
    data = LoginSchema().load(request.json)
    return login_user(data)


@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response, code = success_response("Logout success", code=200)
    unset_jwt_cookies(response)
    return response, code

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = ForgotPasswordSchema().load(request.json)
    return forgot_password_service(data)


@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    data = ResetPasswordSchema().load(request.json)
    return reset_password_service(data)

@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_me():
    user_id = get_jwt_identity()
    claims = get_jwt()

    user = User.query.get(user_id)

    if not user:
        return error_response("User not found", code=404)

    return success_response(
        "User fetched successfully",
        data={
            "id": user.id,
            "email": user.email,
            "role": claims.get("role") 
        },
        code=200
    )

@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()

    new_access_token = create_access_token(identity=identity)

    response, code = success_response("Token refreshed", code=200)
    set_access_cookies(response, new_access_token)

    response.headers["X-CSRF-TOKEN"] = get_csrf_token(new_access_token)

    return response, code