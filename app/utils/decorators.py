from functools import wraps
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from flask import jsonify, request

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            if request.method == 'OPTIONS':
                return '', 200

            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")

            if user_role not in roles:
                return jsonify({
                    "success": False,
                    "message": "Forbidden: insufficient role"
                }), 403

            return fn(*args, **kwargs)
        return decorator
    return wrapper