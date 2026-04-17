from app.extensions import db

class Kesehatan(db.Model):
    __tablename__ = 'kesehatan'

    id = db.Column(db.Integer, primary_key=True)
    id_peserta = db.Column(db.Integer, db.ForeignKey('peserta_didik.id'))

    berat_badan = db.Column(db.Float)
    tinggi_badan = db.Column(db.Float)
    lingkar_kepala = db.Column(db.Float)
    golongan_darah = db.Column(db.String(5))
    riwayat_penyakit = db.Column(db.Text)
    alergi = db.Column(db.Text)
    kebutuhan_khusus = db.Column(db.Text)