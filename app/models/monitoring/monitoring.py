from datetime import datetime
from app.extensions import db

class Monitoring(db.Model):
    __tablename__ = "monitoring_mingguan"

    __table_args__ = (
        db.UniqueConstraint(
            "siswa_kelas_id",
            "semester",
            "minggu",
            name="unique_monitoring_siswa_per_minggu"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    siswa_kelas_id = db.Column(
        db.Integer,
        db.ForeignKey("siswa_kelas.id"),
        nullable=False,
        index=True
    )

    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    semester = db.Column(db.Integer, nullable=False)
    minggu = db.Column(db.Integer, nullable=False)

    topik = db.Column(db.String(150), nullable=False)
    sub_topik = db.Column(db.String(150), nullable=False)

    tanggal_mulai = db.Column(db.Date, nullable=False)
    tanggal_selesai = db.Column(db.Date, nullable=False)

    ringkasan = db.Column(db.Text)

    status = db.Column(
        db.Enum("draft", "published", name="status_monitoring_enum"),
        nullable=False,
        default="draft"
    )

    siswa_kelas = db.relationship(
        "SiswaKelas",
        backref=db.backref("monitoring", lazy=True)
    )

    guru = db.relationship(
        "User",
        backref=db.backref("monitoring_dibuat", lazy=True)
    )

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )