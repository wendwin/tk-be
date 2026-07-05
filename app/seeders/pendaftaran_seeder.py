from datetime import date, datetime
from werkzeug.security import generate_password_hash

from app.extensions import db

from app.models.auth.user import User
from app.models.auth.role import Role

from app.models.pendaftaran import (
    Alamat,
    PesertaDidik,
    Informasi,
    Kesehatan,
    OrangTua,
    Pendaftaran,
    Dokumen,
    TahunAjaran,
    Gelombang,
)

from app.models.akademik.siswa import Siswa

from app.models.observasi import (
    GPPHPertanyaan,
    GPPHJawaban,
    KPSPPertanyaan,
    KPSPJawaban,
)


def seed_pendaftaran():
    role_orang_tua = Role.query.filter_by(name="orang_tua").first()

    if not role_orang_tua:
        print("Role orang_tua tidak ditemukan")
        return

    tahun_ajaran = TahunAjaran.query.filter_by(is_active=True).first()
    gelombang = Gelombang.query.first()

    if not tahun_ajaran or not gelombang:
        print("Tahun ajaran atau gelombang belum ada")
        return

    gpph_pertanyaan = GPPHPertanyaan.query.order_by(
        GPPHPertanyaan.urutan.asc()
    ).all()

    if not gpph_pertanyaan:
        print("Master pertanyaan GPPH belum ada")
        return

    kelompok_data = [
        {
            "kode": "KB",
            "jenis": "kb",
            "bulan": 36,
            "tahun_lahir": 2023,
            "bulan_lahir": 5,
            "nama_list": [
                "Bima Arya Pratama",
                "Aisyah Putri Maharani",
                "Raka Aditya",
                "Kayla Anindya",
                "Farel Mahendra",
                "Nayla Azahra",
                "Rafael Prakoso",
                "Celine Aurora",
                # "Alvaro Wijaya",
                # "Shakira Maharani",
                # "Daffa Ramadhan",
                # "Zahra Amalia",
                # "Arkan Maulana",
                # "Salsabila Putri",
                # "Keanu Pratama",
            ],
        },
        {
            "kode": "TKA",
            "jenis": "tk",
            "bulan": 48,
            "tahun_lahir": 2022,
            "bulan_lahir": 5,
            "nama_list": [
                "Abimanyu Saputra",
                "Naura Khairunnisa",
                "Aditya Fauzan",
                "Syakira Putri",
                "Fathan Alfarezi",
                "Nabila Safitri",
                "Rasyid Ramadhan",
                # "Calista Aurelia",
                # "Aqila Maharani",
                # "Farhan Akbar",
                # "Queen Anindita",
                # "Reyhan Prakoso",
                # "Tasya Kirana",
                # "Haikal Dzaki",
                # "Zivan Alghifari",
            ],
        },
        {
            "kode": "TKB",
            "jenis": "tk",
            "bulan": 60,
            "tahun_lahir": 2021,
            "bulan_lahir": 5,
            "nama_list": [
                "Alfian Nugraha",
                "Aurel Cahyani",
                "Danish Mahardika",
                "Kezia Valencia",
                "Fahri Ramadhan",
                "Mikhaila Putri",
                "Rafandra Wijaya",
                "Kiara Jasmine",
                "Arya Bintang",
                "Sheva Maharani",
                "Dzaky Alfatih",
                # "Meisya Azzahra",
                # "Rendra Saputra",
                # "Alesha Khansa",
                # "Nathaniel Adrian",
            ],
        },
    ]

    tanggal_lahir_list = [
        # KB
        date(2023, 8, 10),
        date(2023, 5, 12),
        date(2023, 1, 20),
        date(2022, 11, 5),
        date(2022, 9, 15),
    
        # TK A
        date(2021, 12, 10),
        date(2021, 10, 15),
        date(2021, 8, 20),
        date(2021, 5, 10),
        date(2021, 2, 1),
    
        # TK B
        date(2020, 12, 20),
        date(2020, 9, 12),
        date(2020, 6, 1),
        date(2020, 3, 15),
        date(2019, 12, 5),
    ]

    tanggal_daftar_list = [

       datetime(2026, 1, 5),
       datetime(2026, 1, 9),
       datetime(2026, 1, 12),
       datetime(2026, 1, 18),
       datetime(2026, 1, 24),
       datetime(2026, 1, 28),

       datetime(2026, 2, 3),
       datetime(2026, 2, 8),
       datetime(2026, 2, 14),
       datetime(2026, 2, 20),
       datetime(2026, 2, 26),

       datetime(2026, 3, 4),
       datetime(2026, 3, 9),
       datetime(2026, 3, 15),
       datetime(2026, 3, 19),
       datetime(2026, 3, 24),
       datetime(2026, 3, 29),

       datetime(2026, 4, 8),
       datetime(2026, 4, 14),
       datetime(2026, 4, 20),
       datetime(2026, 4, 27),

       datetime(2026, 5, 3),
       datetime(2026, 5, 10),
       datetime(2026, 5, 17),
       datetime(2026, 5, 22),
       datetime(2026, 5, 25),
    ]

    counter = 1

    for kelompok in kelompok_data:
        for i, nama in enumerate(kelompok["nama_list"], start=1):
            panggilan = nama.split()[0]

            exists = PesertaDidik.query.filter_by(
                nama_lengkap=nama
            ).first()

            if exists:
                counter += 1
                continue

            email_ortu = f"orangtua{counter}@gmail.com"

            user = User.query.filter_by(email=email_ortu).first()

            if not user:
                nama_split = nama.split()

                first_name = nama_split[0]
                last_name = " ".join(nama_split[1:]) if len(nama_split) > 1 else None
                
                user = User(
                    first_name=first_name,
                    last_name=last_name,
                    email=email_ortu,
                    password=generate_password_hash("password"),
                    role_id=role_orang_tua.id,
                    is_verified=True,
                    is_active=True,
                )
                db.session.add(user)
                db.session.flush()

            alamat = Alamat(
                alamat_lengkap=f"Jl Gatot Subroto Barat No {counter}",
                rt="01",
                rw="05",
                kelurahan="Pemecutan",
                kecamatan="Denpasar Barat",
                kabupaten="Denpasar",
                kode_pos=f"802{counter % 100:02}",
            )

            db.session.add(alamat)
            db.session.flush()

            # tanggal_lahir = date(
            #     kelompok["tahun_lahir"],
            #     kelompok["bulan_lahir"],
            #     min(i, 28),
            # )

            tanggal_lahir = tanggal_lahir_list[i % len(tanggal_lahir_list)]

            peserta = PesertaDidik(
                user_id=user.id,
                alamat_domisili_id=alamat.id,
                alamat_kk_id=alamat.id,
                nama_lengkap=nama,
                nama_panggilan=panggilan,
                tempat_lahir="Denpasar",
                tanggal_lahir=tanggal_lahir,
                jenis_kelamin="L" if i % 2 else "P",
                kewarganegaraan="Indonesia",
                nik=f"510302040506{counter:04}",
                no_kk=f"510302040507{counter:04}",
                no_akta=f"AK{counter:08}",
                agama="islam",
                no_telp=f"08123456{counter:04}",
                anak_ke=1,
                jumlah_saudara=1,
                bahasa="Indonesia",
            )

            db.session.add(peserta)
            db.session.flush()

            ada_catatan = counter in [5, 17, 29, 42]

            informasi = Informasi(
                peserta_id=peserta.id,
                tinggal_dengan="orang tua",
                jarak_sekolah=5.0,
                waktu_tempuh="10 menit",
                kendaraan="mobil",
                pernah_sekolah=False,
                nama_sekolah="",
                npsn="",
                nisn="",
                bakat="Menggambar",
                hobi="Bermain",
                cita_cita="Dokter",
                sumber_informasi="Instagram",
            )

            kesehatan = Kesehatan(
                peserta_id=peserta.id,
                berat_badan=18 + (i % 5),
                tinggi_badan=90 + (i % 10),
                lingkar_kepala=40,
                golongan_darah="O",
                riwayat_penyakit="",
                alergi="",
                kebutuhan_khusus=["perlu pendampingan saat fokus"]
                if ada_catatan
                else ["tidak ada"],
            )

            db.session.add(informasi)
            db.session.add(kesehatan)

            ayah = OrangTua(
                peserta_id=peserta.id,
                alamat_id=alamat.id,
                tipe="ayah",
                nama=f"Ayah {panggilan}",
                tempat_lahir="Denpasar",
                tanggal_lahir=date(1990, 1, 1),
                nik=f"3201010101{counter:06}",
                pendidikan="S1",
                pekerjaan="Pegawai Swasta",
                pendapatan=10000000,
                alamat_kantor="Kantor Denpasar",
                no_hp=f"08111111{counter:04}",
                email=f"ayah{counter}@mail.com",
            )

            ibu = OrangTua(
                peserta_id=peserta.id,
                alamat_id=alamat.id,
                tipe="ibu",
                nama=f"Ibu {panggilan}",
                tempat_lahir="Denpasar",
                tanggal_lahir=date(1992, 1, 1),
                nik=f"3202020202{counter:06}",
                pendidikan="S1",
                pekerjaan="Ibu Rumah Tangga",
                pendapatan=5000000,
                alamat_kantor="",
                no_hp=f"08222222{counter:04}",
                email=f"ibu{counter}@mail.com",
            )

            db.session.add(ayah)
            db.session.add(ibu)

            tanggal_daftar = tanggal_daftar_list[(counter - 1) % len(tanggal_daftar_list)]

            total_pendaftar = sum(
                len(kelompok["nama_list"])
                for kelompok in kelompok_data
            )

            if counter > total_pendaftar - 5:
                status = "pending"
                status_berkas = "pending"
                status_pembayaran = "pending"
                status_observasi = "belum"
                create_siswa = False
            else:
                status = "accepted"
                status_berkas = "verified"
                status_pembayaran = "paid"
                status_observasi = "hadir"
                create_siswa = True

            pendaftaran = Pendaftaran(
                peserta_id=peserta.id,
                tahun_ajaran_id=tahun_ajaran.id,
                gelombang_id=gelombang.id,
                no_pendaftaran=f"{counter:03}",
                tanggal_daftar=tanggal_daftar,
                status=status,
                status_berkas=status_berkas,
                status_pembayaran=status_pembayaran,
                jenis=kelompok["jenis"],
                program="fullday",
                status_observasi=status_observasi,
            )

            db.session.add(pendaftaran)
            db.session.flush()

            if create_siswa:
                siswa = Siswa(
                    peserta_id=peserta.id,
                    nisn=f"00512345{counter:03}",
                    tanggal_masuk=tahun_ajaran.tanggal_mulai,
                    status="aktif",
                )

                db.session.add(siswa)

            dokumen_mapping = {
                "kk": "/uploads/dokumen/kk/contoh_kk.jpg",
                "akta": "/uploads/dokumen/akta/contoh_akta.jpg",
                "kia": "/uploads/dokumen/kia/contoh_kia.jpg",
                "foto": "/uploads/dokumen/foto/contoh_foto.png",
                "surat_pernyataan": "/uploads/dokumen/surat_pernyataan/contoh_surat.pdf",
                "bukti_pembayaran": "/uploads/pembayaran/contoh_pembayaran.jpg",
            }

            for jenis_dokumen, path in dokumen_mapping.items():
                db.session.add(
                    Dokumen(
                        pendaftaran_id=pendaftaran.id,
                        jenis_dokumen=jenis_dokumen,
                        file_path=path,
                    )
                )

            if create_siswa:
                for idx, pertanyaan in enumerate(gpph_pertanyaan):
                    nilai = 2 if ada_catatan and idx in [0, 3, 5] else idx % 2

                    db.session.add(
                        GPPHJawaban(
                            pendaftaran_id=pendaftaran.id,
                            pertanyaan_id=pertanyaan.id,
                            snapshot_urutan=pertanyaan.urutan,
                            snapshot_pertanyaan=pertanyaan.pertanyaan,
                            nilai=nilai,
                        )
                    )

                kpsp_pertanyaan = (
                    KPSPPertanyaan.query
                    .filter_by(usia_bulan=kelompok["bulan"])
                    .order_by(KPSPPertanyaan.urutan.asc())
                    .all()
                )

                catatan = (
                    "Anak perlu perhatian pada fokus dan instruksi berulang."
                    if ada_catatan
                    else "Anak mengikuti observasi dengan baik."
                )

                for idx, pertanyaan in enumerate(kpsp_pertanyaan):
                    jawaban = "tidak" if ada_catatan and idx in [2, 4] else "ya"

                    db.session.add(
                        KPSPJawaban(
                            pendaftaran_id=pendaftaran.id,
                            pertanyaan_id=pertanyaan.id,
                            snapshot_usia_bulan=pertanyaan.usia_bulan,
                            snapshot_aspek_perkembangan=pertanyaan.aspek_perkembangan,
                            snapshot_kemampuan_anak=pertanyaan.kemampuan_anak,
                            snapshot_urutan=pertanyaan.urutan,
                            jawaban=jawaban,
                            keterangan=(
                                "Perlu stimulasi lanjutan"
                                if jawaban == "tidak"
                                else ""
                            ),
                            catatan=catatan,
                        )
                    )

            counter += 1

    db.session.commit()
    print("Seeder pendaftaran 26 siswa berhasil")