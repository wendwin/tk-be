from marshmallow import Schema, fields, validate, validates, ValidationError
from app.models.akademik.siswa_kelas import SiswaKelas


def wajib_isi(value, label):
    if value is None or not str(value).strip():
        raise ValidationError(f"{label} wajib diisi")


class MonitoringKKTPSchema(Schema):
    id = fields.Int(dump_only=True)

    deskripsi = fields.Str(
        required=True,
        error_messages={"required": "Deskripsi KKTP wajib diisi"}
    )

    @validates("deskripsi")
    def validate_deskripsi(self, value, **kwargs):
        wajib_isi(value, "Deskripsi KKTP")


class MonitoringTPSchema(Schema):
    id = fields.Int(dump_only=True)

    elemen = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["kesyuhadaan", "nabp", "jd", "ddlmstrs"],
            error="Elemen tidak valid"
        ),
        error_messages={"required": "Elemen wajib diisi"}
    )

    tujuan = fields.Str(
        required=True,
        error_messages={"required": "Tujuan pembelajaran wajib diisi"}
    )

    kktp = fields.List(
        fields.Nested(MonitoringKKTPSchema),
        required=True,
        validate=validate.Length(min=1, error="KKTP wajib ditambahkan"),
        error_messages={"required": "KKTP wajib ditambahkan"}
    )

    @validates("tujuan")
    def validate_tujuan(self, value, **kwargs):
        wajib_isi(value, "Tujuan pembelajaran")


class MonitoringKegiatanSchema(Schema):
    id = fields.Int(dump_only=True)

    nama = fields.Str(
        required=True,
        error_messages={"required": "Nama kegiatan wajib diisi"}
    )

    media = fields.Str(allow_none=True)

    @validates("nama")
    def validate_nama(self, value, **kwargs):
        wajib_isi(value, "Nama kegiatan")


class MonitoringAsesmenAwalSchema(Schema):
    id = fields.Int(dump_only=True)

    teknik = fields.Str(
        required=True,
        error_messages={"required": "Teknik asesmen wajib diisi"}
    )

    rancangan_kegiatan = fields.Str(
        required=True,
        error_messages={"required": "Rancangan kegiatan wajib diisi"}
    )

    hasil = fields.Str(allow_none=True)

    @validates("teknik")
    def validate_teknik(self, value, **kwargs):
        wajib_isi(value, "Teknik asesmen")

    @validates("rancangan_kegiatan")
    def validate_rancangan_kegiatan(self, value, **kwargs):
        wajib_isi(value, "Rancangan kegiatan")


class MonitoringMingguanSchema(Schema):
    id = fields.Int(dump_only=True)

    kelas_id = fields.Int(
        required=True,
        error_messages={
            "required": "Kelas wajib diisi",
            "null": "Kelas wajib diisi",
            "invalid": "Kelas tidak valid",
        }
    )

    tahun_ajaran_id = fields.Int(
        required=True,
        error_messages={
            "required": "Tahun ajaran wajib diisi",
            "null": "Tahun ajaran wajib diisi",
            "invalid": "Tahun ajaran tidak valid",
        }
    )

    semester = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["ganjil", "genap"],
            error="Semester tidak valid"
        ),
        error_messages={
            "required": "Semester wajib diisi",
            "null": "Semester wajib diisi",
        }
    )

    minggu = fields.Str(
        required=True,
        validate=validate.OneOf(
            ["1", "2", "3", "4"],
            error="Minggu tidak valid"
        ),
        error_messages={
            "required": "Minggu wajib diisi",
            "null": "Minggu wajib diisi",
        }
    )

    topik = fields.Str(
        required=True,
        error_messages={"required": "Topik wajib diisi"}
    )

    sub_topik = fields.Str(
        required=True,
        error_messages={"required": "Sub topik wajib diisi"}
    )

    tanggal_mulai = fields.Date(
        required=True,
        error_messages={
            "required": "Tanggal mulai wajib diisi",
            "null": "Tanggal mulai wajib diisi",
            "invalid": "Tanggal mulai tidak valid",
        }
    )

    tanggal_selesai = fields.Date(
        required=True,
        error_messages={
            "required": "Tanggal selesai wajib diisi",
            "null": "Tanggal selesai wajib diisi",
            "invalid": "Tanggal selesai tidak valid",
        }
    )

    status = fields.Str(
        required=False,
        validate=validate.OneOf(
            ["draft", "published"],
            error="Status tidak valid"
        )
    )

    replace_detail = fields.Bool(required=False)

    tp = fields.List(
        fields.Nested(MonitoringTPSchema),
        required=True,
        validate=validate.Length(min=1, error="Tujuan pembelajaran wajib ditambahkan"),
        error_messages={"required": "Tujuan pembelajaran wajib ditambahkan"}
    )

    kegiatan = fields.List(
        fields.Nested(MonitoringKegiatanSchema),
        required=True,
        validate=validate.Length(min=1, error="Kegiatan wajib ditambahkan"),
        error_messages={"required": "Kegiatan wajib ditambahkan"}
    )

    asesmen_awal = fields.Nested(MonitoringAsesmenAwalSchema, required=False)

    @validates("topik")
    def validate_topik(self, value, **kwargs):
        wajib_isi(value, "Topik")

    @validates("sub_topik")
    def validate_sub_topik(self, value, **kwargs):
        wajib_isi(value, "Sub topik")


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

    semester = fields.Str()
    minggu = fields.Str()

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