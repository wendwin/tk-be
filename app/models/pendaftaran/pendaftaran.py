from app.extensions import db
from datetime import datetime

class Pendaftaran(db.Model):
    __tablename__ = 'pendaftaran'

    id = db.Column(db.Integer, primary_key=True)

    peserta_id = db.Column(db.Integer, db.ForeignKey('peserta_didik.id'), nullable=False)
    tahun_ajaran_id = db.Column(db.Integer, db.ForeignKey('tahun_ajaran.id'), nullable=False)
    gelombang_id = db.Column(db.Integer, db.ForeignKey('gelombang.id'), nullable=False)

    no_pendaftaran = db.Column(db.String(20), unique=True, nullable=False)

    status = db.Column(
        db.Enum(
            'draft',
            'pending',
            'verified',
            'accepted',
            'rejected',
            name='status_pendaftaran_enum'
        ),
        nullable=False,
        default='draft'
    )

    status_pembayaran = db.Column(
        db.Enum(
            'unpaid',
            'pending',
            'paid',
            'failed',
            name='status_pembayaran_enum'
        ),
        nullable=False,
        default='unpaid'
    )

    tanggal_daftar = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.utcnow
    )

    jenis = db.Column(
        db.Enum('tk', 'kb', name='jenis_enum'),
        nullable=False
    )

    program = db.Column(
        db.Enum(
            'reguler',
            'halfday',
            'fullday',
            name='program_enum'
        ),
        nullable=False
    )

    observasi_at = db.Column(db.DateTime)

    status_observasi = db.Column(
        db.Enum(
            'belum',
            'terjadwal',
            'hadir',
            'tidak_hadir',
            name='status_observasi_enum'
        ),
        nullable=False,
        default='belum'
    )

    dokumen = db.relationship('Dokumen', backref='pendaftaran')

    gelombang = db.relationship('Gelombang', backref='pendaftaran')

    tahun_ajaran = db.relationship('TahunAjaran', backref='pendaftaran')

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)