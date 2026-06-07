from app.extensions import db
from app.models.asesmen import AsesmenPertanyaan, AsesmenJawaban
from sqlalchemy import nulls_last

def get_all_pertanyaan_service(active_only=False):
    query = AsesmenPertanyaan.query

    if active_only:
        query = query.filter_by(is_active=True)

    return (
        query
        .order_by(
            AsesmenPertanyaan.urutan.asc(),
            AsesmenPertanyaan.id.asc()
        )
        .all()
    )

def get_pertanyaan_by_id_service(id):
    return AsesmenPertanyaan.query.get(id)


def create_pertanyaan_service(data):
    pertanyaan = AsesmenPertanyaan(**data)
    db.session.add(pertanyaan)
    db.session.commit()
    return pertanyaan


def bulk_create_pertanyaan_service(data_list):
    result = []

    for data in data_list:
        pertanyaan = AsesmenPertanyaan(**data)
        db.session.add(pertanyaan)
        result.append(pertanyaan)

    db.session.commit()
    return result


def update_pertanyaan_service(id, data):
    pertanyaan = get_pertanyaan_by_id_service(id)

    if not pertanyaan:
        return None

    for key, value in data.items():
        setattr(pertanyaan, key, value)

    db.session.commit()
    return pertanyaan


def delete_pertanyaan_service(id):
    pertanyaan = get_pertanyaan_by_id_service(id)

    if not pertanyaan:
        return False

    pertanyaan.is_active = False
    db.session.commit()

    return True


def restore_pertanyaan_service(id):
    pertanyaan = get_pertanyaan_by_id_service(id)

    if not pertanyaan:
        return False

    pertanyaan.is_active = True
    db.session.commit()

    return True


def get_jawaban_by_pendaftaran(id_pendaftaran):
    return (
        AsesmenJawaban.query
        .filter_by(id_pendaftaran=id_pendaftaran)
        .order_by(AsesmenJawaban.id.asc())
        .all()
    )


def create_jawaban_service(data):
    id_pendaftaran = data.get("id_pendaftaran")
    jawaban_list = data.get("jawaban")

    AsesmenJawaban.query.filter_by(
        id_pendaftaran=id_pendaftaran
    ).delete()

    for item in jawaban_list:
        pertanyaan = AsesmenPertanyaan.query.get(item["id_pertanyaan"])

        if not pertanyaan:
            raise ValueError("Pertanyaan tidak ditemukan")

        jawaban = AsesmenJawaban(
            id_pendaftaran=id_pendaftaran,
            id_pertanyaan=item["id_pertanyaan"],
            snapshot_pertanyaan=pertanyaan.pertanyaan,
            jawaban=str(item["jawaban"])
        )

        db.session.add(jawaban)

    db.session.commit()
    return True


def delete_jawaban_service(id_pendaftaran):
    AsesmenJawaban.query.filter_by(
        id_pendaftaran=id_pendaftaran
    ).delete()

    db.session.commit()
    return True