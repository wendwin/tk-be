from marshmallow import Schema, fields, validate, ValidationError

def wajib_isi(value, label):
    if value is None or not str(value).strip():
        raise ValidationError(f"{label} wajib diisi")


from marshmallow import Schema, fields, validate, validates, ValidationError


def wajib_isi(value, label):
    if value is None or not str(value).strip():
        raise ValidationError(f"{label} wajib diisi")


class MonitoringKaryaInputSchema(Schema):
    kktp_id = fields.Int(required=True, error_messages={
        "required": "KKTP wajib dipilih",
        "null": "KKTP wajib dipilih",
        "invalid": "KKTP tidak valid",
    })
    kegiatan = fields.Str(required=True, error_messages={"required": "Kegiatan wajib diisi"})
    foto = fields.Str(allow_none=True)
    deskripsi = fields.Str(required=True, error_messages={"required": "Deskripsi aktivitas wajib diisi"})
    analisa = fields.Str(required=True, error_messages={"required": "Analisa guru wajib diisi"})

    @validates("kegiatan")
    def validate_kegiatan(self, value, **kwargs):
        wajib_isi(value, "Kegiatan")

    @validates("deskripsi")
    def validate_deskripsi(self, value, **kwargs):
        wajib_isi(value, "Deskripsi aktivitas")

    @validates("analisa")
    def validate_analisa(self, value, **kwargs):
        wajib_isi(value, "Analisa guru")


class MonitoringAnekdotInputSchema(Schema):
    kktp_id = fields.Int(required=True, error_messages={
        "required": "KKTP wajib dipilih",
        "null": "KKTP wajib dipilih",
        "invalid": "KKTP tidak valid",
    })
    waktu = fields.DateTime(required=True, error_messages={
        "required": "Waktu observasi wajib diisi",
        "null": "Waktu observasi wajib diisi",
        "invalid": "Waktu observasi tidak valid",
    })
    catatan = fields.Str(required=True, error_messages={"required": "Catatan observasi wajib diisi"})

    @validates("catatan")
    def validate_catatan(self, value, **kwargs):
        wajib_isi(value, "Catatan observasi")


class MonitoringIndikatorInputSchema(Schema):
    tp_id = fields.Int(required=True)
    muncul = fields.Bool(required=True)
    kejadian_teramati = fields.Str(allow_none=True)


class MonitoringRekomendasiInputSchema(Schema):
    elemen = fields.Str(
        required=True,
        validate=validate.OneOf(["kesyuhadaan", "nabp", "jd", "ddlmstrs"])
    )
    tips = fields.Str(required=True)

    @validates("tips")
    def validate_tips(self, value, **kwargs):
        wajib_isi(value, "Tips untuk orang tua")


class MonitoringSiswaSchema(Schema):
    id = fields.Int(dump_only=True)

    monitoring_mingguan_id = fields.Int(required=True)
    siswa_kelas_id = fields.Int(required=True)

    ringkasan = fields.Str(required=True, error_messages={"required": "Ringkasan perkembangan wajib diisi"})

    status = fields.Str(
        required=False,
        validate=validate.OneOf(["draft", "published"], error="Status tidak valid")
    )

    replace_detail = fields.Bool(required=False)

    karya = fields.List(fields.Nested(MonitoringKaryaInputSchema), required=False)
    anekdot = fields.List(fields.Nested(MonitoringAnekdotInputSchema), required=False)
    indikator = fields.List(fields.Nested(MonitoringIndikatorInputSchema), required=False)
    rekomendasi = fields.List(fields.Nested(MonitoringRekomendasiInputSchema),required=False)

    @validates("ringkasan")
    def validate_ringkasan(self, value, **kwargs):
        wajib_isi(value, "Ringkasan perkembangan")


class MonitoringKKTPMiniSchema(Schema):
    id = fields.Int()
    deskripsi = fields.Str()


class MonitoringTPMiniSchema(Schema):
    id = fields.Int()
    elemen = fields.Str()
    tujuan = fields.Str()
    kktp = fields.Nested(MonitoringKKTPMiniSchema, many=True)


class MonitoringKegiatanMiniSchema(Schema):
    id = fields.Int()
    nama = fields.Str()
    media = fields.Str()


class MonitoringAsesmenAwalMiniSchema(Schema):
    id = fields.Int()
    teknik = fields.Str()
    rancangan_kegiatan = fields.Str()
    hasil = fields.Str()


class MonitoringMingguanMiniSchema(Schema):
    id = fields.Int()
    semester = fields.Str()
    minggu = fields.Int()
    topik = fields.Str()
    sub_topik = fields.Str()
    tanggal_mulai = fields.Date()
    tanggal_selesai = fields.Date()

    tp = fields.Nested(MonitoringTPMiniSchema, many=True)
    kegiatan = fields.Nested(MonitoringKegiatanMiniSchema, many=True)
    asesmen_awal = fields.Nested(MonitoringAsesmenAwalMiniSchema)


class SiswaKelasMiniSchema(Schema):
    id = fields.Int()
    siswa = fields.Method("get_siswa")
    kelas = fields.Method("get_kelas")

    def get_siswa(self, obj):
        if not obj.siswa:
            return None

        return {
            "id": obj.siswa.id,
            "nama_lengkap": obj.siswa.peserta.nama_lengkap if obj.siswa.peserta else None,
            "nama_panggilan": obj.siswa.peserta.nama_panggilan if obj.siswa.peserta else None,
        }

    def get_kelas(self, obj):
        if not obj.kelas:
            return None

        return {
            "id": obj.kelas.id,
            "nama": obj.kelas.nama,
            "jenjang": obj.kelas.jenjang,
            "kelompok": obj.kelas.kelompok,
        }


class MonitoringKaryaDetailSchema(Schema):
    id = fields.Int()
    kktp_id = fields.Int()
    kegiatan = fields.Str()
    foto = fields.Str()
    deskripsi = fields.Str()
    analisa = fields.Str()
    kktp = fields.Nested(MonitoringKKTPMiniSchema)


class MonitoringAnekdotDetailSchema(Schema):
    id = fields.Int()
    kktp_id = fields.Int()
    waktu = fields.DateTime()
    catatan = fields.Str()
    kktp = fields.Nested(MonitoringKKTPMiniSchema)


class MonitoringIndikatorDetailSchema(Schema):
    id = fields.Int()
    tp_id = fields.Int()
    muncul = fields.Bool()
    kejadian_teramati = fields.Str()
    tp = fields.Nested(MonitoringTPMiniSchema)

class MonitoringRekomendasiDetailSchema(Schema):
    id = fields.Int()
    elemen = fields.Str()
    tips = fields.Str()


class MonitoringSiswaListSchema(Schema):
    id = fields.Int()
    ringkasan = fields.Str()
    status = fields.Str()

    monitoring_mingguan = fields.Nested(MonitoringMingguanMiniSchema)
    siswa_kelas = fields.Nested(SiswaKelasMiniSchema)


class MonitoringSiswaDetailSchema(MonitoringSiswaListSchema):
    karya = fields.Nested(MonitoringKaryaDetailSchema, many=True)
    anekdot = fields.Nested(MonitoringAnekdotDetailSchema, many=True)
    indikator = fields.Nested(MonitoringIndikatorDetailSchema, many=True)
    rekomendasi = fields.Nested(MonitoringRekomendasiDetailSchema, many=True)