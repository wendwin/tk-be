from app.models.pendaftaran import Pendaftaran
from app.models.observasi.gpph import GPPHPertanyaan, GPPHJawaban
from datetime import date
from app.models.observasi.kpsp import KPSPPertanyaan, KPSPJawaban
from app.extensions import db

# helper
def calculate_age_in_months(tanggal_lahir):
    today = date.today()
    months = (
        (today.year - tanggal_lahir.year) * 12
        + today.month
        - tanggal_lahir.month
    )

    return months

def get_kpsp_group_usia(bulan):
    kelompok = [
        24,
        30,
        36,
        42,
        48,
        54,
        60,
        66,
        72
    ]

    for usia in kelompok:
        if bulan <= usia:
            return usia

    return 72

def set_jadwal_observasi(ids, observasi_at):
    pendaftaran_list = Pendaftaran.query.filter(
        Pendaftaran.id.in_(ids)
    ).all()

    for pendaftaran in pendaftaran_list:
        pendaftaran.observasi_at = observasi_at
        pendaftaran.status_observasi = "terjadwal"

    db.session.commit()

    return pendaftaran_list


def update_status_observasi(id, status):
    pendaftaran = Pendaftaran.query.get(id)

    if not pendaftaran:
        return None

    pendaftaran.status_observasi = status

    db.session.commit()
    return pendaftaran

def get_all_gpph_pertanyaan():

    pertanyaan = (
        GPPHPertanyaan.query
        .order_by(GPPHPertanyaan.nomor.asc())
        .all()
    )

    result = []

    for item in pertanyaan:

        result.append({
            'id': item.id,
            'nomor': item.nomor,
            'pertanyaan': item.pertanyaan
        })

    return result


def get_detail_gpph_pertanyaan(id):

    pertanyaan = GPPHPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError(
            'Pertanyaan GPPH tidak ditemukan'
        )

    return {
        'id': pertanyaan.id,
        'nomor': pertanyaan.nomor,
        'pertanyaan': pertanyaan.pertanyaan
    }


def create_gpph_pertanyaan(data):

    exists = GPPHPertanyaan.query.filter_by(
        nomor=data['nomor']
    ).first()

    if exists:
        raise ValueError(
            'Nomor pertanyaan sudah digunakan'
        )

    pertanyaan = GPPHPertanyaan(
        nomor=data['nomor'],
        pertanyaan=data['pertanyaan']
    )

    db.session.add(pertanyaan)

    db.session.commit()

    return pertanyaan


def update_gpph_pertanyaan(id, data):

    pertanyaan = GPPHPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError(
            'Pertanyaan GPPH tidak ditemukan'
        )

    exists = (
        GPPHPertanyaan.query
        .filter(
            GPPHPertanyaan.nomor == data['nomor'],
            GPPHPertanyaan.id != id
        )
        .first()
    )

    if exists:
        raise ValueError(
            'Nomor pertanyaan sudah digunakan'
        )

    pertanyaan.nomor = data['nomor']
    pertanyaan.pertanyaan = data['pertanyaan']

    db.session.commit()

    return pertanyaan


def delete_gpph_pertanyaan(id):

    pertanyaan = GPPHPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError(
            'Pertanyaan GPPH tidak ditemukan'
        )

    db.session.delete(pertanyaan)

    db.session.commit()

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


def get_all_kpsp_pertanyaan_service():
    pertanyaan = (
        KPSPPertanyaan.query
        .order_by(
            KPSPPertanyaan.usia_bulan.asc(),
            KPSPPertanyaan.urutan.asc()
        )
        .all()
    )

    result = []

    for item in pertanyaan:

        result.append({
            'id': item.id,
            'usia_bulan': item.usia_bulan,
            'aspek_perkembangan': item.aspek_perkembangan,
            'kemampuan_anak': item.kemampuan_anak,
            'urutan': item.urutan
        })

    return result


def get_detail_kpsp_pertanyaan(id):
    pertanyaan = KPSPPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError(
            'Pertanyaan KPSP tidak ditemukan'
        )

    return {
        'id': pertanyaan.id,
        'usia_bulan': pertanyaan.usia_bulan,
        'aspek_perkembangan': pertanyaan.aspek_perkembangan,
        'kemampuan_anak': pertanyaan.kemampuan_anak,
        'urutan': pertanyaan.urutan
    }


def create_kpsp_pertanyaan(data):
    pertanyaan = KPSPPertanyaan(
        usia_bulan=data['usia_bulan'],
        aspek_perkembangan=data['aspek_perkembangan'],
        kemampuan_anak=data['kemampuan_anak'],
        urutan=data['urutan']
    )

    db.session.add(pertanyaan)

    db.session.commit()

    return pertanyaan

def update_kpsp_pertanyaan(id, data):
    pertanyaan = KPSPPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError(
            'Pertanyaan KPSP tidak ditemukan'
        )

    pertanyaan.usia_bulan = data['usia_bulan']
    pertanyaan.aspek_perkembangan = data['aspek_perkembangan']
    pertanyaan.kemampuan_anak = data['kemampuan_anak']
    pertanyaan.urutan = data['urutan']

    db.session.commit()

    return pertanyaan

def delete_kpsp_pertanyaan(id):
    pertanyaan = KPSPPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError(
            'Pertanyaan KPSP tidak ditemukan'
        )

    db.session.delete(pertanyaan)

    db.session.commit()


def get_kpsp_pertanyaan_by_pendaftaran(pendaftaran_id):
    pendaftaran = Pendaftaran.query.get(pendaftaran_id)
    if not pendaftaran:
        raise ValueError(
            'Pendaftaran tidak ditemukan'
        )

    peserta = pendaftaran.peserta

    usia_bulan = calculate_age_in_months(
        peserta.tanggal_lahir
    )

    kelompok_usia = get_kpsp_group_usia(
        usia_bulan
    )

    pertanyaan = (
        KPSPPertanyaan.query
        .filter_by(usia_bulan=kelompok_usia)
        .order_by(KPSPPertanyaan.urutan.asc())
        .all()
    )

    result = []

    for item in pertanyaan:

        result.append({
            'id': item.id,
            'usia_bulan': item.usia_bulan,
            'aspek_perkembangan': item.aspek_perkembangan,
            'kemampuan_anak': item.kemampuan_anak,
            'urutan': item.urutan
        })

    return {
        'usia_bulan': kelompok_usia,
        'pertanyaan': result
    }

def create_kpsp(data):
    pendaftaran = Pendaftaran.query.get(data['pendaftaran_id'])

    if not pendaftaran:
        raise ValueError(
            'Pendaftaran tidak ditemukan'
        )

    KPSPJawaban.query.filter_by(pendaftaran_id=data['pendaftaran_id']).delete()

    for item in data['jawaban']:

        jawaban = KPSPJawaban(
            pendaftaran_id=data['pendaftaran_id'],
            pertanyaan_id=item['pertanyaan_id'],
            jawaban=item['jawaban'],
            keterangan=item.get('keterangan'),
            catatan=data.get('catatan')
        )

        db.session.add(jawaban)

    db.session.commit()

def get_kpsp_result(pendaftaran_id):
    pendaftaran = Pendaftaran.query.get(pendaftaran_id)

    if not pendaftaran:
        raise ValueError(
            'Pendaftaran tidak ditemukan'
        )

    jawaban = (
        KPSPJawaban.query
        .filter_by(pendaftaran_id=pendaftaran_id)
        .all()
    )

    result = []

    catatan = None

    for item in jawaban:

        catatan = item.catatan

        result.append({
            'id': item.id,
            'pertanyaan_id': item.pertanyaan_id,
            'usia_bulan': item.pertanyaan.usia_bulan,
            'aspek_perkembangan': item.pertanyaan.aspek_perkembangan,
            'kemampuan_anak': item.pertanyaan.kemampuan_anak,
            'jawaban': item.jawaban,
            'keterangan': item.keterangan
        })

    return {
        'catatan': catatan,
        'jawaban': result
    }