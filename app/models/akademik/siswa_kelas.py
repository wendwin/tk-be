from datetime import datetime
from app.extensions import db


class SiswaKelas(db.Model):
    __tablename__ = "siswa_kelas"

    __table_args__ = (
        db.UniqueConstraint(
            "siswa_id",
            "tahun_ajaran_id",
            name="unique_siswa_per_tahun_ajaran"
        ),
    )

    id = db.Column(db.Integer, primary_key=True)

    siswa_id = db.Column(db.Integer,db.ForeignKey("siswa.id"),nullable=False,index=True)
    kelas_id = db.Column(db.Integer,db.ForeignKey("kelas.id"),nullable=False,index=True)
    tahun_ajaran_id = db.Column(db.Integer,db.ForeignKey("tahun_ajaran.id"),nullable=False,index=True)

    status = db.Column(db.Enum("aktif","naik","tinggal","pindah","lulus",name="status_siswa_kelas_enum"),nullable=False,default="aktif")
    
    siswa = db.relationship("Siswa",backref="riwayat_kelas")
    kelas = db.relationship("Kelas",backref="siswa_kelas")
    tahun_ajaran = db.relationship("TahunAjaran",backref="siswa_kelas")

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime,nullable=False,default=datetime.utcnow,onupdate=datetime.utcnow)