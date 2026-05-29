from datetime import datetime
from app.extensions import db

class MonitoringAnekdot(db.Model):
    __tablename__ = "monitoring_catatan_anekdot"

    id = db.Column(db.Integer, primary_key=True)

    monitoring_id = db.Column(
        db.Integer,
        db.ForeignKey("monitoring_mingguan.id"),
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

    monitoring = db.relationship("Monitoring", backref="anekdot")
    kktp = db.relationship("MonitoringKKTP", backref="anekdot")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)