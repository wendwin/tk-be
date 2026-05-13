from app.models.pendaftaran import Pendaftaran
from app.models.observasi.gpph import GPPHJawaban

from app.extensions import db

def set_jadwal_observasi(id, data):
    pendaftaran = Pendaftaran.query.get(id)

    if not pendaftaran:
        return None

    pendaftaran.tanggal_observasi = data.get("tanggal_observasi")
    pendaftaran.jam_observasi = data.get("jam_observasi")
    pendaftaran.status_observasi = "terjadwal"

    db.session.commit()
    return pendaftaran


def update_status_observasi(id, status):
    pendaftaran = Pendaftaran.query.get(id)

    if not pendaftaran:
        return None

    pendaftaran.status_observasi = status

    db.session.commit()
    return pendaftaran

def create_gpph(data):

    pendaftaran = Pendaftaran.query.get(
        data['pendaftaran_id']
    )

    if not pendaftaran:
        raise ValueError('Pendaftaran tidak ditemukan')

    pendaftaran_id = data['pendaftaran_id']

    GPPHJawaban.query.filter_by(
        pendaftaran_id=pendaftaran_id
    ).delete()

    for item in data['jawaban']:

        jawaban = GPPHJawaban(
            pendaftaran_id=pendaftaran_id,
            pertanyaan_id=item['pertanyaan_id'],
            nilai=item['nilai']
        )

        db.session.add(jawaban)

    db.session.commit()


def get_gpph_result(pendaftaran_id):

    pendaftaran = Pendaftaran.query.get(
        pendaftaran_id
    )

    if not pendaftaran:
        raise ValueError('Pendaftaran tidak ditemukan')

    jawaban = (
        GPPHJawaban.query
        .filter_by(pendaftaran_id=pendaftaran_id)
        .all()
    )

    jumlah = {
        0: 0,
        1: 0,
        2: 0,
        3: 0
    }

    total_nilai = 0

    hasil_jawaban = []

    for item in jawaban:

        jumlah[item.nilai] += 1

        total_nilai += item.nilai

        hasil_jawaban.append({
            'id': item.id,
            'pertanyaan_id': item.pertanyaan_id,
            'nomor': item.pertanyaan.nomor,
            'pertanyaan': item.pertanyaan.pertanyaan,
            'nilai': item.nilai
        })

    return {
        'jawaban': hasil_jawaban,
        'jumlah': jumlah,
        'total_nilai': total_nilai
    }