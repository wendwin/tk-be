from app.extensions import db
from datetime import datetime

class Gelombang(db.Model):
    __tablename__ = 'gelombang'

    __table_args__ = (
        db.UniqueConstraint(
            'tahun_ajaran_id',
            'nama',
            name='unique_gelombang_per_tahun'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    tahun_ajaran_id = db.Column(db.Integer,db.ForeignKey('tahun_ajaran.id'),nullable=False,  index=True)

    nama = db.Column(db.String(50), nullable=False)
    tanggal_mulai = db.Column(db.Date, nullable=False)
    tanggal_selesai = db.Column(db.Date, nullable=False)

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)