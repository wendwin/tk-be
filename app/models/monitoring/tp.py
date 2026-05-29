
from datetime import datetime
from app.extensions import db

class MonitoringTP(db.Model):
    __tablename__ = "monitoring_tp"

    id = db.Column(db.Integer, primary_key=True)

    monitoring_id = db.Column(
        db.Integer,
        db.ForeignKey("monitoring_mingguan.id"),
        nullable=False,
        index=True
    )

    elemen = db.Column(
        db.Enum(
            "kesyuhadaan",
            "nabp",
            "jd",
            "ddlmstrs",
            name="elemen_monitoring_enum"
        ),
        nullable=False
    )

    tujuan = db.Column(db.Text, nullable=False)

    monitoring = db.relationship("Monitoring", backref="tujuan_pembelajaran")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)