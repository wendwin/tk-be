from app.extensions import db
from datetime import datetime

class OrangTua(db.Model):
    __tablename__ = 'orang_tua'

    id = db.Column(db.Integer, primary_key=True)

    peserta_id = db.Column(db.Integer, db.ForeignKey('peserta_didik.id'), nullable=False)
    alamat_id = db.Column(db.Integer, db.ForeignKey('alamat.id'))

    tipe = db.Column(db.Enum('ayah', 'ibu', 'wali', name='tipe_orangtua_enum'),nullable=False)
    nama = db.Column(db.String(150), nullable=False)
    tempat_lahir = db.Column(db.String(100), nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False)
    nik = db.Column(db.String(16), nullable=False)
    pendidikan = db.Column(db.Enum('SD','SMP','SMA','D1','D2','D3','D4','S1','S2','S3',name='pendidikan_enum'),nullable=False)
    pekerjaan = db.Column(db.String(50), nullable=False)
    pendapatan = db.Column(db.Numeric(15, 2))
    alamat_kantor = db.Column(db.Text)
    no_hp = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100))
    alamat = db.relationship('Alamat')

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)