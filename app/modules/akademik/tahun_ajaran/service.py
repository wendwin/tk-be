from app.extensions import db
from app.models.pendaftaran import TahunAjaran


def get_all_tahun_ajaran():
    return (
        TahunAjaran.query
        .order_by(TahunAjaran.tahun_mulai.desc())
        .all()
    )


def get_tahun_ajaran_by_id(id):
    tahun_ajaran = db.session.get(TahunAjaran, id)

    if not tahun_ajaran:
        raise ValueError("Tahun ajaran tidak ditemukan")

    return tahun_ajaran


def create_tahun_ajaran(data):
    exists = TahunAjaran.query.filter_by(
        tahun_mulai=data["tahun_mulai"],
        tahun_selesai=data["tahun_selesai"],
    ).first()

    if exists:
        raise ValueError("Tahun ajaran sudah ada")

    if data.get("is_active"):
        TahunAjaran.query.update({TahunAjaran.is_active: False})

    tahun_ajaran = TahunAjaran(**data)

    db.session.add(tahun_ajaran)
    db.session.commit()

    return tahun_ajaran


def update_tahun_ajaran(id, data):
    tahun_ajaran = get_tahun_ajaran_by_id(id)

    tahun_mulai = data.get("tahun_mulai", tahun_ajaran.tahun_mulai)
    tahun_selesai = data.get("tahun_selesai", tahun_ajaran.tahun_selesai)

    exists = TahunAjaran.query.filter(
        TahunAjaran.id != id,
        TahunAjaran.tahun_mulai == tahun_mulai,
        TahunAjaran.tahun_selesai == tahun_selesai,
    ).first()

    if exists:
        raise ValueError("Tahun ajaran sudah ada")

    if data.get("is_active") is True:
        TahunAjaran.query.filter(
            TahunAjaran.id != id
        ).update({TahunAjaran.is_active: False})

    for key, value in data.items():
        setattr(tahun_ajaran, key, value)

    db.session.commit()

    return tahun_ajaran


def delete_tahun_ajaran(id):
    tahun_ajaran = get_tahun_ajaran_by_id(id)

    db.session.delete(tahun_ajaran)
    db.session.commit()

    return True