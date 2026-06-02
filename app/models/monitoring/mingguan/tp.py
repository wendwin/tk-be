
from datetime import datetime
from app.extensions import db

class MonitoringTP(db.Model):
    __tablename__ = "monitoring_tp"

    id = db.Column(db.Integer, primary_key=True)

    monitoring_mingguan_id = db.Column(
        db.Integer,
        db.ForeignKey("monitoring_mingguan.id"),
        nullable=False,
        index=True
    )

    elemen = db.Column(
        db.Enum("kesyuhadaan", "nabp", "jd", "ddlmstrs", name="elemen_monitoring_enum"),
        nullable=False
    )

    tujuan = db.Column(db.Text, nullable=False)

    monitoring_mingguan = db.relationship("MonitoringMingguan", backref="tp")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)