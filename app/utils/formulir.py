# import tempfile
# from reportlab.lib.pagesizes import mm
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
# from reportlab.lib.enums import TA_CENTER
# from reportlab.lib import colors
# from sqlalchemy.orm import joinedload

# from app.models.pendaftaran.pendaftaran import Pendaftaran
# from app.models.pendaftaran.peserta_didik import PesertaDidik


# FOLIO = (210 * mm, 330 * mm)


# def value_or_dash(value):
#     return str(value) if value not in [None, ""] else "-"


# def checkmark(condition):
#     return "☑" if condition else "☐"


# def generate_formulir_pendaftaran(pendaftaran_id):
#     pendaftaran = (
#         Pendaftaran.query
#         .options(
#             joinedload(Pendaftaran.peserta)
#             .joinedload(PesertaDidik.alamat_domisili),

#             joinedload(Pendaftaran.peserta)
#             .joinedload(PesertaDidik.alamat_kk),

#             joinedload(Pendaftaran.peserta)
#             .joinedload(PesertaDidik.kesehatan),

#             joinedload(Pendaftaran.peserta)
#             .joinedload(PesertaDidik.orang_tua),

#             joinedload(Pendaftaran.peserta)
#             .joinedload(PesertaDidik.informasi),

#             joinedload(Pendaftaran.tahun_ajaran),
#             joinedload(Pendaftaran.gelombang),
#         )
#         .filter(Pendaftaran.id == pendaftaran_id)
#         .first()
#     )

#     if not pendaftaran:
#         raise Exception("Data pendaftaran tidak ditemukan")

#     peserta = pendaftaran.peserta
#     alamat_dom = peserta.alamat_domisili
#     alamat_kk = peserta.alamat_kk
#     kesehatan = peserta.kesehatan
#     informasi = peserta.informasi

#     ayah = next((o for o in peserta.orang_tua if o.tipe == "ayah"), None)
#     ibu = next((o for o in peserta.orang_tua if o.tipe == "ibu"), None)

#     tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

#     doc = SimpleDocTemplate(
#         tmp.name,
#         pagesize=FOLIO,
#         rightMargin=45,
#         leftMargin=45,
#         topMargin=40,
#         bottomMargin=40,
#     )

#     styles = getSampleStyleSheet()

#     title_style = ParagraphStyle(
#         "TitleStyle",
#         parent=styles["Title"],
#         fontName="Helvetica-Bold",
#         fontSize=13,
#         leading=16,
#         alignment=TA_CENTER,
#     )

#     section_style = ParagraphStyle(
#         "SectionStyle",
#         parent=styles["Normal"],
#         fontName="Helvetica-Bold",
#         fontSize=11,
#         leading=14,
#         spaceBefore=12,
#         spaceAfter=6,
#     )

#     body_style = ParagraphStyle(
#         "BodyStyle",
#         parent=styles["Normal"],
#         fontName="Helvetica",
#         fontSize=10,
#         leading=13,
#     )

#     small_style = ParagraphStyle(
#         "SmallStyle",
#         parent=styles["Normal"],
#         fontName="Helvetica",
#         fontSize=9,
#         leading=12,
#     )

#     elements = []

#     def section(title):
#         elements.append(Paragraph(f"<b>{title}</b>", section_style))

#     def table_rows(rows):
#         data = []

#         for label, value in rows:
#             data.append([
#                 Paragraph(str(label), body_style),
#                 ":",
#                 Paragraph(value_or_dash(value), body_style),
#             ])

#         table = Table(data, colWidths=[150, 10, 350])
#         table.setStyle(TableStyle([
#             ("VALIGN", (0, 0), (-1, -1), "TOP"),
#             ("LEFTPADDING", (0, 0), (-1, -1), 0),
#             ("RIGHTPADDING", (0, 0), (-1, -1), 4),
#             ("TOPPADDING", (0, 0), (-1, -1), 3),
#             ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
#         ]))

#         elements.append(table)

#     def alamat_text(alamat):
#         if not alamat:
#             return "-"

#         return (
#             f"{alamat.alamat_lengkap}, "
#             f"RT {alamat.rt}/RW {alamat.rw}, "
#             f"{alamat.kelurahan}, {alamat.kecamatan}, "
#             f"{alamat.kabupaten}, {alamat.kode_pos}"
#         )

#     def ortu_rows(ortu):
#         return [
#             ("Nama", ortu.nama if ortu else "-"),
#             ("Tempat, Tanggal Lahir", f"{value_or_dash(ortu.tempat_lahir)}, {value_or_dash(ortu.tanggal_lahir)}" if ortu else "-"),
#             ("NIK", ortu.nik if ortu else "-"),
#             ("Pendidikan Terakhir", ortu.pendidikan if ortu else "-"),
#             ("Pekerjaan", ortu.pekerjaan if ortu else "-"),
#             ("Penghasilan", ortu.pendapatan if ortu else "-"),
#             ("Alamat Kantor", ortu.alamat_kantor if ortu else "-"),
#             ("No. HP", ortu.no_hp if ortu else "-"),
#             ("Email", ortu.email if ortu else "-"),
#         ]

#     tahun_label = pendaftaran.tahun_ajaran.label if pendaftaran.tahun_ajaran else "-"

#     elements.append(Paragraph("FORMULIR PENDAFTARAN PESERTA DIDIK BARU", title_style))
#     elements.append(Paragraph("KB & TK MASJID SYUHADA YOGYAKARTA", title_style))
#     elements.append(Paragraph(f"TAHUN AJARAN {tahun_label}", title_style))
#     elements.append(Spacer(1, 12))

#     table_rows([
#         ("No. Pendaftaran", pendaftaran.no_pendaftaran),
#         ("Jenis", pendaftaran.jenis.upper()),
#         ("Program", pendaftaran.program),
#         ("Gelombang", pendaftaran.gelombang.nama if pendaftaran.gelombang else "-"),
#         ("Tanggal Daftar", pendaftaran.created_at.strftime("%d-%m-%Y") if pendaftaran.created_at else "-"),
#     ])

#     section("A. DATA PESERTA DIDIK")
#     table_rows([
#         ("Nama Lengkap", peserta.nama_lengkap),
#         ("Nama Panggilan", peserta.nama_panggilan),
#         ("Jenis Kelamin", "Laki-laki" if peserta.jenis_kelamin == "L" else "Perempuan"),
#         ("Tempat, Tanggal Lahir", f"{peserta.tempat_lahir}, {peserta.tanggal_lahir}"),
#         ("Kewarganegaraan", peserta.kewarganegaraan),
#         ("NIK", peserta.nik),
#         ("No. KK", peserta.no_kk),
#         ("No. Akta Kelahiran", peserta.no_akta),
#         ("Agama", peserta.agama),
#         ("No. Telp/WhatsApp", peserta.no_telp),
#         ("Alamat Domisili", alamat_text(alamat_dom)),
#         ("Alamat Sesuai KK", alamat_text(alamat_kk)),
#         ("Anak ke", peserta.anak_ke),
#         ("Jumlah Saudara", peserta.jumlah_saudara),
#         ("Bahasa Sehari-hari", peserta.bahasa),
#     ])

#     section("B. DATA KESEHATAN ANAK")
#     table_rows([
#         ("Berat Badan", f"{value_or_dash(kesehatan.berat_badan if kesehatan else None)} kg"),
#         ("Tinggi Badan", f"{value_or_dash(kesehatan.tinggi_badan if kesehatan else None)} cm"),
#         ("Lingkar Kepala", f"{value_or_dash(kesehatan.lingkar_kepala if kesehatan else None)} cm"),
#         ("Golongan Darah", kesehatan.golongan_darah if kesehatan else "-"),
#         ("Penyakit yang Pernah Diderita", kesehatan.riwayat_penyakit if kesehatan else "-"),
#         ("Alergi", kesehatan.alergi if kesehatan else "-"),
#         ("Kebutuhan Khusus", ", ".join(kesehatan.kebutuhan_khusus) if kesehatan and kesehatan.kebutuhan_khusus else "-"),
#     ])

#     elements.append(PageBreak())

#     section("C. DATA AYAH KANDUNG")
#     table_rows(ortu_rows(ayah))

#     section("D. DATA IBU KANDUNG")
#     table_rows(ortu_rows(ibu))

#     section("E. KETERANGAN LAIN-LAIN UNTUK ANAK")
#     table_rows([
#         ("Tinggal Dengan", informasi.tinggal_dengan if informasi else "-"),
#         ("Jarak dari Rumah ke Sekolah", f"{value_or_dash(informasi.jarak_sekolah if informasi else None)} km"),
#         ("Waktu Tempuh", informasi.waktu_tempuh if informasi else "-"),
#         ("Kendaraan ke Sekolah", informasi.kendaraan if informasi else "-"),
#         ("Pernah Sekolah", "Ya" if informasi and informasi.pernah_sekolah else "Tidak"),
#         ("Nama Sekolah Sebelumnya", informasi.nama_sekolah if informasi else "-"),
#         ("NPSN", informasi.npsn if informasi else "-"),
#         ("NISN", informasi.nisn if informasi else "-"),
#         ("Bakat / Minat", informasi.bakat if informasi else "-"),
#         ("Hobi Anak", informasi.hobi if informasi else "-"),
#         ("Cita-cita Anak", informasi.cita_cita if informasi else "-"),
#         ("Mengenal Sekolah Dari", informasi.sumber_informasi if informasi else "-"),
#     ])

#     elements.append(Spacer(1, 30))

#     ttd = Table([
#         ["", "Yogyakarta, ................................"],
#         ["", ""],
#         ["", ""],
#         ["", "Orang Tua/Wali"],
#         ["", ""],
#         ["", ""],
#         ["", "( ........................................ )"],
#     ], colWidths=[300, 190])

#     ttd.setStyle(TableStyle([
#         ("ALIGN", (1, 0), (1, -1), "CENTER"),
#         ("TOPPADDING", (0, 0), (-1, -1), 5),
#         ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
#     ]))

#     elements.append(ttd)

#     doc.build(elements)

#     return tmp.name




import os
import tempfile

from reportlab.lib.pagesizes import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
    Image,
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from sqlalchemy.orm import joinedload

from app.models.pendaftaran.pendaftaran import Pendaftaran
from app.models.pendaftaran.peserta_didik import PesertaDidik


FOLIO = (210 * mm, 330 * mm)


def value_or_dash(value):
    return str(value) if value not in [None, ""] else "-"


def generate_formulir_pendaftaran(pendaftaran_id):
    pendaftaran = (
        Pendaftaran.query
        .options(
            joinedload(Pendaftaran.peserta).joinedload(PesertaDidik.alamat_domisili),
            joinedload(Pendaftaran.peserta).joinedload(PesertaDidik.alamat_kk),
            joinedload(Pendaftaran.peserta).joinedload(PesertaDidik.kesehatan),
            joinedload(Pendaftaran.peserta).joinedload(PesertaDidik.orang_tua),
            joinedload(Pendaftaran.peserta).joinedload(PesertaDidik.informasi),
            joinedload(Pendaftaran.dokumen),
            joinedload(Pendaftaran.tahun_ajaran),
            joinedload(Pendaftaran.gelombang),
        )
        .filter(Pendaftaran.id == pendaftaran_id)
        .first()
    )

    if not pendaftaran:
        raise Exception("Data pendaftaran tidak ditemukan")

    peserta = pendaftaran.peserta
    alamat_dom = peserta.alamat_domisili
    alamat_kk = peserta.alamat_kk
    kesehatan = peserta.kesehatan
    informasi = peserta.informasi

    ayah = next((o for o in peserta.orang_tua if o.tipe == "ayah"), None)
    ibu = next((o for o in peserta.orang_tua if o.tipe == "ibu"), None)

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(
        tmp.name,
        pagesize=FOLIO,
        rightMargin=40,
        leftMargin=40,
        topMargin=30,
        bottomMargin=30,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=16,
        leading=20,
        alignment=TA_CENTER,
    )

    sub_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        leading=14,
        alignment=TA_CENTER,
    )   

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        alignment=TA_CENTER,
    )

    number_style = ParagraphStyle(
        "NumberStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=15,
        leading=14,
        alignment=TA_CENTER,
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        leading=14,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
    )

    elements = []

    def section(title):
        elements.append(Paragraph(f"<b>{title}</b>", section_style))

    def create_table(rows):
        data = []

        for no, label, value in rows:
            data.append([
                Paragraph(str(no), body_style),
                Paragraph(str(label), body_style),
                ":",
                Paragraph(value_or_dash(value), body_style),
            ])

        table = Table(data, colWidths=[25, 170, 10, 290])

        table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 3),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
        ]))

        elements.append(table)

    def format_alamat(alamat):
        if not alamat:
            return "-"

        return (
            f"{value_or_dash(alamat.alamat_lengkap)}<br/>"
            f"RT/RW : {value_or_dash(alamat.rt)}/{value_or_dash(alamat.rw)}<br/>"
            f"Kelurahan : {value_or_dash(alamat.kelurahan)}<br/>"
            f"Kecamatan : {value_or_dash(alamat.kecamatan)}<br/>"
            f"Kabupaten : {value_or_dash(alamat.kabupaten)}<br/>"
            f"Kode Pos : {value_or_dash(alamat.kode_pos)}"
        )

    def get_photo_box():
        foto = next(
            (d for d in pendaftaran.dokumen if d.jenis_dokumen == "foto"),
            None
        )

        if foto:
            relative_path = foto.file_path.replace("/uploads/", "uploads/")
            foto_path = os.path.join(os.getcwd(), relative_path)

            if os.path.exists(foto_path):
                return Image(foto_path, width=35 * mm, height=45 * mm)

        box = Table(
            [[Paragraph("Photo anak", body_style)]],
            colWidths=[35 * mm],
            rowHeights=[45 * mm],
        )

        box.setStyle(TableStyle([
            ("BOX", (0, 0), (-1, -1), 1, colors.black),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]))

        return box

    def ortu_rows(ortu):
        return [
            ("1.", "Nama", ortu.nama if ortu else "-"),
            ("2.", "Tempat, Tanggal Lahir", f"{value_or_dash(ortu.tempat_lahir)}, {value_or_dash(ortu.tanggal_lahir)}" if ortu else "-"),
            ("3.", "NIK", ortu.nik if ortu else "-"),
            ("4.", "Alamat", format_alamat(ortu.alamat) if ortu and getattr(ortu, "alamat", None) else "-"),
            ("5.", "Pendidikan Terakhir", ortu.pendidikan if ortu else "-"),
            ("6.", "Pekerjaan", ortu.pekerjaan if ortu else "-"),
            ("7.", "Penghasilan", ortu.pendapatan if ortu else "-"),
            ("8.", "Alamat Kantor", ortu.alamat_kantor if ortu else "-"),
            ("9.", "No. HP", ortu.no_hp if ortu else "-"),
            ("10.", "Email", ortu.email if ortu else "-"),
        ]

    tahun_label = pendaftaran.tahun_ajaran.label if pendaftaran.tahun_ajaran else "-"

    logo_path = os.path.join(
        os.getcwd(),
        "app",
        "static",
        "images",
        "logo.jpg"
    )

    logo = Image(
        logo_path,
        width=24 * mm,
        height=24 * mm
    )

    header_left = Paragraph(
        "<b>KB & TK MASJID SYUHADA</b><br/>"
        "FORMULIR DATA",
        title_style,
    )

    school_info = Table(
        [
            ["Nama Lembaga", ":", "KB & TK Masjid Syuhada"],
            ["Status", ":", "Swasta"],
            ["Yayasan Penyelenggara", ":", "YASMA SYUHADA"],
            ["Alamat", ":", "Jl. Dewa Nyoman Oka No.13"],
            ["Telp/WhatsApp", ":", "082125124586"],
            ["Kelurahan", ":", "Kotabaru"],
            ["Kecamatan", ":", "Gondokusuman"],
            ["Kota", ":", "Yogyakarta"],
            ["Propinsi", ":", "Daerah Istimewa Yogyakarta"],
        ],
        colWidths=[42 * mm, 5 * mm, 58 * mm],
    )
    
    school_info.setStyle(TableStyle([
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
    
        ("TOPPADDING", (0, 0), (-1, -1), 1),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1),
    ]))

    no_pendaftaran_box = Table(
        [
            [Paragraph("<b>NO PENDAFTARAN</b>", subtitle_style)],
            [Paragraph(value_or_dash(pendaftaran.no_pendaftaran), number_style)],
        ],
        colWidths=[38 * mm],
        rowHeights=[10 * mm, 12 * mm],
    )

    no_pendaftaran_box.setStyle(TableStyle([
        ("BOX", (0, 0), (-1, -1), 1, colors.black),
        ("INNERGRID", (0, 0), (-1, -1), 1, colors.black),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))

    header = Table(
        [
            [logo, header_left, no_pendaftaran_box],
            [get_photo_box(), school_info, ""],
        ],
        colWidths=[45 * mm, 105 * mm, 40 * mm],
    )
    

    header.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),

        ("ALIGN", (0, 0), (0, 0), "CENTER"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("ALIGN", (2, 0), (2, 0), "RIGHT"),

        ("SPAN", (2, 0), (2, 1)),

        # jarak atas tiap bagian
        ("TOPPADDING", (0, 0), (0, 0), 0),
        ("TOPPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (2, 0), (2, 0), 0),

        ("TOPPADDING", (0, 1), (0, 1), 10),
        ("TOPPADDING", (1, 1), (1, 1), 8),

         # foto + school info geser kanan
        ("LEFTPADDING", (0, 1), (1, 1), 30),

        # jarak foto ke school info
        ("RIGHTPADDING", (0, 1), (0, 1), 12),

        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (1, 0), (1, 1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))

    elements.append(header)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(f"<b>DATA PESERTA DIDIK BARU TAHUN PELAJARAN {tahun_label}</b>", sub_style))
    elements.append(Spacer(1, 10))

    section("A. DATA PESERTA DIDIK")
    create_table([
        ("1.", "Nama Lengkap", peserta.nama_lengkap),
        ("2.", "Nama Panggilan", peserta.nama_panggilan),
        ("3.", "Jenis Kelamin", "Laki-laki" if peserta.jenis_kelamin == "L" else "Perempuan"),
        ("4.", "Tempat, Tanggal Lahir", f"{peserta.tempat_lahir}, {peserta.tanggal_lahir}"),
        ("5.", "Kewarganegaraan", peserta.kewarganegaraan),
        ("6.", "NIK", peserta.nik),
        ("7.", "No. KK", peserta.no_kk),
        ("8.", "No. Akta Kelahiran", peserta.no_akta),
        ("9.", "Agama", peserta.agama),
        ("10.", "No Telp / WhatsApp", peserta.no_telp),
        ("11.", "Alamat Domisili", format_alamat(alamat_dom)),
        ("12.", "Alamat Sesuai KK", format_alamat(alamat_kk)),
        ("13.", "Anak Ke", peserta.anak_ke),
        ("14.", "Jumlah Saudara", peserta.jumlah_saudara),
        ("15.", "Bahasa Sehari-hari", peserta.bahasa),
    ])

    elements.append(PageBreak())

    section("B. DATA KESEHATAN ANAK")
    create_table([
        ("1.", "Berat Badan", f"{value_or_dash(kesehatan.berat_badan if kesehatan else None)} kg"),
        ("2.", "Tinggi Badan", f"{value_or_dash(kesehatan.tinggi_badan if kesehatan else None)} cm"),
        ("3.", "Lingkar Kepala", f"{value_or_dash(kesehatan.lingkar_kepala if kesehatan else None)} cm"),
        ("4.", "Golongan Darah", kesehatan.golongan_darah if kesehatan else "-"),
        ("5.", "Riwayat Penyakit", kesehatan.riwayat_penyakit if kesehatan else "-"),
        ("6.", "Alergi", kesehatan.alergi if kesehatan else "-"),
        ("7.", "Kebutuhan Khusus", ", ".join(kesehatan.kebutuhan_khusus) if kesehatan and kesehatan.kebutuhan_khusus else "-"),
    ])

    # elements.append(PageBreak())

    section("C. DATA AYAH KANDUNG")
    create_table(ortu_rows(ayah))

    section("D. DATA IBU KANDUNG")
    create_table(ortu_rows(ibu))

    elements.append(PageBreak())

    section("E. KETERANGAN LAIN-LAIN UNTUK ANAK")
    create_table([
        ("1.", "Tinggal Dengan", informasi.tinggal_dengan if informasi else "-"),
        ("2.", "Jarak ke Sekolah", f"{value_or_dash(informasi.jarak_sekolah if informasi else None)} km"),
        ("3.", "Waktu Tempuh", informasi.waktu_tempuh if informasi else "-"),
        ("4.", "Kendaraan ke Sekolah", informasi.kendaraan if informasi else "-"),
        ("5.", "Pernah Sekolah", "Ya" if informasi and informasi.pernah_sekolah else "Tidak"),
        ("6.", "Nama Sekolah Sebelumnya", informasi.nama_sekolah if informasi else "-"),
        ("7.", "NPSN", informasi.npsn if informasi else "-"),
        ("8.", "NISN", informasi.nisn if informasi else "-"),
        ("9.", "Bakat", informasi.bakat if informasi else "-"),
        ("10.", "Hobi", informasi.hobi if informasi else "-"),
        ("11.", "Cita-cita", informasi.cita_cita if informasi else "-"),
        ("12.", "Mengenal Sekolah Dari", informasi.sumber_informasi if informasi else "-"),
    ])

    elements.append(Spacer(1, 30))

    ttd = Table([
        ["", "Yogyakarta, ................................"],
        ["", ""],
        ["", ""],
        ["", "Orang Tua / Wali"],
        ["", ""],
        ["", ""],
        ["", "( ........................................ )"],
    ], colWidths=[280, 180])

    ttd.setStyle(TableStyle([
        ("ALIGN", (1, 0), (1, -1), "CENTER"),
    ]))

    elements.append(ttd)

    doc.build(elements)

    return tmp.name