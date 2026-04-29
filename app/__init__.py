from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate, mail, limiter
from flask_cors import CORS
from app import models
from app.utils.errors import init_error_handlers
from app.commands.db_command import register_db_command

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    # limiter.init_app(app)
    init_error_handlers(app)
    register_db_command(app)
    CORS(app,
          supports_credentials=True,
          origins=app.config["FRONTEND_URL"],
          expose_headers=["X-CSRF-TOKEN"],
          allow_headers=["Content-Type", "X-CSRF-TOKEN"]
        )

    # app.route('/')(lambda: 'running')

    # auth
    from app.modules.auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')

    # pendaftaran
    from app.modules.pendaftaran.routes import bp_pendaftaran
    app.register_blueprint(bp_pendaftaran, url_prefix="/api/pendaftaran")
    
    # asesmen
    from app.modules.asesmen.route import bp_asesmen
    app.register_blueprint(bp_asesmen, url_prefix="/api/asesmen")

    # observasi
    from app.modules.observasi.route import bp_observasi
    app.register_blueprint(bp_observasi, url_prefix="/api/observasi")

    
    return app