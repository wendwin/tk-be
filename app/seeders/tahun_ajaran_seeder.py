from datetime import date
from app.extensions import db
from app.models.pendaftaran.tahun_ajaran import TahunAjaran



def seed_tahun_ajaran():

    data = [
        {
            "tahun_mulai": 2026,
            "tahun_selesai": 2027,
            "tanggal_mulai": date(2026, 7, 13),
            "tanggal_selesai": date(2027, 6, 18),
            "is_active": True
        },
    ]

    for item in data:

        exists = TahunAjaran.query.filter_by(
            tahun_mulai=item["tahun_mulai"],
            tahun_selesai=item["tahun_selesai"]
        ).first()

        if exists:
            continue

        tahun_ajaran = TahunAjaran(
            tahun_mulai=item["tahun_mulai"],
            tahun_selesai=item["tahun_selesai"],
            tanggal_mulai=item["tanggal_mulai"],
            tanggal_selesai=item["tanggal_selesai"],
            is_active=item["is_active"]
        )

        db.session.add(tahun_ajaran)

    db.session.commit()

    print("Seeder tahun ajaran berhasil")