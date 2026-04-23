from app.extensions import db

class AsesmenJawaban(db.Model):
    __tablename__ = 'asesmen_jawaban'

    id = db.Column(db.Integer, primary_key=True)
    
    id_pendaftaran = db.Column(db.Integer, db.ForeignKey('pendaftaran.id'))
    id_pertanyaan = db.Column(db.Integer, db.ForeignKey('asesmen_pertanyaan.id'))

    jawaban = db.Column(db.Text, nullable=False)

    pendaftaran = db.relationship('Pendaftaran', backref='asesmen_jawaban')
    pertanyaan = db.relationship('AsesmenPertanyaan')