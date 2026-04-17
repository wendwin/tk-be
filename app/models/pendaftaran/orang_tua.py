from app.extensions import db

class OrangTua(db.Model):
    __tablename__ = 'orang_tua'

    id = db.Column(db.Integer, primary_key=True)

    id_peserta = db.Column(db.Integer, db.ForeignKey('peserta_didik.id'))
    id_alamat = db.Column(db.Integer, db.ForeignKey('alamat.id'))

    tipe = db.Column(db.String(10))
    nama = db.Column(db.String(150))
    tempat_lahir = db.Column(db.String(100))
    tanggal_lahir = db.Column(db.Date)
    nik = db.Column(db.String(20))
    pendidikan = db.Column(db.String(50))
    pekerjaan = db.Column(db.String(50))
    pendapatan = db.Column(db.Float)
    alamat_kantor = db.Column(db.Text)
    no_hp = db.Column(db.String(20))
    email = db.Column(db.String(100))

    alamat = db.relationship('Alamat')