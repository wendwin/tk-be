from app.extensions import db
from app.models.auth.user import User
from app.models.akademik.kelas import Kelas
from app.models.akademik.guru_kelas import GuruKelas
from app.models.pendaftaran import TahunAjaran


def get_all_guru_kelas():
    return (
        GuruKelas.query
        .order_by(GuruKelas.created_at.desc())
        .all()
    )


def get_guru_kelas_by_id(id):
    guru_kelas = db.session.get(GuruKelas, id)

    if not guru_kelas:
        raise ValueError("Data guru kelas tidak ditemukan")

    return guru_kelas


def create_guru_kelas(data):
    guru = db.session.get(User, data["guru_id"])

    if not guru:
        raise ValueError("Guru tidak ditemukan")

    if not guru.role or guru.role.name != "guru":
        raise ValueError("User yang dipilih bukan guru")

    kelas = db.session.get(Kelas, data["kelas_id"])

    if not kelas:
        raise ValueError("Kelas tidak ditemukan")

    tahun_ajaran = db.session.get(TahunAjaran, data["tahun_ajaran_id"])

    if not tahun_ajaran:
        raise ValueError("Tahun ajaran tidak ditemukan")

    exists = GuruKelas.query.filter_by(
        guru_id=data["guru_id"],
        kelas_id=data["kelas_id"],
        tahun_ajaran_id=data["tahun_ajaran_id"],
    ).first()

    if exists:
        raise ValueError("Guru sudah terdaftar pada kelas dan tahun ajaran ini")

    if data["peran"] == "wali kelas":
        wali_exists = GuruKelas.query.filter_by(
            kelas_id=data["kelas_id"],
            tahun_ajaran_id=data["tahun_ajaran_id"],
            peran="wali kelas",
        ).first()

        if wali_exists:
            raise ValueError("Kelas ini sudah memiliki wali kelas")

    guru_kelas = GuruKelas(
        guru_id=data["guru_id"],
        kelas_id=data["kelas_id"],
        tahun_ajaran_id=data["tahun_ajaran_id"],
        peran=data["peran"],
    )

    db.session.add(guru_kelas)
    db.session.commit()

    return guru_kelas


def update_guru_kelas(id, data):
    guru_kelas = db.session.get(GuruKelas, id)

    if not guru_kelas:
        raise ValueError("Data guru kelas tidak ditemukan")

    if "guru_id" in data:
        guru = db.session.get(User, data["guru_id"])
    
        if not guru:
            raise ValueError("Guru tidak ditemukan")
    
        if not guru.role or guru.role.name != "guru":
            raise ValueError("User yang dipilih bukan guru")

        guru_kelas.guru_id = data["guru_id"]

    if "kelas_id" in data:
        kelas = db.session.get(Kelas, data["kelas_id"])

        if not kelas:
            raise ValueError("Kelas tidak ditemukan")

        guru_kelas.kelas_id = data["kelas_id"]

    if "tahun_ajaran_id" in data:
        tahun_ajaran = db.session.get(TahunAjaran, data["tahun_ajaran_id"])

        if not tahun_ajaran:
            raise ValueError("Tahun ajaran tidak ditemukan")

        guru_kelas.tahun_ajaran_id = data["tahun_ajaran_id"]

    if "peran" in data:
        if data["peran"] == "wali_kelas":
            wali_exists = GuruKelas.query.filter(
                GuruKelas.id != id,
                GuruKelas.kelas_id == guru_kelas.kelas_id,
                GuruKelas.tahun_ajaran_id == guru_kelas.tahun_ajaran_id,
                GuruKelas.peran == "wali_kelas",
            ).first()

            if wali_exists:
                raise ValueError("Kelas ini sudah memiliki wali kelas")

        guru_kelas.peran = data["peran"]

    db.session.commit()

    return guru_kelas


def delete_guru_kelas(id):
    guru_kelas = db.session.get(GuruKelas, id)

    if not guru_kelas:
        raise ValueError("Data guru kelas tidak ditemukan")

    db.session.delete(guru_kelas)
    db.session.commit()

    return True

def get_my_guru_kelas(user_id):
    tahun_ajaran_aktif = TahunAjaran.query.filter_by(
        is_active=True
    ).first()

    if not tahun_ajaran_aktif:
        return []

    guru_kelas = (
        GuruKelas.query
        .filter(
            GuruKelas.guru_id == user_id,
            GuruKelas.tahun_ajaran_id == tahun_ajaran_aktif.id,
        )
        .order_by(GuruKelas.created_at.desc())
        .all()
    )

    return guru_kelas