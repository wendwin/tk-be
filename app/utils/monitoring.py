import tempfile

from reportlab.lib.pagesizes import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from sqlalchemy.orm import joinedload

from app.models.monitoring.mingguan.monitoring import MonitoringMingguan
from app.models.monitoring.mingguan.tp import MonitoringTP
from app.models.monitoring.mingguan.kegiatan import MonitoringKegiatan
from app.models.monitoring.mingguan.asesmen_awal import MonitoringAsesmenAwal
from app.models.akademik.kelas import Kelas
from app.models.akademik.siswa_kelas import SiswaKelas
from app.models.monitoring.siswa.siswa import MonitoringSiswa


FOLIO = (210 * mm, 330 * mm)


def value_or_dash(value):
    return str(value) if value not in [None, ""] else "-"


def format_kelas(kelas):
    if not kelas:
        return "-"

    if kelas.jenjang == "kb":
        return kelas.nama

    kelompok = kelas.kelompok.upper() if kelas.kelompok else ""
    return f"{kelas.jenjang.upper()}-{kelompok} {kelas.nama}"


def format_tanggal(date):
    if not date:
        return "-"

    return date.strftime("%d-%m-%Y")


def format_elemen(elemen):
    mapping = {
        "kesyuhadaan": "Kesyuhadaan",
        "nabp": "Nilai Agama & Budi Pekerti",
        "jd": "Jati Diri",
        "ddlmstrs": "Literasi & STEM",
    }

    return mapping.get(elemen, elemen)


def generate_monitoring_mingguan_pdf(id):
    monitoring = (
        MonitoringMingguan.query
        .options(
            joinedload(MonitoringMingguan.kelas),
            joinedload(MonitoringMingguan.tahun_ajaran),
            joinedload(MonitoringMingguan.tp).joinedload(MonitoringTP.kktp),
            joinedload(MonitoringMingguan.kegiatan),
            joinedload(MonitoringMingguan.asesmen_awal),
        )
        .filter(MonitoringMingguan.id == id)
        .first()
    )

    if not monitoring:
        raise Exception("Data monitoring mingguan tidak ditemukan")

    siswa_kelas_list = (
        SiswaKelas.query
        .filter_by(
            kelas_id=monitoring.kelas_id,
            tahun_ajaran_id=monitoring.tahun_ajaran_id,
            status="aktif",
        )
        .all()
    )

    monitoring_siswa_list = MonitoringSiswa.query.filter_by(
        monitoring_mingguan_id=monitoring.id
    ).all()

    monitoring_siswa_ids = {
        item.siswa_kelas_id for item in monitoring_siswa_list
    }

    total_siswa = len(siswa_kelas_list)
    total_selesai = len(monitoring_siswa_list)
    progress = round((total_selesai / total_siswa) * 100) if total_siswa else 0

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

    elements = []

    elements.append(Paragraph("LAPORAN MONITORING MINGGUAN", title_style))
    elements.append(Paragraph("KB & TK Masjid Syuhada", subtitle_style))

    info_data = [
        ["Kelas", ":", format_kelas(monitoring.kelas)],
        ["Tahun Ajaran", ":", value_or_dash(monitoring.tahun_ajaran.label if monitoring.tahun_ajaran else None)],
        ["Semester", ":", value_or_dash(monitoring.semester)],
        ["Minggu", ":", value_or_dash(monitoring.minggu)],
        ["Topik", ":", value_or_dash(monitoring.topik)],
        ["Sub Topik", ":", value_or_dash(monitoring.sub_topik)],
        [
            "Tanggal",
            ":",
            f"{format_tanggal(monitoring.tanggal_mulai)} s.d. {format_tanggal(monitoring.tanggal_selesai)}",
        ],
        ["Status", ":", value_or_dash(monitoring.status)],
        ["Progress", ":", f"{total_selesai}/{total_siswa} siswa ({progress}%)"],
    ]

    info_table = Table(info_data, colWidths=[95, 10, 360])
    info_table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))

    elements.append(info_table)

    elements.append(Paragraph("A. Tujuan Pembelajaran dan KKTP", section_style))

    tp_rows = [["No", "Elemen", "Tujuan Pembelajaran", "KKTP"]]

    for index, tp in enumerate(monitoring.tp or [], start=1):
        kktp_text = "<br/>".join([
            f"• {value_or_dash(kktp.deskripsi)}"
            for kktp in tp.kktp
        ])

        tp_rows.append([
            str(index),
            Paragraph(format_elemen(tp.elemen), body_style),
            Paragraph(value_or_dash(tp.tujuan), body_style),
            Paragraph(kktp_text or "-", body_style),
        ])

    tp_table = Table(tp_rows, colWidths=[25, 105, 165, 170])
    tp_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(tp_table)

    elements.append(Paragraph("B. Kegiatan", section_style))

    kegiatan_rows = [["No", "Nama Kegiatan", "Media"]]

    for index, kegiatan in enumerate(monitoring.kegiatan or [], start=1):
        kegiatan_rows.append([
            str(index),
            Paragraph(value_or_dash(kegiatan.nama), body_style),
            Paragraph(value_or_dash(kegiatan.media), body_style),
        ])

    kegiatan_table = Table(kegiatan_rows, colWidths=[30, 260, 175])
    kegiatan_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(kegiatan_table)

    if monitoring.asesmen_awal:
        elements.append(Paragraph("C. Asesmen Awal", section_style))

        asesmen_data = [
            ["Teknik", ":", value_or_dash(monitoring.asesmen_awal.teknik)],
            ["Rancangan Kegiatan", ":", value_or_dash(monitoring.asesmen_awal.rancangan_kegiatan)],
            ["Hasil", ":", value_or_dash(monitoring.asesmen_awal.hasil)],
        ]

        asesmen_table = Table(asesmen_data, colWidths=[115, 10, 340])
        asesmen_table.setStyle(TableStyle([
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]))

        elements.append(asesmen_table)

    elements.append(Paragraph("D. Daftar Siswa", section_style))

    siswa_rows = [["No", "Nama Siswa", "NISN", "Jenis Kelamin", "Status"]]

    for index, item in enumerate(siswa_kelas_list, start=1):
        siswa = item.siswa

        nama = (
            getattr(siswa, "nama_lengkap", None)
            or getattr(getattr(siswa, "peserta", None), "nama_lengkap", None)
            or "-"
        )

        nisn = (
            getattr(siswa, "nisn", None)
            or getattr(getattr(siswa, "peserta", None), "nisn", None)
            or "-"
        )

        jk = (
            getattr(siswa, "jenis_kelamin", None)
            or getattr(getattr(siswa, "peserta", None), "jenis_kelamin", None)
            or "-"
        )

        status = "Sudah Diisi" if item.id in monitoring_siswa_ids else "Belum Diisi"

        siswa_rows.append([
            str(index),
            Paragraph(value_or_dash(nama), body_style),
            value_or_dash(nisn),
            value_or_dash(jk),
            status,
        ])

    siswa_table = Table(siswa_rows, colWidths=[30, 190, 80, 80, 85])
    siswa_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (0, -1), "CENTER"),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
        ("PADDING", (0, 0), (-1, -1), 5),
    ]))

    elements.append(siswa_table)

    doc.build(elements)

    return tmp.name