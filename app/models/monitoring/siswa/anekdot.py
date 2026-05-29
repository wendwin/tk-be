from datetime import datetime
from app.extensions import db

class MonitoringAnekdot(db.Model):
    __tablename__ = "monitoring_catatan_anekdot"

    id = db.Column(db.Integer, primary_key=True)

    monitoring_siswa_id = db.Column(
        db.Integer,
        db.ForeignKey("monitoring_siswa.id"),
        nullable=False,
        index=True
    )

    kktp_id = db.Column(
        db.Integer,
        db.ForeignKey("monitoring_kktp.id"),
        nullable=False,
        index=True
    )

    waktu = db.Column(db.DateTime, nullable=False)
    catatan = db.Column(db.Text, nullable=False)

    monitoring_siswa = db.relationship("MonitoringSiswa", backref="anekdot")
    kktp = db.relationship("MonitoringKKTP", backref="anekdot")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)