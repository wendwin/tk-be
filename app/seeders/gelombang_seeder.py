from datetime import date
from app.extensions import db
from app.models.pendaftaran.gelombang import Gelombang

def seed_gelombang():

    data = [
        {
            "nama": "Gelombang 1",
            "tanggal_mulai": date(2025, 10, 1),
            "tanggal_selesai": date(2025, 12, 31),
            "tahun_ajaran_id": 1,
        },
        {
            "nama": "Gelombang 2",
            "tanggal_mulai": date(2026, 1, 1),
            "tanggal_selesai": date(2026, 3, 31),
            "tahun_ajaran_id": 1,
        },
        {
            "nama": "Gelombang 3",
            "tanggal_mulai": date(2026, 4, 1),
            "tanggal_selesai": date(2026, 6, 30),
            "tahun_ajaran_id": 1,
        },
    ]

    for item in data:

        exists = Gelombang.query.filter_by(
            nama=item["nama"],
            tahun_ajaran_id=item["tahun_ajaran_id"]
        ).first()

        if not exists:
            db.session.add(Gelombang(**item))

    db.session.commit()

    print("Seeder gelombang berhasil")