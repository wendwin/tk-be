from io import BytesIO
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


def value_or_dash(value):
    return str(value) if value not in [None, ""] else "-"


def format_date(value):
    if not value:
        return "-"

    if isinstance(value, datetime):
        value = value.date()

    return value.strftime("%d-%m-%Y")


def format_enum(value):
    if not value:
        return "-"

    return str(value).replace("_", " ").title()


def make_table(data):
    table = Table(data, colWidths=[150, 340])

    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("BACKGROUND", (0, 0), (0, -1), colors.whitesmoke),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))

    return table


def generate_bukti_pendaftaran_pdf(pendaftaran):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40,
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "TitleCenter",
        parent=styles["Title"],
        alignment=TA_CENTER,
        fontSize=14,
        leading=18,
        spaceAfter=4,
    )

    subtitle_style = ParagraphStyle(
        "SubtitleCenter",
        parent=styles["Normal"],
        alignment=TA_CENTER,
        fontSize=10,
        leading=14,
    )

    section_style = ParagraphStyle(
        "SectionTitle",
        parent=styles["Heading3"],
        fontSize=10,
        leading=14,
        spaceBefore=12,
        spaceAfter=6,
    )

    note_style = ParagraphStyle(
        "Note",
        parent=styles["Normal"],
        fontSize=9,
        leading=13,
        textColor=colors.dimgray,
    )

    elements = []

    peserta = pendaftaran.peserta

    tahun_ajaran = (
        pendaftaran.tahun_ajaran.label
        if getattr(pendaftaran, "tahun_ajaran", None)
        else "-"
    )

    gelombang = (
        pendaftaran.gelombang.nama
        if getattr(pendaftaran, "gelombang", None)
        else "-"
    )

    nama_peserta = value_or_dash(getattr(peserta, "nama_lengkap", None))
    nama_panggilan = value_or_dash(getattr(peserta, "nama_panggilan", None))
    tempat_lahir = value_or_dash(getattr(peserta, "tempat_lahir", None))
    tanggal_lahir = format_date(getattr(peserta, "tanggal_lahir", None))

    elements.append(Paragraph("<b>TK MASJID SYUHADA YOGYAKARTA</b>", title_style))
    elements.append(Paragraph("BUKTI PENDAFTARAN PESERTA DIDIK BARU", subtitle_style))
    elements.append(Paragraph(f"Tahun Ajaran {tahun_ajaran}", subtitle_style))
    elements.append(Spacer(1, 18))

    elements.append(Paragraph("<b>INFORMASI PENDAFTARAN</b>", section_style))
    elements.append(make_table([
        ["No Pendaftaran", value_or_dash(pendaftaran.no_pendaftaran)],
        ["Tanggal Daftar", format_date(getattr(pendaftaran, "tanggal_daftar", None))],
        ["Gelombang", value_or_dash(gelombang)],
        ["Tahun Ajaran", value_or_dash(tahun_ajaran)],
    ]))

    elements.append(Paragraph("<b>DATA PESERTA DIDIK</b>", section_style))
    elements.append(make_table([
        ["Nama Lengkap", nama_peserta],
        ["Nama Panggilan", nama_panggilan],
        ["Tempat, Tanggal Lahir", f"{tempat_lahir}, {tanggal_lahir}"],
        ["Jenis Kelamin", format_enum(getattr(peserta, "jenis_kelamin", None))],
    ]))

    elements.append(Paragraph("<b>DATA PROGRAM</b>", section_style))
    elements.append(make_table([
        ["Jenjang", format_enum(getattr(pendaftaran, "jenis", None))],
        ["Program", format_enum(getattr(pendaftaran, "program", None))],
    ]))

    # elements.append(Paragraph("<b>STATUS PENDAFTARAN</b>", section_style))
    # elements.append(make_table([
    #     ["Status Pendaftaran", format_enum(getattr(pendaftaran, "status", None))],
    #     ["Status Berkas", format_enum(getattr(pendaftaran, "status_berkas", None))],
    #     ["Status Pembayaran", format_enum(getattr(pendaftaran, "status_pembayaran", None))],
    #     ["Status Observasi", format_enum(getattr(pendaftaran, "status_observasi", None))],
    # ]))

    elements.append(Spacer(1, 18))
    elements.append(Paragraph("<b>Catatan:</b>", styles["Normal"]))
    elements.append(Spacer(1, 4))
    elements.append(Paragraph(
        "Dokumen ini merupakan bukti bahwa peserta didik telah melakukan "
        "pendaftaran melalui Syuhada School Portal. "
        "Bukti pendaftaran ini bukan merupakan surat penerimaan peserta didik. "
        "Silakan memantau informasi selanjutnya melalui Portal Orang Tua.",
        note_style
    ))

    elements.append(Spacer(1, 30))
    elements.append(Paragraph(
        f"Dicetak pada: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        note_style
    ))

    doc.build(elements)

    buffer.seek(0)
    return buffer