from datetime import datetime
from app.extensions import db
from app.models.pendaftaran import *
from sqlalchemy import or_
from sqlalchemy.orm import joinedload
from app.utils.file_helper import upload_dokumen

from app.models.pendaftaran.pendaftaran import Pendaftaran
from app.models.pendaftaran.peserta_didik import PesertaDidik
from app.models.akademik.siswa import Siswa
from app.modules.akademik.siswa.service import create_siswa_from_pendaftaran

# helper
def generate_no():
    last = Pendaftaran.query.order_by(Pendaftaran.id.desc()).first()
    if not last:
        return "001"
    return str(int(last.no_pendaftaran) + 1).zfill(3)

def get_gelombang(tanggal_daftar):
    return Gelombang.query.filter(
        Gelombang.tanggal_mulai <= tanggal_daftar,
        Gelombang.tanggal_selesai >= tanggal_daftar
    ).first()

def get_or_create_alamat(data):
    return Alamat.query.filter_by(
        alamat_lengkap=data.get("alamat_lengkap"),
        rt=data.get("rt"),
        rw=data.get("rw"),
        kelurahan=data.get("kelurahan"),
        kecamatan=data.get("kecamatan"),
        kabupaten=data.get("kabupaten"),
        kode_pos=data.get("kode_pos"),
    ).first() or Alamat(**data)

def sync_status_pendaftaran(pendaftaran):
    if (
        pendaftaran.status_berkas == "verified"
        and pendaftaran.status_pembayaran == "paid"
        and pendaftaran.status not in ["accepted", "rejected"]
    ):
        pendaftaran.status = "verified"

def get_all(
    page=1,
    per_page=10,
    search=None,
    status=None,
    status_pembayaran=None,
    jenis=None,
    program=None,
    tahun_ajaran_id=None):
    
    query = Pendaftaran.query.join(PesertaDidik)

    if jenis:
        query = query.filter(
            Pendaftaran.jenis == jenis
        )

    if program:
        query = query.filter(
            Pendaftaran.program == program
        )

    if tahun_ajaran_id:
        query = query.filter(
            Pendaftaran.tahun_ajaran_id == tahun_ajaran_id
        )

    if search:
        query = query.filter(
            or_(
                PesertaDidik.nama_lengkap.ilike(f"%{search}%"),
                Pendaftaran.no_pendaftaran.ilike(f"%{search}%")
            )
        )
    
    if status:
        query = query.filter(
            Pendaftaran.status == status
        )

    if status_pembayaran:
        query = query.filter(
            Pendaftaran.status_pembayaran == status_pembayaran
        )

    return query.order_by(
        Pendaftaran.tanggal_daftar.is_(None),
        Pendaftaran.tanggal_daftar.desc(),
        Pendaftaran.id.desc()
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

def create(data, user_id):
    peserta_data = data["peserta"]

    alamat_dom = get_or_create_alamat(peserta_data["alamat_domisili"])
    db.session.add(alamat_dom)
    db.session.flush()

    if peserta_data.get("alamat_kk_same", True):
        alamat_kk = alamat_dom
    else:
        alamat_kk = get_or_create_alamat(peserta_data["alamat_kk"])
        db.session.add(alamat_kk)
        db.session.flush()

    # peserta
    peserta = PesertaDidik(
        user_id=user_id,
        alamat_domisili_id=alamat_dom.id,
        alamat_kk_id=alamat_kk.id,
        nama_lengkap=peserta_data.get("nama_lengkap"),
        nama_panggilan=peserta_data.get("nama_panggilan"),
        tempat_lahir=peserta_data.get("tempat_lahir"),
        tanggal_lahir=peserta_data.get("tanggal_lahir"),
        jenis_kelamin=peserta_data.get("jenis_kelamin"),
        kewarganegaraan=peserta_data.get("kewarganegaraan"),
        nik=peserta_data.get("nik"),
        no_kk=peserta_data.get("no_kk"),
        no_akta=peserta_data.get("no_akta"),
        agama=peserta_data.get("agama"),
        no_telp=peserta_data.get("no_telp"),
        anak_ke=peserta_data.get("anak_ke"),
        jumlah_saudara=peserta_data.get("jumlah_saudara"),
        bahasa=peserta_data.get("bahasa"),
    )

    db.session.add(peserta)
    db.session.flush()

    # kesehatan
    kesehatan_data = peserta_data["kesehatan"]

    kesehatan = Kesehatan(
        peserta_id=peserta.id,
        berat_badan=kesehatan_data.get("berat_badan"),
        tinggi_badan=kesehatan_data.get("tinggi_badan"),
        lingkar_kepala=kesehatan_data.get("lingkar_kepala"),
        golongan_darah=kesehatan_data.get("golongan_darah"),
        riwayat_penyakit=kesehatan_data.get("riwayat_penyakit"),
        alergi=kesehatan_data.get("alergi"),

         kebutuhan_khusus=kesehatan_data.get("kebutuhan_khusus", [])
    )
    db.session.add(kesehatan)

    # orang tua
    for ortu in peserta_data["orang_tua"]:

        alamat = alamat_dom
        orang_tua = OrangTua(
            peserta_id=peserta.id,
            alamat_id=alamat.id,
            tipe=ortu.get("tipe"),
            nama=ortu.get("nama"),
            tempat_lahir=ortu.get("tempat_lahir"),
            tanggal_lahir=ortu.get("tanggal_lahir"),
            nik=ortu.get("nik"),
            pendidikan=ortu.get("pendidikan"),
            pekerjaan=ortu.get("pekerjaan"),
            pendapatan=ortu.get("pendapatan"),
            alamat_kantor=ortu.get("alamat_kantor"),
            no_hp=ortu.get("no_hp"),
            email=ortu.get("email"),
        )

        db.session.add(orang_tua)

    # informasi
    informasi = Informasi(
        peserta_id=peserta.id,
        **peserta_data["informasi"]
    )
    db.session.add(informasi)

    # pendaftaran   
    pendaftaran = Pendaftaran(
        peserta_id=peserta.id,
        tahun_ajaran_id=data["tahun_ajaran_id"],
        gelombang_id=None,
        no_pendaftaran=generate_no(),
        jenis=data["jenis"],
        program=data["program"],
        status='draft',
        status_berkas='belum_upload',
        status_pembayaran='unpaid',
        status_observasi='belum'
    )

    db.session.add(pendaftaran)

    db.session.commit()

    return pendaftaran

def get_by_id(id, user_id=None):
    query = (
        Pendaftaran.query
        .join(Pendaftaran.peserta)
        .options(
            joinedload(Pendaftaran.peserta)
                .joinedload(PesertaDidik.kesehatan),
            joinedload(Pendaftaran.peserta)
                .joinedload(PesertaDidik.orang_tua),
            joinedload(Pendaftaran.peserta)
                .joinedload(PesertaDidik.alamat_domisili),
            joinedload(Pendaftaran.peserta)
                .joinedload(PesertaDidik.alamat_kk),
            joinedload(Pendaftaran.peserta)
                .joinedload(PesertaDidik.informasi),
            joinedload(Pendaftaran.dokumen)
        )
        .filter(Pendaftaran.id == id)
    )

    if user_id:
        query = query.filter(PesertaDidik.user_id == user_id)

    return query.first()

# update 
def update_pendaftaran_service(pendaftaran, data):
    pendaftaran.jenis = data.get("jenis", pendaftaran.jenis)
    pendaftaran.program = data.get("program", pendaftaran.program)

    peserta_data = data.get("peserta", {})
    peserta = pendaftaran.peserta

    # peserta
    for field in [
        "nama_lengkap", "nama_panggilan", "tempat_lahir",
        "tanggal_lahir", "jenis_kelamin", "kewarganegaraan",
        "nik", "no_kk", "no_akta", "agama",
        "no_telp", "anak_ke", "jumlah_saudara", "bahasa"
    ]:
        if field in peserta_data:
            setattr(peserta, field, peserta_data[field])

    # alamat domisili
    alamat_data = peserta_data.get("alamat_domisili")
    if alamat_data and peserta.alamat_domisili:
        alamat = peserta.alamat_domisili

        for field in [
            "alamat_lengkap", "rt", "rw",
            "kelurahan", "kecamatan",
            "kabupaten", "kode_pos"
        ]:
            if field in alamat_data:
                setattr(alamat, field, alamat_data[field])

    # alamat kk
    alamat_kk_same = peserta_data.get("alamat_kk_same", True)

    if alamat_kk_same:
        peserta.alamat_kk = peserta.alamat_domisili
    else:
        alamat_kk_data = peserta_data.get("alamat_kk")

        if alamat_kk_data:
            if peserta.alamat_kk:
                alamat_kk = peserta.alamat_kk
                for field in [
                    "alamat_lengkap", "rt", "rw",
                    "kelurahan", "kecamatan",
                    "kabupaten", "kode_pos"
                ]:
                    if field in alamat_kk_data:
                        setattr(alamat_kk, field, alamat_kk_data[field])
            else:
                new_alamat = Alamat(**alamat_kk_data)
                db.session.add(new_alamat)
                db.session.flush()
                peserta.alamat_kk = new_alamat

    # kesehatan
    kesehatan_data = peserta_data.get("kesehatan", {})
    if peserta.kesehatan and kesehatan_data:
        kesehatan = peserta.kesehatan

        for field in [
            "berat_badan", "tinggi_badan", "lingkar_kepala",
            "golongan_darah", "riwayat_penyakit",
            "alergi", "kebutuhan_khusus"
        ]:
            if field in kesehatan_data:
                setattr(kesehatan, field, kesehatan_data[field])

    # informasi
    info_data = peserta_data.get("informasi", {})
    if peserta.informasi and info_data:
        info = peserta.informasi

        for field in [
            "tinggal_dengan", "jarak_sekolah", "waktu_tempuh",
            "kendaraan", "pernah_sekolah", "nama_sekolah",
            "npsn", "nisn", "bakat", "hobi",
            "cita_cita", "sumber_informasi"
        ]:
            if field in info_data:
                setattr(info, field, info_data[field])

    # orang tua
    orang_tua_list = peserta_data.get("orang_tua", [])

    for ot_data in orang_tua_list:
        tipe = ot_data.get("tipe")

        ot = next((o for o in peserta.orang_tua if o.tipe == tipe), None)
        if not ot:
            continue

        for field in [
            "nama", "tempat_lahir", "tanggal_lahir",
            "nik", "pendidikan", "pekerjaan",
            "pendapatan", "no_hp", "email",
            "alamat_kantor"
        ]:
            if field in ot_data:
                setattr(ot, field, ot_data[field])

    db.session.commit()
    return pendaftaran

def upload_berkas_service(pendaftaran_id, user_id, files):
    pendaftaran = Pendaftaran.query.join(Pendaftaran.peserta).filter(
        Pendaftaran.id == pendaftaran_id,
        PesertaDidik.user_id == user_id
    ).first()

    if not pendaftaran:
        raise Exception("Data tidak ditemukan")

    dokumen_map = {
        "kk": ("kk", "kk"),
        "akta": ("akta", "akta"),
        "kia": ("kia", "kia"),
        "foto": ("foto", "foto"),
        "surat_pernyataan": ("surat_pernyataan", "surat_pernyataan")
    }

    missing = [key for key in dokumen_map.keys() if not files.get(key)]
    if missing:
        raise Exception(f"Semua berkas wajib diupload: {', '.join(missing)}")

    uploaded = []

    for key, (jenis, folder) in dokumen_map.items():
        file = files.get(key)

        file_url = upload_dokumen(
            pendaftaran,
            file,
            jenis,
            folder=f"dokumen/{folder}"
        )

        uploaded.append({
            "jenis": jenis,
            "file_path": file_url
        })
    
    pendaftaran.status_berkas = "pending"

    db.session.commit()

    return {
        "total": len(uploaded),
        "status_berkas": pendaftaran.status_berkas,
        "dokumen": uploaded
    }

def update_status_berkas_service(id, status):
    if status not in ["verified", "rejected"]:
        raise ValueError("Status berkas tidak valid")

    pendaftaran = get_by_id(id)

    if not pendaftaran:
        raise ValueError("Data tidak ditemukan")

    pendaftaran.status_berkas = status

    if status == "rejected":
        pendaftaran.status = "pending"
    else:
        sync_status_pendaftaran(pendaftaran)

    db.session.commit()

    return {
        "status_berkas": pendaftaran.status_berkas,
        "status": pendaftaran.status,
    }

def update_status_pembayaran_service(id, status):
    if status not in ["paid", "failed"]:
        raise ValueError("Status pembayaran tidak valid")

    pendaftaran = get_by_id(id)

    if not pendaftaran:
        raise ValueError("Data tidak ditemukan")

    pendaftaran.status_pembayaran = status

    if status == "failed":
        pendaftaran.status = "pending"
    else:
        sync_status_pendaftaran(pendaftaran)

    db.session.commit()

    return {
        "status_pembayaran": pendaftaran.status_pembayaran,
        "status": pendaftaran.status,
    }

def update_status_pendaftaran_service(id, status):
    if status not in ["pending", "verified", "accepted", "rejected"]:
        raise ValueError("Status tidak valid")

    pendaftaran = get_by_id(id)

    if not pendaftaran:
        raise ValueError("Data tidak ditemukan")

    pendaftaran.status = status

    db.session.commit()

    if status == "accepted":
        existing = Siswa.query.filter_by(
            peserta_id=pendaftaran.peserta_id
        ).first()

        if not existing:
            create_siswa_from_pendaftaran(id)

    return {
        "status": pendaftaran.status
    }

def upload_pembayaran_service(pendaftaran_id, user_id, file):
    pendaftaran = Pendaftaran.query.join(Pendaftaran.peserta).filter(
        Pendaftaran.id == pendaftaran_id,
        PesertaDidik.user_id == user_id
    ).first()

    if not pendaftaran:
        raise Exception("Data tidak ditemukan")

    if pendaftaran.status_pembayaran == "paid":
        raise Exception("Pembayaran sudah diverifikasi")

    file_url = upload_dokumen(
        pendaftaran,
        file,
        jenis="bukti_pembayaran",
        folder="pembayaran"
    )

    now = datetime.utcnow()

    gelombang = get_gelombang(now)
    if not gelombang:
        raise Exception("Tidak ada gelombang pendaftaran yang aktif")

    pendaftaran.status_pembayaran = "pending"
    pendaftaran.status = "pending"
    pendaftaran.tanggal_daftar = now
    pendaftaran.gelombang_id = gelombang.id

    db.session.commit()

    return {
        "file_path": file_url,
        "status_pembayaran": pendaftaran.status_pembayaran,
        "status": pendaftaran.status,
        "tanggal_daftar": pendaftaran.tanggal_daftar
    }

def get_by_user_id(user_id):
    return (
        Pendaftaran.query
        .join(PesertaDidik)
        .options(
            joinedload(Pendaftaran.peserta),
            joinedload(Pendaftaran.tahun_ajaran),
            joinedload(Pendaftaran.dokumen),
        )
        .filter(PesertaDidik.user_id == user_id)
        .order_by(Pendaftaran.created_at.desc())
        .all()
    )