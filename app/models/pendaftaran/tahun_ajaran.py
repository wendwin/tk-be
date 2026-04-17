from app.extensions import db

class TahunAjaran(db.Model):
    __tablename__ = 'tahun_ajaran'

    id = db.Column(db.Integer, primary_key=True)
    tahun_mulai = db.Column(db.Integer)
    tahun_selesai = db.Column(db.Integer)
    status = db.Column(db.String(20))