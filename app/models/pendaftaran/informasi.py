from app.extensions import db

class Informasi(db.Model):
    __tablename__ = 'informasi'

    id = db.Column(db.Integer, primary_key=True)
    id_peserta = db.Column(db.Integer, db.ForeignKey('peserta_didik.id'))

    tinggal_dengan = db.Column(db.String(50))
    jarak_sekolah = db.Column(db.Float)
    waktu_tempuh = db.Column(db.String(50))
    kendaraan = db.Column(db.String(50))
    pernah_sekolah = db.Column(db.Boolean)
    nama_sekolah = db.Column(db.String(150))
    npsn = db.Column(db.String(20))
    nisn = db.Column(db.String(20))
    bakat = db.Column(db.String(100))
    hobi = db.Column(db.String(100))
    cita_cita = db.Column(db.String(100))