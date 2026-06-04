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
        + (today.month - tanggal_lahir.month)
    )

    if today.day < tanggal_lahir.day:
        months -= 1

    return months

def get_kpsp_group_usia(bulan):
    kelompok = [24, 30, 36, 42, 48, 54, 60, 66, 72]

    if bulan < 24:
        return None

    result = kelompok[0]

    for usia in kelompok:
        if bulan >= usia:
            result = usia
        else:
            break

    return result

def set_jadwal_observasi(ids, observasi_at):
    pendaftaran_list = Pendaftaran.query.filter(
        Pendaftaran.id.in_(ids)
    ).all()

    for pendaftaran in pendaftaran_list:
        pendaftaran.observasi_at = observasi_at
        pendaftaran.status_observasi = "terjadwal"

    db.session.commit()

    return pendaftaran_list


def update_status_observasi_complete(pendaftaran_id):
    pendaftaran = db.session.get(Pendaftaran, pendaftaran_id)

    if not pendaftaran:
        raise ValueError("Pendaftaran tidak ditemukan")

    if pendaftaran.status_observasi == "hadir":
        return

    has_gpph = GPPHJawaban.query.filter_by(
        pendaftaran_id=pendaftaran_id
    ).first()

    has_kpsp = KPSPJawaban.query.filter_by(
        pendaftaran_id=pendaftaran_id
    ).first()

    if has_gpph and has_kpsp:
        pendaftaran.status_observasi = "hadir"

def update_status_observasi(id, status):
    pendaftaran = Pendaftaran.query.get(id)

    if not pendaftaran:
        return None

    pendaftaran.status_observasi = status

    db.session.commit()
    return pendaftaran

""" GPPH Service"""
def get_all_gpph_pertanyaan(active_only=False):
    query = GPPHPertanyaan.query

    if active_only:
        query = query.filter_by(is_active=True)

    pertanyaan = (
        query
        .order_by(
            GPPHPertanyaan.urutan.asc(),
            GPPHPertanyaan.id.asc()
        )
        .all()
    )

    result = []

    for item in pertanyaan:
        result.append({
            'id': item.id,
            'urutan': item.urutan,
            'pertanyaan': item.pertanyaan,
            'is_active': item.is_active
        })

    return result


def get_detail_gpph_pertanyaan(id):
    pertanyaan = GPPHPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError('Pertanyaan GPPH tidak ditemukan')

    return {
        'id': pertanyaan.id,
        'urutan': pertanyaan.urutan,
        'pertanyaan': pertanyaan.pertanyaan,
        'is_active': pertanyaan.is_active
    }


def create_gpph_pertanyaan(data):
    pertanyaan = GPPHPertanyaan(
        urutan=data['urutan'],
        pertanyaan=data['pertanyaan'],
        is_active=data.get('is_active', True)
    )

    db.session.add(pertanyaan)
    db.session.commit()

    return pertanyaan


def update_gpph_pertanyaan(id, data):
    pertanyaan = GPPHPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError('Pertanyaan GPPH tidak ditemukan')

    pertanyaan.urutan = data['urutan']
    pertanyaan.pertanyaan = data['pertanyaan']
    pertanyaan.is_active = data.get('is_active', pertanyaan.is_active)

    db.session.commit()

    return pertanyaan


def delete_gpph_pertanyaan(id):
    pertanyaan = GPPHPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError('Pertanyaan GPPH tidak ditemukan')

    pertanyaan.is_active = False
    db.session.commit()


def restore_gpph_pertanyaan(id):
    pertanyaan = GPPHPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError('Pertanyaan GPPH tidak ditemukan')

    pertanyaan.is_active = True
    db.session.commit()


def create_gpph(pendaftaran_id, data):
    pendaftaran = Pendaftaran.query.get(pendaftaran_id)

    if not pendaftaran:
        raise ValueError('Pendaftaran tidak ditemukan')

    existing = GPPHJawaban.query.filter_by(
        pendaftaran_id=pendaftaran_id
    ).first()

    if existing:
        raise ValueError("Observasi GPPH sudah diisi")

    for item in data['jawaban']:
        pertanyaan = GPPHPertanyaan.query.get(item['pertanyaan_id'])

        if not pertanyaan:
            raise ValueError('Pertanyaan GPPH tidak ditemukan')

        jawaban = GPPHJawaban(
            pendaftaran_id=pendaftaran_id,
            pertanyaan_id=item['pertanyaan_id'],

            snapshot_urutan=pertanyaan.urutan,
            snapshot_pertanyaan=pertanyaan.pertanyaan,

            nilai=item['nilai']
        )

        db.session.add(jawaban)

    update_status_observasi_complete(pendaftaran_id)
    db.session.commit()


def get_gpph_result(pendaftaran_id):
    pendaftaran = Pendaftaran.query.get(pendaftaran_id)

    if not pendaftaran:
        raise ValueError('Pendaftaran tidak ditemukan')

    jawaban = (
        GPPHJawaban.query
        .filter_by(pendaftaran_id=pendaftaran_id)
        .order_by(
            GPPHJawaban.snapshot_urutan.asc(),
            GPPHJawaban.id.asc()
        )
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

    for index, item in enumerate(jawaban, start=1):
        jumlah[item.nilai] += 1
        total_nilai += item.nilai

        hasil_jawaban.append({
            'id': item.id,
            'pertanyaan_id': item.pertanyaan_id,
            'urutan': index,
            'pertanyaan': item.snapshot_pertanyaan,
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
            'urutan': item.urutan,
            'is_active': item.is_active
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
        'urutan': pertanyaan.urutan,
        'is_active': pertanyaan.is_active
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
        raise ValueError('Pertanyaan KPSP tidak ditemukan')

    pertanyaan.is_active = False
    db.session.commit()

def restore_kpsp_pertanyaan(id):
    pertanyaan = KPSPPertanyaan.query.get(id)

    if not pertanyaan:
        raise ValueError('Pertanyaan KPSP tidak ditemukan')

    pertanyaan.is_active = True
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
       .filter_by(
           usia_bulan=kelompok_usia,
           is_active=True
       )
       .order_by(
           KPSPPertanyaan.urutan.asc(),
           KPSPPertanyaan.id.asc()
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

    return {
        'usia_bulan': kelompok_usia,
        'pertanyaan': result
    }

def create_kpsp(pendaftaran_id, data):
    pendaftaran = Pendaftaran.query.get(pendaftaran_id)

    if not pendaftaran:
        raise ValueError(
            'Pendaftaran tidak ditemukan'
        )

    existing = KPSPJawaban.query.filter_by(
        pendaftaran_id=pendaftaran_id
    ).first()

    if existing:
        raise ValueError("Observasi KPSP sudah diisi")

    for item in data['jawaban']:
        pertanyaan = KPSPPertanyaan.query.get(item['pertanyaan_id'])

        if not pertanyaan:
            raise ValueError('Pertanyaan KPSP tidak ditemukan')

        jawaban = KPSPJawaban(
            pendaftaran_id=pendaftaran_id,
            pertanyaan_id=item['pertanyaan_id'],

            snapshot_usia_bulan=pertanyaan.usia_bulan,
            snapshot_aspek_perkembangan=pertanyaan.aspek_perkembangan,
            snapshot_kemampuan_anak=pertanyaan.kemampuan_anak,
            snapshot_urutan=pertanyaan.urutan,

            jawaban=item['jawaban'],
            keterangan=item.get('keterangan'),
            catatan=data.get('catatan')
        )

        db.session.add(jawaban)

    update_status_observasi_complete(pendaftaran_id)

    db.session.commit()

def get_kpsp_result(pendaftaran_id):
    pendaftaran = Pendaftaran.query.get(pendaftaran_id)

    if not pendaftaran:
        raise ValueError('Pendaftaran tidak ditemukan')

    jawaban = (
        KPSPJawaban.query
        .filter_by(pendaftaran_id=pendaftaran_id)
        .order_by(
            KPSPJawaban.snapshot_urutan.asc(),
            KPSPJawaban.id.asc()
        )
        .all()
    )

    result = []
    catatan = None

    for index, item in enumerate(jawaban, start=1):
        catatan = item.catatan

        result.append({
            'id': item.id,
            'pertanyaan_id': item.pertanyaan_id,
            'usia_bulan': item.snapshot_usia_bulan,
            'aspek_perkembangan': item.snapshot_aspek_perkembangan,
            'kemampuan_anak': item.snapshot_kemampuan_anak,
            'urutan': index,
            'jawaban': item.jawaban,
            'keterangan': item.keterangan
        })

    return {
        'catatan': catatan,
        'jawaban': result
    }