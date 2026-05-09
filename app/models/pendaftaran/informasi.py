from app.extensions import db
from datetime import datetime

class Informasi(db.Model):
    __tablename__ = 'informasi'

    id = db.Column(db.Integer, primary_key=True)

    peserta_id = db.Column(db.Integer, db.ForeignKey('peserta_didik.id'), nullable=False)

    tinggal_dengan = db.Column(db.String(50))
    jarak_sekolah = db.Column(db.Float)
    waktu_tempuh = db.Column(db.String(50))
    kendaraan = db.Column(db.String(50))
    pernah_sekolah = db.Column(db.Boolean,nullable=False,default=False)
    nama_sekolah = db.Column(db.String(150))
    npsn = db.Column(db.String(20))
    nisn = db.Column(db.String(20))
    bakat = db.Column(db.String(100))
    hobi = db.Column(db.String(100))
    cita_cita = db.Column(db.String(100))
    sumber_informasi = db.Column(db.String(100))

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)