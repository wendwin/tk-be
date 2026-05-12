from app.extensions import db
from datetime import datetime

class Alamat(db.Model):
    __tablename__ = 'alamat'

    id = db.Column(db.Integer, primary_key=True)
    alamat_lengkap = db.Column(db.Text, nullable=False)
    rt = db.Column(db.String(3), nullable=False)
    rw = db.Column(db.String(3), nullable=False)
    kelurahan = db.Column(db.String(100), nullable=False)
    kecamatan = db.Column(db.String(100), nullable=False)
    kabupaten = db.Column(db.String(100), nullable=False)
    kode_pos = db.Column(db.String(5), nullable=False)

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)