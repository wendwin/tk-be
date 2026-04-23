from app.extensions import db
from app.models.asesmen import AsesmenPertanyaan, AsesmenJawaban

# pertanyaan asesmen
def get_all_pertanyaan_service():
    return AsesmenPertanyaan.query.order_by(AsesmenPertanyaan.urutan.asc()).all()


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
        pertanyaan = AsesmenPertanyaan(**data, )
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

    db.session.delete(pertanyaan)
    db.session.commit()
    return True


# jawaban asesmen
def get_jawaban_by_pendaftaran(id_pendaftaran):
    return AsesmenJawaban.query.filter_by(id_pendaftaran=id_pendaftaran).all()


def create_jawaban_service(data):
    id_pendaftaran = data.get("id_pendaftaran")
    jawaban_list = data.get("jawaban")

    AsesmenJawaban.query.filter_by(id_pendaftaran=id_pendaftaran).delete()

    for item in jawaban_list:
        jawaban = AsesmenJawaban(
            id_pendaftaran=id_pendaftaran,
            id_pertanyaan=item["id_pertanyaan"],
            jawaban=str(item["jawaban"])
        )
        db.session.add(jawaban)

    db.session.commit()
    return True


def delete_jawaban_service(id_pendaftaran):
    AsesmenJawaban.query.filter_by(id_pendaftaran=id_pendaftaran).delete()
    db.session.commit()
    return True