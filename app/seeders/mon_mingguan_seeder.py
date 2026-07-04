import os
from datetime import date
from app.extensions import db

from app.models.auth.user import User
from app.models.akademik.kelas import Kelas
from app.models.pendaftaran.tahun_ajaran import TahunAjaran

from app.modules.monitoring.mingguan.service import create_mingguan


def seed_monitoring_mingguan():
    guru = User.query.filter_by(
    email=os.getenv("GURU1_EMAIL")
    ).first()

    kelas = Kelas.query.filter_by(
    jenjang="tk",
    kelompok="a"
    ).first()

    tahun_ajaran = TahunAjaran.query.filter_by(
        is_active=True
    ).first()

    if not guru or not kelas or not tahun_ajaran:
        print("Data guru, kelas, atau tahun ajaran belum tersedia")
        return

    monitoring_list = [
        # MINGGU 1
        {
            "kelas_id": kelas.id,
            "tahun_ajaran_id": tahun_ajaran.id,
            "semester": "ganjil",
            "minggu": "1",
            "topik": "Makanan Sehat dan Halal",
            "sub_topik": "Sayur dan Lauk Pauk",
            "tanggal_mulai": date(2026, 7, 6),
            "tanggal_selesai": date(2026, 7, 10),
            "status": "published",
        
            "tp": [
                {
                    "elemen": "nabp",
                    "tujuan": "Murid menerapkan nilai nilai ajaran agama dalam kehidupan sehari hari.",
                    "kktp": [
                        {"deskripsi": "Mengucapkan doa sebelum dan sesudah makan."},
                        {"deskripsi": "Memilih makanan halal sesuai arahan guru."},
                        {"deskripsi": "Menunjukkan perilaku berbagi saat kegiatan makan bersama."},
                    ]
                },
                {
                    "elemen": "ddlmstrs",
                    "tujuan": "Murid mengenal ciri ciri tubuh yang sehat.",
                    "kktp": [
                        {"deskripsi": "Menyebutkan minimal 3 makanan sehat."},
                        {"deskripsi": "Membedakan makanan sehat dan kurang sehat."},
                        {"deskripsi": "Menjelaskan manfaat makanan sehat secara sederhana."},
                    ]
                },
                {
                    "elemen": "jd",
                    "tujuan": "Murid melakukan gerakan motorik kasar dengan melibatkan keseimbangan dan koordinasi.",
                    "kktp": [
                        {"deskripsi": "Mengikuti permainan rintangan dengan baik."},
                        {"deskripsi": "Melompat dan berjalan sesuai instruksi."},
                        {"deskripsi": "Menjaga keseimbangan saat bergerak."},
                    ]
                },
                {
                    "elemen": "jd",
                    "tujuan": "Murid melakukan gerakan motorik halus.",
                    "kktp": [
                        {"deskripsi": "Menggunakan alat sederhana dengan tepat."},
                        {"deskripsi": "Mewarnai gambar makanan dengan rapi."},
                        {"deskripsi": "Memindahkan benda kecil menggunakan alat bantu."},
                    ]
                },
                {
                    "elemen": "ddlmstrs",
                    "tujuan": "Murid terlibat dalam kegiatan eksplorasi dan eksperimen.",
                    "kktp": [
                        {"deskripsi": "Mengamati proses pertumbuhan tanaman sederhana."},
                        {"deskripsi": "Menceritakan hasil pengamatan."},
                        {"deskripsi": "Mengajukan pertanyaan selama kegiatan eksplorasi."},
                    ]
                },
            ],
        
            "kegiatan": [
                {
                    "nama": "Mengenal sayur dan lauk pauk",
                    "media": "Sayuran asli, gambar makanan sehat"
                },
                {
                    "nama": "Membuat sate buah sederhana",
                    "media": "Buah potong, tusuk sate plastik"
                },
                {
                    "nama": "Permainan rintangan makanan sehat",
                    "media": "Cone, kartu gambar makanan"
                },
                {
                    "nama": "Menanam bawang merah",
                    "media": "Gelas plastik, kapas, bawang merah"
                },
                {
                    "nama": "Mewarnai gambar sayuran",
                    "media": "Lembar kerja dan krayon"
                },
            ],
        
            "asesmen_awal": {
                "teknik": "Observasi dan Tanya Jawab",
                "rancangan_kegiatan": "Guru menunjukkan gambar berbagai makanan kemudian mengajak anak berdiskusi tentang makanan sehat, makanan halal, dan manfaatnya bagi tubuh.",
                "hasil": "Sebagian besar anak telah mengenal beberapa jenis sayur dan buah, namun masih memerlukan pendampingan dalam menjelaskan manfaat makanan sehat bagi tubuh."
            }
        },

        # MINGGU 2
        {
            "kelas_id": kelas.id,
            "tahun_ajaran_id": tahun_ajaran.id,
            "semester": "ganjil",
            "minggu": "2",
            "topik": "Sekolahku",
            "sub_topik": "Ruang dan Fasilitas Sekolah",
            "tanggal_mulai": date(2026, 7, 13),
            "tanggal_selesai": date(2026, 7, 17),
            "status": "published",

            "tp": [
                {
                    "elemen": "nabp",
                    "tujuan": "Murid menunjukkan sikap menjaga lingkungan sekolah.",
                    "kktp": [
                        {"deskripsi": "Membuang sampah pada tempatnya."},
                        {"deskripsi": "Menjaga kebersihan kelas."},
                        {"deskripsi": "Merapikan alat bermain setelah digunakan."},
                    ]
                },
                {
                    "elemen": "ddlmstrs",
                    "tujuan": "Murid mengenal berbagai ruang di sekolah.",
                    "kktp": [
                        {"deskripsi": "Menyebutkan minimal 3 ruang di sekolah."},
                        {"deskripsi": "Menjelaskan fungsi ruang sekolah secara sederhana."},
                        {"deskripsi": "Mengelompokkan ruang berdasarkan kegunaannya."},
                    ]
                },
                {
                    "elemen": "jd",
                    "tujuan": "Murid melakukan gerakan motorik kasar melalui permainan mencari lokasi.",
                    "kktp": [
                        {"deskripsi": "Mengikuti permainan mencari lokasi sesuai instruksi."},
                        {"deskripsi": "Bergerak dengan aman saat berpindah tempat."},
                        {"deskripsi": "Menyelesaikan permainan hingga selesai."},
                    ]
                },
                {
                    "elemen": "jd",
                    "tujuan": "Murid membuat denah sederhana sekolah.",
                    "kktp": [
                        {"deskripsi": "Menggambar atau menempel ruang sekolah sederhana."},
                        {"deskripsi": "Menggunakan alat gambar dengan benar."},
                        {"deskripsi": "Menyelesaikan hasil karya hingga tuntas."},
                    ]
                },
                {
                    "elemen": "ddlmstrs",
                    "tujuan": "Murid mengungkapkan pengalaman belajar di sekolah.",
                    "kktp": [
                        {"deskripsi": "Menceritakan kegiatan favorit di sekolah."},
                        {"deskripsi": "Menjawab pertanyaan guru dengan jelas."},
                        {"deskripsi": "Mengungkapkan pendapat secara sederhana."},
                    ]
                },
            ],

            "kegiatan": [
                {"nama": "Jelajah sekolah", "media": "Kartu petunjuk, stiker"},
                {"nama": "Tebak ruangan sekolah", "media": "Flashcard gambar ruangan"},
                {"nama": "Menyusun denah sekolah", "media": "Kertas karton, lem, gambar ruangan"},
                {"nama": "Membangun sekolah mini", "media": "Balok konstruksi"},
                {"nama": "Mewarnai sekolahku", "media": "Krayon, lembar gambar sekolah"},
            ],

            "asesmen_awal": {
                "teknik": "Observasi dan Tanya Jawab",
                "rancangan_kegiatan": "Jelajah lingkungan sekolah.",
                "hasil": "Sebagian besar anak mengenal ruang kelas dan halaman sekolah."
            }
        },

        # MINGGU 3
        {
            "kelas_id": kelas.id,
            "tahun_ajaran_id": tahun_ajaran.id,
            "semester": "ganjil",
            "minggu": "3",
            "topik": "Profesi",
            "sub_topik": "Dokter dan Petugas Kesehatan",
            "tanggal_mulai": date(2026, 7, 20),
            "tanggal_selesai": date(2026, 7, 24),
            "status": "published",

            "tp": [
                {
                    "elemen": "nabp",
                    "tujuan": "Murid menghargai pekerjaan orang lain.",
                    "kktp": [
                        {"deskripsi": "Menunjukkan sikap menghargai profesi dokter."},
                        {"deskripsi": "Mendengarkan penjelasan guru dengan baik."},
                        {"deskripsi": "Menghormati pekerjaan orang lain."},
                    ]
                },
                {
                    "elemen": "ddlmstrs",
                    "tujuan": "Murid mengenal tugas dokter.",
                    "kktp": [
                        {"deskripsi": "Menyebutkan minimal 2 tugas dokter."},
                        {"deskripsi": "Mengenali alat kesehatan sederhana."},
                        {"deskripsi": "Menjelaskan fungsi dokter secara sederhana."},
                    ]
                },
                {
                    "elemen": "jd",
                    "tujuan": "Murid melakukan permainan motorik kasar bertema profesi.",
                    "kktp": [
                        {"deskripsi": "Mengikuti permainan profesi sesuai aturan."},
                        {"deskripsi": "Bergerak aktif saat permainan berlangsung."},
                        {"deskripsi": "Menyelesaikan permainan hingga selesai."},
                    ]
                },
                {
                    "elemen": "jd",
                    "tujuan": "Murid menggunakan alat main profesi dengan tepat.",
                    "kktp": [
                        {"deskripsi": "Menggunakan alat bermain profesi dengan benar."},
                        {"deskripsi": "Menunjukkan koordinasi tangan dan mata yang baik."},
                        {"deskripsi": "Menyelesaikan aktivitas bermain peran."},
                    ]
                },
                {
                    "elemen": "ddlmstrs",
                    "tujuan": "Murid mengungkapkan cita-citanya.",
                    "kktp": [
                        {"deskripsi": "Menyebutkan cita-cita yang diinginkan."},
                        {"deskripsi": "Menjelaskan alasan memilih cita-cita tersebut."},
                        {"deskripsi": "Berani menyampaikan cita-cita di depan teman."},
                    ]
                },
            ],

            "kegiatan": [
                {"nama": "Bermain dokter-dokteran", "media": "Stetoskop mainan, masker, termometer mainan"},
                {"nama": "Memeriksa pasien boneka", "media": "Boneka, perlengkapan dokter mainan"},
                {"nama": "Menyusun puzzle profesi", "media": "Puzzle profesi"},
                {"nama": "Estafet alat kesehatan", "media": "Cone, kartu alat kesehatan"},
                {"nama": "Menggambar cita-cita", "media": "Kertas gambar, krayon"},
            ],

            "asesmen_awal": {
                "teknik": "Observasi dan Tanya Jawab",
                "rancangan_kegiatan": "Pengenalan profesi dokter dan alat kesehatan.",
                "hasil": "Sebagian besar anak telah mengenal profesi dokter dan guru."
            }
        },

        # MINGGU 4
        {
            "kelas_id": kelas.id,
            "tahun_ajaran_id": tahun_ajaran.id,
            "semester": "ganjil",
            "minggu": "4",
            "topik": "Tanaman",
            "sub_topik": "Bagian dan Pertumbuhan Tanaman",
            "tanggal_mulai": date(2026, 7, 27),
            "tanggal_selesai": date(2026, 7, 31),
            "status": "published",

            "tp": [
                {
                    "elemen": "nabp",
                    "tujuan": "Murid mensyukuri ciptaan Tuhan berupa tanaman.",
                    "kktp": [
                        {"deskripsi": "Mengucapkan rasa syukur atas tanaman."},
                        {"deskripsi": "Menunjukkan kepedulian terhadap tanaman."},
                        {"deskripsi": "Tidak merusak tanaman saat kegiatan."},
                    ]
                },
                {
                    "elemen": "ddlmstrs",
                    "tujuan": "Murid mengenal bagian-bagian tanaman.",
                    "kktp": [
                        {"deskripsi": "Menyebutkan akar, batang, daun, dan bunga."},
                        {"deskripsi": "Menunjukkan bagian tanaman yang dimaksud guru."},
                        {"deskripsi": "Mengelompokkan bagian tanaman sederhana."},
                    ]
                },
                {
                    "elemen": "jd",
                    "tujuan": "Murid melakukan gerakan motorik kasar melalui permainan berkebun.",
                    "kktp": [
                        {"deskripsi": "Mengikuti aktivitas berkebun dengan baik."},
                        {"deskripsi": "Menggunakan alat berkebun secara aman."},
                        {"deskripsi": "Menyelesaikan kegiatan hingga selesai."},
                    ]
                },
                {
                    "elemen": "jd",
                    "tujuan": "Murid melakukan kegiatan menanam sederhana.",
                    "kktp": [
                        {"deskripsi": "Menanam biji sesuai tahapan sederhana."},
                        {"deskripsi": "Menggunakan alat dan bahan dengan benar."},
                        {"deskripsi": "Merawat tanaman setelah ditanam."},
                    ]
                },
                {
                    "elemen": "ddlmstrs",
                    "tujuan": "Murid mengamati pertumbuhan tanaman.",
                    "kktp": [
                        {"deskripsi": "Mengamati perubahan tanaman."},
                        {"deskripsi": "Menceritakan hasil pengamatan."},
                        {"deskripsi": "Menjawab pertanyaan guru tentang pertumbuhan tanaman."},
                    ]
                },
            ],

            "kegiatan": [
                {"nama": "Menanam kacang hijau", "media": "Gelas plastik, kapas, biji kacang hijau"},
                {"nama": "Menyiram tanaman", "media": "Gembor air, tanaman"},
                {"nama": "Kolase tanaman", "media": "Daun kering, bunga kering, lem"},
                {"nama": "Mengamati tanaman sekolah", "media": "Tanaman di lingkungan sekolah"},
                {"nama": "Menyusun puzzle bagian tanaman", "media": "Puzzle bagian tanaman"},
            ],

            "asesmen_awal": {
                "teknik": "Observasi dan Tanya Jawab",
                "rancangan_kegiatan": "Mengamati tanaman di lingkungan sekolah.",
                "hasil": "Sebagian besar anak mengenal daun dan bunga."
            }
        },
    ]

    for item in monitoring_list:
        try:
            create_mingguan(item, guru.id)
            print(f"Monitoring {item['topik']} berhasil dibuat")
        except Exception as e:
            print(f"Monitoring {item['topik']} gagal: {e}")

    db.session.commit()