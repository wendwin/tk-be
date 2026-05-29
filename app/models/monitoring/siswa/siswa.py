from datetime import datetime
from app.extensions import db

class MonitoringSiswa(db.Model):
    __tablename__ = "monitoring_siswa"

    __table_args__ = (
        db.UniqueConstraint(
            "monitoring_mingguan_id",
            "siswa_kelas_id",
            name="unique_monitoring_siswa_per_minggu"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    monitoring_mingguan_id = db.Column(
        db.Integer,
        db.ForeignKey("monitoring_mingguan.id"),
        nullable=False,
        index=True
    )

    siswa_kelas_id = db.Column(
        db.Integer,
        db.ForeignKey("siswa_kelas.id"),
        nullable=False,
        index=True
    )

    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    ringkasan = db.Column(db.Text)

    status = db.Column(
        db.Enum("draft", "published", name="status_monitoring_siswa_enum"),
        nullable=False,
        default="draft"
    )

    monitoring_mingguan = db.relationship("MonitoringMingguan", backref="monitoring_siswa")
    siswa_kelas = db.relationship("SiswaKelas", backref="monitoring_siswa")
    guru = db.relationship("User", backref="monitoring_siswa_dibuat")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)