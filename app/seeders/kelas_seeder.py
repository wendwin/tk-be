from app.extensions import db
from app.models.akademik.kelas import Kelas
from app.models.pendaftaran import TahunAjaran


def seed_kelas():
    tahun_ajaran = TahunAjaran.query.filter_by(
        is_active=True
    ).first()

    if not tahun_ajaran:
        print("Tahun ajaran aktif tidak ditemukan")
        return

    data_kelas = [
        {
            "nama": "KB",
            "jenjang": "kb",
            "kelompok": None,
            "kapasitas": 15,
        },
        {
            "nama": "Ayyub",
            "jenjang": "tk",
            "kelompok": "a",
            "kapasitas": 15,
        },
        {
            "nama": "Musa",
            "jenjang": "tk",
            "kelompok": "b",
            "kapasitas": 15,
        },
    ]

    for item in data_kelas:
        exists = Kelas.query.filter_by(
            nama=item["nama"],
            tahun_ajaran_id=tahun_ajaran.id
        ).first()

        if exists:
            continue

        kelas = Kelas(
            tahun_ajaran_id=tahun_ajaran.id,
            nama=item["nama"],
            jenjang=item["jenjang"],
            kelompok=item["kelompok"],
            kapasitas=item["kapasitas"],
        )

        db.session.add(kelas)

    db.session.commit()

    print("Seeder kelas berhasil")