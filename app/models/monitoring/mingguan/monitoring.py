from datetime import datetime
from app.extensions import db

class MonitoringMingguan(db.Model):
    __tablename__ = "monitoring_mingguan"

    __table_args__ = (
        db.UniqueConstraint(
            "kelas_id",
            "tahun_ajaran_id",
            "semester",
            "bulan",
            "minggu",
            name="unique_monitoring_mingguan_per_kelas"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    kelas_id = db.Column(db.Integer, db.ForeignKey("kelas.id"), nullable=False, index=True)
    tahun_ajaran_id = db.Column(db.Integer, db.ForeignKey("tahun_ajaran.id"), nullable=False, index=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)

    semester = db.Column(db.Enum("ganjil", "genap", name="semester_monitoring_mingguan_enum"), nullable=False)
    bulan = db.Column(db.Integer, nullable=False)
    minggu = db.Column(db.Enum("1", "2", "3", "4", name="minggu_monitoring_mingguan_enum"), nullable=False)

    topik = db.Column(db.String(150), nullable=False)
    sub_topik = db.Column(db.String(150), nullable=False)

    tanggal_mulai = db.Column(db.Date, nullable=False)
    tanggal_selesai = db.Column(db.Date, nullable=False)

    status = db.Column(
        db.Enum("draft", "published", name="status_monitoring_mingguan_enum"),
        nullable=False,
        default="draft"
    )

    kelas = db.relationship("Kelas", backref="monitoring_mingguan")
    tahun_ajaran = db.relationship("TahunAjaran", backref="monitoring_mingguan")
    guru = db.relationship("User", backref="monitoring_mingguan_dibuat")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)