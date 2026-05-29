from datetime import datetime
from app.extensions import db

class MonitoringRekomendasi(db.Model):
    __tablename__ = "monitoring_rekomendasi_rumah"

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
            name="elemen_rekomendasi_enum"
        ),
        nullable=False
    )

    tips = db.Column(db.Text, nullable=False)

    mmonitoring = db.relationship("Monitoring", backref="rekomendasi")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)