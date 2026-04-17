from app.extensions import db
from app.models.pendaftaran import *
from sqlalchemy.orm import joinedload

def generate_no():
    last = Pendaftaran.query.order_by(Pendaftaran.id_pendaftaran.desc()).first()
    if not last:
        return "001"
    return str(int(last.no_pendaftaran) + 1).zfill(3)

def get_all(page=1, per_page=10, search=None):
    query = Pendaftaran.query

    # eager loading
    query = query.options(
        joinedload(Pendaftaran.peserta)
        .joinedload(PesertaDidik.kesehatan),

        joinedload(Pendaftaran.peserta)
        .joinedload(PesertaDidik.orang_tua),

        joinedload(Pendaftaran.peserta)
        .joinedload(PesertaDidik.alamat_domisili),

        joinedload(Pendaftaran.peserta)
        .joinedload(PesertaDidik.alamat_kk)
    )

    # filter
    if search:
        query = query.join(PesertaDidik).filter(
            PesertaDidik.nama_lengkap.ilike(f"%{search}%")
        )

    # pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return pagination

def create(data):
    no = generate_no()

    # pendaftaran
    pendaftaran = Pendaftaran(
        no_pendaftaran=no,
        id_tahun=data["id_tahun"]
    )
    db.session.add(pendaftaran)
    db.session.flush()

    # alamat peserta
    alamat_dom = Alamat(**data["alamat_domisili"])
    alamat_kk = Alamat(**data["alamat_kk"])
    db.session.add_all([alamat_dom, alamat_kk])
    db.session.flush()

    # peserta
    peserta = PesertaDidik(
        id_pendaftaran=pendaftaran.id,
        id_alamat_domisili=alamat_dom.id,
        id_alamat_kk=alamat_kk.id_alamat,
        **data["peserta"]
    )
    db.session.add(peserta)
    db.session.flush()

    # kesehatan
    kesehatan = Kesehatan(
        id_peserta=peserta.id_peserta,
        **data["kesehatan"]
    )
    db.session.add(kesehatan)

    # orang tua
    for ortu in data["orang_tua"]:
        alamat = Alamat(**ortu["alamat"])
        db.session.add(alamat)
        db.session.flush()

        orang_tua = OrangTua(
            id_peserta=peserta.id_peserta,
            id_alamat=alamat.id_alamat,
            **{k: v for k, v in ortu.items() if k != "alamat"}
        )
        db.session.add(orang_tua)

    # informasi tambahan
    info = Informasi(
        id_peserta=peserta.id_peserta,
        **data["informasi"]
    )
    db.session.add(info)

    db.session.commit()
    return pendaftaran
