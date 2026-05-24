from app.extensions import db
from datetime import datetime, date

class Siswa(db.Model):
    __tablename__ = "siswa"

    id = db.Column(db.Integer, primary_key=True)

    peserta_id = db.Column(db.Integer,db.ForeignKey("peserta_didik.id"),nullable=False,unique=True,index=True)
    nisn = db.Column(db.String(20),unique=True,nullable=True)
    tanggal_masuk = db.Column(db.Date,nullable=False)
    status = db.Column(db.Enum("aktif","lulus","keluar",name="status_siswa_enum"),nullable=False,default="aktif")

    peserta = db.relationship("PesertaDidik",backref=db.backref("siswa", uselist=False))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)