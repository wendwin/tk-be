from app.extensions import db
from datetime import datetime

class Dokumen(db.Model):
    __tablename__ = 'dokumen'

    id = db.Column(db.Integer, primary_key=True)
    id_pendaftaran = db.Column(db.Integer, db.ForeignKey('pendaftaran.id'))

    jenis_dokumen = db.Column(db.String(50))
    file_path = db.Column(db.String(255))
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)