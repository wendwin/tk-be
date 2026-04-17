from app.extensions import db
from app.models.pendaftaran import *
from sqlalchemy.orm import joinedload

import os
from werkzeug.utils import secure_filename
from datetime import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
UPLOAD_FOLDER = 'uploads/pembayaran'
MAX_FILE_SIZE_PAYMENT = 2 * 1024 * 1024  # 2MB

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_no():
    last = Pendaftaran.query.order_by(Pendaftaran.id.desc()).first()
    if not last:
        return "001"
    return str(int(last.no_pendaftaran) + 1).zfill(3)

def get_all(page=1, per_page=10, search=None):
    query = Pendaftaran.query.join(PesertaDidik)

    if search:
        query = query.filter(
            PesertaDidik.nama_lengkap.ilike(f"%{search}%")
        )

    return query.paginate(page=page, per_page=per_page, error_out=False)

def create(data, user_id):
    no = generate_no()

    peserta_data = data["peserta"]

    # pendaftaran
    pendaftaran = Pendaftaran(
        user_id=user_id,
        no_pendaftaran=no,
        id_tahun=data["id_tahun"],
        jenis=data["jenis"],
        program=data["program"]
    )
    db.session.add(pendaftaran)
    db.session.flush()

    # alamat
    alamat_dom = Alamat(**peserta_data["alamat_domisili"])
    alamat_kk = Alamat(**peserta_data["alamat_kk"])
    db.session.add_all([alamat_dom, alamat_kk])
    db.session.flush()

    # peserta
    peserta = PesertaDidik(
        id_pendaftaran=pendaftaran.id,
        id_alamat_domisili=alamat_dom.id,
        id_alamat_kk=alamat_kk.id,
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
    if peserta_data.get("kesehatan"):
        kesehatan = Kesehatan(
            id_peserta=peserta.id,
            **peserta_data["kesehatan"]
        )
        db.session.add(kesehatan)

    # orang tua
    if peserta_data.get("orang_tua"):
        for ortu in peserta_data["orang_tua"]:
            alamat = Alamat(**ortu["alamat"])
            db.session.add(alamat)
            db.session.flush()

            orang_tua = OrangTua(
                id_peserta=peserta.id,
                id_alamat=alamat.id,
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
    if peserta_data.get("informasi"):
        info = Informasi(
            id_peserta=peserta.id,
            **peserta_data["informasi"]
        )
        db.session.add(info)

    db.session.commit()
    return pendaftaran

from sqlalchemy.orm import joinedload

def get_by_id(id):
    return Pendaftaran.query.options(
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
    ).filter_by(id=id).first()

def upload_pembayaran_service(pendaftaran_id, user_id, file):
    pendaftaran = Pendaftaran.query.filter_by(
        id=pendaftaran_id,
        user_id=user_id
    ).first()

    if not pendaftaran:
        raise Exception("Data tidak ditemukan atau bukan milik user")

    # validasi ekstensi
    if not allowed_file(file.filename):
        raise Exception("Format file tidak diizinkan (png, jpg, jpeg)")

    # validasi ukuran file
    file.seek(0, os.SEEK_END)
    file_length = file.tell()

    if file_length > MAX_FILE_SIZE_PAYMENT:
        raise Exception("Ukuran file maksimal 2MB")

    file.seek(0)

    # generate nama file
    filename = secure_filename(file.filename)
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    filename = f"{timestamp}_{filename}"

    # simpan file
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    file.save(filepath)

    file_url = f"/uploads/pembayaran/{filename}"

    dokumen = Dokumen(
        id_pendaftaran=pendaftaran.id,
        jenis_dokumen="bukti_pembayaran",
        file_path=file_url
    )
    db.session.add(dokumen)

    # update status pembayaran
    pendaftaran.status_pembayaran = "pending"

    db.session.commit()

    return {
        "file_path": filepath,
        "status_pembayaran": pendaftaran.status_pembayaran
    }