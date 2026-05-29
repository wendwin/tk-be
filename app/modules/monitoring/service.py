from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.monitoring.monitoring import Monitoring
from app.models.monitoring.tp import MonitoringTP
from app.models.monitoring.kktp import MonitoringKKTP
from app.models.monitoring.kegiatan import MonitoringKegiatan
from app.models.monitoring.asesmen_awal import MonitoringAsesmenAwal
from app.models.monitoring.karya import MonitoringKarya
from app.models.monitoring.anekdot import MonitoringAnekdot
from app.models.monitoring.indikator import MonitoringIndikator
from app.models.monitoring.rekomendasi import MonitoringRekomendasi

from app.models.akademik.siswa_kelas import SiswaKelas
from app.models.akademik.siswa import Siswa
from app.models.akademik.kelas import Kelas


def get_all_monitoring(
    page=1,
    per_page=10,
    siswa_id=None,
    kelas_id=None,
    tahun_ajaran_id=None,
    semester=None,
    status=None,
    user_id=None,
):
    query = (
        Monitoring.query
        .join(Monitoring.siswa_kelas)
        .options(
            joinedload(Monitoring.siswa_kelas)
            .joinedload(SiswaKelas.siswa)
            .joinedload(Siswa.peserta),
            joinedload(Monitoring.siswa_kelas).joinedload(SiswaKelas.kelas),
            joinedload(Monitoring.siswa_kelas).joinedload(SiswaKelas.tahun_ajaran),
        )
        .order_by(Monitoring.tanggal_mulai.desc())
    )

    if siswa_id:
        query = query.filter(SiswaKelas.siswa_id == siswa_id)

    if kelas_id:
        query = query.filter(SiswaKelas.kelas_id == kelas_id)

    if tahun_ajaran_id:
        query = query.filter(SiswaKelas.tahun_ajaran_id == tahun_ajaran_id)

    if semester:
        query = query.filter(Monitoring.semester == semester)

    if status:
        query = query.filter(Monitoring.status == status)

    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_monitoring_by_id(id):
    monitoring = (
        Monitoring.query
        .options(
            joinedload(Monitoring.siswa_kelas)
            .joinedload(SiswaKelas.siswa)
            .joinedload(Siswa.peserta),
            joinedload(Monitoring.siswa_kelas).joinedload(SiswaKelas.kelas),
            joinedload(Monitoring.siswa_kelas).joinedload(SiswaKelas.tahun_ajaran),
            joinedload(Monitoring.tujuan_pembelajaran).joinedload(MonitoringTP.kktp),
            joinedload(Monitoring.kegiatan),
            joinedload(Monitoring.asesmen_awal),
            joinedload(Monitoring.karya).joinedload(MonitoringKarya.kktp),
            joinedload(Monitoring.anekdot).joinedload(MonitoringAnekdot.kktp),
            joinedload(Monitoring.indikator).joinedload(MonitoringIndikator.kktp),
            joinedload(Monitoring.rekomendasi),
        )
        .filter(Monitoring.id == id)
        .first()
    )

    if not monitoring:
        raise ValueError("Data monitoring tidak ditemukan")

    return monitoring


def create_monitoring(data, user_id):
    monitoring = Monitoring(
        siswa_kelas_id=data["siswa_kelas_id"],
        created_by=user_id,
        semester=data["semester"],
        minggu=data["minggu"],
        topik=data["topik"],
        sub_topik=data["sub_topik"],
        tanggal_mulai=data["tanggal_mulai"],
        tanggal_selesai=data["tanggal_selesai"],
        ringkasan=data.get("ringkasan"),
        status=data.get("status", "draft"),
    )

    db.session.add(monitoring)
    db.session.flush()

    create_child_data(monitoring, data)

    db.session.commit()

    return get_monitoring_by_id(monitoring.id)


def update_monitoring(id, data):
    monitoring = Monitoring.query.get(id)

    if not monitoring:
        raise ValueError("Data monitoring tidak ditemukan")

    monitoring.semester = data.get("semester", monitoring.semester)
    monitoring.minggu = data.get("minggu", monitoring.minggu)
    monitoring.topik = data.get("topik", monitoring.topik)
    monitoring.sub_topik = data.get("sub_topik", monitoring.sub_topik)
    monitoring.tanggal_mulai = data.get("tanggal_mulai", monitoring.tanggal_mulai)
    monitoring.tanggal_selesai = data.get("tanggal_selesai", monitoring.tanggal_selesai)
    monitoring.ringkasan = data.get("ringkasan", monitoring.ringkasan)
    monitoring.status = data.get("status", monitoring.status)

    if "replace_detail" in data and data["replace_detail"] is True:
        delete_child_data(monitoring.id)
        create_child_data(monitoring, data)

    db.session.commit()

    return get_monitoring_by_id(monitoring.id)


def publish_monitoring(id):
    monitoring = Monitoring.query.get(id)

    if not monitoring:
        raise ValueError("Data monitoring tidak ditemukan")

    monitoring.status = "published"

    db.session.commit()

    return get_monitoring_by_id(monitoring.id)


def create_child_data(monitoring, data):
    tp_map = {}
    kktp_map = {}

    for tp_data in data.get("tujuan_pembelajaran", []):
        tp = MonitoringTP(
            monitoring_id=monitoring.id,
            elemen=tp_data["elemen"],
            tujuan=tp_data["tujuan"],
        )

        db.session.add(tp)
        db.session.flush()

        tp_map[tp_data.get("key", str(tp.id))] = tp

        for kktp_data in tp_data.get("kktp", []):
            kktp = MonitoringKKTP(
                tp_id=tp.id,
                deskripsi=kktp_data["deskripsi"],
            )

            db.session.add(kktp)
            db.session.flush()

            kktp_map[kktp_data.get("key", str(kktp.id))] = kktp

    for kegiatan_data in data.get("kegiatan", []):
        db.session.add(MonitoringKegiatan(
            monitoring_id=monitoring.id,
            nama=kegiatan_data["nama"],
            media=kegiatan_data.get("media"),
        ))

    asesmen_awal = data.get("asesmen_awal")

    if asesmen_awal:
        db.session.add(MonitoringAsesmenAwal(
            monitoring_id=monitoring.id,
            teknik=asesmen_awal.get("teknik", "Observasi"),
            rancangan_kegiatan=asesmen_awal["rancangan_kegiatan"],
            hasil=asesmen_awal.get("hasil"),
        ))

    for karya_data in data.get("karya", []):
        db.session.add(MonitoringKarya(
            monitoring_id=monitoring.id,
            kktp_id=resolve_kktp_id(karya_data, kktp_map),
            kegiatan=karya_data["kegiatan"],
            foto=karya_data.get("foto"),
            deskripsi=karya_data["deskripsi"],
            analisa=karya_data["analisa"],
        ))

    for anekdot_data in data.get("anekdot", []):
        db.session.add(MonitoringAnekdot(
            monitoring_id=monitoring.id,
            kktp_id=resolve_kktp_id(anekdot_data, kktp_map),
            waktu=anekdot_data["waktu"],
            catatan=anekdot_data["catatan"],
        ))

    for indikator_data in data.get("indikator", []):
        db.session.add(MonitoringIndikator(
            monitoring_id=monitoring.id,
            kktp_id=resolve_kktp_id(indikator_data, kktp_map),
            muncul=indikator_data.get("muncul", False),
            kejadian_teramati=indikator_data.get("kejadian_teramati"),
        ))

    for rekomendasi_data in data.get("rekomendasi", []):
        db.session.add(MonitoringRekomendasi(
            monitoring_id=monitoring.id,
            elemen=rekomendasi_data["elemen"],
            tips=rekomendasi_data["tips"],
        ))


def resolve_kktp_id(data, kktp_map):
    if data.get("kktp_id"):
        return data["kktp_id"]

    if data.get("kktp_key") and data["kktp_key"] in kktp_map:
        return kktp_map[data["kktp_key"]].id

    raise ValueError("KKTP tidak valid")


def delete_child_data(monitoring_id):
    MonitoringRekomendasi.query.filter_by(monitoring_id=monitoring_id).delete()
    MonitoringIndikator.query.filter_by(monitoring_id=monitoring_id).delete()
    MonitoringAnekdot.query.filter_by(monitoring_id=monitoring_id).delete()
    MonitoringKarya.query.filter_by(monitoring_id=monitoring_id).delete()
    MonitoringAsesmenAwal.query.filter_by(monitoring_id=monitoring_id).delete()
    MonitoringKegiatan.query.filter_by(monitoring_id=monitoring_id).delete()

    tp_list = MonitoringTP.query.filter_by(monitoring_id=monitoring_id).all()

    for tp in tp_list:
        MonitoringKKTP.query.filter_by(tp_id=tp.id).delete()

    MonitoringTP.query.filter_by(monitoring_id=monitoring_id).delete()