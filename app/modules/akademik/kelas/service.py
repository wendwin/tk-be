from app.extensions import db
from app.models.akademik.kelas import Kelas
from app.models.pendaftaran import TahunAjaran

def get_all_kelas():
    return (
        Kelas.query
        .order_by(Kelas.created_at.desc())
        .all()
    )


def get_kelas_by_id(id):
    kelas = db.session.get(Kelas, id)

    if not kelas:
        raise ValueError("Kelas tidak ditemukan")

    return kelas


def create_kelas(data):
    tahun_ajaran = db.session.get(
        TahunAjaran,
        data["tahun_ajaran_id"]
    )

    if not tahun_ajaran:
        raise ValueError("Tahun ajaran tidak ditemukan")

    exists = Kelas.query.filter_by(
        tahun_ajaran_id=data["tahun_ajaran_id"],
        nama=data["nama"]
    ).first()

    if exists:
        raise ValueError("Kelas sudah ada pada tahun ajaran tersebut")

    kelas = Kelas(
        tahun_ajaran_id=data["tahun_ajaran_id"],
        nama=data["nama"],
        jenjang=data["jenjang"],
        kelompok=data.get("kelompok"),
        kapasitas=data["kapasitas"]
    )

    db.session.add(kelas)
    db.session.commit()

    return kelas


def update_kelas(id, data):
    kelas = db.session.get(Kelas, id)

    if not kelas:
        raise ValueError("Kelas tidak ditemukan")

    if "tahun_ajaran_id" in data:
        tahun_ajaran = db.session.get(
            TahunAjaran,
            data["tahun_ajaran_id"]
        )

        if not tahun_ajaran:
            raise ValueError("Tahun ajaran tidak ditemukan")

        kelas.tahun_ajaran_id = data["tahun_ajaran_id"]

    if "nama" in data:
        kelas.nama = data["nama"]

    if "jenjang" in data:
        kelas.jenjang = data["jenjang"]

    if "kelompok" in data:
        kelas.kelompok = data["kelompok"]

    if "kapasitas" in data:
        kelas.kapasitas = data["kapasitas"]

    db.session.commit()

    return kelas


def delete_kelas(id):
    kelas = db.session.get(Kelas, id)

    if not kelas:
        raise ValueError("Kelas tidak ditemukan")

    db.session.delete(kelas)
    db.session.commit()

    return True