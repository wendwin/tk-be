from app.extensions import db

from app.models.auth.user import User
from app.models.akademik.kelas import Kelas
from app.models.akademik.guru_kelas import GuruKelas
from app.models.pendaftaran import TahunAjaran


def seed_guru_kelas():

    tahun_ajaran = TahunAjaran.query.filter_by(
        is_active=True
    ).first()

    if not tahun_ajaran:
        print("Tahun ajaran aktif tidak ditemukan")
        return

    guru = User.query.filter_by(
        first_name="Amelia"
    ).first()

    kelas = Kelas.query.filter_by(
        nama="Ayyub",
        tahun_ajaran_id=tahun_ajaran.id
    ).first()

    if not guru:
        print("Guru Amelia tidak ditemukan")
        return

    if not kelas:
        print("Kelas Ayyub tidak ditemukan")
        return

    exists = GuruKelas.query.filter_by(
        guru_id=guru.id,
        kelas_id=kelas.id,
        tahun_ajaran_id=tahun_ajaran.id
    ).first()

    if exists:
        print("Relasi guru kelas sudah ada")
        return

    db.session.add(
        GuruKelas(
            guru_id=guru.id,
            kelas_id=kelas.id,
            tahun_ajaran_id=tahun_ajaran.id,
            peran="wali kelas"
        )
    )

    db.session.commit()

    print("Seeder guru kelas berhasil")