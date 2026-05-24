# app/models/akademik/kelas.py
from datetime import datetime
from app.extensions import db


class Kelas(db.Model):
    __tablename__ = "kelas"

    id = db.Column(db.Integer, primary_key=True)
    tahun_ajaran_id = db.Column(db.Integer,db.ForeignKey("tahun_ajaran.id"),nullable=False,index=True)

    nama = db.Column(db.String(50),nullable=False)
    jenjang = db.Column(db.Enum("kb", "tk", name="jenjang_kelas_enum"),nullable=False)
    kelompok = db.Column(db.Enum("a", "b", name="kelompok_kelas_enum"),nullable=True)
    kapasitas = db.Column(db.Integer, nullable=False, default=15)

    tahun_ajaran = db.relationship("TahunAjaran",backref="kelas")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)