from datetime import datetime

from app.extensions import db


class KPSPPertanyaan(db.Model):
    __tablename__ = 'kpsp_pertanyaan'

    id = db.Column(db.Integer, primary_key=True)
    usia_bulan = db.Column(db.Integer, nullable=False, index=True)
    aspek_perkembangan = db.Column(db.String(100),nullable=False)
    kemampuan_anak = db.Column(db.Text,nullable=False)
    urutan = db.Column(db.Integer,nullable=False)

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)


class KPSPJawaban(db.Model):
    __tablename__ = 'kpsp_jawaban'

    id = db.Column(db.Integer, primary_key=True)

    pendaftaran_id = db.Column(db.Integer,db.ForeignKey('pendaftaran.id'),nullable=False,index=True)

    pertanyaan_id = db.Column(db.Integer,db.ForeignKey('kpsp_pertanyaan.id'),nullable=False)

    jawaban = db.Column(db.Enum('ya', 'tidak', name='jawaban_kpsp_enum'),nullable=False)
    keterangan = db.Column(db.Text)
    catatan = db.Column(db.Text)

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)

    pertanyaan = db.relationship('KPSPPertanyaan')
    pendaftaran = db.relationship('Pendaftaran',backref='kpsp_jawaban')