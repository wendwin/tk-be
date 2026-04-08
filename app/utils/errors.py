from marshmallow import ValidationError

def init_error_handlers(app):

    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return {
            "success": False,
            "message": "Validation error",
            "errors": err.messages
        }, 400

    @app.errorhandler(404)
    def not_found(e):
        return {
            "success": False,
            "message": "Not found"
        }, 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return {
            "success": False,
            "message": "To many requests, try again later"
        }, 429

    @app.errorhandler(500)
    def internal_error(e):
        return {
            "success": False,
            "message": "Internal server error"
        }, 500
