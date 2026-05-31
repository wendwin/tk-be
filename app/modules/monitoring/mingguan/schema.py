from marshmallow import Schema, fields, validate
from app.models.akademik.siswa_kelas import SiswaKelas

class MonitoringKKTPSchema(Schema):
    id = fields.Int(dump_only=True)
    deskripsi = fields.Str(required=True)


class MonitoringTPSchema(Schema):
    id = fields.Int(dump_only=True)
    elemen = fields.Str(
        required=True,
        validate=validate.OneOf(["kesyuhadaan", "nabp", "jd", "ddlmstrs"])
    )
    tujuan = fields.Str(required=True)
    kktp = fields.List(fields.Nested(MonitoringKKTPSchema), required=True)


class MonitoringKegiatanSchema(Schema):
    id = fields.Int(dump_only=True)
    nama = fields.Str(required=True)
    media = fields.Str(allow_none=True)


class MonitoringAsesmenAwalSchema(Schema):
    id = fields.Int(dump_only=True)
    teknik = fields.Str(required=True)
    rancangan_kegiatan = fields.Str(required=True)
    hasil = fields.Str(allow_none=True)


class MonitoringMingguanSchema(Schema):
    id = fields.Int(dump_only=True)

    kelas_id = fields.Int(required=True)
    tahun_ajaran_id = fields.Int(required=True)

    semester = fields.Int(required=True)
    minggu = fields.Int(required=True)

    topik = fields.Str(required=True)
    sub_topik = fields.Str(required=True)

    tanggal_mulai = fields.Date(required=True)
    tanggal_selesai = fields.Date(required=True)

    status = fields.Str(
        required=False,
        validate=validate.OneOf(["draft", "published"])
    )

    replace_detail = fields.Bool(required=False)

    tp = fields.List(fields.Nested(MonitoringTPSchema), required=True)
    kegiatan = fields.List(fields.Nested(MonitoringKegiatanSchema), required=True)
    asesmen_awal = fields.Nested(MonitoringAsesmenAwalSchema, required=False)


class MonitoringKelasMiniSchema(Schema):
    id = fields.Int()
    nama = fields.Str()
    jenjang = fields.Str()
    kelompok = fields.Str()


class MonitoringTahunAjaranMiniSchema(Schema):
    id = fields.Int()
    label = fields.Method("get_label")

    def get_label(self, obj):
        return obj.label if obj else None


class MonitoringMingguanListSchema(Schema):
    id = fields.Int()
    semester = fields.Int()
    minggu = fields.Int()
    topik = fields.Str()
    sub_topik = fields.Str()
    tanggal_mulai = fields.Date()
    tanggal_selesai = fields.Date()
    status = fields.Str()

    kelas = fields.Nested(MonitoringKelasMiniSchema)
    tahun_ajaran = fields.Nested(MonitoringTahunAjaranMiniSchema)

    total_siswa = fields.Method("get_total_siswa")
    total_selesai = fields.Method("get_total_selesai")

    def get_total_siswa(self, obj):
        return SiswaKelas.query.filter_by(
            kelas_id=obj.kelas_id,
            tahun_ajaran_id=obj.tahun_ajaran_id,
            status="aktif"
        ).count()

    def get_total_selesai(self, obj):
        return len(obj.monitoring_siswa)


class MonitoringMingguanDetailSchema(MonitoringMingguanListSchema):
    tp = fields.Nested(MonitoringTPSchema, many=True)
    kegiatan = fields.Nested(MonitoringKegiatanSchema, many=True)
    asesmen_awal = fields.Nested(MonitoringAsesmenAwalSchema)