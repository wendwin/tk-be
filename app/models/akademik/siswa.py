from app.extensions import db
from datetime import date

class Siswa(db.Model):
    __tablename__ = 'siswa'

    id = db.Column(db.Integer, primary_key=True)

    id_peserta = db.Column(db.Integer, db.ForeignKey('peserta_didik.id'), unique=True)
    nis = db.Column(db.String(20), unique=True)
    tanggal_masuk = db.Column(db.Date, default=date.today)

    status = db.Column(
        db.Enum('aktif', 'lulus', 'keluar', name='status_siswa_enum'),
        default='aktif'
    )

    peserta = db.relationship('PesertaDidik', backref=db.backref('siswa', uselist=False))