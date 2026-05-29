from datetime import datetime
from app.extensions import db

class MonitoringKegiatan(db.Model):
    __tablename__ = "monitoring_kegiatan"

    id = db.Column(db.Integer, primary_key=True)

    monitoring_id = db.Column(
        db.Integer,
        db.ForeignKey("monitoring_mingguan.id"),
        nullable=False,
        index=True
    )

    nama = db.Column(db.String(150), nullable=False)
    media = db.Column(db.Text)

    monitoring = db.relationship("Monitoring", backref="kegiatan")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)