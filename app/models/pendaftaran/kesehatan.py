from app.extensions import db
from datetime import datetime

class Kesehatan(db.Model):
    __tablename__ = 'kesehatan'

    id = db.Column(db.Integer, primary_key=True)

    peserta_id = db.Column(db.Integer, db.ForeignKey('peserta_didik.id'), nullable=False)

    berat_badan = db.Column(db.Float)
    tinggi_badan = db.Column(db.Float)
    lingkar_kepala = db.Column(db.Float)
    golongan_darah = db.Column(db.Enum('A', 'B', 'AB', 'O', name='golongan_darah_enum'))
    riwayat_penyakit = db.Column(db.Text)
    alergi = db.Column(db.Text)
    kebutuhan_khusus = db.Column(db.String(100))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)