from marshmallow import ValidationError
from flask import current_app, request
from werkzeug.exceptions import HTTPException
from flask_jwt_extended import get_jwt_identity

from app.utils.responses import error_response
from app.utils.exceptions import NotFoundError


def get_log_context():
    try:
        user_id = get_jwt_identity()
    except Exception:
        user_id = "anonymous"

    return (
        f"user={user_id} | "
        f"ip={request.remote_addr} | "
        f"{request.method} {request.path}"
    )


def init_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return error_response(
            message="Validation error",
            errors=err.messages,
            code=400
        )

    @app.errorhandler(ValueError)
    def handle_value_error(e):
        return error_response(
            message=str(e),
            code=422
        )

    @app.errorhandler(NotFoundError)
    def handle_not_found_error(e):
        current_app.logger.info(
            f"{get_log_context()} | {str(e)}"
        )

        return error_response(
            message=str(e),
            code=404
        )

    @app.errorhandler(429)
    def ratelimit_handler(e):
        current_app.logger.warning(
            f"{get_log_context()} | Rate limit: {e}"
        )

        return error_response(
            message="Too many requests, try again later",
            code=429
        )

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        current_app.logger.warning(
            f"{get_log_context()} | HTTP {e.code}: {e.description}"
        )

        return error_response(
            message=e.description,
            code=e.code
        )

    @app.errorhandler(Exception)
    def handle_exception(e):
        current_app.logger.exception(
            f"{get_log_context()} | {type(e).__name__}: {str(e)}"
        )
    
        return error_response(
            message="Internal server error",
            code=500
        )