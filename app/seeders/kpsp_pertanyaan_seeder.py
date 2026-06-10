from app.extensions import db
from app.models.observasi.kpsp import KPSPPertanyaan

def seed_kpsp_pertanyaan():
    data = [
        {
            "usia_bulan": 24,
            "aspek_perkembangan": "Gerakan Kasar",
            "kemampuan_anak": "Anak mampu melompati garis dengan kedua kaki sekaligus",
            "urutan": 1
        },
        {
            "usia_bulan": 24,
            "aspek_perkembangan": "Gerakan Halus",
            "kemampuan_anak": "Anak mampu membuka botol dengan memutar tutupnya",
            "urutan": 2
        },
        {
            "usia_bulan": 24,
            "aspek_perkembangan": "Pengamatan",
            "kemampuan_anak": "Anak mampu menunjuk dan menyebutkan 6 bagian tubuh",
            "urutan": 3
        },
        {
            "usia_bulan": 24,
            "aspek_perkembangan": "Bicara",
            "kemampuan_anak": "Anak mampu menjawab dengan kalimat yang terdiri dari dua kata",
            "urutan": 4
        },
        {
            "usia_bulan": 24,
            "aspek_perkembangan": "Sosialisasi",
            "kemampuan_anak": "Anak mampu meniru kegiatan orang dewasa",
            "urutan": 5
        },
        {
            "usia_bulan": 30,
            "aspek_perkembangan": "Gerakan Kasar",
            "kemampuan_anak": "Anak mampu naik tangga dengan berpegangan",
            "urutan": 1
        },
        {
            "usia_bulan": 30,
            "aspek_perkembangan": "Gerakan Halus",
            "kemampuan_anak": "Anak mampu menyusun menara dari 8 balok",
            "urutan": 2
        },
        {
            "usia_bulan": 30,
            "aspek_perkembangan": "Pengamatan",
            "kemampuan_anak": "Anak mampu menunjuk gambar yang disebutkan",
            "urutan": 3
        },
        {
            "usia_bulan": 30,
            "aspek_perkembangan": "Bicara",
            "kemampuan_anak": "Anak mampu menyebut nama benda yang dikenal",
            "urutan": 4
        },
        {
            "usia_bulan": 30,
            "aspek_perkembangan": "Sosialisasi",
            "kemampuan_anak": "Anak mampu makan sendiri menggunakan sendok",
            "urutan": 5
        },
        {
            "usia_bulan": 36,
            "aspek_perkembangan": "Gerakan Kasar",
            "kemampuan_anak": "Anak mampu berdiri dengan satu kaki selama 2 detik",
            "urutan": 1
        },
        {
            "usia_bulan": 36,
            "aspek_perkembangan": "Gerakan Halus",
            "kemampuan_anak": "Anak mampu menggambar garis lurus",
            "urutan": 2
        },
        {
            "usia_bulan": 36,
            "aspek_perkembangan": "Pengamatan",
            "kemampuan_anak": "Anak mampu mengenali warna dasar",
            "urutan": 3
        },
        {
            "usia_bulan": 36,
            "aspek_perkembangan": "Bicara",
            "kemampuan_anak": "Anak mampu menyebut nama lengkap",
            "urutan": 4
        },
        {
            "usia_bulan": 36,
            "aspek_perkembangan": "Sosialisasi",
            "kemampuan_anak": "Anak mampu bermain bersama teman",
            "urutan": 5
        },

        {
            "usia_bulan": 48,
            "aspek_perkembangan": "Gerakan Kasar",
            "kemampuan_anak": "Anak mampu melompat dengan satu kaki",
            "urutan": 1
        },
        {
            "usia_bulan": 48,
            "aspek_perkembangan": "Gerakan Halus",
            "kemampuan_anak": "Anak mampu menggambar lingkaran",
            "urutan": 2
        },
        {
            "usia_bulan": 48,
            "aspek_perkembangan": "Pengamatan",
            "kemampuan_anak": "Anak mampu membedakan ukuran besar dan kecil",
            "urutan": 3
        },
        {
            "usia_bulan": 48,
            "aspek_perkembangan": "Bicara",
            "kemampuan_anak": "Anak mampu bercerita sederhana",
            "urutan": 4
        },
        {
            "usia_bulan": 48,
            "aspek_perkembangan": "Sosialisasi",
            "kemampuan_anak": "Anak mampu memakai pakaian sendiri",
            "urutan": 5
        },

        {
            "usia_bulan": 60,
            "aspek_perkembangan": "Gerakan Kasar",
            "kemampuan_anak": "Anak mampu menangkap bola kecil",
            "urutan": 1
        },
        {
            "usia_bulan": 60,
            "aspek_perkembangan": "Gerakan Halus",
            "kemampuan_anak": "Anak mampu menggambar manusia sederhana",
            "urutan": 2
        },
        {
            "usia_bulan": 60,
            "aspek_perkembangan": "Pengamatan",
            "kemampuan_anak": "Anak mampu mengenali bentuk dasar",
            "urutan": 3
        },
        {
            "usia_bulan": 60,
            "aspek_perkembangan": "Bicara",
            "kemampuan_anak": "Anak mampu menjawab pertanyaan sederhana",
            "urutan": 4
        },
        {
            "usia_bulan": 60,
            "aspek_perkembangan": "Sosialisasi",
            "kemampuan_anak": "Anak mampu bermain bergiliran",
            "urutan": 5
        },

        {
            "usia_bulan": 72,
            "aspek_perkembangan": "Gerakan Kasar",
            "kemampuan_anak": "Anak mampu berjalan lurus tumit ke jari kaki",
            "urutan": 1
        },
        {
            "usia_bulan": 72,
            "aspek_perkembangan": "Gerakan Halus",
            "kemampuan_anak": "Anak mampu menulis beberapa huruf",
            "urutan": 2
        },
        {
            "usia_bulan": 72,
            "aspek_perkembangan": "Pengamatan",
            "kemampuan_anak": "Anak mampu menghitung benda sederhana",
            "urutan": 3
        },
        {
            "usia_bulan": 72,
            "aspek_perkembangan": "Bicara",
            "kemampuan_anak": "Anak mampu berbicara jelas dan mudah dipahami",
            "urutan": 4
        },
        {
            "usia_bulan": 72,
            "aspek_perkembangan": "Sosialisasi",
            "kemampuan_anak": "Anak mampu mengikuti aturan permainan",
            "urutan": 5
        }
    ]

    for item in data:
        exists = KPSPPertanyaan.query.filter_by(
            usia_bulan=item['usia_bulan'],
            urutan=item['urutan']
        ).first()

        if exists:
            continue

        pertanyaan = KPSPPertanyaan(
            usia_bulan=item['usia_bulan'],
            aspek_perkembangan=item['aspek_perkembangan'],
            kemampuan_anak=item['kemampuan_anak'],
            urutan=item['urutan']
        )

        db.session.add(pertanyaan)

    db.session.commit()

    print('Seed KPSP pertanyaan berhasil')