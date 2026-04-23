from app.extensions import db
from app.models.asesmen import AsesmenPertanyaan

def seed_asesmen_pertanyaan():
    data = [
      {
        "pertanyaan": "Dari mana Ayah/Bunda mengetahui informasi tentang KB & TK Masjid Syuhada (media sosial, keluarga, atau lainnya)?",
        "urutan": 1
      },
      {
        "pertanyaan": "Mengapa Ayah/Bunda memilih KB & TK Masjid Syuhada sebagai sekolah ananda?",
        "urutan": 2
      },
      {
        "pertanyaan": "Apa harapan Ayah/Bunda menyekolahkan ananda di KB & TK Masjid Syuhada Yogyakarta?",
        "urutan": 3
      },
      {
        "pertanyaan": "Apa saja aktivitas harian ananda di pagi, siang, sore, dan malam hari?",
        "urutan": 4
      },
      {
        "pertanyaan": "Bagaimana kemampuan komunikasi ananda (lancar, jelas, cadel, atau ada keterlambatan bicara)?",
        "urutan": 5
      },
      {
        "pertanyaan": "Bagaimana pengelolaan emosi ananda (bisa diajak berdiskusi, tantrum, dll) dan bagaimana Ayah/Bunda meregulasinya?",
        "urutan": 6
      },
      {
        "pertanyaan": "Apakah ananda mengonsumsi nasi, sayur, lauk, dan buah serta apakah ada alergi makanan?",
        "urutan": 7
      },
      {
        "pertanyaan": "Apakah ananda memiliki riwayat kesehatan yang perlu diperhatikan saat bersekolah?",
        "urutan": 8
      },
      {
        "pertanyaan": "Bagaimana kemampuan toileting (BAK & BAB) ananda? Apakah sudah mandiri atau masih dibantu, dan apakah sudah lepas popok?",
        "urutan": 9
      },
      {
        "pertanyaan": "Bagaimana Ayah/Bunda mengenalkan pembelajaran agama kepada ananda (mengenal Allah, nabi, sholat, iqro, dll)?",
        "urutan": 10
      },
      {
        "pertanyaan": "Apakah Ayah/Bunda setuju bahwa pendidikan di sekolah dan di rumah harus seiring dan sejalan untuk tumbuh kembang anak yang optimal?",
        "urutan": 11
      }
    ]

    existing = AsesmenPertanyaan.query.first()
    if existing:
        print("Seeder asesmen pertanyaan sudah ada")
        return

    for item in data:
        pertanyaan = AsesmenPertanyaan(**item)
        db.session.add(pertanyaan)

    db.session.commit()
    print("Seeder asesmen pertanyaan berhasil")