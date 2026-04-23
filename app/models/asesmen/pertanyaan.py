from app.extensions import db

class AsesmenPertanyaan(db.Model):
    __tablename__ = 'asesmen_pertanyaan'

    id = db.Column(db.Integer, primary_key=True)
    pertanyaan = db.Column(db.Text, nullable=False)
    urutan = db.Column(db.Integer)