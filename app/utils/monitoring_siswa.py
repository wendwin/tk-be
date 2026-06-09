import os
import tempfile
from datetime import datetime

from reportlab.lib.pagesizes import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    PageBreak,
)
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from sqlalchemy.orm import joinedload

from app.models.monitoring.siswa.siswa import MonitoringSiswa
from app.models.monitoring.mingguan.monitoring import MonitoringMingguan
from app.models.monitoring.mingguan.tp import MonitoringTP
from app.models.akademik.guru_kelas import GuruKelas
from app.models.auth.user import User
from app.models.auth.role import Role


FOLIO = (210 * mm, 330 * mm)


def value_or_dash(value):
    return str(value) if value not in [None, ""] else "-"


def format_tanggal(date):
    if not date:
        return "-"

    return date.strftime("%d-%m-%Y")


def format_datetime(date):
    if not date:
        return "-"

    return date.strftime("%d-%m-%Y %H:%M")


def format_elemen(elemen):
    mapping = {
        "kesyuhadaan": "Kesyuhadaan",
        "nabp": "Nilai Agama & Budi Pekerti",
        "jd": "Jati Diri",
        "ddlmstrs": "Literasi & STEM",
    }

    return mapping.get(elemen, elemen)


def format_kelas(kelas):
    if not kelas:
        return "-"

    if kelas.jenjang == "kb":
        return kelas.nama

    kelompok = kelas.kelompok.upper() if kelas.kelompok else ""
    return f"{kelas.jenjang.upper()}-{kelompok} {kelas.nama}"


def get_siswa_name(siswa):
    if not siswa:
        return "-"

    return (
        getattr(siswa, "nama_lengkap", None)
        or getattr(getattr(siswa, "peserta", None), "nama_lengkap", None)
        or "-"
    )


def get_siswa_nisn(siswa):
    if not siswa:
        return "-"

    return (
        getattr(siswa, "nisn", None)
        or getattr(getattr(siswa, "peserta", None), "nisn", None)
        or "-"
    )


def get_siswa_jk(siswa):
    if not siswa:
        return "-"

    jk = (
        getattr(siswa, "jenis_kelamin", None)
        or getattr(getattr(siswa, "peserta", None), "jenis_kelamin", None)
        or "-"
    )

    if jk == "L":
        return "Laki-laki"

    if jk == "P":
        return "Perempuan"

    return jk


def get_file_path(path):
    if not path:
        return None

    clean_path = path.replace("/uploads/", "uploads/")
    full_path = os.path.join(os.getcwd(), clean_path)

    if os.path.exists(full_path):
        return full_path

    return None


def create_image_or_dash(path, width=55 * mm, height=40 * mm):
    file_path = get_file_path(path)

    if not file_path:
        return Paragraph("-", getSampleStyleSheet()["Normal"])

    try:
        return Image(file_path, width=width, height=height)
    except Exception:
        return Paragraph("-", getSampleStyleSheet()["Normal"])


def get_kktp_text(kktp):
    if not kktp:
        return "-"

    return getattr(kktp, "deskripsi", None) or "-"

def get_guru_kelas(kelas_id, tahun_ajaran_id):
    return (
        GuruKelas.query
        .filter_by(
            kelas_id=kelas_id,
            tahun_ajaran_id=tahun_ajaran_id,
        )
        .all()
    )


def format_guru_list(guru_kelas_list):
    if not guru_kelas_list:
        return "-"

    result = []

    for item in guru_kelas_list:
        nama = item.guru.full_name if item.guru else "-"
        peran = item.peran.capitalize() or "-"

        result.append(f"{nama} ({peran})")

    return "<br/>".join(result)


def table_style():
    return TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 5),
    ])


def info_table_style():
    return TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ])

def get_kepsek_name():
    kepsek = (
        User.query
        .join(User.role)
        .filter(
            Role.name == "kepsek",
            User.is_active == True,
        )
        .first()
    )

    return kepsek.full_name if kepsek else ".................................."


def get_guru_ttd(kelas_id, tahun_ajaran_id):
    guru_kelas = (
        GuruKelas.query
        .filter_by(
            kelas_id=kelas_id,
            tahun_ajaran_id=tahun_ajaran_id,
        )
        .order_by(GuruKelas.peran.desc())
        .all()
    )

    if not guru_kelas:
        return ".................................."

    return "<br/>".join([
        item.guru.full_name
        for item in guru_kelas
        if item.guru
    ])

def generate_monitoring_siswa_pdf(id):
    monitoring_siswa = (
        MonitoringSiswa.query
        .options(
            joinedload(MonitoringSiswa.monitoring_mingguan)
            .joinedload(MonitoringMingguan.kelas),
            joinedload(MonitoringSiswa.monitoring_mingguan)
            .joinedload(MonitoringMingguan.tahun_ajaran),
            joinedload(MonitoringSiswa.monitoring_mingguan)
            .joinedload(MonitoringMingguan.tp)
            .joinedload(MonitoringTP.kktp),
            joinedload(MonitoringSiswa.siswa_kelas),
            joinedload(MonitoringSiswa.karya),
            joinedload(MonitoringSiswa.anekdot),
            joinedload(MonitoringSiswa.indikator),
            joinedload(MonitoringSiswa.rekomendasi),
        )
        .filter(MonitoringSiswa.id == id)
        .first()
    )

    if not monitoring_siswa:
        raise Exception("Data monitoring siswa tidak ditemukan")

    monitoring = monitoring_siswa.monitoring_mingguan
    guru_kelas_list = get_guru_kelas(
        monitoring.kelas_id,
        monitoring.tahun_ajaran_id,
    )
    siswa_kelas = monitoring_siswa.siswa_kelas
    siswa = siswa_kelas.siswa if siswa_kelas else None

    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")

    doc = SimpleDocTemplate(
        tmp.name,
        pagesize=FOLIO,
        rightMargin=40,
        leftMargin=40,
        topMargin=35,
        bottomMargin=35,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=15,
        alignment=TA_CENTER,
        spaceAfter=8,
    )

    subtitle_style = ParagraphStyle(
        "SubtitleStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=16,
    )

    section_style = ParagraphStyle(
        "SectionStyle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=11,
        spaceBefore=12,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12,
    )

    small_style = ParagraphStyle(
        "SmallStyle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8,
        leading=10,
    )

    ttd_style = ParagraphStyle(
        "TtdStyle",
        parent=body_style,
        alignment=TA_CENTER,
    )

    elements = []

    elements.append(Paragraph("LAPORAN MONITORING SISWA", title_style))
    elements.append(Paragraph("KB & TK Masjid Syuhada", subtitle_style))

    info_rows = [
        ["Nama Siswa", ":", get_siswa_name(siswa)],
        ["NISN", ":", get_siswa_nisn(siswa)],
        ["Jenis Kelamin", ":", get_siswa_jk(siswa)],
        ["Kelas", ":", format_kelas(monitoring.kelas if monitoring else None)],
        [
            "Tahun Ajaran",
            ":",
            value_or_dash(monitoring.tahun_ajaran.label if monitoring and monitoring.tahun_ajaran else None),
        ],
        ["Semester", ":", value_or_dash(monitoring.semester if monitoring else None)],
        ["Minggu", ":", value_or_dash(monitoring.minggu if monitoring else None)],
        ["Topik", ":", value_or_dash(monitoring.topik if monitoring else None)],
        ["Sub Topik", ":", value_or_dash(monitoring.sub_topik if monitoring else None)],
        [
            "Tanggal",
            ":",
            f"{format_tanggal(monitoring.tanggal_mulai)} s.d. {format_tanggal(monitoring.tanggal_selesai)}"
            if monitoring else "-",
        ],
        ["Guru", ":", format_guru_list(guru_kelas_list)],
    ]

    info_table = Table(info_rows, colWidths=[100, 10, 355])
    info_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    elements.append(info_table)

    elements.append(Paragraph("A. Tujuan Pembelajaran", section_style))

    tp_rows = [["No", "Elemen", "Tujuan Pembelajaran", "KKTP"]]

    for index, tp in enumerate(monitoring.tp or [], start=1):
        kktp_text = "<br/>".join([
            f"• {value_or_dash(kktp.deskripsi)}"
            for kktp in tp.kktp
        ])

        tp_rows.append([
            str(index),
            Paragraph(format_elemen(tp.elemen), small_style),
            Paragraph(value_or_dash(tp.tujuan), small_style),
            Paragraph(kktp_text or "-", small_style),
        ])

    tp_table = Table(tp_rows, colWidths=[25, 95, 160, 185], repeatRows=1)
    tp_table.setStyle(table_style())
    elements.append(tp_table)

    elements.append(Paragraph("B. Kegiatan", section_style))

    kegiatan_rows = [["No", "Kegiatan", "Alat/Bahan atau Media"]]

    for index, kegiatan in enumerate(monitoring.kegiatan or [], start=1):
        kegiatan_rows.append([
            str(index),
            Paragraph(value_or_dash(kegiatan.nama), small_style),
            Paragraph(value_or_dash(kegiatan.media), small_style),
        ])

    kegiatan_table = Table(kegiatan_rows, colWidths=[25, 220, 220], repeatRows=1)
    kegiatan_table.setStyle(table_style())
    elements.append(kegiatan_table)

    elements.append(PageBreak())

    elements.append(Paragraph("C. Rancangan Kegiatan", section_style))

    if monitoring.asesmen_awal:
        elements.append(Paragraph(
            value_or_dash(monitoring.asesmen_awal.rancangan_kegiatan),
            body_style,
        ))
    else:
        elements.append(Paragraph("-", body_style))

    elements.append(Paragraph("D. Ringkasan Perkembangan", section_style))
    elements.append(Paragraph(value_or_dash(monitoring_siswa.ringkasan), body_style))

    elements.append(Paragraph("E. Asesmen Awal", section_style))

    if monitoring.asesmen_awal:
        asesmen_rows = [
            ["Teknik", ":", value_or_dash(monitoring.asesmen_awal.teknik)],
            ["Hasil", ":", value_or_dash(monitoring.asesmen_awal.hasil)],
        ]
    else:
        asesmen_rows = [["Asesmen Awal", ":", "-"]]

    asesmen_table = Table(asesmen_rows, colWidths=[100, 10, 355])
    asesmen_table.setStyle(info_table_style())
    elements.append(asesmen_table)

    # elements.append(Paragraph("A. Ringkasan Perkembangan", section_style))
    # elements.append(Paragraph(value_or_dash(monitoring_siswa.ringkasan), body_style))

    elements.append(Paragraph("F. Hasil Karya", section_style))

    karya_list = monitoring_siswa.karya or []

    if not karya_list:
        elements.append(Paragraph("Belum ada hasil karya.", body_style))
    else:
        for index, item in enumerate(karya_list, start=1):
            elements.append(Paragraph(f"<b>Karya {index}</b>", body_style))

            karya_info = [
                ["Kegiatan", ":", Paragraph(value_or_dash(item.kegiatan), body_style)],
                ["KKTP", ":", Paragraph(get_kktp_text(item.kktp), body_style)],
                ["Deskripsi", ":", Paragraph(value_or_dash(item.deskripsi), body_style)],
                ["Analisa Guru", ":", Paragraph(value_or_dash(item.analisa), body_style)],
            ]

            karya_table = Table(
                karya_info,
                colWidths=[85, 10, 370],
            )

            karya_table.setStyle(TableStyle([
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
            ]))

            elements.append(karya_table)
            elements.append(Spacer(1, 8))

            foto = create_image_or_dash(
                item.foto,
                width=80 * mm,
                height=55 * mm,
            )

            foto_box = Table(
                [[foto]],
                colWidths=[85 * mm],
                rowHeights=[60 * mm],
            )

            foto_box.setStyle(TableStyle([
                ("BOX", (0, 0), (-1, -1), 0.8, colors.lightgrey),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))

            elements.append(foto_box)
            elements.append(Spacer(1, 14))

    elements.append(Paragraph("G. Catatan Anekdot", section_style))

    anekdot_rows = [["No", "Waktu", "KKTP", "Catatan"]]

    for index, item in enumerate(monitoring_siswa.anekdot or [], start=1):
        anekdot_rows.append([
            str(index),
            format_datetime(item.waktu),
            Paragraph(get_kktp_text(item.kktp), small_style),
            Paragraph(value_or_dash(item.catatan), small_style),
        ])

    if len(anekdot_rows) == 1:
        anekdot_rows.append(["-", "-", "-", "-"])

    anekdot_table = Table(
        anekdot_rows,
        colWidths=[25, 90, 170, 180],
        repeatRows=1,
    )

    anekdot_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(anekdot_table)

    elements.append(Paragraph("H. Checklist Indikator", section_style))

    indikator_rows = [["No", "Tujuan Pembelajaran", "Elemen", "Muncul", "Kejadian Teramati"]]

    indikator_list = monitoring_siswa.indikator or []

    for index, item in enumerate(indikator_list, start=1):
        tp = item.tp

        indikator_rows.append([
            str(index),
            Paragraph(value_or_dash(tp.tujuan if tp else None), small_style),
            Paragraph(format_elemen(tp.elemen if tp else "-"), small_style),
            "Ya" if item.muncul else "Tidak",
            Paragraph(value_or_dash(item.kejadian_teramati), small_style),
        ])

    if len(indikator_rows) == 1:
        indikator_rows.append(["-", "-", "-", "-", "-"])

    indikator_table = Table(
        indikator_rows,
        colWidths=[25, 145, 95, 50, 150],
        repeatRows=1,
    )

    indikator_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("ALIGN", (3, 1), (3, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(indikator_table)

    # elements.append(Paragraph("H. Rekomendasi Rumah", section_style))

    # rekomendasi_rows = [["No", "Elemen", "Tips untuk Orang Tua"]]

    # for index, item in enumerate(monitoring_siswa.rekomendasi or [], start=1):
    #     rekomendasi_rows.append([
    #         str(index),
    #         format_elemen(item.elemen),
    #         Paragraph(value_or_dash(item.tips), small_style),
    #     ])

    # if len(rekomendasi_rows) == 1:
    #     rekomendasi_rows.append(["-", "-", "-"])

    # rekomendasi_table = Table(
    #     rekomendasi_rows,
    #     colWidths=[25, 120, 320],
    #     repeatRows=1,
    # )

    # rekomendasi_table.setStyle(TableStyle([
    #     ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
    #     ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
    #     ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
    #     ("ALIGN", (0, 0), (0, -1), "CENTER"),
    #     ("VALIGN", (0, 0), (-1, -1), "TOP"),
    #     ("FONTSIZE", (0, 0), (-1, -1), 8),
    #     ("PADDING", (0, 0), (-1, -1), 5),
    # ]))

    # elements.append(rekomendasi_table)


    elements.append(Spacer(1, 30))  

    tanggal_cetak = datetime.now().strftime("%d %B %Y") 

    nama_kepsek = get_kepsek_name()

    nama_guru = get_guru_ttd(
       monitoring.kelas_id,
       monitoring.tahun_ajaran_id,
    )

    ttd = Table(
        [
            ["", f"Yogyakarta, {tanggal_cetak}"],
            ["Mengetahui,"],
            ["Kepala TK Masjid Syuhada", "Guru"],
            ["", ""],
            [
                Paragraph(f"<b>{nama_kepsek}</b>", ttd_style),
                Paragraph(f"<b>{nama_guru}</b>", ttd_style),
            ],
        ],
        colWidths=[230, 230],
    )

    ttd.setStyle(TableStyle([
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    
        # ruang tanda tangan
        ("BOTTOMPADDING", (0, 2), (-1, 2), 50),
    ]))

    elements.append(ttd)


    doc.build(elements)

    return tmp.name