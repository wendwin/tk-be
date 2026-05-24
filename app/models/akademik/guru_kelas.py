# app/models/akademik/guru_kelas.py
from datetime import datetime
from app.extensions import db


class GuruKelas(db.Model):
    __tablename__ = "guru_kelas"

    __table_args__ = (
        db.UniqueConstraint(
            "guru_id",
            "kelas_id",
            "tahun_ajaran_id",
            name="unique_guru_kelas_per_tahun"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    guru_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False,index=True)
    kelas_id = db.Column(db.Integer,db.ForeignKey("kelas.id"),nullable=False,index=True)
    tahun_ajaran_id = db.Column(db.Integer,db.ForeignKey("tahun_ajaran.id"),nullable=False,index=True)

    peran = db.Column(db.Enum("wali_kelas","pendamping",name="peran_guru_kelas_enum"),nullable=False,default="wali_kelas")

    guru = db.relationship("User",backref="guru_kelas")
    kelas = db.relationship("Kelas",backref="guru_kelas")
    tahun_ajaran = db.relationship("TahunAjaran",backref="guru_kelas")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)