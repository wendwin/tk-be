from datetime import datetime
from app.extensions import db


class GPPHPertanyaan(db.Model):
    __tablename__ = 'gpph_pertanyaan'

    id = db.Column(db.Integer, primary_key=True)

    urutan = db.Column(db.Integer, nullable=False)
    pertanyaan = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

class GPPHJawaban(db.Model):
    __tablename__ = 'gpph_jawaban'

    id = db.Column(db.Integer, primary_key=True)

    pendaftaran_id = db.Column(db.Integer, db.ForeignKey('pendaftaran.id'), nullable=False, index=True)
    pertanyaan_id = db.Column(db.Integer, db.ForeignKey('gpph_pertanyaan.id'), nullable=False)

    snapshot_urutan = db.Column(db.Integer, nullable=False)
    snapshot_pertanyaan = db.Column(db.Text, nullable=False)

    nilai = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    pertanyaan = db.relationship('GPPHPertanyaan')
    pendaftaran = db.relationship('Pendaftaran', backref='gpph_jawaban')