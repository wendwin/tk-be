from app.extensions import db
from datetime import datetime

class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'

    id = db.Column(db.Integer, primary_key=True)
    no_pendaftaran = db.Column(db.String(3), unique=True)
    tanggal_daftar = db.Column(db.DateTime, default=datetime.utcnow)
    jenis = db.Column(db.Enum('tk', 'kb', name='jenis_enum'))
    program = db.Column(db.Enum('reguler', 'halfday', 'fullday', name='program_enum'))
    
    id_tahun = db.Column(db.Integer, db.ForeignKey('tahun_ajaran.id'))

    peserta = db.relationship('PesertaDidik', backref='pendaftaran', uselist=False)
    dokumen = db.relationship('Dokumen', backref='pendaftaran')