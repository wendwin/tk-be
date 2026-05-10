from datetime import datetime
from app.extensions import db
from app.models.pendaftaran import *
from sqlalchemy.orm import joinedload
from app.utils.file_helper import upload_dokumen

import tempfile
from reportlab.lib.pagesizes import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors
from sqlalchemy.orm import joinedload

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

def get_all(page=1, per_page=10, search=None):
    query = Pendaftaran.query.join(PesertaDidik)

    if search:
        query = query.filter(
            PesertaDidik.nama_lengkap.ilike(f"%{search}%")
        )

    return query.paginate(page=page, per_page=per_page, error_out=False)

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
    kesehatan = Kesehatan(
        peserta_id=peserta.id,
        **peserta_data["kesehatan"]
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
    gelombang = get_gelombang(datetime.utcnow())

    pendaftaran = Pendaftaran(
        peserta_id=peserta.id,
        tahun_ajaran_id=data["tahun_ajaran_id"],
        gelombang_id=gelombang.id if gelombang else None,
        no_pendaftaran=generate_no(),
        jenis=data["jenis"],
        program=data["program"],
        status='draft',
        status_pembayaran='unpaid',
        status_observasi='belum'
    )

    db.session.add(pendaftaran)

    db.session.commit()

    return pendaftaran

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

    db.session.commit()

    return {
        "total": len(uploaded),
        "dokumen": uploaded
    }

def upload_pembayaran_service(pendaftaran_id, user_id, file):
    pendaftaran = Pendaftaran.query.filter_by(
        id=pendaftaran_id,
        user_id=user_id
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

    pendaftaran.status_pembayaran = "pending"

    db.session.commit()

    return {
        "file_path": file_url,
        "status_pembayaran": pendaftaran.status_pembayaran
    }

FOLIO = (210*mm, 330*mm)
def generate_surat_pernyataan(user_id):
    pendaftaran = Pendaftaran.query.options(
        joinedload(Pendaftaran.peserta).joinedload(PesertaDidik.alamat_domisili),
        joinedload(Pendaftaran.peserta).joinedload(PesertaDidik.orang_tua),
        joinedload(Pendaftaran.tahun_ajaran),
    ).filter_by(user_id=user_id).first()

    if not pendaftaran:
        raise Exception("Data pendaftaran tidak ditemukan")

    peserta = pendaftaran.peserta
    ayah = next((o for o in peserta.orang_tua if o.tipe == "ayah"), None)
    alamat = peserta.alamat_domisili
    tahun_ajaran = (pendaftaran.tahun_ajaran.label if pendaftaran.tahun_ajaran else "................")
    
    alamat_text = "-"
    if alamat:
        alamat_text = f"{alamat.alamat_lengkap}, RT {alamat.rt}/RW {alamat.rw}, {alamat.kelurahan}, {alamat.kecamatan}, {alamat.kabupaten}"

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    doc = SimpleDocTemplate(
        tmp.name,
        pagesize=FOLIO,
        rightMargin=50,
        leftMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()
    
    body_style = ParagraphStyle(
        'BodyJustify',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        alignment=TA_JUSTIFY
    )

    sub_point_style = ParagraphStyle(
        'SubPoint',
        parent=body_style,
        leftIndent=5,
        spaceBefore=2
    )

    elements = []

    elements.append(Paragraph("<b>SURAT PERNYATAAN</b>", styles["Title"]))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Saya yang bertanda tangan di bawah ini:", body_style))
    elements.append(Spacer(1, 10))
    
    def create_data_table(label, value):
        t = Table([[Paragraph(label, body_style), ":", Paragraph(value, body_style)]], 
                 colWidths=[100, 10, 360])
    
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'), 
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 1), 
            ('BOTTOMPADDING', (0,0), (-1,-1), 1),
        ]))
        return t

    elements.append(create_data_table("Nama", ayah.nama if ayah else '-'))
    elements.append(create_data_table("Alamat", alamat_text))
    elements.append(Spacer(1, 15))
    elements.append(Paragraph("Orang tua/wali dari calon murid KB & TK Masjid Syuhada Yogyakarta:", body_style))
    elements.append(Spacer(1, 10))
    elements.append(create_data_table("Nama", peserta.nama_lengkap or '-'))
    elements.append(create_data_table("No Pendaftaran", pendaftaran.no_pendaftaran or '-'))
    elements.append(Spacer(1, 20))

    elements.append(Paragraph("Untuk melancarkan Pembelajaran KB & TK Masjid Syuhada dengan ini saya menyatakan:", body_style))
    elements.append(Spacer(1, 10))

    def create_point(no, text, is_sub=False):
        style = body_style if not is_sub else sub_point_style
        
        if is_sub:
            t = Table([["", no, Paragraph(text, style)]], colWidths=[25, 20, 415])
        else:
            t = Table([[no, Paragraph(text, style)]], colWidths=[20, 440])
            
        t.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
            ('TOPPADDING', (0,0), (-1,-1), 2),
        ]))
        return t

    elements.append(create_point("1.",f"Sanggup bersedia membayar deposit sebesar Rp................................. (...............................................................................................................................................) agar tercatat sebagai anak didik baru Tahun Ajaran {tahun_ajaran} yang akan diperhitungkan dalam administrasi keuangan."))
    elements.append(create_point("2.", "Apabila anak saya sudah terdaftar lalu mengundurkan diri/membatalkan menyekolahkan di KB & TK Masjid Syuhada, maka uang deposit akan saya infaqan 80% untuk pengembangan KB & TK Masjid Syuhada."))
    elements.append(create_point("3.", "Apabila saya telah memutuskan menyekolahkan anak saya di KB & TK Masjid Syuhada, maka saya akan menerima pengelompokkan anak saya sesuai ketentuan KB & TK Masjid Syuhada, mendukung penuh kegiatan bagi anak saya dan terlibat aktif pada kegiatan Orang Tua yang diselenggarakan oleh KB & TK Masjid Syuhada dan komite KB & TK Masjid Syuhada."))
    elements.append(create_point("4.", "Apabila saya telah memutuskan menyekolahkan anak saya di KB & TK Masjid Syuhada, maka saya akan mengikuti ketentuan pembayaran administrasi keuangan sesuai ketentuan KB & TK Masjid Syuhada sebagai berikut:"))
    
    elements.append(create_point("a.", "Pembayaran SPP dan komite dibayarkan setiap bulan paling lambat tanggal 10 setiap bulannya.", is_sub=True))
    elements.append(create_point("b.", "Memenuhi kewajiban pembayaran (SPP, Dana Pengembangan, Komite dll) sesuai ketentuan sekolah dan kesanggupan yang saya buat.", is_sub=True))
    
    elements.append(create_point("5.", "Saya bersedia anak saya tidak diperkenankan mengikuti KBM dan kegiatan sekolah lainnya selama jangka waktu tertentu apabila saya tidak mentaati pernyataan yang saya buat ini."))

    elements.append(Spacer(1, 10))
    elements.append(Paragraph("Demikian surat pernyataan ini saya buat dengan sebenar-benarnya dan penuh tanggung jawab.", body_style))
    elements.append(Spacer(1, 25))

    ttd_data = [
        ["", "Yogyakarta, ..............................."],
        ["", Spacer(1, 35)],
        ["", "Materai 10.000"],
        ["", f"( ....................................................... )"]
    ]
    tbl_ttd = Table(ttd_data, colWidths=[280, 190])
    tbl_ttd.setStyle(TableStyle([('ALIGN', (1,0), (1,-1), 'CENTER')]))
    elements.append(tbl_ttd)

    doc.build(elements)
    return tmp.name

def get_by_user_id(user_id):
    return Pendaftaran.query.filter_by(user_id=user_id).first()