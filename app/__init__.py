from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate, mail, limiter
from flask_cors import CORS
from app import models
from app.utils.errors import init_error_handlers

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    limiter.init_app(app)
    init_error_handlers(app)
    CORS(app,
          supports_credentials=True,
          origins=app.config["FRONTEND_URL"])

    # app.route('/')(lambda: 'running')

    # auth
    from app.modules.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    return app