from sqlalchemy.orm import joinedload

from app.extensions import db

from app.models.monitoring.mingguan.monitoring import MonitoringMingguan
from app.models.monitoring.mingguan.tp import MonitoringTP
from app.models.monitoring.mingguan.kktp import MonitoringKKTP
from app.models.monitoring.mingguan.kegiatan import MonitoringKegiatan
from app.models.monitoring.mingguan.asesmen_awal import MonitoringAsesmenAwal
from app.models.akademik.siswa_kelas import SiswaKelas


def get_all_mingguan(
    page=1,
    per_page=10,
    kelas_id=None,
    tahun_ajaran_id=None,
    semester=None,
    status=None,
):
    query = (
        MonitoringMingguan.query
        .options(
            joinedload(MonitoringMingguan.kelas),
            joinedload(MonitoringMingguan.tahun_ajaran),
        )
        .order_by(MonitoringMingguan.tanggal_mulai.desc())
    )

    if kelas_id:
        query = query.filter(MonitoringMingguan.kelas_id == kelas_id)

    if tahun_ajaran_id:
        query = query.filter(MonitoringMingguan.tahun_ajaran_id == tahun_ajaran_id)

    if semester:
        query = query.filter(MonitoringMingguan.semester == semester)

    if status:
        query = query.filter(MonitoringMingguan.status == status)

    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_mingguan_by_id(id):
    monitoring = (
        MonitoringMingguan.query
        .options(
            joinedload(MonitoringMingguan.kelas),
            joinedload(MonitoringMingguan.tahun_ajaran),
            joinedload(MonitoringMingguan.tp).joinedload(MonitoringTP.kktp),
            joinedload(MonitoringMingguan.kegiatan),
            joinedload(MonitoringMingguan.asesmen_awal),
        )
        .filter(MonitoringMingguan.id == id)
        .first()
    )

    if not monitoring:
        raise ValueError("Data monitoring mingguan tidak ditemukan")

    return monitoring


def create_mingguan(data, user_id):
    existing = MonitoringMingguan.query.filter_by(
        kelas_id=data["kelas_id"],
        tahun_ajaran_id=data["tahun_ajaran_id"],
        semester=data["semester"],
        minggu=data["minggu"],
    ).first()

    if existing:
        raise ValueError(
            "Monitoring mingguan untuk kelas, semester, dan minggu ini sudah dibuat"
        )
    
    monitoring = MonitoringMingguan(
        kelas_id=data["kelas_id"],
        tahun_ajaran_id=data["tahun_ajaran_id"],
        created_by=user_id,
        semester=data["semester"],
        minggu=data["minggu"],
        topik=data["topik"],
        sub_topik=data["sub_topik"],
        tanggal_mulai=data["tanggal_mulai"],
        tanggal_selesai=data["tanggal_selesai"],
    )

    if "status" in data:
        monitoring.status = data["status"]

    db.session.add(monitoring)
    db.session.flush()

    create_detail_mingguan(monitoring.id, data)

    db.session.commit()

    return get_mingguan_by_id(monitoring.id)


def update_mingguan(id, data):
    monitoring = MonitoringMingguan.query.get(id)

    if not monitoring:
        raise ValueError("Data monitoring mingguan tidak ditemukan")

    existing = MonitoringMingguan.query.filter(
        MonitoringMingguan.id != monitoring.id,
        MonitoringMingguan.kelas_id == data.get("kelas_id", monitoring.kelas_id),
        MonitoringMingguan.tahun_ajaran_id == data.get(
            "tahun_ajaran_id",
            monitoring.tahun_ajaran_id
        ),
        MonitoringMingguan.semester == data.get("semester", monitoring.semester),
        MonitoringMingguan.minggu == data.get("minggu", monitoring.minggu),
    ).first()

    if existing:
        raise ValueError(
            "Monitoring mingguan untuk kelas, semester, dan minggu ini sudah dibuat"
        )

    monitoring.kelas_id = data.get("kelas_id", monitoring.kelas_id)
    monitoring.tahun_ajaran_id = data.get(
        "tahun_ajaran_id",
        monitoring.tahun_ajaran_id
    )
    monitoring.semester = data.get("semester", monitoring.semester)
    monitoring.minggu = data.get("minggu", monitoring.minggu)
    monitoring.topik = data.get("topik", monitoring.topik)
    monitoring.sub_topik = data.get("sub_topik", monitoring.sub_topik)
    monitoring.tanggal_mulai = data.get("tanggal_mulai", monitoring.tanggal_mulai)
    monitoring.tanggal_selesai = data.get(
        "tanggal_selesai",
        monitoring.tanggal_selesai
    )
    monitoring.status = data.get("status", monitoring.status)

    if data.get("replace_detail") is True:
        delete_detail_mingguan(monitoring.id)
        create_detail_mingguan(monitoring.id, data)

    db.session.commit()

    return get_mingguan_by_id(monitoring.id)


def publish_mingguan(id):
    monitoring = MonitoringMingguan.query.get(id)

    if not monitoring:
        raise ValueError("Data monitoring mingguan tidak ditemukan")

    total_siswa = SiswaKelas.query.filter_by(
        kelas_id=monitoring.kelas_id,
        tahun_ajaran_id=monitoring.tahun_ajaran_id,
        status="aktif"
    ).count()

    total_selesai = len(monitoring.monitoring_siswa)

    if total_siswa == 0:
        raise ValueError(
            "Monitoring tidak dapat dipublikasikan karena belum ada siswa aktif pada kelas ini"
        )

    if total_selesai < total_siswa:
        raise ValueError(
            "Monitoring belum dapat dipublikasikan karena masih ada siswa yang belum diisi"
        )

    monitoring.status = "published"

    db.session.commit()

    return get_mingguan_by_id(monitoring.id)


def create_detail_mingguan(monitoring_id, data):
    for tp_data in data.get("tp", []):
        tp = MonitoringTP(
            monitoring_mingguan_id=monitoring_id,
            elemen=tp_data["elemen"],
            tujuan=tp_data["tujuan"],
        )

        db.session.add(tp)
        db.session.flush()

        for kktp_data in tp_data.get("kktp", []):
            db.session.add(MonitoringKKTP(
                tp_id=tp.id,
                deskripsi=kktp_data["deskripsi"],
            ))

    for kegiatan_data in data.get("kegiatan", []):
        db.session.add(MonitoringKegiatan(
            monitoring_mingguan_id=monitoring_id,
            nama=kegiatan_data["nama"],
            media=kegiatan_data.get("media"),
        ))

    asesmen_awal = data.get("asesmen_awal")

    if asesmen_awal:
        db.session.add(MonitoringAsesmenAwal(
            monitoring_mingguan_id=monitoring_id,
            teknik=asesmen_awal.get("teknik", "Observasi"),
            rancangan_kegiatan=asesmen_awal["rancangan_kegiatan"],
            hasil=asesmen_awal.get("hasil"),
        ))


def delete_detail_mingguan(monitoring_id):
    MonitoringAsesmenAwal.query.filter_by(
        monitoring_mingguan_id=monitoring_id
    ).delete()

    MonitoringKegiatan.query.filter_by(
        monitoring_mingguan_id=monitoring_id
    ).delete()

    tp_list = MonitoringTP.query.filter_by(
        monitoring_mingguan_id=monitoring_id
    ).all()

    for tp in tp_list:
        MonitoringKKTP.query.filter_by(tp_id=tp.id).delete()

    MonitoringTP.query.filter_by(
        monitoring_mingguan_id=monitoring_id
    ).delete()