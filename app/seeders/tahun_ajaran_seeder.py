from app.extensions import db
from app.models.pendaftaran.tahun_ajaran import TahunAjaran

def seed_tahun_ajaran():
    data = [
        # {"tahun_mulai": 2023, "tahun_selesai": 2024, "status": "nonaktif"},
        # {"tahun_mulai": 2024, "tahun_selesai": 2025, "status": "nonaktif"},
        {"tahun_mulai": 2025, "tahun_selesai": 2026, "status": "aktif"},
    ]

    for item in data:
        exists = TahunAjaran.query.filter_by(
            tahun_mulai=item["tahun_mulai"],
            tahun_selesai=item["tahun_selesai"]
        ).first()

        if not exists:
            db.session.add(TahunAjaran(**item))

    db.session.commit()
    print("Seeder tahun ajaran berhasil")