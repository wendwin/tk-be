from app.extensions import db
from app.models.akademik.siswa import Siswa
from app.models.pendaftaran import Pendaftaran, PesertaDidik
from app.models.akademik.siswa_kelas import SiswaKelas

def get_all_siswa(
    page=1,
    per_page=10,
    search=None,
    status=None,
    jenis=None,
    program=None,
    tahun_ajaran_id=None,
    kelas_id=None,
):
    query = (
        Siswa.query
        .join(Siswa.peserta)
        .join(PesertaDidik.pendaftaran)
        .filter(Pendaftaran.status == "accepted")
    )

    if search:
        query = query.filter(
            PesertaDidik.nama_lengkap.ilike(f"%{search}%")
        )

    if status:
        query = query.filter(
            Siswa.status == status
        )

    if jenis:
        query = query.filter(
            Pendaftaran.jenis == jenis
        )

    if program:
        query = query.filter(
            Pendaftaran.program == program
        )

    if tahun_ajaran_id:
        query = query.filter(
            Pendaftaran.tahun_ajaran_id == tahun_ajaran_id
        )

    if kelas_id:
        query = query.join(Siswa.riwayat_kelas).filter(
            SiswaKelas.kelas_id == kelas_id,
            SiswaKelas.status == "aktif"
        )

    return (
        query
        .distinct()
        .order_by(Siswa.created_at.desc())
        .paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
    )


def get_siswa_by_id(id):
    siswa = db.session.get(Siswa, id)

    if not siswa:
        raise ValueError("Siswa tidak ditemukan")

    return siswa


def create_siswa_from_pendaftaran(pendaftaran_id):
    pendaftaran = db.session.get(Pendaftaran, pendaftaran_id)

    if not pendaftaran:
        raise ValueError("Pendaftaran tidak ditemukan")

    if pendaftaran.status != "accepted":
        raise ValueError("Pendaftaran belum diterima")

    existing = Siswa.query.filter_by(
        peserta_id=pendaftaran.peserta_id
    ).first()

    if existing:
        return existing

    nisn = None

    if (
        pendaftaran.peserta
        and pendaftaran.peserta.informasi
    ):
        nisn = pendaftaran.peserta.informasi.nisn or None

    siswa = Siswa(
        peserta_id=pendaftaran.peserta_id,
        nisn=nisn,
        tanggal_masuk=pendaftaran.tahun_ajaran.tanggal_mulai,
        status="aktif"
    )

    db.session.add(siswa)
    db.session.commit()

    return siswa


def update_siswa(id, data):
    siswa = db.session.get(Siswa, id)

    if not siswa:
        raise ValueError("Siswa tidak ditemukan")

    if not data:
        raise ValueError("Tidak ada data yang diupdate")

    if "nisn" in data:
        nisn = data["nisn"].strip() if data["nisn"] else None

        if nisn:
            existing = Siswa.query.filter(
                Siswa.nisn == nisn,
                Siswa.id != siswa.id
            ).first()

            if existing:
                raise ValueError(
                    "NISN sudah digunakan siswa lain"
                )

        siswa.nisn = nisn

    if "status" in data:
        siswa.status = data["status"]

    db.session.commit()

    return siswa