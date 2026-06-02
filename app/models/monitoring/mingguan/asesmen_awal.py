from datetime import datetime
from app.extensions import db

class MonitoringAsesmenAwal(db.Model):
    __tablename__ = "monitoring_asesmen_awal"

    id = db.Column(db.Integer, primary_key=True)

    monitoring_mingguan_id = db.Column(
        db.Integer,
        db.ForeignKey("monitoring_mingguan.id"),
        nullable=False,
        unique=True
    )

    teknik = db.Column(db.String(100), nullable=False, default="Observasi")
    rancangan_kegiatan = db.Column(db.Text, nullable=False)
    hasil = db.Column(db.Text)

    monitoring_mingguan = db.relationship(
        "MonitoringMingguan",
        backref=db.backref("asesmen_awal", uselist=False)
    )

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)