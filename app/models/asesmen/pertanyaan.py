from app.extensions import db
from datetime import datetime

from app.extensions import db
from datetime import datetime

class AsesmenPertanyaan(db.Model):
    __tablename__ = 'asesmen_pertanyaan'

    id = db.Column(db.Integer, primary_key=True)

    pertanyaan = db.Column(db.Text, nullable=False)
    urutan = db.Column(db.Integer)

    is_active = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)