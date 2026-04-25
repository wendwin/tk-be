from app.models.pendaftaran import Pendaftaran
from app.extensions import db

def set_jadwal_observasi(id, data):
    pendaftaran = Pendaftaran.query.get(id)

    if not pendaftaran:
        return None

    pendaftaran.tanggal_observasi = data.get("tanggal_observasi")
    pendaftaran.jam_observasi = data.get("jam_observasi")
    pendaftaran.status_observasi = "terjadwal"

    db.session.commit()
    return pendaftaran


def update_status_observasi(id, status):
    pendaftaran = Pendaftaran.query.get(id)

    if not pendaftaran:
        return None

    pendaftaran.status_observasi = status

    db.session.commit()
    return pendaftaran