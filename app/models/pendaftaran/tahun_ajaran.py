from app.extensions import db
from datetime import datetime

class TahunAjaran(db.Model):
    __tablename__ = 'tahun_ajaran'

    __table_args__ = (
        db.UniqueConstraint(
            'tahun_mulai',
            'tahun_selesai',
            name='unique_tahun_ajaran'
        ),
    )

    id = db.Column(db.Integer, primary_key=True)
    tahun_mulai = db.Column(db.Integer,nullable=False)
    tahun_selesai = db.Column(db.Integer,nullable=False)
    is_active = db.Column(db.Boolean,nullable=False,default=False)

    created_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)

    @property
    def label(self):
        return f"{self.tahun_mulai}/{self.tahun_selesai}"