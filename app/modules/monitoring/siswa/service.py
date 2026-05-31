from sqlalchemy.orm import joinedload

from app.extensions import db

from app.models.monitoring.mingguan.monitoring import MonitoringMingguan
from app.models.monitoring.mingguan.tp import MonitoringTP
from app.models.monitoring.mingguan.kktp import MonitoringKKTP

from app.models.monitoring.siswa.siswa import MonitoringSiswa
from app.models.monitoring.siswa.karya import MonitoringKarya
from app.models.monitoring.siswa.anekdot import MonitoringAnekdot
from app.models.monitoring.siswa.indikator import MonitoringIndikator
from app.models.monitoring.siswa.rekomendasi import MonitoringRekomendasi

from app.models.akademik.siswa_kelas import SiswaKelas
from app.models.akademik.siswa import Siswa

from app.utils.file_helper import validate_monitoring_image, save_file


def get_all_siswa_monitoring(
    page=1,
    per_page=10,
    monitoring_mingguan_id=None,
    siswa_kelas_id=None,
    status=None,
):
    query = (
        MonitoringSiswa.query
        .options(
            joinedload(MonitoringSiswa.monitoring_mingguan),
            joinedload(MonitoringSiswa.siswa_kelas)
            .joinedload(SiswaKelas.siswa)
            .joinedload(Siswa.peserta),
        )
        .order_by(MonitoringSiswa.created_at.desc())
    )

    if monitoring_mingguan_id:
        query = query.filter(
            MonitoringSiswa.monitoring_mingguan_id == monitoring_mingguan_id
        )

    if siswa_kelas_id:
        query = query.filter(
            MonitoringSiswa.siswa_kelas_id == siswa_kelas_id
        )

    if status:
        query = query.filter(MonitoringSiswa.status == status)

    return query.paginate(page=page, per_page=per_page, error_out=False)


def get_siswa_monitoring_by_id(id):
    monitoring = (
        MonitoringSiswa.query
        .options(
            joinedload(MonitoringSiswa.monitoring_mingguan)
            .joinedload(MonitoringMingguan.tp)
            .joinedload(MonitoringTP.kktp),

            joinedload(MonitoringSiswa.monitoring_mingguan)
            .joinedload(MonitoringMingguan.kegiatan),

            joinedload(MonitoringSiswa.monitoring_mingguan)
            .joinedload(MonitoringMingguan.asesmen_awal),

            joinedload(MonitoringSiswa.siswa_kelas)
            .joinedload(SiswaKelas.siswa)
            .joinedload(Siswa.peserta),

            joinedload(MonitoringSiswa.karya)
            .joinedload(MonitoringKarya.kktp),

            joinedload(MonitoringSiswa.anekdot)
            .joinedload(MonitoringAnekdot.kktp),

            joinedload(MonitoringSiswa.indikator)
            .joinedload(MonitoringIndikator.tp)
            .joinedload(MonitoringTP.kktp),

            joinedload(MonitoringSiswa.rekomendasi),
        )
        .filter(MonitoringSiswa.id == id)
        .first()
    )

    if not monitoring:
        raise ValueError("Data monitoring siswa tidak ditemukan")

    return monitoring


def create_siswa_monitoring(data, user_id, files=None):
    validate_detail_belongs_to_mingguan(
        data["monitoring_mingguan_id"],
        data
    )

    monitoring = MonitoringSiswa(
        monitoring_mingguan_id=data["monitoring_mingguan_id"],
        siswa_kelas_id=data["siswa_kelas_id"],
        created_by=user_id,
        ringkasan=data.get("ringkasan"),
    )

    if "status" in data:
        monitoring.status = data["status"]

    db.session.add(monitoring)
    db.session.flush()

    create_detail_siswa(monitoring.id, data, files)

    db.session.commit()

    return get_siswa_monitoring_by_id(monitoring.id)


def update_siswa_monitoring(id, data, files=None):
    monitoring = MonitoringSiswa.query.get(id)

    if not monitoring:
        raise ValueError("Data monitoring siswa tidak ditemukan")

    monitoring.ringkasan = data.get("ringkasan", monitoring.ringkasan)
    monitoring.status = data.get("status", monitoring.status)

    payload = {
        **data,
        "monitoring_mingguan_id": monitoring.monitoring_mingguan_id,
    }

    validate_detail_belongs_to_mingguan(
        monitoring.monitoring_mingguan_id,
        payload
    )

    delete_detail_siswa(monitoring.id)
    create_detail_siswa(monitoring.id, payload, files)

    db.session.commit()

    return get_siswa_monitoring_by_id(monitoring.id)


def publish_siswa_monitoring(id):
    monitoring = MonitoringSiswa.query.get(id)

    if not monitoring:
        raise ValueError("Data monitoring siswa tidak ditemukan")

    monitoring.status = "published"

    db.session.commit()

    return get_siswa_monitoring_by_id(monitoring.id)


def create_detail_siswa(monitoring_siswa_id, data, files=None):
    for index, karya_data in enumerate(data.get("karya", [])):
        foto_path = karya_data.get("foto") 
        
        if files:
            file_key = f"karya[{index}][foto]"
            foto_file = files.get(file_key)

            if foto_file:
                validate_monitoring_image(foto_file)
                foto_path = save_file(foto_file, "monitoring/karya")

        db.session.add(MonitoringKarya(
            monitoring_siswa_id=monitoring_siswa_id,
            kktp_id=karya_data["kktp_id"],
            kegiatan=karya_data["kegiatan"],
            foto=foto_path,
            deskripsi=karya_data["deskripsi"],
            analisa=karya_data["analisa"],
        ))

    for anekdot_data in data.get("anekdot", []):
        db.session.add(MonitoringAnekdot(
            monitoring_siswa_id=monitoring_siswa_id,
            kktp_id=anekdot_data["kktp_id"],
            waktu=anekdot_data["waktu"],
            catatan=anekdot_data["catatan"],
        ))

    for indikator_data in data.get("indikator", []):
        db.session.add(MonitoringIndikator(
            monitoring_siswa_id=monitoring_siswa_id,
            tp_id=indikator_data["tp_id"],
            muncul=indikator_data.get("muncul", False),
            kejadian_teramati=indikator_data.get("kejadian_teramati"),
        ))

    for rekomendasi_data in data.get("rekomendasi", []):
        db.session.add(MonitoringRekomendasi(
            monitoring_siswa_id=monitoring_siswa_id,
            elemen=rekomendasi_data["elemen"],
            tips=rekomendasi_data["tips"],
        ))


def delete_detail_siswa(monitoring_siswa_id):
    MonitoringRekomendasi.query.filter_by(
        monitoring_siswa_id=monitoring_siswa_id
    ).delete()

    MonitoringIndikator.query.filter_by(
        monitoring_siswa_id=monitoring_siswa_id
    ).delete()

    MonitoringAnekdot.query.filter_by(
        monitoring_siswa_id=monitoring_siswa_id
    ).delete()

    MonitoringKarya.query.filter_by(
        monitoring_siswa_id=monitoring_siswa_id
    ).delete()


def validate_detail_belongs_to_mingguan(monitoring_mingguan_id, data):
    tp_ids = []
    kktp_ids = []

    for item in data.get("indikator", []):
        tp_ids.append(item["tp_id"])

    for item in data.get("karya", []):
        if not item.get("kktp_id"):
            raise ValueError("KKTP hasil karya wajib dipilih")
        kktp_ids.append(item["kktp_id"])

    for item in data.get("anekdot", []):
        if not item.get("kktp_id"):
            raise ValueError("KKTP catatan anekdot wajib dipilih")
        kktp_ids.append(item["kktp_id"])

    if tp_ids:
        valid_tp_count = (
            MonitoringTP.query
            .filter(
                MonitoringTP.id.in_(tp_ids),
                MonitoringTP.monitoring_mingguan_id == monitoring_mingguan_id,
            )
            .count()
        )

        if valid_tp_count != len(set(tp_ids)):
            raise ValueError("Terdapat TP yang tidak sesuai dengan monitoring mingguan")

    if kktp_ids:
        valid_kktp_count = (
            MonitoringKKTP.query
            .join(MonitoringTP)
            .filter(
                MonitoringKKTP.id.in_(kktp_ids),
                MonitoringTP.monitoring_mingguan_id == monitoring_mingguan_id,
            )
            .count()
        )

        if valid_kktp_count != len(set(kktp_ids)):
            raise ValueError("Terdapat KKTP yang tidak sesuai dengan monitoring mingguan")