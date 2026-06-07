from app.extensions import db

from app.models.observasi.gpph import (
    GPPHPertanyaan
)


def seed_gpph_pertanyaan():

    data = [
        "Tidak kenal lelah atau aktivitas berlebihan",
        "Mudah menjadi gembira impulsif",
        "Mengganggu anak anak lain",
        "Gagal menyelesaikan kegiatan yang telah dimulai rentang perhatian pendek",
        "Menggerak gerakkan anggota badan atau kepala secara terus menerus",
        "Kurang perhatian mudah teralihkan",
        "Permintaannya harus segera dipenuhi mudah menjadi frustrasi",
        "Sering dan mudah menangis",
        "Suasana hatinya mudah berubah dengan cepat dan drastis",
        "Ledakan kekesalan tingkah laku eksplosif dan tak terduga"
    ]

    for index, item in enumerate(data, start=1):

        exists = GPPHPertanyaan.query.filter_by(
            urutan=index
        ).first()

        if exists:
            continue

        pertanyaan = GPPHPertanyaan(
            urutan=index,
            pertanyaan=item
        )

        db.session.add(pertanyaan)

    db.session.commit()

    print('Seed GPPH pertanyaan berhasil')
    
    