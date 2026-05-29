from datetime import datetime
from app.extensions import db

class MonitoringKKTP(db.Model):
    __tablename__ = "monitoring_kktp"

    id = db.Column(db.Integer, primary_key=True)

    tp_id = db.Column(
        db.Integer,
        db.ForeignKey("monitoring_tp.id"),
        nullable=False,
        index=True
    )

    deskripsi = db.Column(db.Text, nullable=False)

    tp = db.relationship("MonitoringTP", backref="kktp")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)