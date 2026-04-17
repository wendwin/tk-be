from app.extensions import db

class PesertaDidik(db.Model):
    __tablename__ = 'peserta_didik'

    id = db.Column(db.Integer, primary_key=True)

    id_pendaftaran = db.Column(db.Integer, db.ForeignKey('pendaftaran.id'))
    id_alamat_domisili = db.Column(db.Integer, db.ForeignKey('alamat.id'))
    id_alamat_kk = db.Column(db.Integer, db.ForeignKey('alamat.id'))

    nama_lengkap = db.Column(db.String(150))
    status = db.Column(db.Enum('calon', 'aktif', 'nonaktif', name='status_peserta_enum'),default='calon')
    nama_panggilan = db.Column(db.String(100))
    tempat_lahir = db.Column(db.String(100))
    tanggal_lahir = db.Column(db.Date)
    jenis_kelamin = db.Column(db.String(10))
    kewarganegaraan = db.Column(db.String(50))
    nik = db.Column(db.String(20))
    no_kk = db.Column(db.String(20))
    no_akta = db.Column(db.String(20))
    agama = db.Column(db.String(50))
    no_telp = db.Column(db.String(20))
    anak_ke = db.Column(db.Integer)
    jumlah_saudara = db.Column(db.Integer)
    bahasa = db.Column(db.String(50))

    kesehatan = db.relationship('Kesehatan', backref='peserta', uselist=False)
    orang_tua = db.relationship('OrangTua', backref='peserta')
    informasi = db.relationship('Informasi', backref='peserta', uselist=False)  

    alamat_domisili = db.relationship('Alamat', foreign_keys=[id_alamat_domisili])
    alamat_kk = db.relationship('Alamat', foreign_keys=[id_alamat_kk])