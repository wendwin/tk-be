from app.extensions import db

from app.models.akademik.kelas import Kelas
from app.models.akademik.siswa import Siswa
from app.models.akademik.siswa_kelas import SiswaKelas

from app.models.pendaftaran import TahunAjaran


def seed_siswa_kelas():

    tahun_ajaran = TahunAjaran.query.filter_by(
        is_active=True
    ).first()

    if not tahun_ajaran:
        print("Tahun ajaran aktif tidak ditemukan")
        return

    kelas_kb = Kelas.query.filter_by(
        nama="KB",
        tahun_ajaran_id=tahun_ajaran.id
    ).first()

    kelas_tka = Kelas.query.filter_by(
        nama="Ayyub",
        tahun_ajaran_id=tahun_ajaran.id
    ).first()

    kelas_tkb = Kelas.query.filter_by(
        nama="Musa",
        tahun_ajaran_id=tahun_ajaran.id
    ).first()

    siswa_list = Siswa.query.all()

    for siswa in siswa_list:

        nama = siswa.peserta.nama_lengkap

        if nama in [
            "Bima Arya Pratama",
            "Aisyah Putri Maharani",
            "Raka Aditya",
            "Kayla Anindya",
            "Farel Mahendra",
            "Nayla Azahra",
            "Rafael Prakoso",
            "Celine Aurora",
        ]:
            kelas = kelas_kb

        elif nama in [
            "Abimanyu Saputra",
            "Naura Khairunnisa",
            # "Aditya Fauzan",
            # "Syakira Putri",
            # "Fathan Alfarezi",
            # "Nabila Safitri",
            # "Rasyid Ramadhan",
        ]:
            kelas = kelas_tka

        else:
            kelas = kelas_tkb

        exists = SiswaKelas.query.filter_by(
            siswa_id=siswa.id,
            tahun_ajaran_id=tahun_ajaran.id
        ).first()

        if exists:
            continue

        db.session.add(
            SiswaKelas(
                siswa_id=siswa.id,
                kelas_id=kelas.id,
                tahun_ajaran_id=tahun_ajaran.id,
                status="aktif",
            )
        )

    db.session.commit()

    print("Seeder siswa kelas berhasil")