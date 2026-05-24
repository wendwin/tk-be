from flask import Flask
from .config import Config
from .extensions import db, jwt, migrate, mail, limiter
from flask_cors import CORS

from app import models
from app.utils.errors import init_error_handlers
from app.utils.logger import init_logger
from app.commands.db_command import register_db_command

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)
    # limiter.init_app(app)
    init_logger(app)
    
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

    # user
    from app.modules.user.routes import bp_user
    app.register_blueprint(bp_user,url_prefix="/api/users")

    # pendaftaran
    from app.modules.pendaftaran.routes import bp_pendaftaran
    app.register_blueprint(bp_pendaftaran, url_prefix="/api/pendaftaran")
    
    # asesmen
    from app.modules.asesmen.routes import bp_asesmen
    app.register_blueprint(bp_asesmen, url_prefix="/api/asesmen")

    # observasi
    from app.modules.observasi.routes import bp_observasi
    app.register_blueprint(bp_observasi, url_prefix="/api/observasi")

    # siswa
    from app.modules.akademik.siswa.routes import bp_siswa
    app.register_blueprint(bp_siswa, url_prefix="/api/akademik/siswa")

    # kelas
    from app.modules.akademik.kelas.routes import bp_kelas
    app.register_blueprint(bp_kelas, url_prefix="/api/akademik/kelas")

    # guru kelas
    from app.modules.akademik.guru_kelas.routes import bp_guru_kelas
    app.register_blueprint(bp_guru_kelas, url_prefix="/api/akademik/guru-kelas")

    # siswa kelas
    from app.modules.akademik.siswa_kelas.routes import bp_siswa_kelas
    app.register_blueprint(bp_siswa_kelas, url_prefix="/api/akademik/siswa-kelas")

    # tahun ajaran
    from app.modules.akademik.tahun_ajaran.routes import bp_tahun_ajaran
    app.register_blueprint(bp_tahun_ajaran,url_prefix="/api/tahun-ajaran")

    
    return app