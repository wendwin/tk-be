from app.extensions import db
from datetime import datetime

class Dokumen(db.Model):
    __tablename__ = 'dokumen'

    id = db.Column(db.Integer, primary_key=True)

    pendaftaran_id = db.Column(
        db.Integer,
        db.ForeignKey('pendaftaran.id'),
        nullable=False,
        index=True
    )

    jenis_dokumen = db.Column(
        db.Enum(
            'kk',
            'akta',
            'kia',
            'foto',
            'surat_pernyataan',
            'bukti_pembayaran',
            name='jenis_dokumen_enum'
        ),
        nullable=False
    )

    file_path = db.Column(db.String(500), nullable=False)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)