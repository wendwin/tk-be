from app.extensions import db
from datetime import datetime

class PesertaDidik(db.Model):
    __tablename__ = 'peserta_didik'

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    alamat_domisili_id = db.Column(db.Integer, db.ForeignKey('alamat.id'))
    alamat_kk_id = db.Column(db.Integer, db.ForeignKey('alamat.id'))

    nama_lengkap = db.Column(db.String(150), nullable=False)
    nama_panggilan = db.Column(db.String(100))

    tempat_lahir = db.Column(db.String(100), nullable=False)
    tanggal_lahir = db.Column(db.Date, nullable=False)

    jenis_kelamin = db.Column(
        db.Enum('L', 'P', name='jk_enum'),
        nullable=False
    )

    kewarganegaraan = db.Column(db.String(50), nullable=False)

    nik = db.Column(db.String(16), unique=True, nullable=False)
    no_kk = db.Column(db.String(16), nullable=False)
    no_akta = db.Column(db.String(25), nullable=False)

    agama = db.Column(
        db.Enum(
            'islam',
            'kristen',
            'katolik',
            'hindu',
            'buddha',
            'konghucu',
            name='agama_enum'
        ),
        nullable=False
    )

    no_telp = db.Column(db.String(20), nullable=False)

    anak_ke = db.Column(db.Integer, nullable=False)
    jumlah_saudara = db.Column(db.Integer, nullable=False)

    bahasa = db.Column(db.String(50))

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)

    kesehatan = db.relationship('Kesehatan', backref='peserta', uselist=False)
    orang_tua = db.relationship('OrangTua', backref='peserta')
    informasi = db.relationship('Informasi', backref='peserta', uselist=False)
    pendaftaran = db.relationship('Pendaftaran', backref='peserta')
    alamat_domisili = db.relationship(
        'Alamat',
        foreign_keys=[alamat_domisili_id]
    )
    alamat_kk = db.relationship(
        'Alamat',
        foreign_keys=[alamat_kk_id]
    )

