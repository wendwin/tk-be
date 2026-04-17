from app.extensions import db

class Alamat(db.Model):
    __tablename__ = 'alamat'

    id = db.Column(db.Integer, primary_key=True)
    alamat_lengkap = db.Column(db.Text)
    rt = db.Column(db.String(5))
    rw = db.Column(db.String(5))
    desa = db.Column(db.String(100))
    kecamatan = db.Column(db.String(100))
    kabupaten = db.Column(db.String(100))
    kode_pos = db.Column(db.String(10))