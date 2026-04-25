from app.extensions import db
from datetime import datetime

class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    no_pendaftaran = db.Column(db.String(10), unique=True)
    status = db.Column(db.Enum('pending', 'verified', 'accepted', 'rejected', name='status_pendaftaran_enum'),default='pending')
    status_pembayaran = db.Column(db.Enum('unpaid', 'pending', 'paid', 'failed', name='status_pembayaran_enum'), default='unpaid')
    tanggal_daftar = db.Column(db.DateTime, default=datetime.utcnow)
    jenis = db.Column(db.Enum('tk', 'kb', name='jenis_enum'))
    program = db.Column(db.Enum('reguler', 'halfday', 'fullday', name='program_enum'))

    id_tahun = db.Column(db.Integer, db.ForeignKey('tahun_ajaran.id'))
    id_gelombang = db.Column(db.Integer, db.ForeignKey('gelombang.id'))
    tanggal_observasi = db.Column(db.Date)
    jam_observasi = db.Column(db.Time)  

    status_observasi = db.Column(
        db.Enum('belum', 'terjadwal', 'hadir', 'tidak_hadir', name='status_observasi_enum'),
        default='belum'
    )
    
    peserta = db.relationship('PesertaDidik', backref='pendaftaran', uselist=False)
    dokumen = db.relationship('Dokumen', backref='pendaftaran')
    gelombang = db.relationship('Gelombang', backref='pendaftaran')
    tahun_ajaran = db.relationship('TahunAjaran', backref='pendaftaran')