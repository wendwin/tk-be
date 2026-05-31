from datetime import datetime
from app.extensions import db

class MonitoringIndikator(db.Model):
    __tablename__ = "monitoring_indikator"

    id = db.Column(db.Integer, primary_key=True)

    monitoring_siswa_id = db.Column(db.Integer,db.ForeignKey("monitoring_siswa.id"),nullable=False,index=True)

    tp_id = db.Column(db.Integer,db.ForeignKey("monitoring_tp.id"),nullable=False,index=True)

    muncul = db.Column(db.Boolean, nullable=False, default=False)
    kejadian_teramati = db.Column(db.Text)

    monitoring_siswa = db.relationship("MonitoringSiswa",backref="indikator")
    tp = db.relationship("MonitoringTP",backref="indikator_siswa")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)