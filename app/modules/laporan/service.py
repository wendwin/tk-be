import tempfile
from datetime import datetime

from reportlab.lib.pagesizes import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors

from app.models.pendaftaran.pendaftaran import Pendaftaran
from app.models.pendaftaran.tahun_ajaran import TahunAjaran
from app.models.monitoring.mingguan.monitoring import MonitoringMingguan
from app.models.akademik.kelas import Kelas

FOLIO = (210 * mm, 330 * mm)


def count_by(data, field, value):
    return len([item for item in data if getattr(item, field, None) == value])


def generate_laporan_pdf(tahun_ajaran_id=None):
    tahun_ajaran = None

    if tahun_ajaran_id:
        tahun_ajaran = TahunAjaran.query.get(tahun_ajaran_id)
    else:
        tahun_ajaran = TahunAjaran.query.filter_by(is_active=True).first()

    if not tahun_ajaran:
        raise Exception("Tahun ajaran tidak ditemukan")

    pendaftaran_list = Pendaftaran.query.filter_by(
        tahun_ajaran_id=tahun_ajaran.id
    ).all()

    monitoring_list = MonitoringMingguan.query.filter_by(
        tahun_ajaran_id=tahun_ajaran.id
    ).all()

    kelas_list = Kelas.query.filter_by(
        tahun_ajaran_id=tahun_ajaran.id
    ).all()

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
        "Title",
        parent=styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=16,
        alignment=TA_CENTER,
        spaceAfter=12,
    )

    subtitle_style = ParagraphStyle(
        "Subtitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        alignment=TA_CENTER,
        spaceAfter=20,
    )

    section_style = ParagraphStyle(
        "Section",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=12,
        spaceBefore=14,
        spaceAfter=8,
    )

    body_style = ParagraphStyle(
        "Body",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
    )

    elements = []

    elements.append(Paragraph("LAPORAN KEPALA SEKOLAH", title_style))
    elements.append(Paragraph("KB & TK Masjid Syuhada", subtitle_style))
    elements.append(Paragraph(f"Tahun Ajaran {tahun_ajaran.label}", subtitle_style))

    total_pendaftar = len(pendaftaran_list)
    total_diterima = count_by(pendaftaran_list, "status", "accepted")
    total_observasi_hadir = count_by(pendaftaran_list, "status_observasi", "hadir")
    total_monitoring = len(monitoring_list)

    elements.append(Paragraph("A. Ringkasan", section_style))

    summary_table = Table(
        [
            ["Total Pendaftar", total_pendaftar],
            ["Total Diterima", total_diterima],
            ["Observasi Hadir", total_observasi_hadir],
            ["Total Monitoring Mingguan", total_monitoring],
            ["Total Kelas", len(kelas_list)],
        ],
        colWidths=[330, 120],
    )

    summary_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, -1), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(summary_table)

    elements.append(Paragraph("B. Rekap Status Pendaftaran", section_style))

    pendaftaran_table = Table(
        [
            ["Status", "Jumlah"],
            ["Draft", count_by(pendaftaran_list, "status", "draft")],
            ["Pending", count_by(pendaftaran_list, "status", "pending")],
            ["Verified", count_by(pendaftaran_list, "status", "verified")],
            ["Accepted", count_by(pendaftaran_list, "status", "accepted")],
            ["Rejected", count_by(pendaftaran_list, "status", "rejected")],
        ],
        colWidths=[330, 120],
    )

    pendaftaran_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(pendaftaran_table)

    elements.append(Paragraph("C. Rekap Observasi", section_style))

    observasi_table = Table(
        [
            ["Status Observasi", "Jumlah"],
            ["Belum Dijadwalkan", count_by(pendaftaran_list, "status_observasi", "belum")],
            ["Terjadwal", count_by(pendaftaran_list, "status_observasi", "terjadwal")],
            ["Hadir", count_by(pendaftaran_list, "status_observasi", "hadir")],
            ["Tidak Hadir", count_by(pendaftaran_list, "status_observasi", "tidak_hadir")],
        ],
        colWidths=[330, 120],
    )

    observasi_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(observasi_table)

    elements.append(Paragraph("D. Progress Monitoring Per Kelas", section_style))

    monitoring_rows = [["Kelas", "Sudah Diisi", "Total Target", "Persentase"]]

    for kelas in kelas_list:
        monitoring_kelas = [
            item for item in monitoring_list
            if item.kelas_id == kelas.id
        ]

        total = sum([item.total_siswa for item in monitoring_kelas])
        done = sum([item.total_selesai for item in monitoring_kelas])

        percent = 0
        if total > 0:
            percent = round((done / total) * 100)

        if kelas.jenjang == "kb":
            nama_kelas = kelas.nama
        else:
            nama_kelas = f"{kelas.jenjang.upper()}-{kelas.kelompok.upper()} {kelas.nama}"

        monitoring_rows.append([
            nama_kelas,
            done,
            total,
            f"{percent}%",
        ])

    monitoring_table = Table(
        monitoring_rows,
        colWidths=[180, 90, 90, 90],
    )

    monitoring_table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.5, colors.lightgrey),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E5E7EB")),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))

    elements.append(monitoring_table)

    elements.append(Spacer(1, 30))
    elements.append(Paragraph(
        f"Dicetak pada: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        body_style,
    ))

    doc.build(elements)

    return tmp.name