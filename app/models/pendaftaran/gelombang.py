from app.extensions import db

class Gelombang(db.Model):
    __tablename__ = 'gelombang'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    tanggal_mulai = db.Column(db.Date)
    tanggal_selesai = db.Column(db.Date)

    id_tahun = db.Column(db.Integer, db.ForeignKey('tahun_ajaran.id'))