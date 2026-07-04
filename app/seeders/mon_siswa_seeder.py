from datetime import datetime

from app.extensions import db

from app.models.auth.user import User

from app.models.akademik.kelas import Kelas
from app.models.akademik.siswa_kelas import SiswaKelas

from app.models.monitoring.mingguan.monitoring import MonitoringMingguan
from app.models.monitoring.mingguan.tp import MonitoringTP
from app.models.monitoring.mingguan.kktp import MonitoringKKTP

from app.models.monitoring.siswa.siswa import MonitoringSiswa
from app.models.monitoring.siswa.indikator import MonitoringIndikator
from app.models.monitoring.siswa.karya import MonitoringKarya
from app.models.monitoring.siswa.anekdot import MonitoringAnekdot
from app.models.monitoring.siswa.rekomendasi import MonitoringRekomendasi


def seed_monitoring_siswa():

    guru = User.query.filter_by(
        first_name="Amelia"
    ).first()

    kelas = Kelas.query.filter_by(
        nama="Ayyub"
    ).first()

    if not guru or not kelas:
        print("Guru atau kelas tidak ditemukan")
        return

    siswa_kelas = (
        SiswaKelas.query
        .filter_by(kelas_id=kelas.id)
        .first()
    )

    if not siswa_kelas:
        print("Siswa kelas TK A belum ada")
        return

    monitoring_list = (
        MonitoringMingguan.query
        .filter_by(kelas_id=kelas.id)
        .order_by(MonitoringMingguan.minggu.asc())
        .all()
    )

    if not monitoring_list:
        print("Monitoring mingguan belum ada")
        return

    dummy_data = {
        "Makanan Sehat dan Halal": {
            "ringkasan": "Ananda menunjukkan perkembangan yang baik dalam mengenal makanan sehat dan halal. Selama kegiatan berlangsung, ananda aktif mengikuti arahan guru, mampu menyebutkan beberapa jenis sayur dan lauk, serta menunjukkan antusiasme saat kegiatan praktik menanam bawang merah dan membuat sate buah sederhana.",        
            "kegiatan": "Menanam Bawang Merah",     
            "deskripsi": "Ananda mengikuti kegiatan menanam bawang merah menggunakan media gelas plastik dan kapas basah. Ananda mampu mengikuti tahapan kegiatan mulai dari menyiapkan media hingga meletakkan bawang pada kapas.",        
            "analisa": "Ananda mampu mengikuti instruksi guru dengan baik dan menyelesaikan seluruh tahapan kegiatan secara mandiri. Koordinasi tangan dan mata terlihat berkembang dengan baik saat menata media tanam.",      
            "anekdot": "Saat kegiatan makan bersama, ananda menawarkan potongan buah miliknya kepada teman yang belum mendapatkan bagian. Perilaku ini menunjukkan sikap peduli dan kemampuan bersosialisasi yang baik.",
            "foto": "/uploads/monitoring/karya/makanan-sehat.jpg"
        },

        "Sekolahku": {
            "ringkasan": "Ananda menunjukkan antusiasme saat mengikuti kegiatan jelajah sekolah.",
            "kegiatan": "Menyusun Denah Sekolah",
            "deskripsi": "Ananda menyusun gambar ruang sekolah pada karton untuk membentuk denah sederhana sekolah.",
            "analisa": "Ananda memahami letak beberapa fasilitas sekolah dan mampu menyusun gambar sesuai urutan yang dikenalnya.",
            "anekdot": "Setelah kegiatan menggambar selesai, ananda membantu mengumpulkan sisa kertas dan membuangnya ke tempat sampah.",
            "foto": "/uploads/monitoring/karya/sekolahku.jpeg"
        },

        "Profesi": {
            "ringkasan": "Ananda menunjukkan minat yang tinggi terhadap profesi dokter.",
            "kegiatan": "Menggambar Cita-cita",
            "deskripsi": "Ananda menggambar dirinya sebagai dokter lengkap dengan alat kesehatan sederhana.",
            "analisa": "Ananda mampu menghubungkan kegiatan pembelajaran dengan cita-cita yang ingin diraih.",
            "anekdot": "Saat bermain dokter-dokteran, ananda memeriksa teman yang menjadi pasien dan memberi saran agar banyak minum air putih.",
            "foto": "/uploads/monitoring/karya/profesi.jpeg"
        },

        "Tanaman": {
            "ringkasan": "Ananda menunjukkan rasa ingin tahu yang tinggi terhadap tanaman.",
            "kegiatan": "Menanam Kacang Hijau",
            "deskripsi": "Ananda menanam biji kacang hijau menggunakan kapas basah dan melakukan pengamatan pertumbuhan tanaman.",
            "analisa": "Ananda menunjukkan ketelitian saat menanam dan mampu mengamati perubahan pertumbuhan tanaman dengan baik.",
            "anekdot": "Saat kegiatan menyiram tanaman, ananda mengingatkan temannya agar menyiram secukupnya supaya tanaman tidak rusak.",
            "foto": "/uploads/monitoring/karya/tanaman.jpg"
        }
    }

    for monitoring in monitoring_list:

        exists = MonitoringSiswa.query.filter_by(
            monitoring_mingguan_id=monitoring.id,
            siswa_kelas_id=siswa_kelas.id,
        ).first()

        if exists:
            continue

        data = dummy_data.get(monitoring.topik)

        if not data:
            continue

        monitoring_siswa = MonitoringSiswa(
            monitoring_mingguan_id=monitoring.id,
            siswa_kelas_id=siswa_kelas.id,
            created_by=guru.id,
            ringkasan=data["ringkasan"],
            status="published",
        )

        db.session.add(monitoring_siswa)
        db.session.flush()

        # indikator
        for tp in monitoring.tp:

            db.session.add(
                MonitoringIndikator(
                    monitoring_siswa_id=monitoring_siswa.id,
                    tp_id=tp.id,
                    muncul=True,
                    kejadian_teramati=f"Ananda menunjukkan perkembangan yang baik pada tujuan pembelajaran: {tp.tujuan}"
                )
            )

        # hasil karya
        kktp_karya = (
            MonitoringKKTP.query
            .join(MonitoringTP)
            .filter(
                MonitoringTP.monitoring_mingguan_id == monitoring.id
            )
            .first()
        )

        db.session.add(
            MonitoringKarya(
                monitoring_siswa_id=monitoring_siswa.id,
                kktp_id=kktp_karya.id,
                kegiatan=data["kegiatan"],
                foto=data["foto"],
                deskripsi=data["deskripsi"],
                analisa=data["analisa"],
            )
        )

        # anekdot
        db.session.add(
            MonitoringAnekdot(
                monitoring_siswa_id=monitoring_siswa.id,
                kktp_id=kktp_karya.id,
                waktu=datetime.utcnow(),
                catatan=data["anekdot"],
            )
        )

        # rekomendasi
        db.session.add(
            MonitoringRekomendasi(
                monitoring_siswa_id=monitoring_siswa.id,
                elemen="nabp",
                tips="Orang tua dapat melanjutkan stimulasi dan pembiasaan positif di rumah melalui aktivitas sehari-hari."
            )
        )

    db.session.commit()

    print("Seeder monitoring siswa berhasil")