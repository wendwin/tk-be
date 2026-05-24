from sqlalchemy.orm import joinedload
from app.models.pendaftaran.pendaftaran import Pendaftaran
from app.models.pendaftaran.peserta_didik import PesertaDidik

import tempfile
from reportlab.lib.pagesizes import mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib import colors

FOLIO = (210*mm, 330*mm)
def generate_surat_pernyataan(user_id):
    pendaftaran = (
        Pendaftaran.query
        .join(Pendaftaran.peserta)
        .options(
            joinedload(Pendaftaran.peserta)
            .joinedload(PesertaDidik.alamat_domisili),
            joinedload(Pendaftaran.peserta)
            .joinedload(PesertaDidik.orang_tua),
            joinedload(Pendaftaran.tahun_ajaran),
        )
        .filter(PesertaDidik.user_id == user_id)
        .first()
    )

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
