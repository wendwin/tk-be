from datetime import date

from app.extensions import db
from app.models.akademik.siswa import Siswa
from app.models.akademik.kelas import Kelas
from app.models.akademik.siswa_kelas import SiswaKelas
from app.models.pendaftaran import TahunAjaran, Pendaftaran

from app.models.observasi import GPPHJawaban, KPSPJawaban


def get_observasi_summary(siswa):
    pendaftaran = (
        Pendaftaran.query
        .filter_by(
            peserta_id=siswa.peserta_id,
            status="accepted"
        )
        .order_by(Pendaftaran.created_at.desc())
        .first()
    )

    if not pendaftaran:
        return None

    gpph_total = (
        db.session.query(db.func.sum(GPPHJawaban.nilai))
        .filter_by(pendaftaran_id=pendaftaran.id)
        .scalar()
    )

    kpsp_jawaban = (
        KPSPJawaban.query
        .filter_by(pendaftaran_id=pendaftaran.id)
        .all()
    )

    total_ya = len([item for item in kpsp_jawaban if item.jawaban == "ya"])
    catatan = kpsp_jawaban[0].catatan if kpsp_jawaban else None

    return {
        "pendaftaran_id": pendaftaran.id,
        "gpph_total": int(gpph_total or 0),
        "kpsp_total_ya": total_ya,
        "catatan": catatan,
        "kebutuhan_khusus": siswa.peserta.kesehatan.kebutuhan_khusus
        if siswa.peserta and siswa.peserta.kesehatan
        else [],
    }


def hitung_umur_tahun(tanggal_lahir):
    today = date.today()

    return (
        today.year
        - tanggal_lahir.year
        - ((today.month, today.day) < (tanggal_lahir.month, tanggal_lahir.day))
    )


def get_unassigned_siswa(tahun_ajaran_id=None, kelas_id=None, jenjang=None, program=None):
    kelas = None

    if kelas_id:
        kelas = db.session.get(Kelas, kelas_id)

        if not kelas:
            raise ValueError("Kelas tidak ditemukan")

    assigned_subquery = (
        db.session.query(SiswaKelas.siswa_id)
        .filter(SiswaKelas.status == "aktif")
    )

    if tahun_ajaran_id:
        assigned_subquery = assigned_subquery.filter(
            SiswaKelas.tahun_ajaran_id == tahun_ajaran_id
        )

    query = (
        Siswa.query
        .join(Siswa.peserta)
        .filter(Siswa.status == "aktif")
        .filter(~Siswa.id.in_(assigned_subquery))
    )

    result = []

    for siswa in query.all():
        pendaftaran = (
            Pendaftaran.query
            .filter_by(
                peserta_id=siswa.peserta_id,
                status="accepted"
            )
            .order_by(Pendaftaran.created_at.desc())
            .first()
        )

        if not pendaftaran:
            continue

        if kelas:
            umur = hitung_umur_tahun(siswa.peserta.tanggal_lahir)

            if kelas.jenjang == "kb":
                if pendaftaran.jenis != "kb":
                    continue

                if not (2 <= umur < 4):
                    continue

            if kelas.jenjang == "tk" and kelas.kelompok == "a":
                if pendaftaran.jenis != "tk":
                    continue

                if not (4 <= umur < 5):
                    continue

            if kelas.jenjang == "tk" and kelas.kelompok == "b":
                if pendaftaran.jenis != "tk":
                    continue

                if not (5 <= umur <= 6):
                    continue

        elif jenjang and pendaftaran.jenis != jenjang:
            continue

        if program and pendaftaran.program != program:
            continue

        result.append({
            "id": siswa.id,
            "nama_lengkap": siswa.peserta.nama_lengkap,
            "jenis_kelamin": siswa.peserta.jenis_kelamin,
            "tanggal_lahir": siswa.peserta.tanggal_lahir,
            "jenis": pendaftaran.jenis,
            "program": pendaftaran.program,
            "observasi": get_observasi_summary(siswa),
        })

    return sorted(result, key=lambda item: item["tanggal_lahir"], reverse=True)


def get_siswa_by_kelas(kelas_id, tahun_ajaran_id):
    return (
        SiswaKelas.query
        .filter_by(
            kelas_id=kelas_id,
            tahun_ajaran_id=tahun_ajaran_id,
            status="aktif"
        )
        .all()
    )


def get_rekomendasi_siswa_kelas(tahun_ajaran_id, kelas_id, jenjang=None, program=None):
    kelas = db.session.get(Kelas, kelas_id)

    if not kelas:
        raise ValueError("Kelas tidak ditemukan")

    siswa = get_unassigned_siswa(
        tahun_ajaran_id=tahun_ajaran_id,
        kelas_id=kelas_id,
        program=program
    )

    return siswa[:kelas.kapasitas]


def validate_assign(siswa_id, kelas_id, tahun_ajaran_id):
    siswa = db.session.get(Siswa, siswa_id)

    if not siswa:
        raise ValueError("Siswa tidak ditemukan")

    if siswa.status != "aktif":
        raise ValueError("Siswa tidak aktif")

    kelas = db.session.get(Kelas, kelas_id)

    if not kelas:
        raise ValueError("Kelas tidak ditemukan")

    tahun_ajaran = db.session.get(TahunAjaran, tahun_ajaran_id)

    if not tahun_ajaran:
        raise ValueError("Tahun ajaran tidak ditemukan")

    existing = SiswaKelas.query.filter_by(
        siswa_id=siswa_id,
        tahun_ajaran_id=tahun_ajaran_id,
        status="aktif"
    ).first()

    if existing:
        raise ValueError("Siswa sudah masuk kelas pada tahun ajaran ini")

    total_siswa = SiswaKelas.query.filter_by(
        kelas_id=kelas_id,
        tahun_ajaran_id=tahun_ajaran_id,
        status="aktif"
    ).count()

    if total_siswa >= kelas.kapasitas:
        raise ValueError("Kapasitas kelas sudah penuh")

    return siswa, kelas, tahun_ajaran


def assign_siswa_kelas(data):
    validate_assign(
        data["siswa_id"],
        data["kelas_id"],
        data["tahun_ajaran_id"]
    )

    siswa_kelas = SiswaKelas(
        siswa_id=data["siswa_id"],
        kelas_id=data["kelas_id"],
        tahun_ajaran_id=data["tahun_ajaran_id"],
        status="aktif"
    )

    db.session.add(siswa_kelas)
    db.session.commit()

    return siswa_kelas


def bulk_assign_siswa_kelas(data):
    created = []

    for siswa_id in data["siswa_ids"]:
        validate_assign(
            siswa_id,
            data["kelas_id"],
            data["tahun_ajaran_id"]
        )

        siswa_kelas = SiswaKelas(
            siswa_id=siswa_id,
            kelas_id=data["kelas_id"],
            tahun_ajaran_id=data["tahun_ajaran_id"],
            status="aktif"
        )

        db.session.add(siswa_kelas)
        created.append(siswa_kelas)

    db.session.commit()

    return created


def update_siswa_kelas(id, data):
    siswa_kelas = db.session.get(SiswaKelas, id)

    if not siswa_kelas:
        raise ValueError("Data siswa kelas tidak ditemukan")

    if "kelas_id" in data:
        kelas = db.session.get(Kelas, data["kelas_id"])

        if not kelas:
            raise ValueError("Kelas tidak ditemukan")

        siswa_kelas.kelas_id = data["kelas_id"]

    if "status" in data:
        siswa_kelas.status = data["status"]

    db.session.commit()

    return siswa_kelas


def delete_siswa_kelas(id):
    siswa_kelas = db.session.get(SiswaKelas, id)

    if not siswa_kelas:
        raise ValueError("Data siswa kelas tidak ditemukan")

    db.session.delete(siswa_kelas)
    db.session.commit()

    return True