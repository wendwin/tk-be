from datetime import datetime
from app.extensions import db

class MonitoringKarya(db.Model):
    __tablename__ = "monitoring_hasil_karya"

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

    kegiatan = db.Column(db.String(150), nullable=False)
    foto = db.Column(db.String(500))
    deskripsi = db.Column(db.Text, nullable=False)
    analisa = db.Column(db.Text, nullable=False)

    monitoring_siswa = db.relationship("MonitoringSiswa", backref="karya")
    kktp = db.relationship("MonitoringKKTP", backref="karya")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)