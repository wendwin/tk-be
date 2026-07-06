from app.extensions import db
from app.models.pendaftaran.gelombang import Gelombang
from app.models.pendaftaran.tahun_ajaran import TahunAjaran


def get_gelombang_by_tahun_ajaran(tahun_ajaran_id):
    tahun_ajaran = TahunAjaran.query.get(tahun_ajaran_id)

    if not tahun_ajaran:
        raise ValueError("Tahun ajaran tidak ditemukan")

    return (
        Gelombang.query
        .filter_by(tahun_ajaran_id=tahun_ajaran_id)
        .order_by(Gelombang.tanggal_mulai.asc(), Gelombang.id.asc())
        .all()
    )


def get_gelombang_by_id(id):
    gelombang = Gelombang.query.get(id)

    if not gelombang:
        raise ValueError("Gelombang tidak ditemukan")

    return gelombang

def get_active_gelombang():
    tahun_ajaran = (
        TahunAjaran.query
        .filter_by(is_active=True)
        .first()
    )

    if not tahun_ajaran:
        raise ValueError("Tidak ada tahun ajaran aktif")

    return (
        Gelombang.query
        .filter_by(tahun_ajaran_id=tahun_ajaran.id)
        .order_by(Gelombang.tanggal_mulai.asc())
        .all()
    )

def create_gelombang(data):
    tahun_ajaran = TahunAjaran.query.get(data["tahun_ajaran_id"])

    if not tahun_ajaran:
        raise ValueError("Tahun ajaran tidak ditemukan")

    if data["tanggal_selesai"] <= data["tanggal_mulai"]:
        raise ValueError("Tanggal selesai harus lebih besar dari tanggal mulai")

    exists = Gelombang.query.filter_by(
        tahun_ajaran_id=data["tahun_ajaran_id"],
        nama=data["nama"],
    ).first()

    if exists:
        raise ValueError("Nama gelombang sudah digunakan pada tahun ajaran ini")

    gelombang = Gelombang(**data)

    db.session.add(gelombang)
    db.session.commit()

    return gelombang


def update_gelombang(id, data):
    gelombang = get_gelombang_by_id(id)

    if data["tanggal_selesai"] <= data["tanggal_mulai"]:
        raise ValueError("Tanggal selesai harus lebih besar dari tanggal mulai")

    exists = (
        Gelombang.query
        .filter(
            Gelombang.tahun_ajaran_id == gelombang.tahun_ajaran_id,
            Gelombang.nama == data["nama"],
            Gelombang.id != id,
        )
        .first()
    )

    if exists:
        raise ValueError("Nama gelombang sudah digunakan pada tahun ajaran ini")

    gelombang.nama = data["nama"]
    gelombang.tanggal_mulai = data["tanggal_mulai"]
    gelombang.tanggal_selesai = data["tanggal_selesai"]

    db.session.commit()

    return gelombang


def delete_gelombang(id):
    gelombang = get_gelombang_by_id(id)

    if gelombang.pendaftaran:
        raise ValueError("Gelombang sudah digunakan pada pendaftaran dan tidak dapat dihapus")

    db.session.delete(gelombang)
    db.session.commit()