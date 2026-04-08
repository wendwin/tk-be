from flask import Blueprint, request, redirect, current_app as app
from .service import register_user, login_user, verify_user_email
from .schema import RegisterSchema, LoginSchema
from marshmallow import ValidationError
from app.extensions import limiter
from flask_jwt_extended import unset_jwt_cookies, jwt_required, get_jwt_identity
from app.utils.responses import success_response

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