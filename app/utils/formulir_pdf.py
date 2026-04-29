from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

def generate_formulir_pdf(pendaftaran, filepath, tahun_label):
    c = canvas.Canvas(filepath, pagesize=letter)

    y = 750
    line_height = 20

    c.setFont("Helvetica-Bold", 14)
    c.drawString(100, y, "DATA PESERTA DIDIK BARU")

    y -= line_height
    c.setFont("Helvetica", 12)
    c.drawString(100, y, f"KB & TK Masjid Syuhada Yogyakarta")

    y -= line_height
    c.setFont("Helvetica", 10)
    c.drawString(100, y, f"TAHUN AJARAN {tahun_label}")

    y -= line_height * 2
    c.drawString(100, y, f"No: {pendaftaran.no_pendaftaran}")

    y -= line_height
    c.drawString(100, y, f"Nama: {pendaftaran.peserta.nama_lengkap}")

    y -= line_height
    c.drawString(100, y, f"Program: {pendaftaran.program}")

    c.save()